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
print(zika)

# a. Nucleotide and dinucleotide frequencies

# Computing the frequency of each nucleotide in both organisms and plotting the results
z_nuc_freq <- table(zika)/length(zika)
d_nuc_freq <- table(dengue)/length(dengue)
nuc_freq <- rbind(z_nuc_freq,d_nuc_freq)
rownames(nuc_freq) <- c("Zika", "Dengue")
barplot(nuc_freq, beside=TRUE, ylim=c(0,0.45), xlab="Nucleotide", ylab="Frequency", main="Nucleotide frequencies", legend=rownames(nuc_freq), col=c("#606C38","#BC6C25"))

# Doing the same, but counting dinucleotides in this case
z_dinuc_freq <- count(zika,2,freq=TRUE)
d_dinuc_freq <- count(dengue,2,freq=TRUE)
dinuc_freq <- rbind(z_dinuc_freq, d_dinuc_freq)
rownames(dinuc_freq) <- c("Zika","Dengue")
barplot(dinuc_freq, beside=TRUE, ylim=c(0,0.12), xlab="Dinucleotide", ylab="Frequency", main="Dinucleotide frequencies", legend=rownames(nuc_freq), col=c("#606C38","#BC6C25"))


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


# c. GC content

#  i. Genome-wide
zika_GC <- GC(zika)
zika_AT <- 1 - zika_GC
dengue_GC <- GC(dengue)
dengue_AT <- 1 - dengue_GC
comparison_GC <- matrix(c(zika_GC,zika_AT, dengue_GC, dengue_AT),nrow=2, ncol=2, byrow=TRUE)
rownames(comparison_GC) <- c("Zika", "Dengue")
colnames(comparison_GC) <- c("GC", "AT")
barplot(comparison_GC, beside=TRUE, main="GC/AT content", legend=rownames(comparison_GC), col=c("#606C38","#BC6C25"), ylim=c(0,0.75), ylab="Relative content")





#######LEFT TO CLEAN 
#4
nzika <- length(zika)
mzika <- 200
kzika <- nzika%/%mzika
gcczika <- numeric(kzika)

for (i in 1:kzika){
  a<-(i-1)*mzika+1; b <- a+mzika-1
  gcczika[i] <- GC(zika[a:b])
}

hist(gcczika)
ts.plot(gcczika)

#9 Sliding window of GC overrepresentation
nzika <- length(zika)
mszika <- c(50,100,200,400,800)

for (mzika in mszika){
  kzika <- nzika%/%mzika
  rhozika <- numeric(kzika)
  for (i in 1:kzika){
    a<-(i-1)*mzika+1; b <- a+mzika-1
    rhozika[i] <- rho(zika[a:b])["gc"]
    
  }
  jpeg(paste(mzika,"rhocg_zika.jpg"))
  ts.plot(rhozika, main=paste("Window:", mzika), ylim=c(0,2), ylab="rho(GC)", xlab="# Window")
  dev.off()
}
