#include <stdio.h>

#include <iostream>

#include "generated_code/example.hpp"
#include "generated_code/lions.hpp"

// Define a constant for the device identifier used in the message.
constexpr uint8_t this_device_id = 1;
constexpr uint8_t brodcast_id = 255;

// System-specific implementation of sending a byte.
void send();

// System-specific implementation of sending an array of bytes.
void send_array(uint8_t *data, uint8_t size);

void send_msg(LMsg &encoded_msg) {
    // Send each component of the message header.
    send(encoded_msg.src);       // Source device ID
    send(encoded_msg.dst);       // Destination device ID
    send(encoded_msg.msg_id);    // Message ID
    send(encoded_msg.next_hop);  // Next hop ID

    // Send the payload.
    send_array(encoded_msg.payload, encoded_msg.payload_size);
}

void send_msg_example(uint8_t dst_id, uint8_t next_hop) {
    int16_t sound_level = -23;

    // Create a microphone message with the string "Hello World!"
    lions::MicrophoneMsg msg(this_device_id, dst_id, next_hop, sound_level, "Hello World!");

    // Encode the message for sending.
    auto encoded_msg = msg.encode(this_device_id, 2, 3);

    // Use system-specific implementation to send the message.
    send_msg(encoded_msg);

    // Another example with an accelerometer message.
    lions::AccelerometerMsg msg2(this_device_id, dst_id, next_hop, 1.0, 2.0, 3.0);
    auto encoded_msg2 = msg2.encode(this_device_id, 2, 3);
    send_msg(encoded_msg2);

    // Another example with a ping message.
    lions::PingMsg msg3(brodcast_id, dst_id, next_hop);
    auto encoded_msg3 = msg3.encode(this_device_id, 2, 3);
    send_msg(encoded_msg3);
}
