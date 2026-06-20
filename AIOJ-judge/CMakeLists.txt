cmake_minimum_required(VERSION 3.14)
project(AIOJ-Judge LANGUAGES CXX)

# vcpkg 工具链
if(DEFINED ENV{VCPKG_ROOT})
    set(CMAKE_TOOLCHAIN_FILE "$ENV{VCPKG_ROOT}/scripts/buildsystems/vcpkg.cmake")
endif()

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# 依赖查找
find_package(Threads REQUIRED)
find_package(nlohmann_json CONFIG REQUIRED)

# hiredis：apt 包不提供 CMake config，手动查找
find_library(HIREDIS_LIBRARY hiredis REQUIRED)
find_path(HIREDIS_INCLUDE_DIR hiredis/hiredis.h REQUIRED)
add_library(hiredis::hiredis UNKNOWN IMPORTED)
set_target_properties(hiredis::hiredis PROPERTIES
    IMPORTED_LOCATION "${HIREDIS_LIBRARY}"
    INTERFACE_INCLUDE_DIRECTORIES "${HIREDIS_INCLUDE_DIR}"
)

# 源文件集合
set(COMMON_SOURCES
    src/common/types.cpp
    src/common/config.cpp
)

set(REDIS_SOURCES
    src/redis/redis_client.cpp
)

set(JUDGE_SOURCES
    src/judge/judge_worker.cpp
    src/judge/sandbox.cpp
    src/judge/language_handler.cpp
)

set(THREAD_POOL_SOURCES
    src/thread_pool/thread_pool.cpp
)

# 主库
add_library(aioj_judge_lib STATIC
    ${COMMON_SOURCES}
    ${REDIS_SOURCES}
    ${JUDGE_SOURCES}
    ${THREAD_POOL_SOURCES}
)

target_include_directories(aioj_judge_lib PUBLIC include)
target_link_libraries(aioj_judge_lib PUBLIC
    Threads::Threads
    hiredis::hiredis
    nlohmann_json::nlohmann_json
)

# 主程序
add_executable(aioj-judge src/main.cpp)
target_link_libraries(aioj-judge PRIVATE aioj_judge_lib)
