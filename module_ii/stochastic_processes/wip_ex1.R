# Jakub Widawsky & Xoel Mato Blanco
# MSc Bioinformatics
# Module II: Stochastic processes for sequence analysis. Homework exercises.

#setwd("/home/masterbio/Escritorio/Xoel/git/masters/module_ii/stochastic_processes/")
#setwd("/home/xoel/github/masters/module_ii/stochastic_processes/")

# EXERCISE 1. Comparing Zika and Dengue virus genomes.

# Loading the sequences of both viruses
library(seqinr)
zika <- read.fasta(file="./zika.fasta")
zika <- zika[[1]]
dengue <- read.fasta(file="./dengue.fasta")
dengue <- dengue[[1]]

# a. Nucleotide frequencies
# i. Nucleotides
# Computing the frequency of each nucleotide in both organisms and plotting the results
z_nuc_freq <- table(zika)/length(zika)
d_nuc_freq <- table(dengue)/length(dengue)
nuc_freq <- rbind(z_nuc_freq,d_nuc_freq)
rownames(nuc_freq) <- c("Zika", "Dengue")
barplot(nuc_freq, beside=TRUE, ylim=c(0,0.45), xlab="Nucleotide", ylab="Frequency", main="Nucleotide frequencies", legend=rownames(nuc_freq), col=c("#606C38","#BC6C25"))

# ii. Dinucleotides
# Doing the same, but counting dinucleotides in this case
z_dinuc_freq <- count(zika,2,freq=TRUE)
d_dinuc_freq <- count(dengue,2,freq=TRUE)
dinuc_freq <- rbind(z_dinuc_freq, d_dinuc_freq)
rownames(dinuc_freq) <- c("Zika","Dengue")
barplot(dinuc_freq, beside=TRUE, ylim=c(0,0.12), xlab="Dinucleotide", ylab="Frequency", main="Dinucleotide frequencies", legend=rownames(dinuc_freq), col=c("#606C38","#BC6C25"))

# iii. Trinucleotides
# Counting trinucleotides
z_trinuc_freq <- count(zika,3,freq=TRUE)
d_trinuc_freq <- count(dengue,3,freq=TRUE)
trinuc_freq <- rbind(z_trinuc_freq, d_trinuc_freq)
rownames(trinuc_freq) <- c("Zika","Dengue")
barplot(trinuc_freq, beside=TRUE, ylim=c(0,0.12), xlab="Trinucleotide", ylab="Frequency", main="Trinucleotide frequencies", legend=rownames(trinuc_freq), col=c("#606C38","#BC6C25"))

# b. Under/Overrepresentation

#install.packages("formattable")
#install.packages("dplyr")
library(formattable)
library(dplyr)

# i. Dinucleotides
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

# ii. Trinucleotides
# Zika
zika_rho <- rho(zika, 3)
zika_zscore <- zscore(zika, modele="base")
zika_representation <- cbind(zika_rho, zika_zscore)
colnames(zika_representation) <- c("rho value","Z score")
zika_representation <- as.data.frame(zika_representation)
formattable(zika_representation, list(`Z score` = formatter("span",style = x ~ style(color = ifelse(x < -2, "red",ifelse(x >2, "green","black"))))))

# Dengue
dengue_rho <- rho(dengue, 3)
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


# ii. Sliding-windows for GC content
win_lengths <- c(50,100,200,400,800)

# Zika
for (window in win_lengths){
  chunks <- length(zika)%/%window
  zika_gcs <- numeric(chunks)
  for (i in 1:chunks){
    a<-(i-1)*window+1; b <- a+window-1
    zika_gcs[i] <- GC(zika[a:b])
    
  }
  png(paste("Zika", window, "GC.png"))
  ts.plot(zika_gcs, main=paste("Window:", window), ylim=c(0.25,0.75), ylab="GC content", xlab="# Window")
  dev.off()
}

# Dengue
for (window in win_lengths){
  chunks <- length(dengue)%/%window
  dengue_gcs <- numeric(chunks)
  for (i in 1:chunks){
    a<-(i-1)*window+1; b <- a+window-1
    dengue_gcs[i] <- GC(zika[a:b])
    
  }
  png(paste("Dengue", window, "GC.png"))
  ts.plot(dengue_gcs, main=paste("Window:", window), ylim=c(0.25,0.75), ylab="GC content", xlab="# Window")
  dev.off()
}



### SOME THOUGHTS ON THE CODE ABOVE:#########################################################################################
#
# Would it be better to merge both overrepresentation tables in section b?
#
# So I tried to create a list with the organism and use a for loop to run the code that is repeated. It didn't work,
# I really don't get why, but I don't see the point in shrinking the code for this assignment.
# 
# So we're computing the GC content of all the sequence with different window sizes. The thing is that I am not sure if it's 
# better to check the overrepresentation (rho value or zscore) of gc dinucleotide. At class, we used the GC content, but
# the exercise 9 in class exercises asks for the rho(GC) with sliding windows. I already have that code ready in another file
# just in case.
#
###FOLLOWING EXERCISES...######################################################################################################
