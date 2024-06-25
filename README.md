# LIONS (Lightweight IoT Network Specification)

## Index

<!-- TOC start (generated with https://github.com/derlin/bitdowntoc) -->

-   [Description](#description)
-   [Install](#install)
-   [Usage](#usage)
-   [Raw Message format](#raw-message-format)
    -   [Code representation](#code-representation)
-   [Defining Messages](#defining-messages)
    -   [Structure of Message Files](#structure-of-message-files)
    -   [Generated code](#generated-code)
        -   [Constants](#constants)
        -   [Message struct/class](#message-structclass)
-   [Examples](#examples)
-   [Target Language Support](#target-language-support)
<!-- TOC end -->

<!-- TOC --><a name="lions"></a>

## Description

LIONS is a communication protocol coupled with a compiler (lionsc), specifically designed for low-bandwidth IoT mesh and ad hoc networks. Originally tailored for LoRa, LIONS is versatile enough to be adapted to various communication standards, thanks to its protocol-agnostic message encoding approach.

The core of LIONS lies in its efficient message encoding system. Messages are compactly encoded into byte arrays, ensuring that each value occupies only the necessary space required by its type, thus minimizing space.

Message structures are defined using YAML files (.lmsg.yaml), which detail the message name, ID, and its data fields. These files serve as input for the LIONS compiler, which generates the necessary code for accurate message encoding and decoding.

This protocol is ideal for developers looking to implement efficient, data-constraint communications in their IoT network projects.

## Install

    $ pip install lionsc

## Usage

    $ lionsc <msg_files_dir> <output_dir> <target_language>

-   **msg_files_dir**: Directory containing your .lmsg.yaml files
-   **output_dir**: Directory to place the generated code
-   **target_language**: Target language for the generated code
    -   c / cpp / js / ts / py

## Raw Message format

The message structure is composed of a 6-byte header, followed by a variable-length payload. The payload length can range from 0 to 244 bytes, allowing for flexible data encapsulation. Fields within the payload are tightly packed, with no intervening spaces, to maximize message efficiency and minimize overhead.

| Byte Index | Field    | Size (Bytes) | Description                                       |
| ---------- | -------- | ------------ | ------------------------------------------------- |
| 0          | src      | 1            | Source identifier                                 |
| 1          | dst      | 1            | Destination identifier                            |
| 2          | next_hop | 1            | Next hop identifier (used for message forwarding) |
| 3          | msg_id   | 1            | Message identifier                                |
| 4-5        | checksum | 2            | Checksum for error checking                       |
| 6-249      | payload  | 244          | Actual data payload                               |

### Code representation

-   [C++](https://github.com/ItsNotSoftware/lions/blob/main/examples/c/generated_code/lions.h)
-   [C++](https://github.com/ItsNotSoftware/lions/blob/main/examples/c%2B%2B/generated_code/lions.hpp)
-   [JavaScript](https://github.com/ItsNotSoftware/lions/blob/main/examples/js/generated_code/lions.js)
-   [TypeScript](https://github.com/ItsNotSoftware/lions/blob/main/examples/ts/generated_code/lions.ts)
-   [Python](https://github.com/ItsNotSoftware/lions/blob/main/examples/python/generated_code/lions.py)

## Defining Messages

LIONS uses `.lmsg.yaml` files to define message specifications for IoT networks. Each file can contain multiple message definitions that are used by the LIONS compiler to generate C++ code for message handling.

### Structure of Message Files

-   **Name of the Message**: Unique identifier for each message type.
-   **ID**: Identifier unique to each message ()can be given in hexadecimal, decimal, or binary.
-   **Period**: Used to generate a constant for message scheduling (implementation needs to be done by teh user).
-   **Description**: Brief explanation of the message's purpose.
-   **Fields**:
    -   **Type**: Data type (`float`, `int16_t`, `string`, etc.).
    -   **Size**: Size in bytes, variable for strings.
    -   **Description**: Explanation of the field's purpose.

```yaml
accelerometer:
    id: 0x01
    period: 1000
    description: "Accelerometer data"

    fields:
        acc_x:
            type: float
            size: 4
            description: "Acceleration in x-axis m/s^2"

        acc_y:
            type: float
            size: 4
            description: "Acceleration in y-axis m/s^2"

        acc_z:
            type: float
            size: 4
            unit: "m/s^2"
            description: "Acceleration in z-axis m/s^2"

microphone:
    id: 0x02
    period: 0
    description: "Microphone data"

    fields:
        message:
            type: string
            size: 100
            description: "Speach-to-text message"

ping:
    id: 0x03
    period: 1000
    description: "Ping message"
```

### Generated code

The LIONS compiler auto-generates code to facilitate handling, encoding and decoding of messages defined in `.lmsg.yaml` files. Below is an example of how part of the generated code might look for the yaml file above.

#### Constants

The code defines namespaces to hold constants for message IDs and periods, ensuring easy reference throughout the codebase:

C++ example:

```C++
namespace msg_id {
    constexpr uint8_t ACCELEROMETER = 1;
    constexpr uint8_t MICROPHONE = 2;
    constexpr uint8_t PING = 3;
}  // namespace msg_id

namespace msg_period {
    constexpr uint8_t ACCELEROMETER = 1000;
    constexpr uint8_t MICROPHONE = 0;
    constexpr uint8_t PING = 1000;
}  // namespace msg_period
```

#### Message struct/class

For each message type defined in the YAML files, the LIONS compiler generates a corresponding struct/class. This class includes the specific fields of the message, two constructors, and an encode method.

1. **Initialization Constructor**

    - Used to create a new instance of the message class with predefined field values. This constructor initializes the message with specific data relevant to its type.

2. **Decoding Constructor**

    - Transforms a generic, raw-form message (`LMsg`) into the structured format of the class. This conversion facilitates easier manipulation and interpretation of the message contents within the application.

3. **Encode Method**
    - Converts the structured message back into its raw binary form (`LMsg`) for transmission. This method ensures that the message is properly packaged with its header and payload according to the protocol specifications before being sent over the network.

---

Generated message classes examples:

-   [C](https://github.com/ItsNotSoftware/lions/blob/main/examples/c/generated_code/my_messages_lmsg.h)
-   [C++](https://github.com/ItsNotSoftware/lions/blob/main/examples/c%2B%2B/generated_code/my_messages_lmsg.hpp)
-   [JavaScript](https://github.com/ItsNotSoftware/lions/blob/main/examples/js/generated_code/my_messages_lmsg.js)
-   [TypeScript](https://github.com/ItsNotSoftware/lions/blob/main/examples/ts/generated_code/my_messages_lmsg.ts)
-   [Python](https://github.com/ItsNotSoftware/lions/blob/main/examples/python/generated_code/my_messages_lmsg.py)

## Examples

-   [C](https://github.com/ItsNotSoftware/lions/blob/main/examples/c)
-   [C++](https://github.com/ItsNotSoftware/lions/blob/main/examples/c%2B%2B)
-   [JavaScript](https://github.com/ItsNotSoftware/lions/blob/main/examples/js)
-   [TypeScript](https://github.com/ItsNotSoftware/lions/blob/main/examples/ts)
-   [Python](https://github.com/ItsNotSoftware/lions/blob/main/examples/python)

## Target Language Support

-   [x] C
-   [x] C++
-   [x] JavaScript
-   [x] TypeScript
-   [x] Python
