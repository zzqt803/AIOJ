#include <catch2/catch_test_macros.hpp>
#include "common/types.h"
#include "judge/judge_worker.h"
#include "common/config.h"

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

TEST_CASE("JudgeWorker end-to-end", "[judge]") {
    Config config;
    config.testcase_root = "../../test/testcases";

    JudgeWorker worker(config);

    JudgeTask task;
    task.submission_id = "test_001";
    task.problem_id = "1001";
    task.language = "cpp";
    task.source_code = R"(
#include <iostream>
using namespace std;
int main() {
    int a, b;
    cin >> a >> b;
    cout << a + b << endl;
    return 0;
}
)";
    task.time_limit_ms = 2000;
    task.memory_limit_kb = 262144;

    JudgeResult result = worker.judge(task);

    REQUIRE(result.overall_status == JudgeStatus::ACCEPTED);
    REQUIRE(result.details.size() == 1);
    REQUIRE(result.details[0].status == JudgeStatus::ACCEPTED);
}

TEST_CASE("JudgeWorker wrong answer", "[judge]") {
    Config config;
    config.testcase_root = "../../test/testcases";

    JudgeWorker worker(config);

    JudgeTask task;
    task.submission_id = "test_002";
    task.problem_id = "1001";
    task.language = "cpp";
    task.source_code = R"(
#include <iostream>
using namespace std;
int main() {
    int a, b;
    cin >> a >> b;
    cout << a - b << endl;
    return 0;
}
)";
    task.time_limit_ms = 2000;
    task.memory_limit_kb = 262144;

    JudgeResult result = worker.judge(task);

    REQUIRE(result.overall_status == JudgeStatus::WRONG_ANSWER);
}

TEST_CASE("JudgeWorker compile error", "[judge]") {
    Config config;
    config.testcase_root = "../../test/testcases";

    JudgeWorker worker(config);

    JudgeTask task;
    task.submission_id = "test_003";
    task.problem_id = "1001";
    task.language = "cpp";
    task.source_code = "this is not valid c++ code";
    task.time_limit_ms = 2000;
    task.memory_limit_kb = 262144;

    JudgeResult result = worker.judge(task);

    REQUIRE(result.overall_status == JudgeStatus::COMPILE_ERROR);
}
