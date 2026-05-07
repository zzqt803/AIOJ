#include <catch2/catch_test_macros.hpp>
#include "thread_pool/thread_pool.h"

using namespace aioj;

TEST_CASE("ThreadPool creation", "[thread_pool]") {
    REQUIRE_NOTHROW(ThreadPool(2));
}
