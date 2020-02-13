#!/bin/bash

for FILE in sampleA.fastq sampleB.fastq sampleC.fastq

do

    wc -l $FILE > $FILE.wc &

done
wait
cat *.wc > results.txt

#echo -e "sampleA.fastq\nsampleB.fastq\nsampleC.fastq" | xargs -n1 -P0 -I{} $wc -l {} > {}.wc
#cat *.wc > results.txt
##
#
#
#echo -e "sampleA.fastq\nsampleB.fastq\nsampleC.fastq" | parallel -j 3 NAME = {}; wc -l {} > {1}.wc
#



#saved for later
#optimize <- function(n, max_seed, min_seed, num_iterations)
#
# {
#
#     #initialize the population of plants (solutions)
#
#         current.sols <- matrix(nrow=n, ncol = 2, rnorm(n*2));
#
##estimate the fitness of each solution
#
#         fit.current.sols <- apply(current.sols,1,fitness);
#
##evolve the population following the rules of the natural event that we are trying to mimic to optimize the function
#
#for(it in 1:num_iterations)
#
#        {
#
#min.fitness.pop <- min(fit.current.sols);
#
#max.fitness.pop <- max(fit.current.sols);
#
## decide the number of offspring of each plant based on the fitness of the solution.
#
#for(p in 1:nrow(current.sols))
#
#{
#
#num.seed.offspring.of.this.seed <- number.of.offspring(fit.current.sols[p], min.fitness.pop,             max.fitness.pop, min_seed, max_seed);
#
#jump <- matrix(nrow=num.seed.offspring.of.this.seed, ncol=2,rnorm(num.seed.offspring.of.this.seed*2,0,1));
#
#sols.seed.offspring <- matrix(nrow=num.seed.offspring.of.this.seed, ncol=2,current.sols[p,],byrow=T) + jump;
#
## limit of the function to be optimized
#
#sols.seed.offspring[sols.seed.offspring>10] <- 10;
#
#sols.seed.offspring[sols.seed.offspring< 0] <- 0;
#
#current.sols <- rbind(current.sols,sols.seed.offspring);
#
#fit.current.sols <- c(fit.current.sols,apply(sols.seed.offspring,1,fitness));
#}
#compare.fitness <- quantile(fit.current.sols, 1-n/length(fit.current.sols));
#current.sols <- current.sols[fit.current.sols>=compare.fitness,];
#fit.current.sols <- fit.current.sols[fit.current.sols>=compare.fitness];
#best.seed <- which(fit.current.sols==max(fit.current.sols));
#print(c(current.sols[best.seed,],fit.current.sols[best.seed]));
#}
#return(current.sols[fit.current.sols==max(fit.current.sols),]);
#
#}
#
# fitness of the function to optimize
#
#fitness <- function(v)
#
#{
#
#  x <- v[1];
#
#  y <- v[2];
#
#  return(x*sin(4*x) + 1.1*y*sin(2*y));
#
#}
#
#number.of.offspring <- function(fitness.parent, min.fitness.pop, max.fitness.pop, min_seed, max_seed)
#
#{
#
#  a <- (fitness.parent - min.fitness.pop)/(max.fitness.pop - min.fitness.pop);
#
#  b <- (max_seed - min_seed);
#
#  c <- round(a*b+ min_seed,0);
#
#  return(c);
#
#}
#
#res <- optimize(100,10,2,100);