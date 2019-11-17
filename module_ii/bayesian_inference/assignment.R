# Xoel Mato Blanco
# 1421896
# 17/11/19

# Goal: estimate lambda from a poisson distribution.

# Step 1. Simulate a poisson distribution:
my_lambda=20
size=100
sample <- rpois(size, my_lambda)
plot(density(sample), main=paste("Sample size:",size))
abline(v=my_lambda, col="cyan")
# Step 2. Define a function that computes the probability of the data belonging to a poisson distribution of a given lambda:
log_density <- function(data, lambda){
  log_d <- dpois(data, lambda=lambda, log=TRUE)  # Stores the probability of all data points in a vector
  return(sum(log_d))  # Returns the sum of such vector
}

# Step 3. Since R does not support minimization, we define another function that returns the negative result of log_density:
min_to_max <- function(lambda){
  return(-log_density(sample, lambda))
}

# Step 4. Maximize the probability using nlm on min_to_max, which eventually maximizes log_density.
estimation <- nlm(min_to_max, p=10)
estimation$estimate
abline(v=estimation$estimate, col="red")

# EXTRA. To check how the estimation performs with other sample sizes:
size_range <- c(10, 100, 1000, 10000, 100000, 1000000, 10000000)
estimations <- c()
difference <- c()
for (s in size_range){
  sample <- rpois(s, my_lambda)
  current_est <- nlm(min_to_max, p=10)$estimate
  estimations <- append(estimations, current_est)
  difference <- append(difference, (my_lambda-current_est))
}
results <- as.data.frame(cbind(size_range, estimations, difference))
plot(results$size_range, results$estimations, log="x", main="Estimation", xlab="Sample size", ylab="Estimate")
abline(h=my_lambda, col="cyan")
plot(results$size_range, results$difference, log="x", main="Estimation error", xlab="Sample size", ylab="Difference")
abline(h=0, col="cyan")
