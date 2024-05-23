/**
 * @file multiple_lmsg.cpp
 *
 * @brief Implementation of multiple_lmsg.hpp Classes
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

#include <algorithm>
#include <utility>

#include "multiple_lmsg.hpp"

namespace lions {

AccelerometerMsg::AccelerometerMsg(const float acc_x, const float acc_y, const float acc_z)
    : acc_x(acc_x), acc_y(acc_y), acc_z(acc_z) {}

AccelerometerMsg::AccelerometerMsg(const LMsg &msg) {
    header = std::move(msg.header);

    acc_x = *reinterpret_cast<const float *>(&msg.payload[0]);
    acc_y = *reinterpret_cast<const float *>(&msg.payload[4]);
    acc_z = *reinterpret_cast<const float *>(&msg.payload[8]);
}

LMsg AccelerometerMsg::encode(const uint8_t src, const uint8_t dst, const uint8_t next_hop) {
    LMsg msg(12);

    msg.header.src = src;
    msg.header.dst = dst;
    msg.header.next_hop = next_hop;
    msg.header.msg_id = static_cast<uint8_t>(msg_id::ACCELEROMETER);

    *reinterpret_cast<float *>(&msg.payload[0]) = acc_x;
    *reinterpret_cast<float *>(&msg.payload[4]) = acc_y;
    *reinterpret_cast<float *>(&msg.payload[8]) = acc_z;
    msg.calculate_checksum();

    return msg;
}

MicrophoneMsg::MicrophoneMsg(const int16_t sound_level, const std::string message)
    : sound_level(sound_level), message(message) {}

MicrophoneMsg::MicrophoneMsg(const LMsg &msg) {
    header = std::move(msg.header);

    sound_level = *reinterpret_cast<const int16_t *>(&msg.payload[0]);
    message = std::string(reinterpret_cast<const char *>(&msg.payload[2]), 100);
}

LMsg MicrophoneMsg::encode(const uint8_t src, const uint8_t dst, const uint8_t next_hop) {
    LMsg msg(102);

    msg.header.src = src;
    msg.header.dst = dst;
    msg.header.next_hop = next_hop;
    msg.header.msg_id = static_cast<uint8_t>(msg_id::MICROPHONE);

    *reinterpret_cast<int16_t *>(&msg.payload[0]) = sound_level;
    std::copy(message.begin(), message.end(), msg.payload + 2);
    msg.payload[2 + message.size()] = '\0';  // terminate string

    msg.calculate_checksum();

    return msg;
}

PingMsg::PingMsg() {}

PingMsg::PingMsg(const LMsg &msg) { header = std::move(msg.header); }

LMsg PingMsg::encode(const uint8_t src, const uint8_t dst, const uint8_t next_hop) {
    LMsg msg(0);

    msg.header.src = src;
    msg.header.dst = dst;
    msg.header.next_hop = next_hop;
    msg.header.msg_id = static_cast<uint8_t>(msg_id::PING);

    msg.calculate_checksum();

    return msg;
}

}  // namespace lions