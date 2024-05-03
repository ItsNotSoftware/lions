#ifndef NODE_LMSG_HPP
#define NODE_LMSG_HPP

#include <string>

#include "lmsg.hpp"

namespace lions {

namespace msg_id {

constexpr uint8_t ACCELEROMETER = 0x01;
constexpr uint8_t MICROPHONE = 0x02;
constexpr uint8_t PING = 0x03;

}  // namespace msg_id

class AccelerometerMsg {
   public:
    Header header;

    float x;
    float y;
    float z;

    AccelerometerMsg(const LMsg &msg);
    LMsg encode(const uint8_t src, const uint8_t dst, const uint8_t next_hop);
};

class MicrophoneMsg {
   public:
    Header header;

    float sound_level;
    std::string message;

    MicrophoneMsg(const LMsg &msg);
    LMsg encode();
};
class PingMsg {
   public:
    Header header;

    PingMsg(const LMsg &msg);
    LMsg encode();
};

}  // namespace lions

#endif