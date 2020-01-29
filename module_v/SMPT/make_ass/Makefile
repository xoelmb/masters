FASTA_FILES=$(wildcard ./references/*.fa*)
AMB_FILES=$(patsubst ./references/%.fa, ./index/%/%.amb, $(FASTA_FILES))
ANN_FILES=$(patsubst ./references/%.fa, ./index/%/%.ann, $(FASTA_FILES))
BTW_FILES=$(patsubst ./references/%.fa, ./index/%/%.btw, $(FASTA_FILES))
PAC_FILES=$(patsubst ./references/%.fa, ./index/%/%.pac, $(FASTA_FILES))
SA_FILES=$(patsubst ./references/%.fa, ./index/%/%.sa, $(FASTA_FILES))

all:
	@echo $(FASTA_FILES)
	@echo $(AMB_FILES)
	@echo $(ANN_FILES)
	@echo $(BTW_FILES)
	@echo $(PAC_FILES)
	@echo $(SA_FILES)
