from generated_code.my_messages_lmsg import (
    AccelerometerMsg,
    MicrophoneMsg,
    PingMsg,
    MsgID,
)
from generated_code.my_messages_lmsg import LMsg

THIS_DEVICE_ID = 1
BOARDCAST_ID = 0
routing_table = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# ====================================================================================
# User created functions to send messages depending on the hardware/protocol.
#
# NOTE: this is just an example, you can use any other method to recieve the messages.


def recieve_byte():
    return 0


def data_available():
    return True


def send_msg(msg: LMsg):
    pass


def recieve_msg():
    msg = LMsg()

    msg.header.src = recieve_byte()
    msg.header.dst = recieve_byte()
    msg.header.msg_id = recieve_byte()
    msg.header.next_hop = recieve_byte()

    # Construct the checksum from the two bytes.
    checksum_low = recieve_byte()
    checksum_high = recieve_byte()
    msg.header.set_checksum(checksum_low, checksum_high)

    msg.payload_size = 0
    while data_available():
        msg.payload[msg.payload_size] = recieve_byte()
        msg.payload_size += 1

    return msg


# ====================================================================================


def recieve_and_decode_example():
    """
    Example how to decode messages using lions

        1. Check the message header:
            1.1. Check if the message is to be forwarded. If so forward it.
            1.2. Check if the message is for this device. If not ignore it.
            1.3. Check if the message has a valid checksum.

        4. Decode the message based on the message ID, and construct the proper message object.
    """

    rcv_msg = recieve_msg()

    if not rcv_msg.valid_checksum():
        print("Invalid checksum")
        return

    to_forward = (
        rcv_msg.header.next_hop == THIS_DEVICE_ID
        and rcv_msg.header.dst != BOARDCAST_ID
        and rcv_msg.header.src != THIS_DEVICE_ID
    )
    is_destiantion = (
        rcv_msg.header.dst == THIS_DEVICE_ID or rcv_msg.header.dst == BOARDCAST_ID
    )

    if to_forward and not is_destiantion:
        # Forward the message to the next hop.
        rcv_msg.header.next_hop = routing_table[rcv_msg.header.dst]
        send_msg(rcv_msg)
        return

    if not is_destiantion:
        return

    match rcv_msg.header.msg_id:
        case MsgID.ACCELEROMETER_MSG:
            acc_msg = AccelerometerMsg.from_lmsg(rcv_msg)
            # Handle the accelerometer message
            print(acc_msg)

        case MsgID.MICROPHONE_MSG:
            mic_msg = MicrophoneMsg.from_lmsg(rcv_msg)
            # Handle the microphone message
            print(mic_msg)

        case MsgID.PING_MSG:
            ping_msg = PingMsg.from_lmsg(rcv_msg)
            # Handle the ping message
            print(ping_msg)

        case _:
            print("Unknown message ID")
