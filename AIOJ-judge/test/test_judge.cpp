#include <catch2/catch_test_macros.hpp>
#include "common/types.h"

using namespace aioj;

TEST_CASE("JudgeStatus to_string", "[types]") {
    REQUIRE(to_string(JudgeStatus::ACCEPTED) == "accepted");
    REQUIRE(to_string(JudgeStatus::WRONG_ANSWER) == "wrong_answer");
    REQUIRE(to_string(JudgeStatus::TIME_LIMIT) == "time_limit");
    REQUIRE(to_string(JudgeStatus::MEMORY_LIMIT) == "memory_limit");
    REQUIRE(to_string(JudgeStatus::RUNTIME_ERROR) == "runtime_error");
    REQUIRE(to_string(JudgeStatus::COMPILE_ERROR) == "compile_error");
    REQUIRE(to_string(JudgeStatus::SYSTEM_ERROR) == "system_error");
}

TEST_CASE("JudgeStatus from_string", "[types]") {
    REQUIRE(status_from_string("accepted") == JudgeStatus::ACCEPTED);
    REQUIRE(status_from_string("wrong_answer") == JudgeStatus::WRONG_ANSWER);
    REQUIRE(status_from_string("compile_error") == JudgeStatus::COMPILE_ERROR);
}

TEST_CASE("JudgeStatus from_string invalid", "[types]") {
    REQUIRE_THROWS_AS(status_from_string("invalid"), std::invalid_argument);
}
