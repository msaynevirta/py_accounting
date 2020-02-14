#include <algorithm>
#include <stdexcept>
#include <iostream>
#include <vector>

#include "bank_data_op.hpp"
#include "../file_readers/common_reader.hpp"

std::string RemoveQuotes(std::string& in) {
    std::string::iterator new_end = std::remove(in.begin(), in.end(), '\"'); // remove '\"' from string so stod works
    if(new_end != in.end())
    {
        in = in.substr(0, in.size()-2);
    }

    return in;
}

std::pair<std::string, int> BankDataOP::ConvertTime(const std::string time_str) const {
    std::string time_format = "%d.%m.%Y";
    struct tm tm = {0};
    char buffer[256];

    strptime(time_str.c_str(), time_format.c_str(), &tm);
    strftime(buffer, sizeof(buffer), "%FT%T%z", &tm);

    std::string time_cpp_str(buffer);
    return std::make_pair(time_cpp_str, tm.tm_mon);
}

bool BankDataOP::CollectData() {
    CommonReader sdv(filename_, ';');
    CommonReader_data raw_data;

    try {
        raw_data = sdv.GetData();
    } catch (FileEmptyException::exception &e) { // if file is empty / missing
        std::cerr << "Error: Collecting data failed" << std::endl;
        return false;
    }

    std::vector<std::string> new_vector; // working vector for storing the cleaned data
    
    for(std::vector<std::string> it_line : raw_data) {

        // clean quotes from data
        for(std::string it : it_line) {
            it = RemoveQuotes(it);
            new_vector.push_back(it);
        };

        it_line = new_vector; // replace old vector with the cleaned one
        new_vector.clear(); // clean the working vector for a new iteration

        Common_vals vals;

        // read values from raw_data
        try {
            if(it_line.at(0) != "Kirjausp�iv�") {
            try {
                // amount
                try {
                    
                    std::replace(it_line.at(2).begin(), it_line.at(2).end(), ',', '.'); // convert commas to dot
                    vals.amount = std::stod(it_line.at(2));
                } catch (std::invalid_argument) {
                    std::cerr << "Error: conversion to double failed (" << it_line[2] << ")" << std::endl;
                    throw CollectFailedException();
                }

                vals.beneficiary = it_line.at(5);
                vals.entry_date = ConvertTime(it_line.at(0)).first;
                vals.value_date = ConvertTime(it_line.at(1)).first;

                // payment method from csv as an int
                int payment_type = 0;

                try {
                    payment_type = std::stod(it_line.at(3));
                } catch (std::invalid_argument) {
                    std::cerr << "Error: conversion to int failed (" << it_line.at(3) << ")" << std::endl;
                }

                // 162 == pankkikorttimaksu
                if(payment_type == 162) {
                    vals.payment_method = std::make_pair("OP", "Visa Debit");
                }

                // 106 == tilisiirto
                // 129 == maksupalvelu
                // 521 == etuus (asumistuki)
                // 524 == etuus (opintotuki)
                else if(payment_type == 106 || payment_type == 129 || payment_type == 521 || payment_type == 524) {
                    vals.payment_method = std::make_pair("OP", "Wire");
                }

                if(it_line.at(7) != "" && it_line.at(7).length() < 21) {
                    vals.ref_num = it_line.at(7);
                }

                if(it_line.at(9)[8] == '/' && it_line.at(9)[15] == '/') {
                    vals.archival_id = it_line.at(9);
                }

            } catch (std::out_of_range &e) {
                std::cerr << "Error: " << e.what() << std::endl;
                throw CollectFailedException();
            }

            int month = ConvertTime(it_line.at(0)).second;

            // if amount less than 0 -> write as an expense
            if (vals.amount <= 0){
                expenses_[month].push_back(vals);
            }
            // write as income
            else {
                income_[month].push_back(vals);
            }
            }
        } catch (CollectFailedException::exception &e) {
            std::cerr << "Error: " << e.what() << " -> skip adding malformed entry" << std::endl;
        }
    }
    return true;
}