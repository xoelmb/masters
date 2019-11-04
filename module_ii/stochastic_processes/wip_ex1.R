# Jakub Widawsky & Xoel Mato Blanco
# MSc Bioinformatics
# Module II: Stochastic processes for sequence analysis. Homework exercises.

setwd("/home/masterbio/Escritorio/Xoel/git/masters/module_ii/stochastic_processes/")

# EXERCISE 1. Comparing Zika and Dengue virus genomes.

# Loading the sequences of both viruses
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

#install.packages("formattable")
#install.packages("dplyr")
library(formattable)
library(dplyr)

# Computing rho and zscores, and creating a data frame with the results for zika and dengue viruses

# Zika
zika_rho <- rho(zika, 2)
zika_zscore <- zscore(zika, modele="base")
zika_representation <- cbind(zika_rho, zika_zscore)
colnames(zika_representation) <- c("rho value","Z score")
zika_representation <- as.data.frame(zika_representation)
formattable(zika_representation, list(`Z score` = formatter("span",style = x ~ style(color = ifelse(x < -2, "red",ifelse(x >2, "green","black"))))))

# Dengue
dengue_rho <- rho(dengue, 2)
dengue_zscore <- zscore(dengue, modele="base")
dengue_representation <- cbind(dengue_rho, dengue_zscore)
colnames(dengue_representation) <- c("rho value","Z score")
dengue_representation <- as.data.frame(dengue_representation)
formattable(dengue_representation, list(`Z score` = formatter("span",style = x ~ style(color = ifelse(x < -2, "red",ifelse(x >2, "green","black"))))))
