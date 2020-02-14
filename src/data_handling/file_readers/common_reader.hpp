#ifndef COMMONREADER_H
#define COMMONREADER_H

#include <vector>
#include <string>

#include "../../exception.hpp"

typedef std::vector<std::vector<std::string>> CommonReader_data;

class CommonReader {
public:
    CommonReader(std::string filename, char delim) : filename_(filename), delim_(delim) { };

    // prevent copying for now
    CommonReader(const CommonReader&) = delete;
    CommonReader& operator=(const CommonReader&) = delete;

    ~CommonReader() = default;

    CommonReader_data GetData();

private:
    std::string filename_;
    char delim_;
};

#endif /* COMMONREADER_H */