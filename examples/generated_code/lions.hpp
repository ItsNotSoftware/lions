/**
 * @file lions.hpp
 *
 * @brief LMsg defenition.
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

#ifndef LMSG_HPP
#define LMSG_HPP

#include <cstdint>

namespace lions {
struct Header {
    uint8_t src;
    uint8_t dst;
    uint8_t next_hop;
    uint8_t msg_id;
};

class LMsg {
   public:
    Header header;
    uint8_t payload[248];
    uint8_t payload_size;

    LMsg(uint8_t payload_size);
    uint16_t calculate_checksum();
    bool valid_checksum();

   private:
    uint16_t checksum;
};

}  // namespace lions

#endif