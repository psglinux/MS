# LaTeX Makefile v0.33 -- LaTeX only

PAPER=finalPreso.tex  # set the path to your TeX file here
SHELL=/bin/bash   # for the while loop below
PAPERPDF=finalPreso.pdf

all:  ## Compile paper
	latexmk -pdf $(PAPER)

clean:  ## Clean output files
	latexmk -c $(PAPER)

watch:  ## Recompile on updates to the source file
	while [ 1 ]; do \
		inotifywait $(PAPER); \
		sleep 0.01; \
		make all; \
		echo "=================================="; \
		killall -9 'xpdf.real' 2> /dev/null || true; \
		echo "=================================="; \
		if [ -e $(PAPERPDF) ]; then \
			xpdf $(PAPERPDF) & \
		fi; \
		done
	# for Bash users, replace the while loop with the following
	# @while true; do; inotifywait $(PAPER); sleep 0.01; make all; done
