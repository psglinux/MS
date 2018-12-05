#ifndef __SCF_PARSE_H__
#define __SCF_PARSE_H__

/*
C:\Users\gargi-partha\Desktop\SCFProgram>SCFParser.exe -h

        Parse CTL File

        --------------

Version:        1.2
HeaderLength:   312 (BYTES)

BYTEPOS TAG             LENGTH  VALUE
------- ---             ------  -----
3       SIGNERID        2       127
4       SIGNERNAME      55
5       SERIALNUMBER    8
6       CANAME  55
7       SIGNATUREINFO   2       55
8       DIGESTALGO      2
9       SIGNATUREALGOINFO       2
10      SIGNATUREALGO   2
11      SIGNATUREMODULUS        2
12      SIGNATURE       128
                35  6d  f0  f8  aa  f1  05  6e
                f7  ab  1b  5d  3e  df  84  5e
                f3  49  5b  4f  39  95  76  99
                bb  06  16  80  e8  de  fb  08
                a4  4f  b4  c3  f7  2a  be  86
                0a  70  88  36  ab  0a  17  52
                b0  cd  1a  60  80  29  ae  7a
                47  a8  95  3e  ef  27  65  3e
                7c  70  db  e0  53  aa  6e  9f
                26  77  e5  5e  83  7c  d6  d9
                66  ae  c5  bb  6e  bc  a2  03
                ee  3d  07  7a  90  04  a2  15
                8b  9b  c3  f5  b2  cd  46  e7
                e3  a2  27  c9  19  7c  65  e9
                2e  9f  bc  02  f3  99  ab  78
                c3  be  5c  e9  2d  72  50  bc
14      FILENAME        12
15      TIMESTAMP       4

        Start CTL Records
        -----------------

        CTL Record  #: 1
                     ----
BYTEPOS TAG             LENGTH  VALUE
------- ---             ------  -----
1       RECORDLENGTH    2       1147
2       DNSNAME         11      gigantic-6
3       SUBJECTNAME     55      CN=gigantic-6.cisco.com;OU=VTG;O=Alpha;L=SJ;ST=CA;C=US
4       FUNCTION        2       Security Token
5       ISSUERNAME      55      CN=gigantic-6.cisco.com;OU=VTG;O=Alpha;L=SJ;ST=CA;C=US
6       SERIAL NUMBER   8
7       PUBLICKEY       140
8       SIGNATURE       128
9       CERTIFICATE     712
Signature Verified successfully
10      IPADDRESS       4

        CTL Record  #: 2
                     ----
BYTEPOS TAG             LENGTH  VALUE
------- ---             ------  -----
1       RECORDLENGTH    2       1147
2       DNSNAME         11      gigantic-6
3       SUBJECTNAME     55      CN=gigantic-6.cisco.com;OU=VTG;O=Alpha;L=SJ;ST=CA;C=US
4       FUNCTION        2       CCM+TFTP
5       ISSUERNAME      55      CN=gigantic-6.cisco.com;OU=VTG;O=Alpha;L=SJ;ST=CA;C=US
6       SERIAL NUMBER   8
7       PUBLICKEY       140
8       SIGNATURE       128
9       CERTIFICATE     712
10      IPADDRESS       4

        CTL Record  #: 3
                     ----
BYTEPOS TAG             LENGTH  VALUE
------- ---             ------  -----
1       RECORDLENGTH    2       1171
2       DNSNAME         11      gigantic-7
3       SUBJECTNAME     61      CN=gigantic-7.cisco.com;OU=vtg;O=cisco;L=san jose;ST=ca;C=US
4       FUNCTION        2       CCM+TFTP
5       ISSUERNAME      61      CN=gigantic-7.cisco.com;OU=vtg;O=cisco;L=san jose;ST=ca;C=US
6       SERIAL NUMBER   8
7       PUBLICKEY       140
8       SIGNATURE       128
9       CERTIFICATE     724
10      IPADDRESS       4

        CTL Record  #: 4
                     ----
BYTEPOS TAG             LENGTH  VALUE
------- ---             ------  -----
1       RECORDLENGTH    2       1085
2       DNSNAME         11      gigantic-6
3       SUBJECTNAME     48      CN=CAPF-2076a1a2;OU=VTG;O=Alpha;L=SJ;ST=CA;C=US
4       FUNCTION        2       CAPF
5       ISSUERNAME      48      CN=CAPF-2076a1a2;OU=VTG;O=Alpha;L=SJ;ST=CA;C=US
6       SERIAL NUMBER   16
7       PUBLICKEY       140
8       SIGNATURE       128
9       CERTIFICATE     656
10      IPADDRESS       4

        CTL Record  #: 5
                     ----
BYTEPOS TAG             LENGTH  VALUE
------- ---             ------  -----
1       RECORDLENGTH    2       1161
2       DNSNAME         11      gigantic-6
3       SUBJECTNAME     67      CN=ITLRECOVERY_gigantic-6.cisco.com;OU=CTG;O=Alpha;L=SJ;ST=CA;C=US
4       FUNCTION        2       Security Token
5       ISSUERNAME      67      CN=ITLRECOVERY_gigantic-6.cisco.com;OU=CTG;O=Alpha;L=SJ;ST=CA;C=US
6       SERIAL NUMBER   16
7       PUBLICKEY       140
8       SIGNATURE       128
9       CERTIFICATE     694
Signature verification failed,openssl reason=106
10      IPADDRESS       4

        CTL Record  #: 6
                     ----
BYTEPOS TAG             LENGTH  VALUE
------- ---             ------  -----
1       RECORDLENGTH    2       1143
2       DNSNAME         15      ccm-sjcctg-013
3       SUBJECTNAME     59      CN=ccm-sjcctg-013.cisco.com;OU=CTG;O=Alpha;L=SJ;ST=CA;C=US
4       FUNCTION        2       CCM+TFTP
5       ISSUERNAME      59      CN=ccm-sjcctg-013.cisco.com;OU=CTG;O=Alpha;L=SJ;ST=CA;C=US
6       SERIAL NUMBER   16
7       PUBLICKEY       140
8       SIGNATURE       128
9       CERTIFICATE     688
10      IPADDRESS       4

 * */

#define PRINT_DBG(...)
//#define PRINT_DBG printf

#define TLV_FNAME "SCFFile.tlv"
#define LEN_STR "LENGTH"
#define VAL_STR "VALUE"
#define BYTE_POS_STR "BYTEPOS"
#define TAG_STR "TAG"

#define BYTES_STR "(BYTES)"

#define PARSE_CTL_FILE "Parse CTL File"
#define START_CTL_STR "Start CTL Records"
#define CTL_RECORD_HDR "CTL Record  #:" 
#define UNKNOWN_STR "Unknown"

typedef enum {
    SCFH_START = 0x01,
    SCFH_REVISION = SCFH_START,
    SCFH_HDR_LEN = 0x02,
    SCFH_SIGNER_ID = 0x03,
    SCFH_SIGNER_NAME = 0x04,
    SCFH_SERIAL_NUM = 0x05,
    SCFH_CA_NAME = 0x06,
    SCFH_SIGNATURE_INFO = 0x07,
    SCFH_DIGEST_ALGO = 0x08,
    SCFH_SIGNATURE_ALGO_INFO = 0x09,
    SCFH_SIGNATURE_ALGO = 0x0a,
    SCFH_SIGNATURE_MODULUS = 0x0b,
    SCFH_SIGNATURE = 0x0c,
    SCFH_0X0D = 0x0d, /* Unknown*/
    SCFH_FILENAME = 0x0e,
    SCFH_TIMESTAMP = 0x0f,
    SCFH_END = SCFH_TIMESTAMP
} scfh_type_e;

typedef enum {
    SCFB_START = 0x01,
    SCFB_RECORD_LENGTH = SCFB_START,
    SCFB_DNSNAME = 0x02,
    SCFB_SUBJECTNAME = 0x03,
    SCFB_FUNCTION = 0x04,
    SCFB_ISSUERNAME = 0x05,
    SCFB_SERIAL_NUMBER = 0x06,
    SCFB_PUBLIC_KEY = 0x07,
    SCFB_SIGNATURE = 0x08,
    SCFB_CERTIFICATE = 0x09,
    SCFB_IP_ADDRESS = 0x0a,
    SCFB_END = SCFB_IP_ADDRESS 
} scfb_type_e;

typedef enum {
    SCF_HEADER = 1,
    SCF_BODY = 2
} scf_type_e;

typedef enum {
    UINT8,
    UINT16,
    UINT32,
    UINT64,
    BYTE,
    STRING,
    NONE
} datatype_e;


typedef struct scfh_parse_ {
    union {
        scfh_type_e h;
        scfb_type_e b;
    } type;
    bool has_value;
    const char *type_str;
    datatype_e dtype; 
} scfh_parse_t;

typedef struct scf_tlv_ {
    scf_type_e n_type;
    uint8_t type;
    uint16_t length;
    void *value;
} scf_tlv_t;



const char *scfh_type_to_str(scfh_type_e e); 
const char *scfb_type_to_str(scfb_type_e e); 
int scf_parse_file(const char*pathname); 

#endif /* __SCF_PARSE_H__*/
