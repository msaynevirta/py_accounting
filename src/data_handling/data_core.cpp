#include "data_core.hpp"
#include "algorithm"

#include <vector>
#include <string>
#include <ctime>

time_t ParseDate(std::string date_cpp_str) // convert ISO 8601 date std::string to a time_t value
{
    tm date_tm = {}; // init as empty struct
    strptime(date_cpp_str.c_str(), "%Y-%m-%dT%H:%M:%S%z", &date_tm);

    date_tm.tm_isdst = -1; // dst info not available

    return mktime(&date_tm);
}

bool CompareEntryDate(Json::Value i, Json::Value j) // helper for sorting
{
    time_t t_i = ParseDate(i["entry_date"].asString());
    time_t t_j = ParseDate(j["entry_date"].asString());

    if(t_i == t_j) { // if same date, compare beneficiaries or payers
        if(i["beneficiary"].asString() < j["beneficiary"].asString() || i["payer"].asString() < j["payer"].asString()) {
            return true;
        }
    }
    else if(t_i > t_j) {
        return true;
    }
    return false;
}

bool CompareForAutoMerge(const Json::Value& i, const Json::Value& j, const std::string& sort_value) // helper for mergeidentical
{
    std::vector<std::string> variable_vector = {"archival_id",
                                                 "amount",
                                                 "entry_date",
                                                 "ref_number",
                                                 "ref_number_payer",
                                                 sort_value};

    for(auto it : variable_vector) {
        if(i[it] != j[it]) {
            return false;
        }
    }
    return true;
}

// helper for mergesimilar, returns false if required variables don't match
bool CompareForManualMerge(const Json::Value& i, const Json::Value& j, const std::string& sort_value, const bool fast)
{
    std::vector<std::string> variable_vector = {"amount", sort_value};
    std::vector<std::string> skip_vector = {"taxes", "sub_cat", "main_cat", "payment_method", "individual_products"}; // skip if no differences in these vars

    if(i["amount"] == j["amount"] && i[sort_value] == j[sort_value])
    {
        if(fast)
        {
            for(auto it : skip_vector)
            {
                if(i[it] != j[it])
                {
                    return true;
                }
            }
        }
        else {
            return true;
        }
    }
    return false;
}

std::vector<std::string> ParseOpString(std::string op_string, std::string sort_value) // helper for mergesimilar
{
    /*
    a = amount
    b = beneficiary / payer
    c = payment_method (card)
    e = entry_date
    i = archival_id
    m = main_cat
    p = individual_products
    r = ref_number & ref_number_payer
    s = sub_cat
    t = taxes
    v = value_date
    */
    std::vector<std::string> var_vector;

    for(char& c : op_string)
    {
        switch(c)
        {
            case '0':
                var_vector.push_back("0"); // it_to_check
                break;
            case '1':
                var_vector.push_back("1"); // it_second
                break;
            case 'a':
                var_vector.push_back("amount");
                break;
            case 'b':
                var_vector.push_back(sort_value);
                break;
            case 'c':
                var_vector.push_back("payment_method");
                break;
            case 'e':
                var_vector.push_back("entry_date");
                break;
            case 'i':
                var_vector.push_back("archival_id");
                break;
            case 'm':
                var_vector.push_back("main_cat");
                break;
            case 'p':
                var_vector.push_back("individual_products");
                break;
            case 'r':
                var_vector.push_back("ref_number");
                var_vector.push_back("ref_number_payer");
                break;
            case 's':
                var_vector.push_back("sub_cat");
                break;
            case 't':
                var_vector.push_back("taxes");
                break;
            case 'v':
                var_vector.push_back("value_date");
                break;
        }
    }
    return var_vector;
}

bool DisplayDiff(Json::Value& i, Json::Value& j, std::string sort_value)
{
    // Console highlighting
    std::string reset_colour = "\033[0m";
    std::string text_white = "\033[0;97m";
    std::string on_blue = "\033[44m";
    std::string on_red = "\033[41m";

    std::vector<std::string> transaction_vars = {"entry_date",
                                                 "value_date",
                                                 "amount",
                                                 "taxes",
                                                 sort_value,
                                                 "sub_cat",
                                                 "main_cat",
                                                 "ref_number",
                                                 "ref_number_payer",
                                                 "archival_id",
                                                 "payment_method",
                                                 "individual_products"};

    bool identical = true;
    std::vector<std::string> diff_vars;

    for(auto json_var : transaction_vars)
    {
        if(i[json_var] != j[json_var]) {
            identical = false;
        }
    }

    if(!identical) {
        std::cout << "\n\n";

        for(auto json_var : transaction_vars)
        {
            bool values_match = i[json_var] == j[json_var];

            if(!values_match) {
                std::cout << json_var << ": \n";
                std::cout << text_white << on_red << i[json_var] << reset_colour << "\n";
                std::cout << on_blue << j[json_var] << reset_colour << std::endl;
                identical = false;
            }
            else {
                std::cout  << json_var << ": \n";
                std::cout << i[json_var] << "\n" << j[json_var] << std::endl;
            }
        }
    }



    if(identical) {
        return true;
    } else {
        return false;
    }
}

DataCore::DataCore(const std::string& filename) : filename_(filename)
{
    DataCore::ReadFromFile(filename_);
}

void DataCore::ReadFromFile(const std::string& filename)
{
    filename_ = filename;
    std::ifstream root_ifs(filename_);
    std::ifstream alias_ifs("data/alias_database.json");

    // throw & handle error for empty / missing files
    try {
        if(root_ifs.peek() == std::ifstream::traits_type::eof() || alias_ifs.peek() == std::ifstream::traits_type::eof()) {
            throw FileEmptyException();
        }
    } catch (FileEmptyException::exception &e) {
        std::cerr << "Error: " << e.what() << std::endl;
    }

    builder_["precision"] = 8; // precision of float values
    Json::parseFromStream(builder_, root_ifs, &root_, &error_str_); // parse main database to root_
    Json::parseFromStream(builder_, alias_ifs, &alias_db_, &error_str_); // parse alias database to alias_db_
}

void DataCore::WriteToFile() const
{
    std::ofstream ofs(filename_);

    Json::StreamWriterBuilder builder;
    builder["commentStyle"] = "None"; // don't enter comments to the output file
    builder["indentation"] = "    "; // indent with 4 spaces
    builder["precision"] = 8; // precision of float values

    std::unique_ptr<Json::StreamWriter> writer(builder.newStreamWriter());
    writer->write(root_, &ofs);
}

void DataCore::AppendToRoot(const Json::Value& transaction, const int month)
{
    root_["expenses"]["months"][std::to_string(month)].append(transaction);
}

std::vector<std::pair<std::string, std::string>> DataCore::GetCategories(const int month) const
{
    std::vector<std::pair<std::string, std::string>> cat_vector;

    std::vector<std::string> sort_value_vector = {"expenses", "income"}; // go trough both expenses & income
    for(std::string& sort_value : sort_value_vector)
    {
        for(auto& it : root_[sort_value]["months"][std::to_string(month)])
        {
            std::pair<std::string, std::string> cat_pair = std::make_pair(it["main_cat"].asString(), it["sub_cat"].asString());

            bool already_in_vector = false;
            // check if already in vector
            for(auto it_second : cat_vector)
            {
                if(cat_pair == it_second) { already_in_vector = true; }
            }
            if(!already_in_vector) {
                cat_vector.push_back(cat_pair);
            }
        }
    }

    std::sort(cat_vector.begin(), cat_vector.end(),
              [](const std::pair<std::string, std::string>& a, const std::pair<std::string, std::string>& b)
              { return a.first < b.first; }); // sort working vector by main_cat

    return cat_vector;
}

void DataCore::Sort(const int month)
{
    // Sort values with insertion sort based on date & beneficiary
    Json::Value tmp;
    int j;

    std::vector<std::string> sort_value_vector = {"expenses", "income"}; // go trough both expenses & income

    for(std::string& sort_value : sort_value_vector)
    {
        Json::Value& transactions = root_[sort_value]["months"][std::to_string(month)];

        for(unsigned int i = 0; i < transactions.size(); i++)
        {
            tmp = transactions[i];
            for(j = i; j > 0 && CompareEntryDate(transactions[j-1], tmp); j--) {
                transactions[j] = transactions[j-1];
            }
            transactions[j] = tmp;
        }
    }
}

void DataCore::CategoriesToOStream(std::ostream& os, const int month) const
{
    std::vector<std::pair<std::string, std::string>> cat_vector = GetCategories(month);

    for(auto it : cat_vector)
    {
        os << it.first << ", " << it.second << std::endl; // write main_cat and sub_cat to ostream
    }
}

void DataCore::ConvertAliases(const int month)
{
    std::vector<std::string> sort_value_vector = {"expenses", "income"}; // go trough both expenses & income

    // check if aliases are missing
    try {
        if(alias_db_["aliases"] == Json::nullValue) {
            throw NoAliasesException();
        }
        for(auto alias_it : alias_db_["aliases"])
        {
            std::cout << "Checking alias \"" << alias_it[0].asString() << "\"" << std::endl;

            for(std::string& sort_value : sort_value_vector)
            {
                Json::Value& transactions = root_[sort_value]["months"][std::to_string(month)];

                for(Json::Value& it : transactions)
                {
                    if(it["beneficiary"].asString() == alias_it[0].asString())
                    { // expenses
                        it["beneficiary"] = alias_it[1];
                        it["sub_cat"] = alias_it[3].asString();
                        it["main_cat"] = alias_it[2].asString();
                    }
                    else if(it["payer"].asString() == alias_it[0].asString())
                    { // income
                        it["payer"] = alias_it[1];
                        it["sub_cat"] = alias_it[2];
                        it["main_cat"] = alias_it[3];
                    }
                }
            }
        }
    } catch (NoAliasesException::exception &e) {
        std::cerr << "Error: " << e.what() << std::endl;
    }
}

void DataCore::SwapCategories(const int month)
{
    std::vector<std::vector<std::string>> sort_value_vector = {{"expenses", "beneficiary"}, {"income", "payer"}}; // go trough both expenses & income
    for(auto sort_value : sort_value_vector)
    {
        for(auto& it : root_[sort_value[0]]["months"][std::to_string(month)])
        {
            char op;
            std::cout << "main: " << it["main_cat"] << ", Sub: " << it["sub_cat"] << "\n";
            
            if(it["main_cat"] != it["sub_cat"])
            {
                if(it["sub_cat"].asString() == "ravintola"
                   || it["sub_cat"].asString() == "asuminen"
                   || it["sub_cat"].asString() == "liikenne"
                   || it["sub_cat"].asString() == "tuki"
                   || it["main_cat"].asString() == "bank norwegian")
                {
                    it["main_cat"].swap(it["sub_cat"]); // autoswap common ones
                }
                else
                {
                    if(it["main_cat"].asString() == "ravintola"
                       || it["main_cat"].asString() == "asuminen"
                       || it["main_cat"].asString() == "liikenne"
                       || it["main_cat"].asString() == "tuki"
                       || it["main_cat"].asString() == "oma tilisiirto"
                       || it["main_cat"].asString() == "bank norwegian"
                       || it["main_cat"].asString() == "velka")
                    {
                        //skip
                    }
                    else
                    {
                        std::cout << "Swap (enter y to swap)?" << std::endl;
                        std::cin >> op;

                        if(op == 'y')
                        {
                            it["main_cat"].swap(it["sub_cat"]);
                        }
                    }
                }
            }
        }
    }
}

void DataCore::MobilePay(const int month)
{
    std::vector<std::vector<std::string>> sort_value_vector = {{"expenses", "beneficiary"}, {"income", "payer"}}; // go trough both expenses & income
    for(auto sort_value : sort_value_vector)
    {
        for(auto& it : root_[sort_value[0]]["months"][std::to_string(month)])
        {
            const std::string& recipient = it[sort_value[1]].asString();
            if(recipient.find("MobilePay") != std::string::npos || recipient.find("MOB.PAY") != std::string::npos) {
                if(it["main_cat"] == Json::nullValue && it["sub_cat"] == Json::nullValue)
                {
                    it["main_cat"] = "velka";
                    it["sub_cat"] = "mobilepay";
                }
                it["payment_method"] = Json::arrayValue;
                it["payment_method"].append("Danske Bank");
                it["payment_method"].append("MobilePay");
            }
        }
    }
}

void DataCore::MergeIdentical(const int month)
{
    std::vector<std::vector<std::string>> sort_value_vector = {{"expenses", "beneficiary"}, {"income", "payer"}}; // go trough both expenses & income
    for(auto sort_value : sort_value_vector)
    {
        Json::Value new_transaction_array;
        new_transaction_array["transactions"] = Json::arrayValue; // working array

        for(auto& it_to_check : root_[sort_value[0]]["months"][std::to_string(month)])
        {
            // check if transaction is already in working array
            bool in_new_array = false;
            bool individual_products_found = false;

            for(auto& it_new : new_transaction_array["transactions"])
            {
                // compare contents -> archival id, amount, beneficiary / payer, idividual products
                in_new_array = CompareForAutoMerge(it_to_check, it_new, sort_value[1]);

                if(in_new_array) // transaction found, break loop
                {

                    if(it_new["individual_products"] != it_to_check["individual_products"]
                    && it_to_check["individual_products"] != Json::nullValue) {
                        it_new["individual_products"] = it_to_check["individual_products"];
                    }
                    break;
                }
            }

            // copy transaction if not present in working array
            if(!in_new_array)
            {
                new_transaction_array["transactions"].append(it_to_check);
            }
        }

        // write working array in place of the original
        root_[sort_value[0]]["months"][std::to_string(month)] = new_transaction_array["transactions"];
    }
}

void DataCore::MergeSimilar(const int month, const bool fast)
{
    std::vector<std::vector<std::string>> sort_value_vector = {{"expenses", "beneficiary"}, {"income", "payer"}}; // go trough both expenses & income
    for(auto sort_value : sort_value_vector)
    {
        Json::Value new_transaction_array;
        new_transaction_array["transactions"] = Json::arrayValue; // working array

        unsigned int first = 0;

        std::cout << "\n\n----------- Checking " << sort_value[0] << " ----------------" << std::endl;

        for(auto& it_to_check : root_[sort_value[0]]["months"][std::to_string(month)])
        {
            if(first == 0) { // init working array
                new_transaction_array["transactions"].append(it_to_check);
                first++;
            }

            // check if transaction is already in working array
            bool possible_match = false;
            bool individual_products_found = false;
            bool merged = false;
            bool abort_merge = false;
            bool skip = false;

            for(auto& it_second : new_transaction_array["transactions"])
            {
                // compare contents -> archival id, amount, beneficiary / payer, idividual products
                possible_match = CompareForManualMerge(it_to_check, it_second, sort_value[1], fast);

                if(possible_match) // possible match, show diff & do edits
                {
                    bool identical = false;

                    while(!merged && !identical) {
                        identical = DisplayDiff(it_to_check, it_second, sort_value[1]);

                        if(!identical) {
                            std::string op_string;

                            // clear stream before reading op_string again
                            std::cin.clear();
                            std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');

                            std::cin >> op_string;
                            if(op_string == ",") {
                                it_second = it_to_check;
                                merged = true;
                            }
                            else if(op_string == ".") {
                                abort_merge = true;
                                break;
                            }
                            else if(op_string == "-") { // skip adding it_to_check
                                skip = true;
                                break; // skip merge
                            }
                            else if(op_string == "'") { // add both
                                break;
                            }
                            else
                            {
                                std::vector<std::string> var_vector = ParseOpString(op_string, sort_value[0]);

                                auto var = var_vector.begin();
                                var++; // skip first

                                if(var_vector[0] == "0") { // copy values from it_to_check
                                    for(; var != var_vector.end(); var++) {
                                        it_second[*var] = it_to_check[*var];
                                    }
                                }
                                else if(var_vector[0] == "1") { // copy values from it_second
                                    for(; var != var_vector.end(); var++) {
                                        it_to_check[*var] = it_second[*var];
                                    }
                                }
                            }
                        } else {
                            skip = true; // skip identical ones
                        }
                    }
                }
            }
            if(abort_merge) {
                break;
            }
            if(!merged && !skip) {
                std::cout << it_to_check[sort_value[1]] << std::endl;
                new_transaction_array["transactions"].append(it_to_check);
            }
        }

        std::cout << "Writing" << std::endl;

        // write working array in place of the original
        root_[sort_value[0]]["months"][std::to_string(month)] = new_transaction_array["transactions"];
    }
}