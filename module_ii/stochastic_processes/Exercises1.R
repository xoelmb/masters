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












####################2

library(seqinr)

x <- c("c", "a", "g", "g", "c", "g", "g", "g", "a", "t", "t", "t", "c", "t", "c", "t", "t", "g", "t", "t", "g", "a", "c", "a", "t", "g", "a", "a", "t", "c", "c")

ebola <- read.fasta(file="/home/masterbio/Escritorio/Xoel/git/masters/module_ii/stochastic_processes/evola.fasta")
ebola <- ebola[[1]]


ae=count(ebola,2)
ce = matrix(ae, 4, 4, byrow=TRUE, dimnames = list(c("a","c","g","t"),c("a","c","g","t")))
tranebola=ce[,]/(ce[,1]+ce[,2]+ce[,3]+ce[,4])



hepat <- read.fasta(file="/home/masterbio/Escritorio/Xoel/git/masters/module_ii/stochastic_processes/hepat.fasta")
hepat <- hepat[[1]]


ah=count(hepat,2)
ch = matrix(ah, 4, 4, byrow=TRUE, dimnames = list(c("a","c","g","t"),c("a","c","g","t")))
tranhepat=ch[,]/(ch[,1]+ch[,2]+ch[,3]+ch[,4])

n=length(x); s=0
for(i in 1:(n-1)){s=s+log(tranebola[x[i],x[i+1]]/tranhepat[x[i],x[i+1]])}
s






















  

