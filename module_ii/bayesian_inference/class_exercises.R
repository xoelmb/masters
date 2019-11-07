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
