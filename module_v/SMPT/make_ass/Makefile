REFDIR=./references/
IDXDIR=./index/
FASTA_FILES=$(wildcard $(REFDIR)*.f*a)
FA_FILES=$(patsubst %.fasta, %.fa, $(FASTA_FILES))
AMB_FILES=$(patsubst $(REFDIR)%.fa, %.amb, $(FA_FILES))
TARGET_DIRS=$(patsubst $(REFDIR)%.fa, $(IDXDIR)%/, $(FA_FILES))

all: $(AMB_FILES)
	

%.amb: $(IDXDIR)%/
	bwa index -p $<$* $(REFDIR)$*.f*a
	
$(TARGET_DIRS):
	mkdir -p $@

