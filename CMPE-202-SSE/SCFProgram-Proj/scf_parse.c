#include "scf_glibc.h"
#include "scf.h"

extern int errno;
uint16_t scf_hdr_len = 0;
bool scf_hdr_len_found = false;
bool scf_hdr_parsing_done = false;

struct slisthead *headp;

const scfh_parse_t scf_parse_hdr [SCFH_END] = {
    {
        .type.h = SCFH_REVISION, 
        .has_value = true,
        .type_str = "Version",
        .dtype = UINT16,
    }, 
    {
        .type.h = SCFH_HDR_LEN, 
        .has_value = true,
        .type_str = "Header Length",
        .dtype = UINT16,
    }, 
    {
        .type.h = SCFH_SIGNER_ID, 
        .has_value = false,
        .type_str = "Signer Identity",
        .dtype = NONE ,
    }, 
    {
        .type.h = SCFH_SIGNER_NAME, 
        .has_value = true,
        .type_str = "Signer Name",
        .dtype = STRING,
    }, 
    {
        .type.h = SCFH_SERIAL_NUM, 
        .has_value = true,
        .type_str = "Cert Serial Number",
        .dtype = STRING,
    }, 
    {
        .type.h = SCFH_CA_NAME, 
        .has_value = true,
        .type_str = "CA Name",
        .dtype = STRING,
    }, 
    {
        .type.h = SCFH_SIGNATURE_INFO, 
        .has_value = false,
        .type_str = "SIGNATUREINFO",
        .dtype = NONE,
    }, 
    {
        .type.h = SCFH_DIGEST_ALGO, 
        .has_value = true,
        .type_str = "Digest Algo",
        .dtype = UINT16,
    }, 
    {
        .type.h = SCFH_SIGNATURE_ALGO_INFO, 
        .has_value = false,
        .type_str = "Signature Algo Info",
        .dtype = NONE,
    }, 
    {
        .type.h = SCFH_SIGNATURE_ALGO, 
        .has_value = true,
        .type_str = "Signature Algo",
        .dtype = UINT16,
    }, 
    {
        .type.h = SCFH_SIGNATURE_MODULUS, 
        .has_value = true,
        .type_str = "Signature Modulus",
        .dtype = UINT8,
    }, 
    {
        .type.h = SCFH_SIGNATURE, 
        .has_value = true,
        .type_str = "SIGNATURE",
        .dtype = BYTE,
    }, 
    {
        .type.h = SCFH_0X0D, 
        .has_value = true,
        .type_str = "Unknown",
        .dtype = BYTE,
    }, 
    {
        .type.h = SCFH_FILENAME, 
        .has_value = true,
        .type_str = "FILENAME",
        .dtype = STRING,
    }, 
    {
        .type.h = SCFH_TIMESTAMP, 
        .has_value = true,
        .type_str = "TIMESTAMP",
        .dtype = STRING,
    } 
};

const scfh_parse_t scf_parse_body [SCFB_END] = {
    {
        .type.b = SCFB_RECORD_LENGTH, 
        .has_value = true,
        .type_str = "RECORDLENGTH",
        .dtype = UINT16,
    }, 
    {
        .type.b = SCFB_DNSNAME, 
        .has_value = true,
        .type_str = "DNSNAME",
        .dtype = STRING,
    }, 
    {
        .type.b = SCFB_SUBJECTNAME, 
        .has_value = true,
        .type_str = "SUBJECTNAME",
        .dtype = STRING,
    }, 
    {
        .type.b = SCFB_FUNCTION, 
        .has_value = true,
        .type_str = "FUNCTION",
        .dtype = STRING,
    }, 
    {
        .type.b = SCFB_ISSUERNAME, 
        .has_value = true,
        .type_str = "ISSUERNAME",
        .dtype = STRING,
    }, 
    {
        .type.b = SCFB_SERIAL_NUMBER, 
        .has_value = true,
        .type_str = "SERIAL NUMBER",
        .dtype = STRING,
    }, 
    {
        .type.b = SCFB_PUBLIC_KEY, 
        .has_value = true,
        .type_str = "PUBLICKEY",
        .dtype = BYTE,
    }, 
    {
        .type.b = SCFB_SIGNATURE, 
        .has_value = true,
        .type_str = "SIGNATURE",
        .dtype = BYTE,
    }, 
    {
        .type.b = SCFB_CERTIFICATE, 
        .has_value = true,
        .type_str = "CERTIFICATE",
        .dtype = BYTE,
    }, 
    {
        .type.b = SCFB_IP_ADDRESS, 
        .has_value = true,
        .type_str = "IPADDRESS",
        .dtype = STRING,
    } 
};


const char *scfh_type_str[] = {
    "",
    "Version",
    "HeaderLength",
    "SIGNERID",
    "SIGNERNAME",
    "SERIALNUMBER",
    "CANAME",
    "SIGNATUREINFO",
    "DIGESTALGO",
    "SIGNATUREALGOINFO",
    "SIGNATUREALGO",
    "SIGNATUREMODULUS",
    "SIGNATURE",
    "Unknown",
    "FILENAME",
    "TIMESTAMP",
};

const char *scfb_type_str[] = {
    "",
    "RECORDLENGTH",
    "DNSNAME",
    "SUBJECTNAME",
    "FUNCTION",
    "ISSUERNAME",
    "SERIAL NUMBER",
    "PUBLICKEY",
    "SIGNATURE",
    "CERTIFICATE",
    "IPADDRESS"
};

const char *scfh_type_to_str(scfh_type_e e) 
{
    for (uint32_t i = 0; i < SCFH_END; i++) {
        if (scf_parse_hdr[i].type.h == e) {
            return (scf_parse_hdr[i].type_str); 
        }
    }
    return (UNKNOWN_STR);
}
const char *scfb_type_to_str(scfb_type_e e) 
{
    for (uint32_t i = 0; i < SCFB_END; i++) {
        if (scf_parse_body[i].type.b == e) {
            return (scf_parse_body[i].type_str); 
        }
    }
    return (UNKNOWN_STR);
}

static bool check_scf_hdr_len_type(uint8_t type) 
{
    if ((!scf_hdr_len_found) && (type == SCFH_HDR_LEN)) {
        scf_hdr_len_found = true;
        return (true);
    }
    return (false);
}

static bool is_hdr_value_present(scfh_type_e e) 
{
    for (uint32_t i = 0; i < SCFH_END; i++) {
        if (scf_parse_hdr[i].type.h == e) {
            return (scf_parse_hdr[i].has_value);
        }
    }
    return (false);
}

void print_hex_value(uint16_t len, void *value)
{
    uint16_t i;
    for (i = 0; i < len; i++) {
        printf("%x ", *(uint8_t*)(value+i));
        if (!(i%8)) {
            printf("\n");
        }
    }
    printf("\n");
}

typedef int (*print_data)(scf_type_e e, scf_tlv_t *t);

void scf_hdr_print(uint8_t type, uint16_t len, void *value)
{
    printf("%d\t%s\t%d\tTBD\n",type, scfh_type_to_str(type), len);
}

void scf_body_print(uint8_t type, uint16_t len, void *value)
{
    printf("%d\t%s\t%d\tTBD\n",type, scfb_type_to_str(type), len);
}

int scf_parse_file(const char*pathname) 
{
    FILE *fp = NULL;
    size_t sz;
    uint8_t type;
    uint16_t len;
    void *value;
    long offset = 0;

    fp = fopen(pathname, "r");
    if (!fp) {
        printf("error opening file (%s) : %s\n", pathname, strerror(errno));
        exit(EXIT_FAILURE);
    } 


    while (true) {
        bzero((void*)&type, sizeof(type));
        bzero((void*)&len, sizeof(len));

        sz = fread((void*)&type, sizeof(type), 1, fp);
        PRINT_DBG(" type : 0x%02x sizeof(type) : %ld\n", type, sizeof(type));
        PRINT_DBG("file pos : %ld\n", ftell(fp));

        offset += sizeof(type); 
        sz = fread((void*)&len, sizeof(len), 1, fp);
        if (!sz) {
            if (feof(fp)) {
                printf ("reading of file is complete\n");
                break;
            } else {
                printf ("reading file encounteded error : %s\n", strerror(errno));
                exit(EXIT_FAILURE);
            }
        }
        len = be16toh(len);
        PRINT_DBG(" len : 0x%02x sizeof(type) : %ld\n", len, sizeof(len));
        PRINT_DBG("file pos : %ld\n", ftell(fp));
        offset += sizeof(len); 

        /* some TLV does not have value*/
        if (is_hdr_value_present(type)) {
            value = calloc(1, len);
            if (!value) {
                printf("calloc error : %s\n", strerror(errno));
                exit(EXIT_FAILURE);
            }

            sz = fread(value, len, 1, fp);
            PRINT_DBG(" value : 0x%02x sizeof(type) : %ld\n", *(char*)value, sizeof(len));
            PRINT_DBG("file pos : %ld\n", ftell(fp));
            offset += len;
        }

        if (check_scf_hdr_len_type(type)) {
            scf_hdr_len = be16toh(*(uint16_t*)(value)); 
            PRINT_DBG("scf header length : %u\n", scf_hdr_len);
        }

        if (!scf_hdr_parsing_done) {
            PRINT_DBG("+++ in scf header\n");
            scf_hdr_print(type, len, value);
        } else {
            PRINT_DBG("+++ in scf body\n");
            scf_body_print(type, len, value);
        }
        if (value) {
            free(value);
        }

        PRINT_DBG("offset : %ld scf_hdr_len : %d scf_hdr_parsing_done : %d\n", offset, scf_hdr_len, scf_hdr_parsing_done);
        if ((offset >= scf_hdr_len) && scf_hdr_len_found) {
            scf_hdr_parsing_done = true;
        }
    }

    if (fclose(fp)) {
        printf("error closing file (%s) : %s\n", pathname, strerror(errno));
        exit(EXIT_FAILURE);
    }
    return (0);
}
