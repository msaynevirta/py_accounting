#ifndef DATACORE_H
#define DATACORE_H

#include "../jsoncpp/include/json/json.h"
#include "../exception.hpp"

#include <fstream>
#include <iostream>

class DataCore {
public:
    DataCore() { };
    DataCore(const std::string& filename); // construct database from a json file

    // prevent copying of the main database for now
    DataCore(const DataCore&) = delete;
    DataCore& operator=(const DataCore&) = delete;

    // tell to use default
    ~DataCore() = default;

    Json::Value& GetRoot() { return root_; };
    std::vector<std::pair<std::string, std::string>> GetCategories(const int month) const; // print categories in a single month

    void ReadFromFile(const std::string& filename);
    void WriteToFile() const; // write main database back to a json file specified in filename_

    // give month as int to avoid type conversions with when using ctime
    void AppendToRoot(const Json::Value& transaction, const int month); // add new transaction under a month in root

    void Sort(const int month); // sort values by date in a single month
    void ConvertAliases(const int month); // convert beneficiaries / payers in a single month based on a alias database
    void SwapCategories(const int month); // swap categories (main / sub in wrong order)
    void CategoriesToOStream(std::ostream& os, const int month) const; // write transaction categories of a single month to a ostream
    void MobilePay(const int month); // fix mb transactions

    void MergeIdentical(const int month); // merge similar enough transactions automatically (same archival_id, entry_date & amount)
    void MergeSimilar(const int month, const bool fast); // merge similar ones, prompt user for final decision

protected:
    Json::Value root_;
    Json::String error_str_;
    std::string filename_;

private:
    Json::CharReaderBuilder builder_;
    Json::Value alias_db_;
};

#endif /* DATACORE_H */