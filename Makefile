
SLIDES = submitting-seqspecs.slides.html

PDFS =

NOTEBOOKS = submitting-seqspecs.html

ORG = 

all: $(SLIDES) $(NOTEBOOKS) $(PDFS) $(ORG)

%.slides.html:%.ipynb Makefile
	jupyter nbconvert --to slides $<

%.html:%.ipynb Makefile
	jupyter nbconvert --to html $<

%.pdf:%.ipynb Makefile
	jupyter nbconvert --to pdf $<

%.html:%.org Makefile
	emacs $< --batch -f org-html-export-to-html --kill

clean:
	rm $(SLIDES) $(NOTEBOOKS) $(PDFS) $(ORG)
