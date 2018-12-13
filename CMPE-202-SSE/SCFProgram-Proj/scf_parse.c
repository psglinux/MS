#include "scf_glibc.h"
#include "scf.h"

extern int errno;
long scf_hdr_len = 0;
bool scf_hdr_len_found = false;

struct slisthead *headp;

const scf_parse_t scf_parse_hdr [SCFH_END] = {
    {
        .type.h = SCFH_REVISION, 
        .has_value = true,
        .type_str = "Version",
        .dtype = VERSION,
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
        .dtype = NONE,
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
        .dtype = UINT64,
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
        .has_value = false,
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
        .dtype = BYTE,
    } 
};

const scf_parse_t scf_parse_body [SCFB_END] = {
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
        .dtype = UINT16,
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
        .dtype = BYTE,
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
        .dtype = IPADDR,
    } 
};

static const datatype_e scf_hdr_data_type_get(scfh_type_e e) 
{
    for (uint32_t i = 0; i < SCFH_END; i++) {
        if (scf_parse_hdr[i].type.h == e) {
            return (scf_parse_hdr[i].dtype); 
        }
    }
    return (NONE);
}
static const datatype_e scf_body_data_type_get(scfb_type_e e) 
{
    for (uint32_t i = 0; i < SCFB_END; i++) {
        if (scf_parse_body[i].type.b == e) {
            return (scf_parse_body[i].dtype); 
        }
    }
    return (NONE); 
}

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
static bool check_scfb_record_len_type(uint8_t type) 
{
    if (type == SCFB_RECORD_LENGTH) {
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

static bool is_parsable(scfh_type_e e)
{
    if (e == SCFH_0X0D) {
        return (false);
    } else {
        return (true);
    }
}

static bool is_body_value_present(scfb_type_e e) 
{
    for (uint32_t i = 0; i < SCFB_END; i++) {
        if (scf_parse_body[i].type.b == e) {
            return (scf_parse_body[i].has_value);
        }
    }
    return (false);
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

#define FILE_READ_ERR_CHECK(sz) \
    if (!sz) { \
        if (feof(fp)) { \
            printf ("reading of file is complete\n"); \
            break; \
        } else { \
            printf ("reading file encounteded error : %s\n", strerror(errno)); \
            exit(EXIT_FAILURE); \
        } \
    } \
    

int scf_parse_file(const char*pathname) 
{
    FILE *fp = NULL;
    size_t sz = 0;
    uint8_t type;
    uint16_t len = 0;
    void *value = NULL;
    long offset = 0;
    long scfb_record_len = 0;
    struct tailq_entry *tq_entry = NULL;
    struct tailq_entry *ltq_entry = NULL;
    struct tailq_entry *rec_entry = NULL;
    struct tailq_entry *lrec_entry = NULL;
    bool hdr_val_present;
    bool body_val_present;

    struct queuehead h_head = TAILQ_HEAD_INITIALIZER(h_head); 
    TAILQ_INIT(&h_head);


    fp = fopen(pathname, "r");
    if (!fp) {
        printf("error opening file (%s) : %s\n", pathname, strerror(errno));
        exit(EXIT_FAILURE);
    } 

    while (true) {
        bzero((void*)&type, sizeof(type));
        bzero((void*)&len, sizeof(len));
        value = NULL;

        sz = fread((void*)&type, sizeof(type), 1, fp);
        FILE_READ_ERR_CHECK(sz)
        PRINT_DBG(" type : 0x%02x sizeof(type) : %ld\n", type, sizeof(type));
        PRINT_DBG("file pos : %ld\n", ftell(fp));
        offset += sizeof(type); 
        if (!is_parsable(type)) {
            printf("parsing of header is complete\n\n");
            break;
        }
        sz = fread((void*)&len, sizeof(len), 1, fp);
        FILE_READ_ERR_CHECK(sz) 
        len = be16toh(len);
        PRINT_DBG(" len : 0x%02x sizeof(type) : %ld\n", len, sizeof(len));
        PRINT_DBG("file pos : %ld\n", ftell(fp));
        offset += sizeof(len); 

        /* some TLV does not have value*/
        hdr_val_present = is_hdr_value_present(type);
        if (hdr_val_present) {
            value = calloc(1, len);
            if (!value) {
                printf("calloc error : %s\n", strerror(errno));
                exit(EXIT_FAILURE);
            }

            sz = fread(value, len, 1, fp);
            FILE_READ_ERR_CHECK(sz)
            PRINT_DBG(" value : 0x%02x sizeof(type) : %ld\n", *(char*)value, sizeof(len));
            PRINT_DBG("file pos : %ld\n", ftell(fp));
            offset += len;
        }

        if (check_scf_hdr_len_type(type)) {
            scf_hdr_len = be16toh(*(uint16_t*)(value)); 
            PRINT_DBG("scf header length : %ld\n", scf_hdr_len);
        }

        /* store */
        tq_entry = allocate_tailq_entry();
        if (update_data_tlv(&tq_entry->tlv, SCF_HEADER, type, len, scf_hdr_data_type_get(type), hdr_val_present, value?value:NULL)) {
            exit(EXIT_FAILURE);
        }
        if (insert_tailq_entry(&h_head, ltq_entry, tq_entry)) {
            exit(EXIT_FAILURE);
        }

        ltq_entry = tq_entry;

        //scf_hdr_print(type, len, value);

        if (value) {
            free(value);
        }

        PRINT_DBG("offset : %ld scf_hdr_len : %ld\n", offset, scf_hdr_len);
        if ((offset >= scf_hdr_len) && scf_hdr_len_found) {
            printf("parsing of header is complete\n\n");
            break;
        }

    }
    print_tailq_entry(&h_head);
    offset = 0;

    /* prepare btailq */

    struct bqueuehead bhead = TAILQ_HEAD_INITIALIZER(bhead);
    TAILQ_INIT(&bhead);
    struct queuehead rec_head = TAILQ_HEAD_INITIALIZER(rec_head); 
    TAILQ_INIT(&rec_head);

    /* Parse the body */


    while (true) {
        bzero((void*)&type, sizeof(type));
        bzero((void*)&len, sizeof(len));
        value = NULL;

        sz = fread((void*)&type, sizeof(type), 1, fp);
        FILE_READ_ERR_CHECK(sz)
        PRINT_DBG(" type : 0x%02x sizeof(type) : %ld\n", type, sizeof(type));
        PRINT_DBG("file pos : %ld\n", ftell(fp));

        offset += sizeof(type); 
        sz = fread((void*)&len, sizeof(len), 1, fp);
        FILE_READ_ERR_CHECK(sz)

        len = be16toh(len);
        PRINT_DBG(" len : 0x%02x sizeof(type) : %ld\n", len, sizeof(len));
        PRINT_DBG("file pos : %ld\n", ftell(fp));
        offset += sizeof(len); 

        /* some TLV does not have value*/
        body_val_present = is_body_value_present(type);
        if (body_val_present) {
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

        if (check_scfb_record_len_type(type) && value) {
            scfb_record_len = be16toh(*(uint16_t*)(value)); 
            PRINT_DBG("scf body record length : %ld\n", scfb_record_len);
        }
        /* store */
        rec_entry = allocate_tailq_entry();
        if (update_data_tlv(&rec_entry->tlv, SCF_BODY, type, len, scf_body_data_type_get(type), body_val_present, value?value:NULL)) {
            exit(EXIT_FAILURE);
        }
        if (insert_tailq_entry(&rec_head, lrec_entry, rec_entry)) {
            exit(EXIT_FAILURE);
        }

        lrec_entry = rec_entry;

        //scf_body_print(type, len, value);

        if (value) {
            free(value);
        }

        PRINT_DBG("offset : %ld scfb_record_len : %ld\n", offset, scfb_record_len);
        if (offset >= scfb_record_len) {
            /* reset the record len and offset as we are done with parsing of 
             * the body for this cert */
            scfb_record_len = 0;
            offset = 0;
            print_tailq_entry(&rec_head);
            TAILQ_INIT(&rec_head);
            printf("finished parsing the body \n\n");
        }
    }

    if (fclose(fp)) {
        printf("error closing file (%s) : %s\n", pathname, strerror(errno));
        exit(EXIT_FAILURE);
    }
    return (0);
}
