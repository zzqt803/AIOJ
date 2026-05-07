// include/judge/language_handler.h
#pragma once

#include <string>
#include <vector>
#include <memory>

namespace aioj {

class LanguageHandler {
public:
    virtual ~LanguageHandler() = default;

    // 语言名称
    virtual std::string name() const = 0;

    // 编译源代码
    // 成功返回可执行文件名，失败返回空字符串并设置compile_error
    virtual std::string compile(
        const std::string& source_code,
        const std::string& work_dir,
        std::string& compile_error
    ) = 0;

    // 获取运行命令
    virtual std::vector<std::string> get_run_command(
        const std::string& executable
    ) = 0;

    // 是否需要编译
    virtual bool needs_compilation() const = 0;
};

// C/C++处理器
class CppHandler : public LanguageHandler {
public:
    std::string name() const override { return "cpp"; }

    std::string compile(
        const std::string& source_code,
        const std::string& work_dir,
        std::string& compile_error
    ) override;

    std::vector<std::string> get_run_command(
        const std::string& executable
    ) override;

    bool needs_compilation() const override { return true; }
};

// 语言处理器工厂
class LanguageHandlerFactory {
public:
    static std::unique_ptr<LanguageHandler> create(const std::string& language);
};

} // namespace aioj
