#ifndef __SCF_DATA__H__
#define __SCF_DATA__H__

struct tailq_entries;

struct tailq_entry {
    scf_tlv_t tlv;
    TAILQ_ENTRY(tailq_entry) tailq_entries;
};

TAILQ_HEAD(queuehead, tailq_entry);

/* body tailq would be a list of tailq_entry*/
struct btailq_entry {
    TAILQ_ENTRY(btailq_entry) btailq_entries;
};

TAILQ_HEAD(bqueuehead, body_tailq_entry);

struct tailq_entry *allocate_tailq_entry(void);
void free_tailq_entry(struct tailq_entry *t);
int insert_tailq_entry(struct queuehead *qhead, struct tailq_entry *lelem, struct tailq_entry *elem); 
void print_tailq_entry(struct queuehead *qhead);
int update_data_tlv(scf_tlv_t *tlv, scf_type_e t, uint8_t type, uint16_t len, datatype_e dt, 
                    bool has_val, void *val); 
struct btailq_entry *allocate_btailq_entry(void);
void free_btailq_entry(struct btailq_entry *t);
int insert_btailq_entry(struct bqueuehead *qhead, struct btailq_entry *lelem, struct btailq_entry *elem); 
void print_btailq_entry(struct bqueuehead *qhead);


#endif /* __SCF_DATA__H__*/
