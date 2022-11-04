# LaTeX Makefile v1.0 -- LaTeX + PDF figures + PNG figures

ALL=$(wildcard *.tex content/*.tex defense/index.html figures/svg/*.svg)
MAIN=main.tex
PAPERPDF=main.pdf
LATEXPDF=latexmk -pdf
LATEXPS=latexmk -ps
LATEXCLEAN=latexmk -c
SHELL=/bin/bash

FIGURES_SVG=$(wildcard figures/svg/*.svg)
FIGURES_PDF=$(subst svg/,pdf/,$(FIGURES_SVG:.svg=.pdf))
FIGURES_PNG=$(subst figures/svg/,defense/images/,$(FIGURES_SVG:.svg=.png))

all: $(FIGURES_PDF) $(FIGURES_PNG)  ## Build full thesis (LaTeX + figures)
	$(LATEXPDF) $(MAIN)                # main run
	#$(LATEXPS) $(MAIN)                # main run
	#bibtex $(MAIN:.tex=)            # bibliography
	#makeglossaries $(MAIN:.tex=)    # list of abbreviations, nomenclature
	#$(LATEXPDF) $(MAIN)                # incremental run

clean:  ## Clean LaTeX and output figure files
	$(LATEXCLEAN) #$(MAIN)
	rm main.bbl
	rm -f $(FIGURES_PDF) $(FIGURES_PNG)

figures/pdf/%.pdf: figures/svg/%.svg  ## Figures for the manuscript
	inkscape -C -z --file=$< --export-pdf=$@

defense/images/%.png: figures/svg/%.svg  ## Figures for my defense slides
	inkscape -C -z --file=$< --export-png=$@

watch:  ## Recompile on updates to the source file
	while [ 1 ]; do \
		inotifywait $(ALL); \
		sleep 0.01; \
		make all; \
		killall -9 'xpdf.real' 2> /dev/null || true; \
		if [ -e $(PAPERPDF) ]; then \
			xpdf $(PAPERPDF) & \
		fi; \
		done

help:  # http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
	@grep -P '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
.DEFAULT_GOAL := help
.PHONY: help
