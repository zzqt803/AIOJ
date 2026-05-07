// test/test_thread_pool.cpp
#include <catch2/catch_test_macros.hpp>
#include "thread_pool/thread_pool.h"
#include <atomic>
#include <chrono>
#include <thread>

using namespace aioj;

TEST_CASE("ThreadPool basic task execution", "[thread_pool]") {
    ThreadPool pool(2);
    std::atomic<int> counter{0};

    for (int i = 0; i < 10; ++i) {
        pool.enqueue([&counter] {
            counter.fetch_add(1);
        });
    }

    // 等待任务完成
    std::this_thread::sleep_for(std::chrono::milliseconds(100));
    REQUIRE(counter.load() == 10);
}

TEST_CASE("ThreadPool thread count", "[thread_pool]") {
    ThreadPool pool(4);
    REQUIRE(pool.thread_count() == 4);
}

TEST_CASE("ThreadPool pending tasks", "[thread_pool]") {
    ThreadPool pool(1);
    REQUIRE(pool.pending_tasks() == 0);

    // 阻塞唯一的线程
    std::mutex mtx;
    mtx.lock();
    pool.enqueue([&mtx] {
        std::lock_guard<std::mutex> lock(mtx);
    });

    // 提交更多任务
    pool.enqueue([] {});
    pool.enqueue([] {});

    std::this_thread::sleep_for(std::chrono::milliseconds(10));
    REQUIRE(pool.pending_tasks() == 2);

    mtx.unlock();
}
