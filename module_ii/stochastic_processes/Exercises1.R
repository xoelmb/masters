library(seqinr)

#1
ebola <- read.fasta(file="/home/masterbio/Escritorio/Xoel/git/masters/module_ii/stochastic_processes/evola.fasta")
ebola <- ebola[[1]]
ebola[1:200]
#2
count(ebola,1,freq=T)
barplot(count(ebola,1,freq=T))

#3
GC(ebola)
1-GC(ebola)

#4
n <- length(ebola)
m <- 200
k <- n%/%m
gcc <- numeric(k)

for (i in 1:k){
  a<-(i-1)*m+1; b <- a+m-1
  gcc[i] <- GC(ebola[a:b])
}

hist(gcc)
ts.plot(gcc)

#5
probs <- c(count(ebola,1,freq=T))
sample(c("A","C","G","T"), 1000, replace=T, prob=probs)

#6
dinuc_f <- count(ebola,2,freq=T)
rho(ebola)
scores <- zscore(ebola, modele="base")
scores < -2
scores > 2
