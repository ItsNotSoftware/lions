/**
 * @file lions.ts
 *
 * @brief LMsg definition.
 * LMsg is a class that represents a message in the Lions protocol.
 * 
 * This file contains the implementation of the message classes generated by the Lions Compiler.
 * 
 * @details
 * This file was generated by the Lions Compiler (https://github.com/ItsNotSoftware/lions).
 * Modifying this file manually is not recommended as it may lead to unexpected behavior.
 * 
 * @note
 * Generated files should not be manually edited.
 * 
 * @author Lions Compiler
 */

const MAX_PAYLOAD_SIZE = 248;

class Header {
    src: number;
    dst: number;
    next_hop: number;
    msg_id: number;
    checksum: number;

    constructor(src = 0, dst = 0, next_hop = 0, msg_id = 0, checksum = 0) {
        this.src = src;
        this.dst = dst;
        this.next_hop = next_hop;
        this.msg_id = msg_id;
        this.checksum = checksum;
    }
}

class LMsg {
    header: Header;
    payload: ArrayBuffer;
    payload_size: number;

    constructor(payload_size = 0) {
        this.header = new Header();
        this.payload = new ArrayBuffer(payload_size);
        this.payload_size = payload_size;
    }

    calculateChecksum(): number {
        let checksum = 0;

        // Calculate checksum for the header
        checksum += this.header.src;
        checksum += this.header.dst;
        checksum += this.header.msg_id;
        checksum += this.header.next_hop;

        // Calculate checksum for the payload
        const payloadView = new Uint8Array(this.payload);
        for (let i = 0; i < this.payload_size; i++) {
            checksum += payloadView[i];
        }

        checksum = ~checksum & 0xFFFF;

        this.header.checksum = checksum;

        return checksum;
    }

    validChecksum(): boolean {
        const prev_checksum = this.header.checksum;
        return this.calculateChecksum() === prev_checksum;
    }
}

export { LMsg, MAX_PAYLOAD_SIZE };