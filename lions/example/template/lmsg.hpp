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

}  // namespace lions

#endif