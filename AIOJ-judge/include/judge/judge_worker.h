// include/judge/judge_worker.h
#pragma once

#include "common/types.h"
#include "common/config.h"
#include "judge/language_handler.h"
#include "judge/sandbox.h"

namespace aioj {

class JudgeWorker {
public:
    explicit JudgeWorker(const Config& config);

    // 执行评测任务
    JudgeResult judge(const JudgeTask& task);

private:
    const Config& config_;

    // 查找题目测试用例
    bool load_test_cases(
        const std::string& problem_id,
        std::vector<std::pair<std::string, std::string>>& cases
    );

    // 比较输出文件
    bool compare_output(
        const std::string& actual_file,
        const std::string& expected_file
    );
};

} // namespace aioj
