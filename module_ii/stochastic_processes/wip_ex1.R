# Jakub Widawsky & Xoel Mato Blanco
# MSc Bioinformatics
# Module II: Stochastic processes for sequence analysis. Homework exercises.

setwd("/home/xoel/github/masters/module_ii/stochastic_processes/")

# EXERCISE 1. Comparing Zika and Dengue virus genomes.

# Reading the sequences of both viruses
library(seqinr)
zika <- read.fasta(file="./zika.fasta")
zika <- zika[[1]]
dengue <- read.fasta(file="./dengue.fasta")
dengue <- dengue[[1]]

# a. Nucleotide and dinucleotide frequencies
# Computing the frequency of each nucleotide in both organisms and plotting the results
z_nuc_freq <- table(zika)/length(zika)
d_nuc_freq <- table(dengue)/length(dengue)
nuc_freq <- rbind(z_nuc_freq,d_nuc_freq)
rownames(nuc_freq) <- c("Zika", "Dengue")
barplot(nuc_freq, beside=TRUE, ylim=c(0,0.45), xlab="Nucleotide", ylab="Frequency", main="Nucleotide frequencies", legend=rownames(nuc_freq), col=c("gold","pink"))

# Doing the same, but counting dinucleotides in this case
z_dinuc_freq <- count(zika,2,freq=TRUE)
d_dinuc_freq <- count(dengue,2,freq=TRUE)
dinuc_freq <- rbind(z_dinuc_freq, d_dinuc_freq)
rownames(dinuc_freq) <- c("Zika","Dengue")
barplot(dinuc_freq, beside=TRUE, ylim=c(0,0.12), xlab="Dinucleotide", ylab="Frequency", main="Dinucleotide frequencies", legend=rownames(nuc_freq), col=c("gold","pink"))

# b. Under/Overrepresentation of dinculeotides
# Computing rho and zscores, and creating a data frame with the results for zika and dengue viruses
zika_rho <- rho(zika, 2)
zika_zscore <- zscore(zika, modele="base")
zika_representation <- cbind(zika_rho, zika_zscore, zika_zscore < -2, zika_zscore > 2)
colnames(zika_representation) <- c("rho value","Z score", "Underrepresented", "Overrepresented")
# I intend change the 1 and 0 to Yes or No in the table somehow
dengue_rho <- rho(dengue, 2)
dengue_zscore <- zscore(dengue, modele="base")
dengue_representation <- cbind(dengue_rho, dengue_zscore, dengue_zscore < -2, dengue_zscore > 2)
colnames(dengue_representation) <- c("rho value","Z score", "Underrepresented", "Overrepresented")
