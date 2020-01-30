REFDIR=./references/
IDXDIR=./index/
FASTA_FILES=$(wildcard $(REFDIR)*.fa*)
AMB_FILES=$(patsubst $(REFDIR)%.fa, %.amb, $(FASTA_FILES))
ANN_FILES=$(patsubst $(REFDIR)%.fa, %.ann, $(FASTA_FILES))
BTW_FILES=$(patsubst $(REFDIR)%.fa, %.btw, $(FASTA_FILES))
PAC_FILES=$(patsubst $(REFDIR)%.fa, %.pac, $(FASTA_FILES))
SA_FILES=$(patsubst $(REFDIR)%.fa, %.sa, $(FASTA_FILES))
#
#ANN_FILES=$(patsubst ./references/%.fa, ./index/%/%.ann, $(FASTA_FILES))
#BTW_FILES=$(patsubst ./references/%.fa, ./index/%/%.btw, $(FASTA_FILES))
#PAC_FILES=$(patsubst ./references/%.fa, ./index/%/%.pac, $(FASTA_FILES))
#SA_FILES=$(patsubst ./references/%.fa, ./index/%/%.sa, $(FASTA_FILES))

all: 
	@echo Done
