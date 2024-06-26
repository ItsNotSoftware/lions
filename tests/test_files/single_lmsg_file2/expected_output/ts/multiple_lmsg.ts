/**
 * @file multiple_lmsg.ts
 *
 * @brief multiple_lmsg Classes
 * 
 * This file contains the declaration of the message classes generated by the Lions Compiler.
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

import { LMsg, Header } from './lions.ts';

const msg_id = {
    accelerometer: 1,
    microphone: 2,
    ping: 3
};

const msg_period = {
    accelerometer: 1000,
    microphone: 0,
    ping: 1000
};


class AccelerometerMsg {
    header: Header;
    acc_x: number;
    acc_y: number;
    acc_z: number;

    constructor(acc_x: number, acc_y: number, acc_z: number) {
        this.header = new Header();
        this.acc_x = acc_x;
        this.acc_y = acc_y;
        this.acc_z = acc_z;
    }

    static fromLMsg(msg: LMsg): AccelerometerMsg {
        const dataView = new DataView(msg.payload);
        const acc_x = dataView.getFloat32(0, true);  // true for little-endian
        const acc_y = dataView.getFloat32(4, true);  // true for little-endian
        const acc_z = dataView.getFloat32(8, true);  // true for little-endian

        let instance = new AccelerometerMsg(acc_x, acc_y, acc_z);
        instance.header = msg.header;

        return instance;
    }

    encode(src: number, dst: number, next_hop: number): LMsg {
        const msg = new LMsg(12);
        
        msg.header.src = src;
        msg.header.dst = dst;
        msg.header.next_hop = next_hop;
        msg.header.msg_id = msg_id.accelerometer;
        
        const dataView = new DataView(msg.payload);
        dataView.setFloat32(0, this.acc_x, true);  // true for little-endian
        dataView.setFloat32(4, this.acc_y, true);  // true for little-endian
        dataView.setFloat32(8, this.acc_z, true);  // true for little-endian

        msg.calculateChecksum();

        return msg;
    }
}

class MicrophoneMsg {
    header: Header;
    sound_level: number;
    message: string;

    constructor(sound_level: number, message: string) {
        this.header = new Header();
        this.sound_level = sound_level;
        this.message = message;
    }

    static fromLMsg(msg: LMsg): MicrophoneMsg {
        const dataView = new DataView(msg.payload);
        const sound_level = dataView.getInt16(0, true);  // true for little-endian
        const message = new TextDecoder().decode(msg.payload.slice(2, 2 + 100)).replace(/\0.*$/,"");
        

        let instance = new MicrophoneMsg(sound_level, message);
        instance.header = msg.header;

        return instance;
    }

    encode(src: number, dst: number, next_hop: number): LMsg {
        const msg = new LMsg(102);
        
        msg.header.src = src;
        msg.header.dst = dst;
        msg.header.next_hop = next_hop;
        msg.header.msg_id = msg_id.microphone;
        
        const dataView = new DataView(msg.payload);
        dataView.setInt16(0, this.sound_level, true);  // true for little-endian
        
        const encodedMessage = new TextEncoder().encode(this.message);
        for (let i = 0; i < Math.min(encodedMessage.length, 100); i++) {
            dataView.setUint8(2 + i, encodedMessage[i]);
        }
        
        if (encodedMessage.length < 100) {
            dataView.setUint8(2 + encodedMessage.length, 0);
        }
        

        msg.calculateChecksum();

        return msg;
    }
}

class PingMsg {
    header: Header;

    constructor() {
        this.header = new Header();
    }

    static fromLMsg(msg: LMsg): PingMsg {
        const dataView = new DataView(msg.payload);

        let instance = new PingMsg();
        instance.header = msg.header;

        return instance;
    }

    encode(src: number, dst: number, next_hop: number): LMsg {
        const msg = new LMsg(0);
        
        msg.header.src = src;
        msg.header.dst = dst;
        msg.header.next_hop = next_hop;
        msg.header.msg_id = msg_id.ping;
        
        const dataView = new DataView(msg.payload);

        msg.calculateChecksum();

        return msg;
    }
}


export { msg_id, msg_period, AccelerometerMsg, MicrophoneMsg, PingMsg };