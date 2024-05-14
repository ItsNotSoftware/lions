#include "generated_code/my_messages_lmsgs.hpp"  // Include the generated messages.

// Define a constant for the device identifier used in the message.
constexpr uint8_t this_device_id = 1;
constexpr uint8_t broadcast_id = 255;
uint8_t routing_table[255] = {0};

// ====================================================================================
// User created functions to send messages depending on the hardware/protocol.
//
// NOTE: this is just an example, you can use any other method to send the messages.

void send_msg(lions::LMsg);

uint8_t recieve_byte();

lions::LMsg recive_msg() {
    lions::LMsg msg(0);
    msg.header.src = recieve_byte();
    msg.header.dst = recieve_byte();
    msg.header.msg_id = recieve_byte();
    msg.header.next_hop = recieve_byte();
    msg.header.checksum_low = recieve_byte();
    msg.header.checksum_high = recieve_byte();

    while (data_available()) {
        msg.payload[msg.payload_size++] = recieve_byte();
    }
    return msg;
}
//====================================================================================

/** Example how to decode messages using lions
 *
 * 1. Check the message header.
 *     1.1. Check if the message is to be forwarded. If so forward it.
 *     1.2. Check if the message is for this device. If not ignore it.
 *     1.3. Check if the message has a valid checksum.
 *
 * 4. Decode the message based on the message ID, and construct the proper message object.
 */
void receive_and_decode_example(uint8_t dst_id, uint8_t next_hop) {
    auto received_msg = recive_msg();

    bool to_forward = received_msg.header.next_hop == this_device_id;
    bool is_destination = received_msg.header.dst =
        broadcast_id || received_msg.header.dst == this_device_id;

    if (to_forward) {
        received_msg.header.next_hop =
            routing_table[received_msg.header.dst];  // Forward the message to the next hop.

        send_msg(received_msg);
        return;
    }

    if (!is_destination) return;  // Ignore message if not for this device.

    // Check if the message has a valid checksum.
    if (!received_msg.valid_checksum()) {
        // Invalid message, do something.
    }

    switch (received_msg.header.msg_id) {
        case lions::msg_id::ACCELEROMETER: {
            const lions::AccelerometerMsg accel_msg(received_msg);
            // Do something with the accelerometer message.
        } break;

        case lions::msg_id::MICROPHONE: {
            const lions::MicrophoneMsg mic_msg(received_msg);
            // Do something with the microphone message.
        } break;

        case lions::msg_id::PING: {
            const lions::PingMsg ping_msg(received_msg);
            // Do something with the ping message.
        } break;

        default:
            // Do something with the message.
            break;
    }
}
