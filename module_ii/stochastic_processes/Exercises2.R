library(seqinr)
ebola = read.fasta(file="/home/masterbio/Escritorio/Xoel/git/masters/module_ii/stochastic_processes/evola.fasta")
ebola = ebola[[1]]
ebola
n = length(ebola)
m = 200
k = n%/%200
gcc = numeric(k)
cacc = numeric(k)

for (i in 1:k){
  a=(i-1)*m+1
  b=a+m-1
  gcc[i]=GC(ebola[a:b])
  cacc[i] = count(ebola[a:b],3)["acc"]
}

plot(gcc,cacc)

pacc=ifelse(cacc>0,1,0)

logit<-glm(pacc~gcc,family=binomial)
summary(logit)
plot(gcc,logit$fitted.values)

poisson<-glm(cacc~gcc,family=poisson)
summary(poisson)
plot(gcc,cacc)
lines(gcc,poisson$fitted.values,type="p",col="red")
