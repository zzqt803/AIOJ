// src/redis/redis_client.cpp
#include "redis/redis_client.h"
#include <stdexcept>

namespace aioj {

RedisClient::RedisClient(const std::string& host, int port, int db)
    : host_(host), port_(port), db_(db), context_(nullptr) {
    context_ = redisConnect(host.c_str(), port);
    if (context_ == nullptr || context_->err) {
        std::string err = context_ ? context_->errstr : "cannot allocate context";
        if (context_) redisFree(context_);
        context_ = nullptr;
        throw std::runtime_error("redis connect failed: " + err);
    }

    // 选择数据库
    if (db != 0) {
        redisReply* reply = (redisReply*)redisCommand(context_, "SELECT %d", db);
        if (reply) freeReplyObject(reply);
    }
}

RedisClient::~RedisClient() {
    if (context_) {
        redisFree(context_);
    }
}

bool RedisClient::is_connected() const {
    return context_ != nullptr && !context_->err;
}

bool RedisClient::reconnect() {
    if (context_) {
        redisFree(context_);
    }
    context_ = redisConnect(host_.c_str(), port_);
    if (context_ == nullptr || context_->err) {
        if (context_) redisFree(context_);
        context_ = nullptr;
        return false;
    }
    if (db_ != 0) {
        redisReply* reply = (redisReply*)redisCommand(context_, "SELECT %d", db_);
        if (reply) freeReplyObject(reply);
    }
    return true;
}

bool RedisClient::lpush(const std::string& queue, const std::string& value) {
    redisReply* reply = (redisReply*)redisCommand(
        context_, "LPUSH %s %s", queue.c_str(), value.c_str()
    );
    if (!reply) {
        return false;
    }
    bool ok = (reply->type != REDIS_REPLY_ERROR);
    freeReplyObject(reply);
    return ok;
}

std::string RedisClient::brpop(const std::string& queue, int timeout_sec) {
    redisReply* reply = (redisReply*)redisCommand(
        context_, "BRPOP %s %d", queue.c_str(), timeout_sec
    );
    if (!reply) {
        return "";
    }

    std::string result;
    if (reply->type == REDIS_REPLY_ARRAY && reply->elements == 2) {
        result = reply->element[1]->str;
    }

    freeReplyObject(reply);
    return result;
}

} // namespace aioj
