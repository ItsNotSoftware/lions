

#include <numeric>

#include "lions.hpp"

namespace lions {

LMsg::LMsg(uint8_t payload_size) : payload_size(payload_size) {}

uint16_t LMsg::calculate_checksum() {
    checksum = 0;

    // Calculate checksum for the header
    checksum += header.src;
    checksum += header.dst;
    checksum += header.msg_id;
    checksum += header.next_hop;

    // Calculate checksum for the payload
    checksum += std::accumulate(payload, payload + payload_size, 0);

    checksum = ~checksum;

    return checksum;
}

bool LMsg::valid_checksum() {
    uint16_t prev_checksum = checksum;
    return calculate_checksum() == prev_checksum;
}

}  // namespace lions