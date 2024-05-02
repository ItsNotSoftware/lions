#ifndef LMSG_HPP
#define LMSG_HPP

#include <cstdint>

namespace lions {
struct Header {
    uint8_t src_id;
    uint8_t dst_id;
    uint8_t msg_id;
    uint8_t msg_len;
    uint16_t checksum;
};

struct LMsg {
    Header header;
    uint8_t payload[248];
};

enum class msg_id {
    ACCELEROMETER = 0x01,
    MICROPHONE = 0x02,
    PING = 0x03,
};

uint16_t calculate_checksum(Header header, uint8_t* payload);
bool valid_checksum(Header header, uint8_t* payload);

}  // namespace lions

#endif