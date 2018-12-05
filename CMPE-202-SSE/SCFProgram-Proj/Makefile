#------------------------------------------------------------------------------
#
#
#
#
#------------------------------------------------------------------------------
CC = gcc
CFLAGS = -g -Wall
SCFPRG = scfprg

$(DEPHDR) :  scf.h scf_glibc.h 

$(SCFPRG) : main.o scf_parse.o scf_parse_test.o
			$(CC) $(CFLAGS) -o $(SCFPRG) main.o scf_parse.o scf_parse_test.o

main.o : main.c $(DEPHDR)
		$(CC) $(CFLAGS) -c main.c

scf_parse.o : scf_parse.c $(DEPHDR)
		$(CC) $(CFLAGS) -c scf_parse.c

scf_parse_test.o : scf_parse.c $(DEPHDR) 
		$(CC) $(CFLAGS) -c scf_parse_test.c

clean : 
	rm scfprg main.o scf_parse.o scf_parse_test.o

#objdir : 

all : $(SCFPRG)
