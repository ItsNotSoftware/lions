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
def send_msg(encoded_msg):
    # Send each component of the message header.
    send_byte(encoded_msg.header.src)  # Source device ID
    send_byte(encoded_msg.header.dst)  # Destination device ID
    send_byte(encoded_msg.header.msg_id)  # Message ID
    send_byte(encoded_msg.header.next_hop)  # Next hop device ID

    checksum_low = encoded_msg.header.checksum & 0xFF
    checksum_high = (encoded_msg.header.checksum >> 8) & 0xFF
    send_byte(checksum_low)  # Checksum low byte
    send_byte(checksum_high)  # Checksum high byte
