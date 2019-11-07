# Jakub Widawsky & Xoel Mato Blanco
# MSc Bioinformatics
# Module II: Stochastic processes for sequence analysis. Homework exercises.

#setwd("/home/masterbio/Escritorio/Xoel/git/masters/module_ii/stochastic_processes/")
#setwd("/home/xoel/github/masters/module_ii/stochastic_processes/")

source_dir <- dirname(rstudioapi::getSourceEditorContext()$path)

# EXERCISE 1. Comparing Zika and Dengue virus genomes.

writeLines("\n\n\t\tQuestion 1. Compare Dengue (NC_001477) with Zika virus (NC_012532.1).
\t\tThey are both mosquito borne viruses spread especially by the Aedes Aegypti mosquito.
\t\tBoth have similar symptoms, including:
\t\tconjunctivitis, muscle and joint pain, rashes, headaches and fever.\n
\t\tUse all the techniques explained in the lectures that you consider suitable. \n
           
\n In order to see Question 1. results, please look at the plots produced\n")

# Loading the sequences of both viruses
library(seqinr)
zika <- read.fasta(paste(source_dir,"/zika.fasta", sep = ""))
zika <- zika[[1]]
dengue <- read.fasta(paste(source_dir,"/dengue.fasta", sep = ""))
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
  
z_dinuc_freq <- seqinr::count(zika, 2, freq=TRUE)
d_dinuc_freq <- seqinr::count(dengue,2,freq=TRUE)
dinuc_freq <- rbind(z_dinuc_freq, d_dinuc_freq)
rownames(dinuc_freq) <- c("Zika","Dengue")
barplot(dinuc_freq, beside=TRUE, ylim=c(0,0.12), xlab="Dinucleotide", ylab="Frequency", main="Dinucleotide frequencies", legend=rownames(dinuc_freq), col=c("#606C38","#BC6C25"))

# iii. Trinucleotides
# Counting trinucleotides 
z_trinuc_freq <- seqinr::count(zika,3,freq=TRUE)
d_trinuc_freq <- seqinr::count(dengue,3,freq=TRUE)
trinuc_freq <- rbind(z_trinuc_freq, d_trinuc_freq)
rownames(trinuc_freq) <- c("Zika","Dengue")
barplot(trinuc_freq, beside=TRUE, ylim=c(0,0.045), xlab="Trinucleotide", ylab="Frequency", main="Trinucleotide frequencies", legend=rownames(trinuc_freq), col=c("#606C38","#BC6C25"))


# b. Under/Overrepresentation

#install.packages("formattable")
#install.packages("dplyr")
library(formattable)
library(dplyr)

# i. Dinucleotides
# Computing rho and zscores, and creating a data frame with the results for zika and dengue viruses
zika_dinuc_rho <- rho(zika, 2)
zika_dinuc_zscore <- zscore(zika, modele="base")
dengue_dinuc_rho <- rho(dengue, 2)
dengue_dinuc_zscore <- zscore(dengue, modele="base")

dinuc_representation <- cbind(zika_dinuc_rho, dengue_dinuc_rho, zika_dinuc_zscore, dengue_dinuc_zscore)
colnames(dinuc_representation) <- c("Zika rho", "Dengue rho", "Zika Z score", "Dengue Z score")
dinuc_representation <- as.data.frame(dinuc_representation)

formattable(dinuc_representation, list(`Zika Z score` = formatter
                                       ("span",style = x ~ style(color = ifelse(x < -2, "red",ifelse(x >2, "green","black")))),
                                       `Dengue Z score` = formatter
                                       ("span",style = x ~ style(color = ifelse(x < -2, "red",ifelse(x >2, "green","black"))))))

# ii. Trinucleotides
zika_trinuc_rho <- rho(zika, 3)
zika_trinuc_zscore <- zscore(zika, modele="base")
dengue_trinuc_rho <- rho(dengue, 3)
dengue_trinuc_zscore <- zscore(dengue, modele="base")

trinuc_representation <- cbind(zika_trinuc_rho, dengue_trinuc_rho, zika_trinuc_zscore, dengue_trinuc_zscore)
colnames(trinuc_representation) <- c("Zika rho", "Dengue rho", "Zika Z score", "Dengue Z score")
trinuc_representation <- as.data.frame(trinuc_representation)

formattable(trinuc_representation, list(`Zika Z score` = formatter
                                       ("span",style = x ~ style(color = ifelse(x < -2, "red",ifelse(x >2, "green","black")))),
                                       `Dengue Z score` = formatter
                                       ("span",style = x ~ style(color = ifelse(x < -2, "red",ifelse(x >2, "green","black"))))))

# c. GC content

#  i. Genome-wide
# GC content is known to be very variable between species. We can check if there's a difference between both viruses using the code below.

zika_GC <- GC(zika)
zika_AT <- 1 - zika_GC
dengue_GC <- GC(dengue)
dengue_AT <- 1 - dengue_GC
comparison_GC <- matrix(c(zika_GC,zika_AT, dengue_GC, dengue_AT),nrow=2, ncol=2, byrow=TRUE)
rownames(comparison_GC) <- c("Zika", "Dengue")
colnames(comparison_GC) <- c("GC", "AT")
barplot(comparison_GC, beside=TRUE, main="GC/AT content", legend=rownames(comparison_GC), col=c("#606C38","#BC6C25"), ylim=c(0,0.75), ylab="Relative content")


# ii. Sliding-windows for GC content
# The GC content within a species has also great variability. Coding sequences usually have a greater GC content than other 
# sequences. Using sliding windows, we can infere which regions are more likely to be coding sequences.

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


# d. GpC overrepresentation
# The dinculeotide CpG is partly responsible for the regulation of the gene expression in many organisms. This nucleotide is
# usually underrepresented across the genome, except for those regions that are regulated by cytosine methylation.

# Zika
for (window in win_lengths){
  chunks <- length(zika)%/%window
  zika_zscores <- numeric(chunks)
  for (i in 1:chunks){
    a<-(i-1)*window+1; b <- a+window-1
    zika_zscores[i] <- zscore(zika[a:b], modele="base")["gc"]
    
  }
  png(paste("Zika", window, "zscore GC.png"))
  ts.plot(zika_zscores, main=paste("GC representation\nWindow:", window), ylim=c(-4,4), ylab="GC zscore", xlab="# Window")
  dev.off()
}

# Dengue
for (window in win_lengths){
  chunks <- length(dengue)%/%window
  dengue_zscores <- numeric(chunks)
  for (i in 1:chunks){
    a<-(i-1)*window+1; b <- a+window-1
    dengue_zscores[i] <- zscore(dengue[a:b], modele="base")["gc"]
    
  }
  png(paste("Dengue", window, "zscore GC.png"))
  ts.plot(dengue_zscores, main=paste("GC representation\nWindow:", window), ylim=c(-4,4), ylab="GC zscore", xlab="# Window")
  dev.off()
}



## Question 2 - Download Zika virus (NC_012532.1). Fit its genoma sequence to a Markov chain
## model, estimating its transition probability matrix
writeLines("\n\n\t\t Question 2 - Download Zika virus (NC_012532.1).
           \t\tFit its genoma sequence to a Markov chain model
           \t\testimating its transition probability matrix\n")

a=seqinr::count(zika,2)
c = matrix(a, 4, 4, byrow=TRUE, dimnames=list(c("a","c","g","t"), c("a","c","g","t")))
tranzika = c[,]/(c[,1]+c[,2]+c[,3]+c[,4])
writeLines("\n\n\t\t Transition probability matrix - Zika virus genome\n")
print(tranzika)


## Question 3 - Take the sequence of Dengue virus (NC_001477) from position 101 to 200
##(this is a chunk of length 100). Suppose now that you don't know whether this sequence
##belongs to Zica or Dengue virus (of course, you know it!).
##Decide using the loglikelihood method to which virus this sequence belongs.
writeLines("\n\n\t\tQuestion 3 - Take the sequence of Dengue virus (NC_001477) from position 101 to 200
            \t\tSuppose now that you don't know whether this sequence
            \t\tbelongs to Zica or Dengue virus (of course, you know it!).
            \t\tDecide using the loglikelihood method to which virus this sequence belongs.\n")


a=seqinr::count(dengue,2)
c = matrix(a, 4, 4, byrow=TRUE, dimnames=list(c("a","c","g","t"), c("a","c","g","t")))
trandengue = c[,]/(c[,1]+c[,2]+c[,3]+c[,4])
writeLines("\n\n\t\t Transition probability matrix - Dengue virus genome\n")
print(trandengue)

# seq - slice of dengue virus genome (positions 101:200 - length = 100)
# test whether seq is more likely to belong to zika or dengue genome
writeLines("\n\n\t\t Create slice of sequence of length 100 from dengue genome,
           \t\tfit it into the probability matrix using log likelihood method.\n")
seq <- dengue[101:200]
print(seq)
n = length(seq)
s=0
for(i in 1:(n-1)){
  s=s+log(trandengue[seq[i],seq[i+1]]/tranzika[seq[i], seq[i+1]])
}

writeLines("\n\n\t\t Log likelihood method:
           \t\tif score > 0 the sequence belongs to dengue, if score < 0 then to zika\n")
print(s)


## Question 4. Fit the Zica virus sequence to a two second order Markov chain model.
## Compare the results with respect a simple Markov chain model. 
writeLines("\n\n\t\tQuestion 4. Fit the Zica virus sequence to a two second order Markov chain model.
            \t\tCompare the results with respect a simple Markov chain model.\n")
writeLines("\n\n\t\t Comparing results = multinomial, classical markov chain model and
              \t\ta second order markov chain model\n")
# k=0 (multinomial)
n=length(zika); par=3
c=seqinr::count(zika,1)
p=seqinr::count(zika,1,freq=T)
BIC1=-2*sum(c*log(p)) + par*log(n)
writeLines("BIC multinomial:")
print(BIC1)

# k=1 (classical Markov chain)
n=length(zika)-1; par=12
a=seqinr::count(zika,2)
c = matrix(a, 4, 4, byrow=TRUE, dimnames =
             list(c("A","C","G","T"),c("A","C","G","T")))
p=c[,]/(c[,1]+c[,2]+c[,3]+c[,4])
BIC2=-2*sum(c*log(p)) + par*log(n)
writeLines ("BIC classical Markov Chain:")
print(BIC2)

# k=2
xt=factor(zika[3:n]) 
xt_1=factor(zika[2:(n-1)])
xt_2=factor(zika[1:(n-2)])
n=length(zika)-2; par=48
c=table(xt_1:xt_2,xt)
p=c[,]/(c[,1]+c[,2]+c[,3]+c[,4])
BIC3=-2*sum(c*log(p)) + par*log(n)
writeLines("BIC k=2:")
print(BIC3)

cat("Min BIC: ", min(BIC1, BIC2, BIC3))
cat("\nMin BIC (best model): Classical Markov Chain")