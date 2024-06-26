/**
 * @file lions.cpp
 *
 * @brief Checksum Calculation and Validation
 * 
 * This file contains the implementation of the message classes generated by the Lions Compiler.
 * 
 * @details
 * This file was generated by the Lions Compiler (https://github.com/ItsNotSoftware/lions) on .
 * Modifying this file manually is not recommended as it may lead to unexpected behavior.
 * 
 * @note
 * Generated files should not be manually edited.
 * 
 * @author Lions Compiler
*/

#include <numeric>

#include "lions.hpp"

namespace lions {

LMsg::LMsg(uint8_t payload_size) : payload_size(payload_size) {}

uint16_t LMsg::calculate_checksum() {
    header.checksum = 0;

    // Calculate checksum for the header
    header.checksum += header.src;
    header.checksum += header.dst;
    header.checksum += header.msg_id;
    header.checksum += header.next_hop;

    // Calculate checksum for the payload
    header.checksum += std::accumulate(payload, payload + payload_size, 0);

    header.checksum = ~header.checksum;

    return header.checksum;
}

bool LMsg::valid_checksum() {
    uint16_t prev_checksum = header.checksum;
    return calculate_checksum() == prev_checksum;
}

}  // namespace lions