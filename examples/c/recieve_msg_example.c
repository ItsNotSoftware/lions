#include "generated_code/lions.h"
#include "generated_code/my_messages_lmsg.h" // Include the generated messages.

// Define a constant for the device identifier used in the message.
#define THIS_DEV_ID 1
#define BROADCAST_ID 255
uint8_t routing_table[255] = {0};

// ====================================================================================
// User created functions to send/recieve messages depending on the
// hardware/protocol.
//
// NOTE: this is just an example, you can use any other method to recieve the
// messages.

void send_msg(LMsg);

uint8_t recieve_byte();

LMsg Receive_msg() {
    LMsg msg = {0};
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
 * 4. Decode the message based on the message ID, and construct the proper
 * message object.
 */
void receive_and_decode_example() {
    LMsg received_msg = Receive_msg();

    // Check if the message has a valid checksum.
    if (!LMsg_valid_checksum(&received_msg)) {

        // Invalid message, do something.
    }

    bool to_forward = received_msg.header.next_hop == THIS_DEV_ID;
    bool is_destination = received_msg.header.dst =
        BROADCAST_ID || received_msg.header.dst == THIS_DEV_ID;

    if (to_forward) {
        received_msg.header.next_hop =
            routing_table[received_msg.header.dst]; // Forward the message to
                                                    // the next hop.

        send_msg(received_msg);
        return;
    }

    if (!is_destination)
        return; // Ignore message if not for this device.

    switch (received_msg.header.msg_id) {

    case MSG_ID_ACCELEROMETER: {
        const AccelerometerMsg acc_msg = AccelerometerMsg_decode(&received_msg);
        // Do something with the accelerometer message.
    } break;

    case MSG_ID_MICROPHONE: {
        const MicrophoneMsg mic_msg = MicrophoneMsg_decode(&received_msg);
        // Do something with the microphone message.
    } break;

    case MSG_ID_PING: {
        const PingMsg ping_msg = PingMsg_decode(&received_msg);
        // Do something with the ping message.
    } break;

    default:
        // Unknown message, do something.
        break;
    }
}
