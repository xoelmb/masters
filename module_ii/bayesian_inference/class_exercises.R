#multiple plots, one row, two columns
par(mfrow=c(1,2), pch=20)

# binom dist in log scale
plot(0:10,log10(dbinom(x=0:10,size=10,prob=0.3)),
     type='h', lwd=2, col="dodgerblue", xlab="", ylab="log10(dbinom)")
# grid
grid(col="gray", lty="solid")

# plot binom non-log
plot(0:10,dbinom(x=0:10,size=10,prob=0.3),type='h',lwd=2,
     col="dodgerblue",ylab="dbinom", xlab="")
grid(col="gray", lty="solid")



dist=rbinom(0:100,size=100,prob=0.5)
plot(table(dist), type='h', lwd=2)
mean(dist)
var(dist)










#### beta distribution to infere theta from data
# This will compute the prob dist of beta, so it's the prob of beta having that value, I guess
x <- seq(0,1,by=0.01)
plot(x, dbeta(x,4,8))


x <- seq(0,1,by=0.01)
plot(x, dbeta(x,11,11))

plot(x, dbeta(x,26,26))
  


plot(x, dbeta(x,40,80))



## inferring lambda iteratively


logprobf1 <- function(data, l){
  logp <- dpois(data,lambda=l, log=TRUE)
  return(sum(logp))
}

data <- rpois(1000, lambda=50.5)
plot(density(data))
niter <- 1000
oldl <- runif(1, min=0, max=100)

x <- rep(NA, niter)
for (t in seq(1, niter)){
  newl <- runif(1, min=0, max=100)
  r <- exp(logprobf1(data, newl) -
             logprobf1(data, oldl))
  p <- min(r, 1)
  if (runif(1) < p){
    x[t] <- newl
  } else {
    x[t] <- oldl
  }
  oldl <- newl
}

oldl














