#pragma once

#include <string>

namespace aioj {

class LanguageHandler {
public:
    LanguageHandler();
    ~LanguageHandler();
    bool compile(const std::string& language, const std::string& source_code);
};

} // namespace aioj
