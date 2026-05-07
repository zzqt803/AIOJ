#pragma once

#include <string>
#include <vector>
#include <nlohmann/json.hpp>

namespace aioj {

// 判题状态（仅最终状态）
enum class JudgeStatus {
    ACCEPTED,
    WRONG_ANSWER,
    TIME_LIMIT,
    MEMORY_LIMIT,
    RUNTIME_ERROR,
    COMPILE_ERROR,
    SYSTEM_ERROR
};

// 状态转字符串
std::string to_string(JudgeStatus status);

// 字符串转状态
JudgeStatus status_from_string(const std::string& str);

// 单个测试点结果
struct TestCaseResult {
    int test_case_id;
    JudgeStatus status;
    int time_used_ms;
    int memory_used_kb;
    std::string error_message;
};

// 完整判题结果
struct JudgeResult {
    std::string submission_id;
    std::string problem_id;
    JudgeStatus overall_status;
    std::vector<TestCaseResult> details;
    int total_time_ms;
    int max_memory_kb;
};

// 判题任务
struct JudgeTask {
    std::string submission_id;
    std::string problem_id;
    std::string language;
    std::string source_code;
    int time_limit_ms;
    int memory_limit_kb;
};

// JSON序列化
void to_json(nlohmann::json& j, const TestCaseResult& r);
void to_json(nlohmann::json& j, const JudgeResult& r);
JudgeTask task_from_json(const nlohmann::json& j);

} // namespace aioj
