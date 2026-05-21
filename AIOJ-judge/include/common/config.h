// include/common/config.h
#pragma once

#include <string>

namespace aioj {

class Config {
public:
    // 从文件加载配置
    static Config load(const std::string& filepath);

    // Redis配置
    std::string redis_host = "localhost";
    int redis_port = 6379;
    int redis_db = 0;
    std::string task_queue = "judge_task";
    std::string result_queue = "judge_result";

    // 线程配置
    size_t thread_count = 4;

    // 默认资源限制
    int default_time_limit_ms = 2000;
    int default_memory_limit_kb = 262144;

    // 测试用例根目录（相对于配置文件位置，或绝对路径）
    std::string testcase_root = "./testcases";

    // 日志级别
    std::string log_level = "INFO";
};

} // namespace aioj
