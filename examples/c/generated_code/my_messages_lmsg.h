
/**
 * @file my_messages_lmsg.h
 *
 * @brief my_messages_lmsg Classes
 *
 * This file contains the declaration of the message classes generated by the
Lions Compiler.
 *
 * @details
 * This file was generated by the Lions Compiler
(https://github.com/ItsNotSoftware/lions) on .
 * Modifying this file manually is not recommended as it may lead to unexpected
behavior.
 *
 * @note
 * Generated files should not be manually edited.
 *
 * @author Lions Compiler
 */

#ifndef MY_MESSAGES_LMSG_H
#define MY_MESSAGES_LMSG_H

#include "lions.h"
#include <stdint.h>
#include <string.h>


#define MSG_ID_ACCELEROMETER 1

#define MSG_ID_MICROPHONE 2

#define MSG_ID_PING 3



#define MSG_PERIOD_ACCELEROMETER 1000

#define MSG_PERIOD_MICROPHONE 0

#define MSG_PERIOD_PING 1000



typedef struct {
    Header header;
    
     float acc_x; 
    
     float acc_y; 
    
     float acc_z; 
    
} AccelerometerMsg;

typedef struct {
    Header header;
    
     int16_t sound_level; 
    
     char* message; 
    
} MicrophoneMsg;

typedef struct {
    Header header;
    
} PingMsg;



AccelerometerMsg AccelerometerMsg_create(float acc_x, float acc_y, float acc_z);
AccelerometerMsg AccelerometerMsg_decode(const LMsg *lmsg);
LMsg AccelerometerMsg_encode(const AccelerometerMsg *msg, uint8_t src, uint8_t dst, uint8_t next_hop);

MicrophoneMsg MicrophoneMsg_create(int16_t sound_level, char* message);
MicrophoneMsg MicrophoneMsg_decode(const LMsg *lmsg);
LMsg MicrophoneMsg_encode(const MicrophoneMsg *msg, uint8_t src, uint8_t dst, uint8_t next_hop);

PingMsg PingMsg_create();
PingMsg PingMsg_decode(const LMsg *lmsg);
LMsg PingMsg_encode(const PingMsg *msg, uint8_t src, uint8_t dst, uint8_t next_hop);


#endif