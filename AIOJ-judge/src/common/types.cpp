#include "common/types.h"
#include <stdexcept>

namespace aioj {

std::string to_string(JudgeStatus status) {
    switch (status) {
        case JudgeStatus::ACCEPTED:      return "accepted";
        case JudgeStatus::WRONG_ANSWER:  return "wrong_answer";
        case JudgeStatus::TIME_LIMIT:    return "time_limit";
        case JudgeStatus::MEMORY_LIMIT:  return "memory_limit";
        case JudgeStatus::RUNTIME_ERROR: return "runtime_error";
        case JudgeStatus::COMPILE_ERROR: return "compile_error";
        case JudgeStatus::SYSTEM_ERROR:  return "system_error";
        default: throw std::invalid_argument("unknown status");
    }
}

JudgeStatus status_from_string(const std::string& str) {
    if (str == "accepted")      return JudgeStatus::ACCEPTED;
    if (str == "wrong_answer")  return JudgeStatus::WRONG_ANSWER;
    if (str == "time_limit")    return JudgeStatus::TIME_LIMIT;
    if (str == "memory_limit")  return JudgeStatus::MEMORY_LIMIT;
    if (str == "runtime_error") return JudgeStatus::RUNTIME_ERROR;
    if (str == "compile_error") return JudgeStatus::COMPILE_ERROR;
    if (str == "system_error")  return JudgeStatus::SYSTEM_ERROR;
    throw std::invalid_argument("unknown status: " + str);
}

void to_json(nlohmann::json& j, const TestCaseResult& r) {
    j = {
        {"test_case_id", r.test_case_id},
        {"status", to_string(r.status)},
        {"time_used_ms", r.time_used_ms},
        {"memory_used_kb", r.memory_used_kb},
        {"error_message", r.error_message}
    };
}

void to_json(nlohmann::json& j, const JudgeResult& r) {
    j = {
        {"submission_id", r.submission_id},
        {"problem_id", r.problem_id},
        {"overall_status", to_string(r.overall_status)},
        {"total_time_ms", r.total_time_ms},
        {"max_memory_kb", r.max_memory_kb},
        {"details", r.details}
    };
}

JudgeTask task_from_json(const nlohmann::json& j) {
    JudgeTask task;
    task.submission_id = j.at("submission_id").get<std::string>();
    task.problem_id = j.at("problem_id").get<std::string>();
    task.language = j.at("language").get<std::string>();
    task.source_code = j.at("source_code").get<std::string>();
    task.time_limit_ms = j.value("time_limit_ms", 0);
    task.memory_limit_kb = j.value("memory_limit_kb", 0);
    return task;
}

} // namespace aioj
