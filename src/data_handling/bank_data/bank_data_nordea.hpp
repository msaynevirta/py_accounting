#include "bank_data.hpp"

class BankDataNordea : public BankData {
public:
    BankDataNordea(const std::string& filename) : BankData(filename) { };

    // prevent copying of the bank statements for now
    BankDataNordea(const BankDataNordea&) = delete;
    BankDataNordea& operator=(const BankDataNordea&) = delete;

    ~BankDataNordea() = default;

    virtual bool CollectData();
    virtual std::pair<std::string, int> ConvertTime(const std::string time_str) const;
};