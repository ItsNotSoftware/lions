/**
 * @file lions.js
 *
 * @brief LMsg definition.
 * LMsg is a class that represents a message in the Lions protocol.
 * 
 * This file contains the implementation of the message classes generated by the Lions Compiler.
 * 
 * @details
 * This file was generated by the Lions Compiler (https://github.com/ItsNotSoftware/lions) on .
 * Modifying this file manually is not recommended as it may lead to unexpected behavior.
 * 
 * @note
 * Generated files should not be manually edited.
 * 
 * @author Lions Compiler
 */

 const MAX_PAYLOAD_SIZE = 248;

 class Header {
    constructor(src = 0, dst = 0, next_hop = 0, msg_id = 0, checksum = 0) {
        this.src = src;
        this.dst = dst;
        this.next_hop = next_hop;
        this.msg_id = msg_id;
        this.checksum = checksum;
    }

    setChecksum(low, high) {
        this.checksum = (high << 8) | low;
    }

    get checksumLow() {
        return this.checksum & 0x00ff;
    }

    get checksumHigh() {
        return (this.checksum & 0xff00) >> 8;
    }
}

 class LMsg {
    constructor(payload_size = MAX_PAYLOAD_SIZE) {
        this.header = new Header();
        this.payload = new ArrayBuffer(payload_size);
        this.payload_size = payload_size;
    }

    calculateChecksum() {
        let checksum = 0;

        // Calculate checksum for the header
        checksum += this.header.src;
        checksum += this.header.dst;
        checksum += this.header.msg_id;
        checksum += this.header.next_hop;

        // Calculate checksum for the payload
        for (let i = 0; i < this.payload_size; i++) {
            checksum += this.payload[i];
        }

        checksum = ~checksum & 0xFFFF;

        this.header.checksum = checksum;

        return checksum;
    }

    validChecksum() {
        const prev_checksum = this.header.checksum;
        return this.calculateChecksum() === prev_checksum;
    }
}

export { LMsg, MAX_PAYLOAD_SIZE };