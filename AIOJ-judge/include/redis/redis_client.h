// include/redis/redis_client.h
#pragma once

#include <string>
#include <hiredis/hiredis.h>

namespace aioj {

class RedisClient {
public:
    RedisClient(const std::string& host, int port, int db = 0);
    ~RedisClient();

    // 禁止拷贝
    RedisClient(const RedisClient&) = delete;
    RedisClient& operator=(const RedisClient&) = delete;

    // 检查连接是否正常
    bool is_connected() const;

    // LPUSH：推送到队列左侧
    bool lpush(const std::string& queue, const std::string& value);

    // BRPOP：阻塞从队列右侧弹出，timeout秒
    // 返回空字符串表示超时
    std::string brpop(const std::string& queue, int timeout_sec = 5);

    // 重新连接
    bool reconnect();

private:
    std::string host_;
    int port_;
    int db_;
    redisContext* context_;
};

} // namespace aioj
