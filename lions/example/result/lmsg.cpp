#include "lmsg.hpp"

namespace lions {
uint16_t calculate_checksum(Header header, uint8_t* payload) {
    uint16_t checksum = 0;

    checksum += header.src_id;
    checksum += header.dst_id;
    checksum += header.msg_id;
    checksum += header.msg_len;

    for (uint8_t i = 0; i < header.msg_len; i++) {
        checksum += payload[i];
    }

    return ~checksum;
}

bool valid_checksum(Header header, uint8_t* payload) {
    return calculate_checksum(header, payload) == header.checksum;
}
}  // namespace lions