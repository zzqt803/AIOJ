#include "redis/redis_client.h"

namespace aioj {

RedisClient::RedisClient(const std::string& /*host*/, int /*port*/) {}
RedisClient::~RedisClient() {}
bool RedisClient::connect() { return true; }
void RedisClient::disconnect() {}

} // namespace aioj
