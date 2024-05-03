#include "node_lmsgs.hpp"

#include <algorithm>

namespace lions {
AccelerometerMsg::AccelerometerMsg(const LMsg& msg) {
    header = msg.header;
    x = *reinterpret_cast<const float*>(&msg.payload[0]);
    y = *reinterpret_cast<const float*>(&msg.payload[4]);
    z = *reinterpret_cast<const float*>(&msg.payload[8]);
}

LMsg AccelerometerMsg::encode(const uint8_t src, const uint8_t dst, const uint8_t next_hop) {
    LMsg msg(12);

    msg.header.src = src;
    msg.header.dst = dst;
    msg.header.next_hop = next_hop;
    msg.header.msg_id = static_cast<uint8_t>(msg_id::ACCELEROMETER);

    *reinterpret_cast<float*>(&msg.payload[0]) = x;
    *reinterpret_cast<float*>(&msg.payload[4]) = y;
    *reinterpret_cast<float*>(&msg.payload[8]) = z;

    msg.calculate_checksum();

    return msg;
}

MicrophoneMsg::MicrophoneMsg(const LMsg& msg) {
    header = msg.header;
    sound_level = *reinterpret_cast<const float*>(&msg.payload[0]);
    message = std::string(reinterpret_cast<const char*>(&msg.payload[4]), 248);
}

LMsg MicrophoneMsg::encode() {
    LMsg msg(252);

    msg.header.src = header.src;
    msg.header.dst = header.dst;
    msg.header.next_hop = header.next_hop;
    msg.header.msg_id = static_cast<uint8_t>(msg_id::MICROPHONE);

    *reinterpret_cast<float*>(&msg.payload[0]) = sound_level;
    std::copy(message.begin(), message.end(), msg.payload + 4);

    msg.calculate_checksum();

    return msg;
}

PingMsg::PingMsg(const LMsg& msg) { header = msg.header; }

LMsg PingMsg::encode() {
    LMsg msg(0);

    msg.header.src = header.src;
    msg.header.dst = header.dst;
    msg.header.next_hop = header.next_hop;
    msg.header.msg_id = static_cast<uint8_t>(msg_id::PING);

    msg.calculate_checksum();

    return msg;
}
}  // namespace lions