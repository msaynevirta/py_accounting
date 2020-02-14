#include <algorithm>
#include <stdexcept>
#include <iostream>
#include <vector>

#include "bank_data_nordea.hpp"
#include "../file_readers/common_reader.hpp"

std::pair<std::string, int> BankDataNordea::ConvertTime(const std::string time_str) const {
    std::string time_format = "%d.%m.%Y";
    struct tm tm = {0};
    char buffer[256];

    strptime(time_str.c_str(), time_format.c_str(), &tm);
    strftime(buffer, sizeof(buffer), "%FT%T%z", &tm);

    std::string time_cpp_str(buffer);
    return std::make_pair(time_cpp_str, tm.tm_mon);
}

bool BankDataNordea::CollectData() {
    CommonReader csv(filename_, '\t');
    CommonReader_data raw_data;

    try {
        raw_data = csv.GetData();
    } catch (FileEmptyException::exception &e) { // if file is empty / missing
        std::cerr << "Error: Collecting data failed" << std::endl;
        return false;
    }

    std::vector<std::string> new_vector; // working vector for storing the cleaned data
    
    for(auto it_line : raw_data) {

        // clean quotes from data
        for(std::string it : it_line) {
            new_vector.push_back(it);
        };

        it_line = new_vector; // replace old vector with the cleaned one
        new_vector.clear(); // clean the working vector for a new iteration

        Common_vals vals;
        
        // read values from raw_data
        try {
            if(it_line.size() > 1 && it_line.at(0) != "Kirjauspäivä" && it_line.at(0) != "Tilinumero") {
            try {
                // amount
                try {
                    std::replace(it_line.at(3).begin(), it_line.at(3).end(), ',', '.');
                    vals.amount = std::stod(it_line.at(3));
                } catch (std::invalid_argument) {
                    std::cerr << "Error: conversion to double failed (" << it_line[3] << ")" << std::endl;
                }

                vals.beneficiary = it_line.at(4);
                vals.entry_date = ConvertTime(it_line.at(0)).first;
                vals.value_date = ConvertTime(it_line.at(1)).first;

                // Sort wire and card payments
                std::size_t foundMB1 = (it_line.at(4)).find("MobilePay");
                std::size_t foundMB2 = (it_line.at(4)).find("MOB.PAY*");

                if(it_line.at(7) == "e-maksu" 
                   || it_line.at(7) == "e-lasku"
                   || foundMB1 != std::string::npos 
                   || foundMB2 != std::string::npos) {
                   vals.payment_method = std::make_pair("Nordea", "Wire");
                }
                else {
                    vals.payment_method = std::make_pair("Nordea", "Visa Electron");
                }
                
                try {
                    vals.ref_num = it_line.at(8);
                } catch (std::invalid_argument) {
                    std::cerr << "Error: conversion to string failed (" << it_line[8] << ")" << std::endl;
                    throw CollectFailedException();
                }

                try {                   
                    vals.ref_num_payer = it_line.at(9);
                } catch (std::invalid_argument) {
                    std::cerr << "Error: conversion to string failed (" << it_line[9] << ")" << std::endl;
                    throw CollectFailedException();
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