#ifndef EXCEPTION_H
#define EXCEPTION_H

#include <exception>

class CollectFailedException : public std::exception {
    virtual const char* what() const noexcept {
        return "Collecting values from parsed data failed";
    }
};

class FileEmptyException : public std::exception {
    virtual const char* what() const noexcept {
        return "File is empty";
    }
};

class NoAliasesException : public std::exception {
    virtual const char* what() const noexcept {
        return "Alias database is empty";
    }
};

#endif /* EXCEPTION_H */