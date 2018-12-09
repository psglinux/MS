#------------------------------------------------------------------------------
#
#
#
#
#------------------------------------------------------------------------------
CC = clang
CFLAGS = -g -Wall
SCFPRG = scfprg
SCANBLD = scan-build

$(DEPHDR) :  scf.h scf_glibc.h 

$(SCFPRG) : main.o scf_parse.o scf_parse_test.o scf_data.o
			$(CC) $(CFLAGS) -o $(SCFPRG) main.o scf_parse.o scf_parse_test.o scf_data.o

main.o : main.c $(DEPHDR)
		$(CC) $(CFLAGS) -c main.c

scf_data.o : scf_data.c $(DEPHDR)
		$(CC) $(CFLAGS) -c scf_data.c

scf_parse.o : scf_parse.c $(DEPHDR)
		$(CC) $(CFLAGS) -c scf_parse.c

scf_parse_test.o : scf_parse.c $(DEPHDR) 
		$(CC) $(CFLAGS) -c scf_parse_test.c

clean : 
	rm scfprg main.o scf_parse.o scf_parse_test.o scf_data.o

#objdir : 

all : $(SCFPRG)

sa : main.c scf_parse.c scf_parse_test.c scf_data.c
	$(SCANBLD) $(CC) main.c scf_parse.c scf_data.c scf_parse_test.c
	
