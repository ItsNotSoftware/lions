#ifndef LMSG_HPP
#define LMSG_HPP

#include <cstdint>

namespace lions {
struct Header {
    uint8_t src;
    uint8_t dst;
    uint8_t next_hop;
    uint8_t msg_id;
};

class LMsg {
   public:
    Header header;
    uint8_t payload[248];

    LMsg(uint8_t payload_size);
    uint16_t calculate_checksum();
    bool valid_checksum();

   private:
    uint8_t payload_size;
    uint16_t checksum;
};

enum class msg_id {
    ACCELEROMETER = 0x01,
    MICROPHONE = 0x02,
    PING = 0x03,
};

}  // namespace lions

#endif