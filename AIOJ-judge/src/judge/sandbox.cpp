// src/judge/sandbox.cpp
#include "judge/sandbox.h"
#include <fstream>
#include <sstream>
#include <cstdlib>
#include <stdexcept>

namespace aioj {

Sandbox::Sandbox(int box_id, const std::string& work_dir)
    : box_id_(box_id), work_dir_(work_dir), initialized_(false) {}

Sandbox::~Sandbox() {
    cleanup();
}

bool Sandbox::init() {
    std::string cmd = "isolate --box-id=" + std::to_string(box_id_) + " --init 2>&1";
    int ret = system(cmd.c_str());
    initialized_ = (ret == 0);
    return initialized_;
}

void Sandbox::cleanup() {
    if (initialized_) {
        std::string cmd = "isolate --box-id=" + std::to_string(box_id_) + " --cleanup 2>/dev/null";
        system(cmd.c_str());
        initialized_ = false;
    }
}

SandboxResult Sandbox::execute(
    const std::string& command,
    const std::string& input_file,
    const std::string& output_file,
    int time_limit_ms,
    int memory_limit_kb
) {
    if (!initialized_) {
        return {false, -1, 0, 0, false, false, "sandbox not initialized"};
    }

    // 时间转换：毫秒转秒，向上取整
    int time_sec = (time_limit_ms + 999) / 1000;
    int wall_time_sec = time_sec + 1;  // 墙钟时间多1秒

    std::string meta_file = work_dir_ + "/meta.txt";

    // 构建isolate命令
    std::ostringstream cmd;
    cmd << "isolate"
        << " --box-id=" << box_id_
        << " --processes=10"
        << " --time=" << time_sec
        << " --wall-time=" << wall_time_sec
        << " --memory=" << memory_limit_kb
        << " --meta=" << meta_file
        << " --stdin=" << input_file
        << " --stdout=" << output_file
        << " --stderr=/dev/null"
        << " --run -- " << command
        << " 2>&1";

    int ret = system(cmd.str().c_str());

    // 解析meta文件获取详细信息
    SandboxResult result = parse_meta(meta_file);
    if (ret != 0 && result.error.empty()) {
        result.error = "isolate execution failed";
    }

    return result;
}

SandboxResult Sandbox::parse_meta(const std::string& meta_file) {
    SandboxResult result = {true, 0, 0, 0, false, false, ""};

    std::ifstream file(meta_file);
    if (!file.is_open()) {
        result.success = false;
        result.error = "cannot open meta file";
        return result;
    }

    std::string line;
    while (std::getline(file, line)) {
        size_t eq = line.find(':');
        if (eq == std::string::npos) continue;

        std::string key = line.substr(0, eq);
        std::string value = line.substr(eq + 1);

        if (key == "time") {
            // isolate报告的是秒，转换为毫秒
            result.time_used_ms = static_cast<int>(std::stod(value) * 1000);
        } else if (key == "max-rss") {
            result.memory_used_kb = std::stoi(value);
        } else if (key == "exitcode") {
            result.exit_code = std::stoi(value);
        } else if (key == "status") {
            if (value == "TO") {
                result.time_limit_hit = true;
                result.success = false;
            } else if (value == "RE") {
                result.success = false;
            } else if (value == "SG") {
                result.success = false;
            }
        } else if (key == "message") {
            result.error = value;
        }
    }

    return result;
}

} // namespace aioj
