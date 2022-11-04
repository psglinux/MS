# LaTeX Makefile v0.33 -- LaTeX only
NAME=gantchart
PAPER=$(NAME).tex  # set the path to your TeX file here
SHELL=/bin/bash   # for the while loop below
PAPERPDF=$(NAME).pdf

all:  ## Compile paper
	latexmk -pdf $(PAPER)

clean:  ## Clean output files
	latexmk -c $(PAPER)

watch:  ## Recompile on updates to the source file
	while [ 1 ]; do \
		inotifywait $(PAPER); \
		sleep 0.01; \
		make all; \
		PDFPID=pidof "xpdf.real"; \
		kill -9 $(PDFPID); \
		xpdf $(PAPERPDF); \
		done
	# for Bash users, replace the while loop with the following
	# @while true; do; inotifywait $(PAPER); sleep 0.01; make all; done
