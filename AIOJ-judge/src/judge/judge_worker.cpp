// src/judge/judge_worker.cpp
#include "judge/judge_worker.h"
#include <fstream>
#include <sstream>
#include <algorithm>
#include <filesystem>
#include <iostream>
#include <atomic>

namespace fs = std::filesystem;

namespace aioj {

// 全局box_id计数器（多线程安全）
static std::atomic<int> g_box_id_counter{0};

JudgeWorker::JudgeWorker(const Config& config) : config_(config) {}

bool JudgeWorker::load_test_cases(
    const std::string& problem_id,
    std::vector<std::pair<std::string, std::string>>& cases
) {
    fs::path problem_dir = fs::path(config_.testcase_root) / problem_id;

    if (!fs::exists(problem_dir) || !fs::is_directory(problem_dir)) {
        return false;
    }

    cases.clear();
    int i = 1;
    while (true) {
        fs::path in_file = problem_dir / (std::to_string(i) + ".in");
        fs::path out_file = problem_dir / (std::to_string(i) + ".out");

        if (!fs::exists(in_file) || !fs::exists(out_file)) {
            break;
        }

        cases.emplace_back(in_file.string(), out_file.string());
        ++i;
    }

    return !cases.empty();
}

static std::string normalize(const std::string& str) {
    std::istringstream iss(str);
    std::ostringstream oss;
    std::string line;
    bool first = true;
    while (std::getline(iss, line)) {
        size_t end = line.find_last_not_of(" \t\r\n");
        if (end != std::string::npos) {
            line = line.substr(0, end + 1);
        } else {
            line.clear();
        }
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
    std::string full_executable_path;
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
        full_executable_path = work_dir + "/" + executable;
    }

    // 为当前任务分配唯一的box_id
    int box_id = g_box_id_counter.fetch_add(1) % 100;

    // 初始化沙箱（只初始化一次）
    Sandbox sandbox(box_id, work_dir);
    if (!sandbox.init()) {
        result.overall_status = JudgeStatus::SYSTEM_ERROR;
        return result;
    }

    // 准备可执行文件（只复制一次）
    if (!sandbox.prepare_executable(full_executable_path)) {
        result.overall_status = JudgeStatus::SYSTEM_ERROR;
        sandbox.cleanup();
        return result;
    }

    // 设置资源限制
    int time_limit = task.time_limit_ms > 0
        ? task.time_limit_ms
        : config_.default_time_limit_ms;
    int memory_limit = task.memory_limit_kb > 0
        ? task.memory_limit_kb
        : config_.default_memory_limit_kb;

    // 逐个测试点评测
    bool all_accepted = true;
    for (size_t i = 0; i < cases.size(); ++i) {
        std::string output_file = work_dir + "/output_" + std::to_string(i + 1) + ".txt";

        std::cerr << "[Judge] Running test case " << (i + 1) << std::endl;

        SandboxResult exec_result = sandbox.execute(
            cases[i].first, output_file,
            time_limit, memory_limit
        );

        std::cerr << "[Judge] Test case " << (i + 1) << " executed, exit_code=" << exec_result.exit_code << std::endl;

        TestCaseResult tc;
        tc.test_case_id = static_cast<int>(i + 1);
        tc.time_used_ms = exec_result.time_used_ms;
        tc.memory_used_kb = exec_result.memory_used_kb;

        // 判断状态
        if (exec_result.time_limit_hit) {
            tc.status = JudgeStatus::TIME_LIMIT;
        } else if (exec_result.memory_used_kb > memory_limit) {
            tc.status = JudgeStatus::MEMORY_LIMIT;
        } else if (exec_result.exit_code != 0) {
            tc.status = JudgeStatus::RUNTIME_ERROR;
            tc.error_message = exec_result.error;
        } else if (!compare_output(output_file, cases[i].second)) {
            tc.status = JudgeStatus::WRONG_ANSWER;
        } else {
            tc.status = JudgeStatus::ACCEPTED;
        }

        std::cerr << "[Judge] Test case " << (i + 1) << " result: " << to_string(tc.status) << std::endl;

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

    std::cerr << "[Judge] Cleaning up sandbox" << std::endl;
    sandbox.cleanup();
    std::cerr << "[Judge] Removing work dir" << std::endl;
    fs::remove_all(work_dir);
    std::cerr << "[Judge] Done" << std::endl;

    return result;
}

} // namespace aioj
