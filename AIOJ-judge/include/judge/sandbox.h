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

    // 准备可执行文件（复制到沙箱）
    bool prepare_executable(const std::string& executable_path);

    // 执行命令（使用已准备好的可执行文件）
    SandboxResult execute(
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
