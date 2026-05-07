// test/test_config.cpp
#include <catch2/catch_test_macros.hpp>
#include "common/config.h"
#include <fstream>

using namespace aioj;

TEST_CASE("Config load from file", "[config]") {
    // 创建临时配置文件
    std::string tmpfile = "/tmp/test_judge.conf";
    {
        std::ofstream f(tmpfile);
        f << "# comment\n";
        f << "redis_host=127.0.0.1\n";
        f << "redis_port=6380\n";
        f << "thread_count=8\n";
        f << "default_time_limit_ms=3000\n";
    }

    Config config = Config::load(tmpfile);

    REQUIRE(config.redis_host == "127.0.0.1");
    REQUIRE(config.redis_port == 6380);
    REQUIRE(config.thread_count == 8);
    REQUIRE(config.default_time_limit_ms == 3000);
    // 未配置的项使用默认值
    REQUIRE(config.redis_db == 0);
    REQUIRE(config.task_queue == "judge_task");
}

TEST_CASE("Config load nonexistent file", "[config]") {
    REQUIRE_THROWS_AS(
        Config::load("/nonexistent/path.conf"),
        std::runtime_error
    );
}
