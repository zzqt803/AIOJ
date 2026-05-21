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
    std::string config_path = "../config/judge.conf";
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

    // 连接Redis（用于接收任务）
    RedisClient* redis_recv = nullptr;
    for (int retry = 0; retry < 3; ++retry) {
        try {
            redis_recv = new RedisClient(config.redis_host, config.redis_port, config.redis_db);
            break;
        } catch (const std::exception& e) {
            std::cerr << "redis connect failed (attempt " << retry + 1 << "): " << e.what() << std::endl;
            if (retry < 2) {
                sleep(1);
            }
        }
    }

    if (!redis_recv || !redis_recv->is_connected()) {
        std::cerr << "cannot connect to redis, exiting" << std::endl;
        return 1;
    }

    // 连接Redis（用于发送结果）
    RedisClient* redis_send = nullptr;
    try {
        redis_send = new RedisClient(config.redis_host, config.redis_port, config.redis_db);
    } catch (const std::exception& e) {
        std::cerr << "cannot create redis send connection: " << e.what() << std::endl;
        delete redis_recv;
        return 1;
    }

    // 创建线程池
    ThreadPool pool(config.thread_count);

    std::cout << "Judge ready, waiting for tasks..." << std::endl;

    // 主循环
    while (running) {
        // 使用单独的连接接收任务（阻塞5秒）
        std::string task_json = redis_recv->brpop(config.task_queue, 5);

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

        // 提交到线程池（使用单独的发送连接）
        pool.enqueue([task, &config, redis_send]() {
            JudgeWorker worker(config);
            JudgeResult result = worker.judge(task);

            // 推送结果（使用单独的连接，无需加锁）
            nlohmann::json result_json = result;
            redis_send->lpush(config.result_queue, result_json.dump());

            std::cout << "task " << task.submission_id
                      << " completed: " << to_string(result.overall_status) << std::endl;
        });
    }

    std::cout << "shutting down..." << std::endl;
    delete redis_recv;
    delete redis_send;
    return 0;
}
