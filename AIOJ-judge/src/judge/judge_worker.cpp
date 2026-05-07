// src/judge/judge_worker.cpp
#include "judge/judge_worker.h"
#include <fstream>
#include <sstream>
#include <algorithm>
#include <filesystem>
#include <iostream>

namespace fs = std::filesystem;

namespace aioj {

JudgeWorker::JudgeWorker(const Config& config) : config_(config) {}

bool JudgeWorker::load_test_cases(
    const std::string& problem_id,
    std::vector<std::pair<std::string, std::string>>& cases
) {
    std::string problem_dir = config_.testcase_root + "/" + problem_id;
    if (!fs::exists(problem_dir)) {
        return false;
    }

    cases.clear();
    int i = 1;
    while (true) {
        std::string in_file = problem_dir + "/" + std::to_string(i) + ".in";
        std::string out_file = problem_dir + "/" + std::to_string(i) + ".out";

        if (!fs::exists(in_file) || !fs::exists(out_file)) {
            break;
        }

        cases.emplace_back(in_file, out_file);
        ++i;
    }

    return !cases.empty();
}

// 去除行尾空白和多余空行
static std::string normalize(const std::string& str) {
    std::istringstream iss(str);
    std::ostringstream oss;
    std::string line;
    bool first = true;
    while (std::getline(iss, line)) {
        // 去除行尾空白
        size_t end = line.find_last_not_of(" \t\r\n");
        if (end != std::string::npos) {
            line = line.substr(0, end + 1);
        } else {
            line.clear();
        }
        // 跳过末尾空行
        if (line.empty() && iss.eof()) continue;
        if (!first) oss << "\n";
        oss << line;
        first = false;
    }
    return oss.str();
}

bool JudgeWorker::compare_output(
    const std::string& actual_file,
    const std::string& expected_file
) {
    std::ifstream af(actual_file), ef(expected_file);
    if (!af.is_open() || !ef.is_open()) return false;

    std::string actual((std::istreambuf_iterator<char>(af)),
                        std::istreambuf_iterator<char>());
    std::string expected((std::istreambuf_iterator<char>(ef)),
                         std::istreambuf_iterator<char>());

    return normalize(actual) == normalize(expected);
}

TestCaseResult JudgeWorker::judge_single(
    const std::string& executable,
    LanguageHandler* handler,
    int box_id,
    const std::string& input_file,
    const std::string& expected_output,
    int test_case_id,
    int time_limit_ms,
    int memory_limit_kb
) {
    TestCaseResult result;
    result.test_case_id = test_case_id;

    // 创建工作目录
    std::string work_dir = "/tmp/box_" + std::to_string(box_id);
    fs::create_directories(work_dir);

    Sandbox sandbox(box_id, work_dir);
    if (!sandbox.init()) {
        result.status = JudgeStatus::SYSTEM_ERROR;
        result.error_message = "failed to init sandbox";
        return result;
    }

    // 获取运行命令
    auto run_cmd = handler->get_run_command(executable);
    std::string command;
    for (size_t i = 0; i < run_cmd.size(); ++i) {
        if (i > 0) command += " ";
        command += run_cmd[i];
    }

    std::string output_file = work_dir + "/output.txt";

    // 执行
    SandboxResult exec_result = sandbox.execute(
        command, input_file, output_file,
        time_limit_ms, memory_limit_kb
    );

    result.time_used_ms = exec_result.time_used_ms;
    result.memory_used_kb = exec_result.memory_used_kb;

    // 判断状态
    if (exec_result.time_limit_hit) {
        result.status = JudgeStatus::TIME_LIMIT;
    } else if (exec_result.memory_used_kb > memory_limit_kb) {
        result.status = JudgeStatus::MEMORY_LIMIT;
    } else if (exec_result.exit_code != 0) {
        result.status = JudgeStatus::RUNTIME_ERROR;
        result.error_message = exec_result.error;
    } else if (!compare_output(output_file, expected_output)) {
        result.status = JudgeStatus::WRONG_ANSWER;
    } else {
        result.status = JudgeStatus::ACCEPTED;
    }

    sandbox.cleanup();
    return result;
}

JudgeResult JudgeWorker::judge(const JudgeTask& task) {
    JudgeResult result;
    result.submission_id = task.submission_id;
    result.problem_id = task.problem_id;
    result.total_time_ms = 0;
    result.max_memory_kb = 0;

    // 加载测试用例
    std::vector<std::pair<std::string, std::string>> cases;
    if (!load_test_cases(task.problem_id, cases)) {
        result.overall_status = JudgeStatus::SYSTEM_ERROR;
        return result;
    }

    // 创建语言处理器
    auto handler = LanguageHandlerFactory::create(task.language);
    if (!handler) {
        result.overall_status = JudgeStatus::SYSTEM_ERROR;
        return result;
    }

    // 编译
    std::string work_dir = "/tmp/judge_" + task.submission_id;
    fs::create_directories(work_dir);

    std::string executable;
    if (handler->needs_compilation()) {
        std::string compile_error;
        executable = handler->compile(task.source_code, work_dir, compile_error);
        if (executable.empty()) {
            result.overall_status = JudgeStatus::COMPILE_ERROR;
            TestCaseResult ce;
            ce.test_case_id = 0;
            ce.status = JudgeStatus::COMPILE_ERROR;
            ce.error_message = compile_error;
            result.details.push_back(ce);
            return result;
        }
    }

    // 逐个测试点评测
    int time_limit = task.time_limit_ms > 0
        ? task.time_limit_ms
        : config_.default_time_limit_ms;
    int memory_limit = task.memory_limit_kb > 0
        ? task.memory_limit_kb
        : config_.default_memory_limit_kb;

    bool all_accepted = true;
    for (size_t i = 0; i < cases.size(); ++i) {
        TestCaseResult tc = judge_single(
            executable, handler.get(), 0,
            cases[i].first, cases[i].second,
            static_cast<int>(i + 1),
            time_limit, memory_limit
        );

        result.details.push_back(tc);
        result.total_time_ms += tc.time_used_ms;
        result.max_memory_kb = std::max(result.max_memory_kb, tc.memory_used_kb);

        if (tc.status != JudgeStatus::ACCEPTED) {
            all_accepted = false;
        }
    }

    result.overall_status = all_accepted
        ? JudgeStatus::ACCEPTED
        : JudgeStatus::WRONG_ANSWER;

    // 清理工作目录
    fs::remove_all(work_dir);

    return result;
}

} // namespace aioj
