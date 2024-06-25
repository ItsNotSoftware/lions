#include "generated_code/lions.h"
#include "generated_code/my_messages_lmsg.h" // Include the generated messages.

// Define a constant for the device identifier used in the message.
#define THIS_DEV_ID 1
#define BROADCAST_ID 255

// ====================================================================================
// User created functions to send messages depending on the hardware/protocol.
//
// NOTE: this is just an example, you can use any other method to send the
// messages.

void send_byte(uint8_t byte) {}

void send_array(uint8_t *data, uint8_t size) {}

// Example of a possible function to send a full message.
void send_msg(LMsg *encoded_msg) {
    // Send each component of the message header.
    send_byte(encoded_msg->header.src);      // Source device ID
    send_byte(encoded_msg->header.dst);      // Destination device ID
    send_byte(encoded_msg->header.msg_id);   // Message ID
    send_byte(encoded_msg->header.next_hop); // Next hop ID
    send_byte(encoded_msg->header.checksum_low);
    send_byte(encoded_msg->header.checksum_high);

    // Send the payload.
    send_array(encoded_msg->payload, encoded_msg->payload_size);
}
//====================================================================================

/** Example how to encode messages using lions for sending.
 *
 * 1. Construct the message object.
 * 2. Encode the message object into a LMsg object. (Header + Payload binary
 * representation)
 * 3. Send the LMsg object using your hardware/protocol.
 */
void encode_and_send_example(uint8_t dst_id, uint8_t next_hop) {
    // Microphone message example: sound level of -23, and a greeting message.
    MicrophoneMsg mic_msg = MicrophoneMsg_create(23, "Hello World!");
    LMsg encoded_mic_msg =
        MicrophoneMsg_encode(&mic_msg, THIS_DEV_ID, dst_id, next_hop);
    send_msg(&encoded_mic_msg);

    // Accelerometer message example: acceleration readings along three axes.
    AccelerometerMsg acc_msg = AccelerometerMsg_create(1.0, 2.0, 3.0);
    LMsg encoded_acc_msg =
        AccelerometerMsg_encode(&acc_msg, THIS_DEV_ID, dst_id, next_hop);
    send_msg(&encoded_acc_msg);

    // Ping message example: a simple broadcast message
    PingMsg ping_msg = PingMsg_create();
    LMsg encoded_ping_msg =
        PingMsg_encode(&ping_msg, THIS_DEV_ID, BROADCAST_ID, next_hop);
    send_msg(&encoded_ping_msg);
}
