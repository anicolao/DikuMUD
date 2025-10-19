/* ************************************************************************
*  file: websocket.c , WebSocket support module.          Part of DIKUMUD *
*  Usage: WebSocket protocol handling for browser connections             *
*  Copyright (C) 2024 - see 'license.doc' for complete information.       *
************************************************************************* */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <stdint.h>

/* SHA-1 implementation for websocket handshake */
static void sha1_transform(uint32_t state[5], const unsigned char buffer[64])
{
    uint32_t a, b, c, d, e;
    uint32_t w[80];
    int i;
    
    /* Copy buffer to w[0..15] */
    for (i = 0; i < 16; i++) {
        w[i] = ((uint32_t)buffer[i * 4] << 24) |
               ((uint32_t)buffer[i * 4 + 1] << 16) |
               ((uint32_t)buffer[i * 4 + 2] << 8) |
               ((uint32_t)buffer[i * 4 + 3]);
    }
    
    /* Expand w[16..79] */
    for (i = 16; i < 80; i++) {
        uint32_t temp = w[i-3] ^ w[i-8] ^ w[i-14] ^ w[i-16];
        w[i] = (temp << 1) | (temp >> 31);
    }
    
    /* Initialize working variables */
    a = state[0];
    b = state[1];
    c = state[2];
    d = state[3];
    e = state[4];
    
    /* Main loop */
    for (i = 0; i < 80; i++) {
        uint32_t f, k, temp;
        
        if (i < 20) {
            f = (b & c) | ((~b) & d);
            k = 0x5A827999;
        } else if (i < 40) {
            f = b ^ c ^ d;
            k = 0x6ED9EBA1;
        } else if (i < 60) {
            f = (b & c) | (b & d) | (c & d);
            k = 0x8F1BBCDC;
        } else {
            f = b ^ c ^ d;
            k = 0xCA62C1D6;
        }
        
        temp = ((a << 5) | (a >> 27)) + f + e + k + w[i];
        e = d;
        d = c;
        c = (b << 30) | (b >> 2);
        b = a;
        a = temp;
    }
    
    /* Add this chunk's hash to result */
    state[0] += a;
    state[1] += b;
    state[2] += c;
    state[3] += d;
    state[4] += e;
}

void sha1_hash(const char *input, int len, unsigned char output[20])
{
    uint32_t state[5] = {
        0x67452301,
        0xEFCDAB89,
        0x98BADCFE,
        0x10325476,
        0xC3D2E1F0
    };
    
    unsigned char buffer[64];
    int i;
    uint64_t bit_len = (uint64_t)len * 8;
    
    /* Process complete 64-byte blocks */
    int blocks = len / 64;
    for (i = 0; i < blocks; i++) {
        sha1_transform(state, (const unsigned char *)input + i * 64);
    }
    
    /* Handle remaining bytes */
    int remaining = len % 64;
    memcpy(buffer, input + blocks * 64, remaining);
    buffer[remaining] = 0x80;
    
    /* If not enough room for length, process this block and start a new one */
    if (remaining >= 56) {
        memset(buffer + remaining + 1, 0, 64 - remaining - 1);
        sha1_transform(state, buffer);
        memset(buffer, 0, 56);
    } else {
        memset(buffer + remaining + 1, 0, 56 - remaining - 1);
    }
    
    /* Append length in bits */
    for (i = 0; i < 8; i++) {
        buffer[63 - i] = (unsigned char)(bit_len >> (i * 8));
    }
    sha1_transform(state, buffer);
    
    /* Output hash */
    for (i = 0; i < 5; i++) {
        output[i * 4] = (unsigned char)(state[i] >> 24);
        output[i * 4 + 1] = (unsigned char)(state[i] >> 16);
        output[i * 4 + 2] = (unsigned char)(state[i] >> 8);
        output[i * 4 + 3] = (unsigned char)state[i];
    }
}

/* Base64 encoding */
static const char base64_chars[] = 
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";

void base64_encode(const unsigned char *input, int len, char *output)
{
    int i, j;
    unsigned char a3[3];
    unsigned char a4[4];
    
    for (i = 0, j = 0; i < len;) {
        int n = 0;
        for (n = 0; n < 3 && i < len; n++, i++) {
            a3[n] = input[i];
        }
        
        if (n > 0) {
            a4[0] = (a3[0] & 0xfc) >> 2;
            a4[1] = ((a3[0] & 0x03) << 4) + ((a3[1] & 0xf0) >> 4);
            a4[2] = ((a3[1] & 0x0f) << 2) + ((a3[2] & 0xc0) >> 6);
            a4[3] = a3[2] & 0x3f;
            
            for (int k = 0; k < n + 1; k++) {
                output[j++] = base64_chars[a4[k]];
            }
            
            while (n++ < 3) {
                output[j++] = '=';
            }
        }
    }
    output[j] = '\0';
}

/* Check if incoming data is a websocket handshake request */
int is_websocket_handshake(const char *buf, int len)
{
    if (len < 16)
        return 0;
    
    /* Check for "GET " at the start */
    if (strncmp(buf, "GET ", 4) != 0)
        return 0;
    
    /* Check for "Upgrade: websocket" */
    if (strstr(buf, "Upgrade: websocket") == NULL &&
        strstr(buf, "Upgrade: WebSocket") == NULL)
        return 0;
    
    return 1;
}

/* Extract Sec-WebSocket-Key from HTTP headers */
static int extract_websocket_key(const char *buf, char *key_out, int key_out_size)
{
    const char *key_header = "Sec-WebSocket-Key: ";
    char *key_start = strstr(buf, key_header);
    
    if (!key_start)
        return 0;
    
    key_start += strlen(key_header);
    char *key_end = strstr(key_start, "\r\n");
    
    if (!key_end)
        return 0;
    
    int key_len = key_end - key_start;
    if (key_len >= key_out_size)
        key_len = key_out_size - 1;
    
    strncpy(key_out, key_start, key_len);
    key_out[key_len] = '\0';
    
    return 1;
}

/* Perform websocket handshake and return response */
int websocket_handshake(const char *request_buf, int request_len, char *response_buf, int response_size)
{
    char key[256];
    char accept_input[512];
    unsigned char sha1_result[20];
    char accept_key[64];
    
    /* Extract the Sec-WebSocket-Key */
    if (!extract_websocket_key(request_buf, key, sizeof(key)))
        return 0;
    
    /* Concatenate with magic string */
    snprintf(accept_input, sizeof(accept_input), "%s258EAFA5-E914-47DA-95CA-C5AB0DC85B11", key);
    
    /* Calculate SHA-1 hash */
    sha1_hash(accept_input, strlen(accept_input), sha1_result);
    
    /* Base64 encode the hash */
    base64_encode(sha1_result, 20, accept_key);
    
    /* Build response */
    snprintf(response_buf, response_size,
        "HTTP/1.1 101 Switching Protocols\r\n"
        "Upgrade: websocket\r\n"
        "Connection: Upgrade\r\n"
        "Sec-WebSocket-Accept: %s\r\n"
        "\r\n",
        accept_key);
    
    return 1;
}

/* Encode data as a websocket text frame */
int websocket_encode_frame(const char *data, int data_len, unsigned char *frame_out, int frame_out_size)
{
    int frame_len = 0;
    
    /* First byte: FIN=1, opcode=1 (text frame) */
    frame_out[frame_len++] = 0x81;
    
    /* Second byte: mask=0, payload length */
    if (data_len < 126) {
        frame_out[frame_len++] = data_len;
    } else if (data_len < 65536) {
        frame_out[frame_len++] = 126;
        frame_out[frame_len++] = (data_len >> 8) & 0xFF;
        frame_out[frame_len++] = data_len & 0xFF;
    } else {
        /* For simplicity, we don't support payloads >= 64KB */
        return -1;
    }
    
    /* Copy payload data */
    if (frame_len + data_len > frame_out_size)
        return -1;
    
    memcpy(frame_out + frame_len, data, data_len);
    frame_len += data_len;
    
    return frame_len;
}

/* Decode a websocket frame */
int websocket_decode_frame(const unsigned char *frame, int frame_len, char *data_out, int data_out_size)
{
    int pos = 0;
    
    if (frame_len < 2)
        return 0;  /* Incomplete frame */
    
    /* First byte */
    unsigned char fin = (frame[pos] & 0x80) >> 7;
    unsigned char opcode = frame[pos] & 0x0F;
    pos++;
    
    /* Handle close frame */
    if (opcode == 0x08)
        return -1;  /* Connection close */
    
    /* Only handle text frames (opcode 1) and continuation frames (opcode 0) */
    if (opcode != 0x01 && opcode != 0x00)
        return 0;  /* Not a text frame, skip */
    
    /* Second byte */
    unsigned char masked = (frame[pos] & 0x80) >> 7;
    uint64_t payload_len = frame[pos] & 0x7F;
    pos++;
    
    /* Extended payload length */
    if (payload_len == 126) {
        if (frame_len < pos + 2)
            return 0;  /* Incomplete */
        payload_len = ((uint64_t)frame[pos] << 8) | frame[pos + 1];
        pos += 2;
    } else if (payload_len == 127) {
        if (frame_len < pos + 8)
            return 0;  /* Incomplete */
        payload_len = 0;
        for (int i = 0; i < 8; i++) {
            payload_len = (payload_len << 8) | frame[pos + i];
        }
        pos += 8;
    }
    
    /* Masking key */
    unsigned char mask[4];
    if (masked) {
        if (frame_len < pos + 4)
            return 0;  /* Incomplete */
        memcpy(mask, frame + pos, 4);
        pos += 4;
    }
    
    /* Check if we have complete payload */
    if (frame_len < pos + payload_len)
        return 0;  /* Incomplete */
    
    /* Check output buffer size */
    if (payload_len >= data_out_size)
        payload_len = data_out_size - 1;
    
    /* Unmask and copy payload */
    for (uint64_t i = 0; i < payload_len; i++) {
        if (masked)
            data_out[i] = frame[pos + i] ^ mask[i % 4];
        else
            data_out[i] = frame[pos + i];
    }
    data_out[payload_len] = '\0';
    
    /* Return total frame size consumed (header + payload) */
    return pos + payload_len;
}
