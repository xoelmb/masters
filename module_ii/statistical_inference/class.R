
## Me estoy intentando ubicar. **Toma pastilla de ubicaína** Es la segunda clase de inferencia estadística. No guardé nada de la anterior.
## Estamos demostrando la ley de los números grandes.

#1 Probamos generando una secuencia de DNA con unas proporciones nucleotídicas dadas.

randomDNAseq <- function(vprob,lseq){
  nucleotide = c("A","C","G","T");
  sequence<- sample(nucleotide,lseq,vprob,replace=T);
  print(sequence);
  round(table(sequence)/lseq,3);
}
randomDNAseq(c(0.3,0.2,0.4,0.1),100)

# The higher the number of nucleotides generated, the closer their proportions will approximate the established probabilities


#2 Let's try with tossing a coin

prob <- c(0.5,0.5); #head and tails have the same probs
coin <- c(1,0); # 1 is head, 0 is tail

start <- 1
finish <- 500

vector_mean <- c()

for (i in start:finish){
  vector_mean[i] <- mean(sample(coin,i,prob,replace=T));
}

plot(vector_mean, type="l", main="Large number Law", xlab="Throw number", ylab="Proportion of heads")

# The variance is smaller as higher is the number of replicates.
# We can create a function that replicates this. It's on the slides.

