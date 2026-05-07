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

} // namespace aioj
