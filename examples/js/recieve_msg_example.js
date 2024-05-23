import {
    AccelerometerMsg,
    MicrophoneMsg,
    PingMsg,
} from "./generated_code/my_messages_lmsg.js";
import { LMsg } from "./generated_code/lmsg.js";

const this_device_id = 1;
const brodcast_id = 255;

// ====================================================================================
// User created functions to send messages depending on app specific msg implementation
//
// NOTE: this is just an example, you can use any other method to send the messages.

function recieve_byte() {}

function recieve_msg() {
    let msg = new LMsg();

    msg.header.src = recieve_byte();
    msg.header.dst = recieve_byte();
    msg.header.msg_id = recieve_byte();
    msg.header.next_hop = recieve_byte();

    const checksum_low = recieve_byte();
    const checksum_high = recieve_byte();
    msg.checksum = (checksum_high << 8) | checksum_low;

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
function receive_and_decode_example() {
    const received_msg = receive_msg();

    // Check if the message has a valid checksum.
    if (!received_msg.valid_checksum()) {
        // Invalid message, do something.
    }

    const to_forward = received_msg.header.next_hop === this_device_id;
    const is_destination =
        received_msg.header.dst === broadcast_id ||
        received_msg.header.dst === this_device_id;

    if (to_forward) {
        received_msg.header.next_hop = routing_table[received_msg.header.dst]; // Forward the message to the next hop.
        send_msg(received_msg);
        return;
    }

    if (!is_destination) return; // Ignore message if not for this device.

    switch (received_msg.header.msg_id) {
        case msg_id.accelerometer:
            const accel_msg = AccelerometerMsg.fromLMsg(received_msg);
            // Handle the accelerometer message.
            console.log("Handling Accelerometer message:", accel_msg);
            break;

        case msg_id.microphone:
            const mic_msg = MicrophoneMsg.fromLMsg(received_msg);
            // Handle the microphone message.
            console.log("Handling Microphone message:", mic_msg);
            break;

        case msg_id.ping:
            const ping_msg = PingMsg.fromLMsg(received_msg);
            // Handle the ping message.
            console.log("Handling Ping message:", ping_msg);

            break;

        default:
            // Handle other types of messages.
            console.log("Handling unknown message type.");
            break;
    }
}
