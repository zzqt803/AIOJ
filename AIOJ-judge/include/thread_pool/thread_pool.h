#pragma once

#include <functional>

namespace aioj {

class ThreadPool {
public:
    explicit ThreadPool(int threads);
    ~ThreadPool();
    void submit(std::function<void()> task);
};

} // namespace aioj
