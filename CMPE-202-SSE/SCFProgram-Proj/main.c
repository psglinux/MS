#include "scf_glibc.h"
#include "scf.h"

typedef struct scf_opts_ {
    bool debug;
    bool parse;
    bool verbose;
    bool output;
    bool test;
} scf_opts_t;

int
main(int argc, char **argv)
{
    int c;
    //int digit_optind = 0;
    scf_opts_t scf_op;
    bzero((void*)(&scf_op), sizeof(scf_op));

    while (1) {
        //int this_option_optind = optind ? optind : 1;
        int option_index = 0;
        static struct option long_options[] = {
            {"parse",  required_argument, 0, 'p' },
            {"debug",  no_argument,       0, 'd' },
            {"verbose", no_argument,      0, 'v' },
            {"output", required_argument, 0, 'o' },
            {"test", no_argument,         0, 't' },
            {"help", no_argument,         0, 'h' },
            {0,         0,                0,  0 }
        };

        c = getopt_long(argc, argv, "dho:p:tv",
                 long_options, &option_index);
        if (c == -1)
            break;

        switch (c) {

        case 'd':
            printf("option d\n");
            scf_op.debug = true;
            break;

        case 'h':
            printf("option h\n");
            exit(EXIT_SUCCESS);
 
        case 'o':
            printf("option o with value '%s'\n", optarg);
            scf_op.output = true;
            break;

        case 'p':
            printf("option p with value '%s'\n", optarg);
            scf_op.parse = true;
            break;

        case 't':
            printf("option t with value '%s'\n", optarg);
            scf_op.test = true;
            break;
 
        case 'v':
            printf("option v\n");
            break;

        case '?':
            break;

        default:
            printf("?? getopt returned character code 0%o ??\n", c);
        }
    }

    if (optind < argc) {
        printf("non-option ARGV-elements: ");
        while (optind < argc)
            printf("%s ", argv[optind++]);
        printf("\n");
    }

    if (scf_op.test) {
        scfb_test();
    }

    scf_parse_file(TLV_FNAME);

    exit(EXIT_SUCCESS);
}

