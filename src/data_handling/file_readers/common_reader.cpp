#include <fstream>
#include <sstream>
#include <iostream>

#include "common_reader.hpp"

CommonReader_data CommonReader::GetData()
{
    std::ifstream ifs(filename_);

    // test for empty file
    try {
        if(ifs.peek() ==  std::ifstream::traits_type::eof()) {
            throw FileEmptyException();
        }
    } catch (std::exception &e) {
        std::cerr << "Error: " << e.what() << std::endl;
        throw FileEmptyException(); // rethrow, so can be handled outside
    }

    CommonReader_data data_vector;
    std::string line = "";

    // Read file line by line
    while(std::getline(ifs, line))
    {
        std::stringstream ss(line);
        std::vector<std::string> sub_vector;

        // Parse line to single std::string variables
        while(ss.good())
        {
            std::string sub;
            std::getline(ss, sub, delim_);
            sub_vector.push_back(sub);
        }
        data_vector.push_back(sub_vector);
    }

    ifs.close();

    return data_vector;
}