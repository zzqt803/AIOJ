// src/common/config.cpp
#include "common/config.h"
#include <fstream>
#include <sstream>
#include <stdexcept>

namespace aioj {

// 去除字符串首尾空白
static std::string trim(const std::string& str) {
    size_t start = str.find_first_not_of(" \t\r\n");
    if (start == std::string::npos) return "";
    size_t end = str.find_last_not_of(" \t\r\n");
    return str.substr(start, end - start + 1);
}

Config Config::load(const std::string& filepath) {
    Config config;
    std::ifstream file(filepath);

    if (!file.is_open()) {
        throw std::runtime_error("cannot open config file: " + filepath);
    }

    std::string line;
    while (std::getline(file, line)) {
        line = trim(line);

        // 跳过空行和注释
        if (line.empty() || line[0] == '#') {
            continue;
        }

        // 解析 key=value
        size_t eq_pos = line.find('=');
        if (eq_pos == std::string::npos) {
            continue;
        }

        std::string key = trim(line.substr(0, eq_pos));
        std::string value = trim(line.substr(eq_pos + 1));

        // 匹配配置项
        if (key == "redis_host") {
            config.redis_host = value;
        } else if (key == "redis_port") {
            config.redis_port = std::stoi(value);
        } else if (key == "redis_db") {
            config.redis_db = std::stoi(value);
        } else if (key == "task_queue") {
            config.task_queue = value;
        } else if (key == "result_queue") {
            config.result_queue = value;
        } else if (key == "thread_count") {
            config.thread_count = std::stoul(value);
        } else if (key == "default_time_limit_ms") {
            config.default_time_limit_ms = std::stoi(value);
        } else if (key == "default_memory_limit_kb") {
            config.default_memory_limit_kb = std::stoi(value);
        } else if (key == "testcase_root") {
            config.testcase_root = value;
        } else if (key == "log_level") {
            config.log_level = value;
        }
    }

    return config;
}

} // namespace aioj
