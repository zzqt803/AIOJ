// src/judge/language_handler.cpp
#include "judge/language_handler.h"
#include <fstream>
#include <cstdlib>
#include <array>
#include <memory>

namespace aioj {

// 执行命令并捕获输出
static std::string exec_command(const std::string& cmd) {
    std::array<char, 128> buffer;
    std::string result;
    std::unique_ptr<FILE, decltype(&pclose)> pipe(popen(cmd.c_str(), "r"), pclose);
    if (!pipe) return "";
    while (fgets(buffer.data(), buffer.size(), pipe.get())) {
        result += buffer.data();
    }
    return result;
}

std::string CppHandler::compile(
    const std::string& source_code,
    const std::string& work_dir,
    std::string& compile_error
) {
    // 写入源文件
    std::string src_path = work_dir + "/main.cpp";
    std::ofstream src_file(src_path);
    if (!src_file.is_open()) {
        compile_error = "cannot create source file";
        return "";
    }
    src_file << source_code;
    src_file.close();

    // 编译
    std::string exe_path = work_dir + "/program";
    std::string cmd = "g++ -O2 -std=c++17 -o " + exe_path + " " + src_path + " 2>&1";
    compile_error = exec_command(cmd);

    // 检查是否生成了可执行文件
    std::ifstream exe_file(exe_path);
    if (!exe_file.good()) {
        return "";
    }

    return "program";
}

std::vector<std::string> CppHandler::get_run_command(
    const std::string& executable
) {
    return {"./" + executable};
}

std::unique_ptr<LanguageHandler> LanguageHandlerFactory::create(
    const std::string& language
) {
    if (language == "cpp" || language == "c") {
        return std::make_unique<CppHandler>();
    }
    return nullptr;
}

} // namespace aioj
