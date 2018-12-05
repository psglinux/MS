#include "scf_glibc.h"
#include "scf.h"

void scfh_print_all(void)
{
    uint32_t i;
    printf("HEDER TAG\n");
    for (i = SCFH_START; i <= SCFH_END; i++) {
        printf("0x%02x => %s \n", i , scfh_type_to_str(i-1));
    }
}
void scfb_print_all(void)
{
    uint32_t i;
    printf("BODY TAG\n");
    for (i = SCFB_START; i <= SCFB_END; i++) {
        printf("0x%02x => %s \n", i , scfb_type_to_str(i-1));
    }
}

void scfb_test(void) 
{
    scfh_print_all();
    scfb_print_all();
}
