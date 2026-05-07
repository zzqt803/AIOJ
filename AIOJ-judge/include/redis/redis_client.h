#pragma once

#include <string>

namespace aioj {

class RedisClient {
public:
    RedisClient(const std::string& host, int port);
    ~RedisClient();
    bool connect();
    void disconnect();
};

} // namespace aioj
