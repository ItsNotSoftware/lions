from generated_code.my_messages_lmsg import AccelerometerMsg, MicrophoneMsg, PingMsg
from generated_code.my_messages_lmsg import LMsg, Header

THIS_DEVICE_ID = 1
BOARDCAST_ID = 0


# ====================================================================================
# User created functions to send messages depending on the hardware/protocol.
#
# NOTE: this is just an example, you can use any other method to send the messages.
def send_byte(byte):
    pass


def send_array(data, size):
    pass


# Example of a possible function to send a full message.
def send_msg(encoded_msg: LMsg):
    # Send each component of the message header.
    send_byte(encoded_msg.header.src)  # Source device ID
    send_byte(encoded_msg.header.dst)  # Destination device ID
    send_byte(encoded_msg.header.msg_id)  # Message ID
    send_byte(encoded_msg.header.next_hop)  # Next hop device ID

    # Send the checksum in 2 parts (low and high).
    send_byte(encoded_msg.header.checksum_low)
    send_byte(encoded_msg.header.checksum_high)

    # Send the payload.
    send_array(encoded_msg.payload, encoded_msg.payload_size)


# ====================================================================================


def encode_and_send_example(dst_id, next_hop):
    """
    * Example how to encode messages using lions for sending.
    *
    * 1. Construct the message object.
    * 2. Encode the message object into a LMsg object. (Header + Payload binary representation)
    * 3. Send the LMsg object using your hardware/protocol.
    """
    # Microphone message example: sound level of -23, and a greeting message.
    mic_msg = MicrophoneMsg(10, "Hello World!")
    encoded_msg = mic_msg.encode(THIS_DEVICE_ID, dst_id, next_hop)
    send_msg(encoded_msg)

    # Accelerometer message example: x=10, y=20, z=30.
    acc_msg = AccelerometerMsg(10, 20, 30)
    encoded_msg = acc_msg.encode(THIS_DEVICE_ID, dst_id, next_hop)
    send_msg(encoded_msg)

    # Ping message example.
    ping_msg = PingMsg()
    encoded_msg = ping_msg.encode(THIS_DEVICE_ID, dst_id, next_hop)
    send_msg(encoded_msg)
