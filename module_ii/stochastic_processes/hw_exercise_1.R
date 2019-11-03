library(seqinr)
setwd("/home/xoel/github/masters/module_ii/stochastic_processes/")

#### First exercise: still uncommented, need to make it look nice.
###ZIKA
#1
zika <- read.fasta(file="./zika.fasta")
zika <- zika[[1]]
#2
count(zika,1,freq=T)
barplot(count(zika,1,freq=T))

#3
GCzika <- GC(zika)
ATzika <- 1-GC(zika)


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

#6
dinuc_f <- count(zika,2,freq=T)
rho(zika)
scores <- zscore(zika, modele="base")
scores < -2
scores > 2


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


###DENGUE
library(seqinr)
setwd("./dengue.fasta")
#1
dengue <- read.fasta(file="./dengue.fasta")
dengue <- dengue[[1]]
dengue[1:200]
#2
count(dengue,1,freq=T)
barplot(count(dengue,1,freq=T))

#3
GCdengue <- GC(ebola)
ATdengue <- 1-GC(ebola)

#4
ndengue <- length(dengue)
mdengue <- 200
kdengue <- ndengue%/%mdengue
gccdengue <- numeric(kdengue)

for (i in 1:kdengue){
  a<-(i-1)*mdengue+1; b <- a+mdengue-1
  gccdengue[i] <- GC(dengue[a:b])
}

hist(gcc)
ts.plot(gcc)


#6
dinuc_f <- count(dengue,2,freq=T)
rho(dengue)
scores <- zscore(dengue, modele="base")
scores < -2
scores > 2

#9 Sliding window of GC overrepresentation
ndengue <- length(dengue)
msdengue <- c(50,100,200,400,800)

for (mdengue in msdengue){
  kdengue <- ndengue%/%mdengue
  rhodengue <- numeric(kdengue)
  for (i in 1:kdengue){
    a<-(i-1)*mdengue+1; b <- a+mdengue-1
    rhodengue[i] <- rho(dengue[a:b])["gc"]
    
  }
  jpeg(paste(mdengue,"rhocg_dengue.jpg"))
  ts.plot(rhodengue, main=paste("Window:", mdengue), ylim=c(0,2), ylab="rho(GC)", xlab="# Window")
  dev.off()
  
}

###This is only the first exercise