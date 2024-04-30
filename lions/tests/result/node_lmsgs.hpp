#ifndef NODE_LMSG_HPP
#define NODE_LMSG_HPP

#include "lmsg.hpp"

namespace lions {
struct AccelerometerMsg {
    Header header;

    float x;
    float y;
    float z;
};

struct MicrophoneMsg {
    Header header;

    float sound_level;
    char message[100];
};
struct PingMsg {
    Header header;
};

enum class msg_id {
    ACCELEROMETER = 0x01,
    MICROPHONE = 0x02,
    PING = 0x03,
};
}  // namespace lions

#endif