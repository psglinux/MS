#include "scf_glibc.h"
#include "scf.h"

struct tailq_entry *allocate_tailq_entry(void)
{
    struct tailq_entry *t;
    t = calloc(1, sizeof(struct tailq_entry));
    if (!t) {
        printf("failed to allocate memory : %s\n", strerror(errno));
        exit(EXIT_FAILURE);
    }
    return (t);
}
void free_tailq_entry(struct tailq_entry *t)
{
    if (t) {
        if (t->tlv.value) {
            free(t->tlv.value);
        }
        free(t);
    }
}

int update_data_tlv(scf_tlv_t *tlv, scf_type_e t, uint8_t type, uint16_t len, 
                    datatype_e dt, bool has_val, void *val) 
{
    if (!tlv) return (EXIT_FAILURE);

    tlv->n_type = t;
    tlv->type = type;  
    tlv->length = len;
    tlv->has_value = has_val;
    tlv->dtype = dt;
    if (has_val) {
        tlv->value = calloc(1, len);
        if (!tlv->value) {
            printf("failed to allocate memory : %s\n", strerror(errno));
            exit(EXIT_FAILURE);
        }
        memcpy(tlv->value, val, len);
    }
    return (EXIT_SUCCESS);  
}

int insert_tailq_entry(struct queuehead *qhead, struct tailq_entry *lelem, 
                        struct tailq_entry *elem)
{
    if (!elem) {
        printf("element is not present\n");
        return (EXIT_FAILURE);
    }
    if (TAILQ_EMPTY(qhead)) {
        TAILQ_INSERT_HEAD(qhead, elem, tailq_entries);
    } else {
        if (!lelem) {
            printf("last element is empty");
            return (EXIT_FAILURE);
        }
        TAILQ_INSERT_AFTER(qhead, lelem, elem, tailq_entries);
    }
    return (EXIT_SUCCESS);
}

void print_hex_value(uint32_t len, void *value)
{
    uint16_t i, l;
    if (len > MAX_PRINT_LEN) {
        l = MAX_PRINT_LEN;
    } else {
        l = len;
    }
    for (i = 0; i < l; i++) {
        printf("%x ", *(uint8_t*)(value+i));
    }
}
void print_ip_addr(void *data)
{
    uint8_t ip[4];
    memcpy(&ip, data, sizeof(uint32_t));
    printf("%d.%d.%d.%d", ip[0], ip[1], ip[2], ip[3]);
}

void print_data_value(datatype_e dt, uint32_t len, void *data)
{
    switch(dt) {
        case UINT8:
            printf("%-8u", *(uint8_t*)data);
            break;
        case UINT16:
        case VERSION:
            printf("%-8u", *(uint16_t*)data);
            break;
        case UINT32:
            printf("%-8u", *(uint32_t*)data);
            break;
        case UINT64:
            printf("%-8lu", *(uint64_t*)data);
            break;
        case BYTE:
            print_hex_value(len, data);
            break;
        case STRING:
            printf("%-8s", (char*)data);
            break;
        case IPADDR:
            print_ip_addr(data);
            break;
        case NONE:
            printf("(None)");
            break;
    }
}

void print_tailq_entry(struct queuehead *qhead)
{
    struct tailq_entry *elem;

    if (!qhead) {
        printf("queue is empty\n");
        return;
    }
    printf("Type\tTag\t\t\tLength\tValue\n");
    printf("----\t---\t\t\t------\t-----\n");
    TAILQ_FOREACH(elem, qhead, tailq_entries) {
        printf("%-8d%-24s%-8d", 
               elem->tlv.type, 
               (elem->tlv.n_type == SCF_HEADER)?scfh_type_to_str(elem->tlv.type):scfb_type_to_str(elem->tlv.type), 
               elem->tlv.length);
        print_data_value(elem->tlv.dtype, elem->tlv.length, elem->tlv.value);
        printf("\n");
    }
}

struct btailq_entry *allocate_btailq_entry(void)
{
    struct btailq_entry *t;
    t = calloc(1, sizeof(struct btailq_entry));
    if (!t) {
        printf("failed to allocate memory : %s\n", strerror(errno));
        exit(EXIT_FAILURE);
    }
    return (t);
}
void free_btailq_entry(struct btailq_entry *t)
{
    if (t) {
        /*TBD Free each list present*/
        free(t);
    }
}
int insert_btailq_entry(struct bqueuehead *qhead, struct btailq_entry *lelem, struct btailq_entry *elem)
{
    return (EXIT_FAILURE);
}
void print_btailq_entry(struct bqueuehead *bqhead)
{
#if 0
    struct btailq_entry *belem;
    struct tailq_entry *elem;

    if (!bqhead) {
        printf("body queue is empty\n");
        return;
    }

    TAILQ_FOREACH(belem, bqhead, btailq_entries) {
        printf ("printing record\n");
        print_tailq_entry(belem->btailq_entry_head);
    }
#endif
}
