#include "bank_data.hpp"

BankData::BankData(const std::string& filename) : filename_(filename) {
    // Space for each month's data
    expenses_.resize(12);
    income_.resize(12);
}

bool BankData::WriteExpenses(Json::Value& root) const
{
    Json::Value new_expense;

    for(int i = 0; i <= 11; i++) {
        // Create empty array if the month is empty (null)
        if(root["expenses"]["months"][std::to_string(i+1)] == Json::Value::null) {
            root["expenses"]["months"][std::to_string(i+1)] = Json::Value(Json::arrayValue);
        }

        for(auto it : expenses_[i]) {
            // Create a Json::Value object
            new_expense["entry_date"] = it.entry_date;
            new_expense["value_date"] = it.value_date;
            new_expense["amount"] = -1 * it.amount; // write as positive values
            new_expense["beneficiary"] = it.beneficiary;

            new_expense["payment_method"] = Json::Value(Json::arrayValue);
            new_expense["payment_method"].append(it.payment_method.first);
            new_expense["payment_method"].append(it.payment_method.second);

            new_expense["ref_number"] = it.ref_num;
            new_expense["ref_number_payer"] = it.ref_num_payer;
            new_expense["archival_id"] = it.archival_id;

            // Append the created object to the correct month
            root["expenses"]["months"][std::to_string(i+1)].append(new_expense);
        }
    }
}

bool BankData::WriteIncome(Json::Value& root) const
{
    Json::Value new_income;

    for(int i = 0; i <= 11; i++) {

        // Create empty array if the month is empty (null)
        if(root["income"]["months"][std::to_string(i+1)] == Json::Value::null) {
            root["income"]["months"][std::to_string(i+1)] = Json::Value(Json::arrayValue);
        }
        for(auto it : income_[i]) {
            // Create a Json::Value object
            new_income["entry_date"] = it.entry_date;
            new_income["value_date"] = it.value_date;
            new_income["amount"] = it.amount;
            new_income["payer"] = it.beneficiary;

            new_income["payment_method"] = Json::Value(Json::arrayValue);
            new_income["payment_method"].append(it.payment_method.first);
            new_income["payment_method"].append(it.payment_method.second);

            new_income["ref_number"] = it.ref_num;
            new_income["ref_number_payer"] = it.ref_num_payer;
            new_income["archival_id"] = it.archival_id;

            // Append the created object to the correct month
            root["income"]["months"][std::to_string(i+1)].append(new_income);
        }
    }
}
