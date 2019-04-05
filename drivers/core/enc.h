#ifndef ENC_H
#define ENC_H

struct Enc {
    int encA;
    int encB;
    int levA;
    int levB;
    int lastGpio;
    long pos;
    Enc(int apin, int bpin);
    ~Enc();
};

#endif
