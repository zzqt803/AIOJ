// src/main.cpp
#include "common/config.h"
#include "common/types.h"
#include "redis/redis_client.h"
#include "thread_pool/thread_pool.h"
#include "judge/judge_worker.h"
#include <nlohmann/json.hpp>
#include <iostream>
#include <csignal>
#include <atomic>
#include <unistd.h>

using namespace aioj;

static std::atomic<bool> running{true};

void signal_handler(int) {
    running = false;
}

int main(int argc, char* argv[]) {
    // 信号处理
    signal(SIGINT, signal_handler);
    signal(SIGTERM, signal_handler);

    // 加载配置
    std::string config_path = "config/judge.conf";
    if (argc > 1) {
        config_path = argv[1];
    }

    Config config;
    try {
        config = Config::load(config_path);
    } catch (const std::exception& e) {
        std::cerr << "failed to load config: " << e.what() << std::endl;
        return 1;
    }

    std::cout << "AIOJ Judge starting..." << std::endl;
    std::cout << "Redis: " << config.redis_host << ":" << config.redis_port << std::endl;
    std::cout << "Threads: " << config.thread_count << std::endl;

    // 连接Redis
    RedisClient* redis = nullptr;
    for (int retry = 0; retry < 3; ++retry) {
        try {
            redis = new RedisClient(config.redis_host, config.redis_port, config.redis_db);
            break;
        } catch (const std::exception& e) {
            std::cerr << "redis connect failed (attempt " << retry + 1 << "): " << e.what() << std::endl;
            if (retry < 2) {
                sleep(1);
            }
        }
    }

    if (!redis || !redis->is_connected()) {
        std::cerr << "cannot connect to redis, exiting" << std::endl;
        return 1;
    }

    // 创建线程池
    ThreadPool pool(config.thread_count);

    std::cout << "Judge ready, waiting for tasks..." << std::endl;

    // 主循环
    while (running) {
        std::string task_json = redis->brpop(config.task_queue, 5);

        if (task_json.empty()) {
            continue;
        }

        // 解析任务
        JudgeTask task;
        try {
            task = task_from_json(nlohmann::json::parse(task_json));
        } catch (const std::exception& e) {
            std::cerr << "failed to parse task: " << e.what() << std::endl;
            continue;
        }

        std::cout << "received task: " << task.submission_id << std::endl;

        // 提交到线程池
        pool.enqueue([task, &config, redis]() {
            JudgeWorker worker(config);
            JudgeResult result = worker.judge(task);

            // 推送结果
            nlohmann::json result_json = result;
            redis->lpush(config.result_queue, result_json.dump());

            std::cout << "task " << task.submission_id
                      << " completed: " << to_string(result.overall_status) << std::endl;
        });
    }

    std::cout << "shutting down..." << std::endl;
    delete redis;
    return 0;
}
