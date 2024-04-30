#include "node_lmsgs.hpp"

#include <algorithm>

namespace lions {
AccelerometerMsg decode_accelerometer_msg(const LMsg& msg) {
    AccelerometerMsg result;

    result.header = msg.header;
    result.x = *reinterpret_cast<const float*>(&msg.payload[0]);
    result.y = *reinterpret_cast<const float*>(&msg.payload[4]);
    result.z = *reinterpret_cast<const float*>(&msg.payload[8]);

    return result;
}

LMsg encode_accelerometer_msg(const uint8_t src_id, const uint8_t dst_id,
                              const AccelerometerMsg& msg) {
    LMsg result;

    *reinterpret_cast<float*>(&result.payload[0]) = msg.x;
    *reinterpret_cast<float*>(&result.payload[4]) = msg.y;
    *reinterpret_cast<float*>(&result.payload[8]) = msg.z;

    result.header.src_id = src_id;
    result.header.dst_id = dst_id;
    result.header.msg_id = (uint8_t)msg_id::ACCELEROMETER;
    result.header.msg_len = sizeof(float) * 3;
    result.header.checksum = calculate_checksum(result.header, result.payload);

    return result;
}

MicrophoneMsg decode_microphone_msg(const LMsg& msg) {
    MicrophoneMsg result;

    result.header = msg.header;
    result.sound_level = *reinterpret_cast<const float*>(&msg.payload[0]);
    std::copy(msg.payload + 2, msg.payload + 104, result.message);

    return result;
}

LMsg encode_microphone_msg(const uint8_t src_id, const uint8_t dst_id, const MicrophoneMsg& msg) {
    LMsg result;

    *reinterpret_cast<float*>(&result.payload[0]) = msg.sound_level;
    std::copy(msg.message, msg.message + 100, result.payload + 4);

    result.header.src_id = src_id;
    result.header.dst_id = dst_id;
    result.header.msg_id = (uint8_t)msg_id::MICROPHONE;
    result.header.msg_len = sizeof(float) + 100;
    result.header.checksum = calculate_checksum(result.header, result.payload);

    return result;
}

PingMsg decode_ping_msg(const LMsg& msg) {
    PingMsg result;

    result.header = msg.header;

    return result;
}

LMsg encode_ping_msg(const uint8_t src_id, const uint8_t dst_id, const PingMsg& msg) {
    LMsg result;

    result.header.src_id = src_id;
    result.header.dst_id = dst_id;
    result.header.msg_id = (uint8_t)msg_id::PING;
    result.header.msg_len = 0;
    result.header.checksum = calculate_checksum(result.header, result.payload);

    return result;
}
}  // namespace lions