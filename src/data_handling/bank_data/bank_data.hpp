#ifndef BANKDATA_HPP
#define BANKDATA_HPP

#include <vector>
#include <ctime>

#include "../data_core.hpp"
#include "../../exception.hpp"

typedef struct Common_vals {
    std::string entry_date; // kirjauspäivä
    std::string value_date; // arvopäivä
    double amount;
    std::string beneficiary;
    std::pair<std::string, std::string> payment_method; // company handling the payment + card used (e.g. "OP", "Visa Debit" or "Cash", "Cash")

    std::string ref_num; // viitenumero
    std::string ref_num_payer; // maksajan viite (nordea)
    std::string archival_id; // arkistointitunnus (op)

    Common_vals() : entry_date("00-00-0000T00:00:00+00:00"), value_date("00-00-0000T00:00:00+00:00"), amount(0.0) { };
} Common_vals;

class BankData : public DataCore {
public:
    BankData() { };
    BankData(const std::string& filename);

    // prevent copying of the bank statements for now
    BankData(const BankData&) = delete;
    BankData& operator=(const BankData&) = delete;

    virtual ~BankData() = default;

    std::vector<std::vector<Common_vals>> GetExpenses() { return expenses_; };
    std::vector<std::vector<Common_vals>> GetIncome() { return income_; };

    virtual bool CollectData() = 0;
    bool WriteExpenses(Json::Value& root) const; // write expenses to the root_ object in DataCore
    bool WriteIncome(Json::Value& root) const; // write income to the root_ object in DataCore

    virtual std::pair<std::string, int> ConvertTime(const std::string time_str) const = 0;

protected:
    std::string filename_;

    std::vector<std::vector<Common_vals>> expenses_;
    std::vector<std::vector<Common_vals>> income_;
};

#endif /* BANKDATA_HPP */