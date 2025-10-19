/* ************************************************************************
*  file: websocket.h , WebSocket support module header.   Part of DIKUMUD *
*  Usage: WebSocket protocol handling for browser connections             *
************************************************************************* */

#ifndef WEBSOCKET_H
#define WEBSOCKET_H

/* Check if incoming data looks like a websocket handshake */
int is_websocket_handshake(const char *buf, int len);

/* Perform websocket handshake and generate response */
int websocket_handshake(const char *request_buf, int request_len, 
                       char *response_buf, int response_size);

/* Encode data as a websocket text frame */
int websocket_encode_frame(const char *data, int data_len, 
                          unsigned char *frame_out, int frame_out_size);

/* Decode a websocket frame, returns frame size consumed or 0 if incomplete, -1 on close */
int websocket_decode_frame(const unsigned char *frame, int frame_len, 
                          char *data_out, int data_out_size);

#endif /* WEBSOCKET_H */
