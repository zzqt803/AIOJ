// include/judge/sandbox.h
#pragma once

#include <string>

namespace aioj {

// isolate执行结果
struct SandboxResult {
    bool success;           // 是否成功执行
    int exit_code;          // 程序退出码
    int time_used_ms;       // CPU时间（毫秒）
    int memory_used_kb;     // 内存使用（KB）
    bool time_limit_hit;    // 是否超时
    bool memory_limit_hit;  // 是否内存超限
    std::string error;      // 错误信息
};

class Sandbox {
public:
    Sandbox(int box_id, const std::string& work_dir);
    ~Sandbox();

    // 初始化沙箱
    bool init();

    // 清理沙箱
    void cleanup();

    // 执行命令
    // time_limit_ms: CPU时间限制（毫秒）
    // memory_limit_kb: 内存限制（KB）
    SandboxResult execute(
        const std::string& command,
        const std::string& input_file,
        const std::string& output_file,
        int time_limit_ms,
        int memory_limit_kb
    );

private:
    int box_id_;
    std::string work_dir_;
    bool initialized_;

    // 解析isolate的meta文件
    SandboxResult parse_meta(const std::string& meta_file);
};

} // namespace aioj
