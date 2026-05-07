#include "thread_pool/thread_pool.h"

namespace aioj {

ThreadPool::ThreadPool(int /*threads*/) {}
ThreadPool::~ThreadPool() {}
void ThreadPool::submit(std::function<void()> /*task*/) {}

} // namespace aioj
