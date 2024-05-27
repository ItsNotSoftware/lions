import {
    AccelerometerMsg,
    MicrophoneMsg,
    PingMsg,
} from "./generated_code/my_messages_lmsg.ts";
import { LMsg } from "./generated_code/lions.ts";

const this_device_id = 1;
const broadcast_id = 255;

// ====================================================================================
// User created functions to send messages depending on the hardware/protocol.
//
// NOTE: this is just an example, you can use any other method to send the messages.
function sendByte(byte: number) {}

function sendArray(data: ArrayBuffer, size: number) {}

// Example of a possible function to send a full message.
function sendMsg(encoded_msg: LMsg) {
    // Send each component of the message header.
    sendByte(encoded_msg.header.src); // Source device ID
    sendByte(encoded_msg.header.dst); // Destination device ID
    sendByte(encoded_msg.header.msg_id); // Message ID
    sendByte(encoded_msg.header.next_hop); // Next hop ID

    // Send the checksum in 2 parts (low and high).
    sendByte(encoded_msg.header.checksum_low);
    sendByte(encoded_msg.header.checksum_high);

    // Send the payload.
    sendArray(encoded_msg.payload, encoded_msg.payload_size);
}
//====================================================================================

/** Example how to encode messages using lions for sending.
 *
 * 1. Construct the message object.
 * 2. Encode the message object into a LMsg object. (Header + Payload binary representation)
 * 3. Send the LMsg object using your hardware/protocol.
 */
function encodeAndSendExample(dst_id: number, next_hop: number) {
    // Microphone message example: sound level of -23, and a greeting message.
    const mic_msg = new MicrophoneMsg(-23, "Hello World!");
    const encoded_mic_msg = mic_msg.encode(this_device_id, dst_id, next_hop);
    sendMsg(encoded_mic_msg);

    // Accelerometer message example: acceleration readings along three axes.
    const accel_msg = new AccelerometerMsg(1.0, 2.0, 3.0);
    const encoded_accel_msg = accel_msg.encode(
        this_device_id,
        dst_id,
        next_hop
    );
    sendMsg(encoded_accel_msg);

    // Ping message example: a simple broadcast message to inform device availability.
    const ping_msg = new PingMsg();
    const encoded_ping_msg = ping_msg.encode(
        this_device_id,
        broadcast_id,
        broadcast_id
    );
    sendMsg(encoded_ping_msg);
}
