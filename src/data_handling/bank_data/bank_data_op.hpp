#include "bank_data.hpp"

class BankDataOP : public BankData {
public:
    BankDataOP(const std::string& filename) : BankData(filename) { };

    // prevent copying of the bank statements for now
    BankDataOP(const BankDataOP&) = delete;
    BankDataOP& operator=(const BankDataOP&) = delete;

    ~BankDataOP() = default;

    virtual bool CollectData();
    virtual std::pair<std::string, int> ConvertTime(const std::string time_str) const;
};