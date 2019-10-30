
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


#3. DISTRIBUTIONS

dpois(16, lambda=12);

ppois(16,lambda=12)+ppois(16,lambda=12, lower=FALSE); #16 is not included in one of them (lower=FALSE, most likely)

# Poisson is not that good for small chromosomes since at least 1 crossover is needed, and that distribution would assume lots of 0 events.
  
# One of those exercises: número de hijos para que la prob de tener esos o menos sea 94.5%
qpois(.945,2);

# Continuous:
  sort(round(runif(10, min=1, max=1345234)));



# 29.10

dnorm(-1.1)
x<-seq(-4,4,0.1)
plot(x,dnorm(x),type="l")
x<-seq(0,4,0.1)
plot(x,dnorm(x,2,0.25),type="l")
pnorm(84,mean=72,sd=15.2,lower.tail = FALSE)
pnorm(65,72,15.2, lower.tail = FALSE) - pnorm(89,72,15.2, lower.tail = FALSE) 


#
qnorm(.975)

samplenorm = rnorm(100)
samplenorm
mean(samplenorm)
sd(samplenorm)
normalmean2s3 = rnorm(300,2,3)
mean(normalmean2s3)
#you have to put lower tail FALSE with pnorm
#Or you could use qnorm...¿? no me estoy enterando y es importante
1.17


##Two ways of making the same question
#       ¿?¿?¿?¿?
pnorm(65,72,15.2, lower.tail = FALSE) - pnorm(89,72,15.2, lower.tail = FALSE) 




######## De los ejemplos, no podemos decir el color del sweater, wiene que ser el numero de veces que cojo un color.    

z = (74-79)/(sqrt(225/42));
z
pnorm(z);
qnorm(.975);

  
  z.test <- function(a, mu, sd){
    zeta = (mean(a) - mu) / (sd/sqrt(length(a)));
    prob = pnorm(abs(zeta),lower=FALSE); #one tail
    result = c("z = ",round(zeta,4),", prob. =",round(prob,4));
    return(result);
  }
  a = c(65, 78, 88, 55, 48, 95, 66, 57, 79, 81);
  z.test(a, 75, 18) ;
















