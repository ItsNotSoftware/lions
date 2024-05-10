#include <stdio.h>

#include <iostream>

#include "generated_code/my_messages.hpp"  // Include the generated messages.

// Define a constant for the device identifier used in the message.
constexpr uint8_t this_device_id = 1;
constexpr uint8_t broadcast_id = 255;

// ====================================================================================
// User created functions to send messages depending on the hardware/protocol.
//
// NOTE: this is just an example, you can use any other method to send the messages.

void send_byte(uint8_t byte) {}

void send_array(uint8_t *data, uint8_t size) {}

// Example of a possible function to send a full message.
void send_msg(lions::LMsg &encoded_msg) {
    // Send each component of the message header.
    send_byte(encoded_msg.header.src);       // Source device ID
    send_byte(encoded_msg.header.dst);       // Destination device ID
    send_byte(encoded_msg.header.msg_id);    // Message ID
    send_byte(encoded_msg.header.next_hop);  // Next hop ID

    // Send the payload.
    send_array(encoded_msg.payload, encoded_msg.payload_size);
}
//====================================================================================

/** Example how to encode messages from the generated messages classes. */
void encode_and_send(uint8_t dst_id, uint8_t next_hop) {
    // Microphone message example: sound level of -23, and a greeting message.
    lions::MicrophoneMsg mic_msg(-23, "Hello World!");
    auto encoded_mic_msg = mic_msg.encode(this_device_id, dst_id, next_hop);
    send_msg(encoded_mic_msg);

    // Accelerometer message example: acceleration readings along three axes.
    lions::AccelerometerMsg accel_msg(1.0, 2.0, 3.0);
    auto encoded_accel_msg = accel_msg.encode(this_device_id, dst_id, next_hop);
    send_msg(encoded_accel_msg);

    // Ping message example: a simple broadcast message to inform device availability.
    lions::PingMsg ping_msg;
    auto encoded_ping_msg = ping_msg.encode(this_device_id, broadcast_id, broadcast_id);
    send_msg(encoded_ping_msg);
}
