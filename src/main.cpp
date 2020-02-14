#include "data_handling/data_core.hpp"
#include "data_handling/bank_data/bank_data_op.hpp"
#include "data_handling/bank_data/bank_data_nordea.hpp"

#include <iostream>
#include <limits>
#include "exception.hpp"

void print_out(Json::Value root)
{
    std::cout << "-------------- TEST DATABASE ---------------" << std::endl;
    double tot = 0;
    for(int i = 1; i <= 12; i++)
    {
        for(auto it : root["expenses"]["months"][std::to_string(i)])
        {
            tot += it["amount"].asDouble();
        }
        std::cout << i << ": " << tot << std::endl;
        tot = 0;
    }
}

/*
    Template function for reading bank statements
*/
template<class T>
void read_bankdata(Json::Value& root, std::string& bank_name, std::string& filename){
    std::cout << "Please enter a file path to a " << bank_name << " bank statement: " << std::flush;
    std::cin >> filename;
    T bankdata(filename);

    bankdata.CollectData();
    bankdata.WriteExpenses(root);
    bankdata.WriteIncome(root);
}

void clear_stream(std::istream& is){
    is.clear();
    is.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
}

/*
    Month loop template, takes a class T member function pmemfn and object
    referece obj as parameters.
*/
template<class T>
void month_loop(void (T::*pmemfn)(int), T &obj)
{
    while(true) {
        int month;
        std::cout << "Please enter month as int or 0 for all months: " << std::flush;
        std::cin >> month;
        if(month > 0 && month <= 12) {
            (obj.*pmemfn)(month); // run member function for the specified month
            break;
        }
        else if(month == 0) {
            for(unsigned int i = 1; i <= 12; i++) {
                (obj.*pmemfn)(i); // run member function for each month
            }
            break;
        }
        else {
            std::cout << "Month must be between 1 ... 12" << std::endl;
        }
        clear_stream(std::cin); // clear stream before reading month again
    }
}



int main(void)
{
    std::cout << "cpp_accounting 2019\nTrying to read main database from default location src/data/main_database.json" << std::endl;

    DataCore core("data/main_database.json");

    while(true)
    {
        char letter; // opertation id

        std::cout << "\n\nPlease enter a letter code for a operation\n";
        std::cout << "Options:\n";
        std::cout << "A: categorise transactions & convert beneficiaries based on a alias database\n";
        std::cout << "B: load transactions from bank statement\n";
        std::cout << "C: swap categories\n";
        std::cout << "D: Fix MobilePay transactions\n";
        std::cout << "M: merge transactions\n";
        std::cout << "P: print out monthly totals\n";
        std::cout << "R: reload the main database from different file\n";
        std::cout << "S: sort transactions in a single month\n";
        std::cout << "W: write out main database\n\n";
        std::cout << "Q: quit" << std::endl;

        std::cin >> letter;
        switch(letter)
        {
            case 'A': case 'a':
            {
                month_loop<DataCore>(&DataCore::ConvertAliases, core);
                break;
            }
            case 'B': case 'b':
            {
                while(true) {
                    char bank;
                    std::cout << "Please enter bank as char (Nordea = N, OP = O): " << std::flush;
                    std::cin >> bank;

                    Json::Value& root = core.GetRoot();
                    std::string filename;

                    switch(bank)
                    {
                        case 'N': case 'n': // Nordea
                        {
                            std::string bank_name = "Nordea";
                            read_bankdata<BankDataNordea>(root, bank_name, filename);
                            break;
                        }
                        case 'O': case 'o': // OP
                        {
                            std::string bank_name = "OP";
                            read_bankdata<BankDataOP>(root, bank_name, filename);
                            break;
                        }
                        default:
                            std::cout << "Not valid bank id" << std::endl;
                            break;
                    }
                    break;
                }
                break;
            }
            case 'C': case 'c':
            {
                month_loop<DataCore>(&DataCore::SwapCategories, core);
                break;
            }
            case 'D': case 'd':
            {
                month_loop<DataCore>(&DataCore::MobilePay, core);
                break;
            }
            case 'M': case 'm':
            {
                char merge_letter, fast_letter;
                bool fast;

                std::cout << "Identical (I) or similar (S)? Do a fast merge (F)? " << std::flush;
                std::cin >> merge_letter;
                std::cin >> fast_letter;

                if(fast_letter == 'F' || fast_letter == 'f') {
                    fast = true;
                }
                else {
                    fast = false;
                }

                switch(merge_letter)
                {
                    case 'I': case 'i':
                    {
                        month_loop<DataCore>(&DataCore::MergeIdentical, core);
                        break;
                    }
                    case 'S': case 's':
                    {
                        while(true)
                        {
                            int month;
                            std::cout << "Please enter month as int or 0 for all months: " << std::flush;
                            std::cin >> month;
                            if(month > 0 && month <= 12)
                            {
                                core.MergeSimilar(month, fast); // run member function for the specified month
                                break;
                            }
                            else if(month == 0) {
                                for(unsigned int i = 1; i <= 12; i++)
                                {
                                    core.MergeSimilar(i, fast); // run member function for each month
                                }
                                break;
                            }
                            else {
                                std::cout << "Month must be between 1 ... 12" << std::endl;
                            }
                        }
                        clear_stream(std::cin); // clear stream before reading month again
                        break;
                    }
                }
                break;
            }
            case 'P': case 'p':
            {
                char print_letter;
                std::cout << "Monthly expenses (M) or categories (P)? " << std::flush;
                std::cin >> print_letter;

                switch (print_letter)
                {
                    case 'M': case 'm':
                        print_out(core.GetRoot());
                        break;
                    
                    case 'C': case 'c':
                    {
                        while(true)
                        {
                            int month;
                            std::cout << "Please enter month as int or 0 for all months: " << std::flush;
                            std::cin >> month;
                            if(month > 0 && month <= 12) {
                                core.CategoriesToOStream(std::cout, month);
                                break;
                            }
                            else if(month == 0) {
                                for(unsigned int i = 1; i <= 12; i++) {
                                    core.CategoriesToOStream(std::cout, i);
                                }
                                break;
                            }
                            else {
                                std::cout << "Month must be between 1 ... 12" << std::endl;
                            }
                        }
                    }
                }
                break;
            }
            case 'R': case 'r':
            {
                std::string filename;
                std::cout << "Please enter a file path to a new json database: " << std::flush;
                std::cin >> filename;
                core.ReadFromFile(filename);
                break;
            }
            case 'S': case 's':
            {
                month_loop<DataCore>(&DataCore::Sort, core);
                break;
            }
            case 'W': case 'w':
            {
                core.WriteToFile();
                break;
            }
            case 'Q': case 'q':
                return 0;
            
            default:
                std::cout << "Please enter a valid operation code" << std::endl;
                break;
        }
    }

    return 0;
}