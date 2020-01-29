tbl <- read.table("./tbl-macro-tcell.txt", as.is=TRUE, row.names=1)
# print(dim(tbl))
head(tbl)
#We have rows that have 0 values. All the genes are completely off or their expression is too low to detect.
# The rows are the genes, and the samples are the columns. First ten are one cell type, and the rest are the other one.
# We convert the table to a boolean table:
tbl_bool <- (tbl > 0)
# We want only the genes which are expressed in at least 10 samples.
tbl_clean <- log10(tbl[rowSums(tbl_bool)> 10, ] + 1e-5)
# The logarithm makes life easier. If you take the logarithm, the values will be closer to each other. 1e-5 will allow
# us to not compute the log of 0s.
# print(dim(tbl_clean))
# plot(1:28,tbl_clean[1,1:28]) # plot(as.numeric(tbl_clean[1,])

#The sigmoid function
sigmoid <- function(x){
    return(exp(x) / (1 + exp(x)))
}

x <- seq(-5,5,by=0.1)
# plot(x,sigmoid(x))


y <- c(rep(0,18), rep(1,10))
m <- as.matrix(tbl_clean)
i <- 1
fit <- glm(y ~ t(m[i,,drop=FALSE]), family=binomial)
pval <- summary(fit)$coefficients[2,4]
ypred <- predict(fit)
intercept <- summary(fit)$coefficients[1,1]
slope <- summary(fit)$coefficients[2,1]

# Code below is a by hand predict function
prob <- rep(NA, 28)
pred <- rep(0,28)
for (j in seq(1,28)){
    y <- intercept + slope * tbl_clean[i,j]
    # cat(sigmoid(y),sigmoid(ypred[j]), "\n")
    prob[j] <- sigmoid(y)
    pred[j] <- (prob[j] >= 0.5)
}

# boxplot(prob[1:18],prob[19:28], border=c("blue", "orange"))
# stripchart(list(prob[1:18],prob[19:28]), add=TRUE, vertical=TRUE, pch=20, method="jitter")


tp <- sum( pred[19:28]==1 )
fp <- sum( pred[1:18] == 1 )
tn <- sum( pred[1:18]==0 )
fn <- sum( pred[19:28]==0 )

recall <- tp /(tp + fn)
precision <- tp /(tp +fp)
#
# print(recall)
# print(precision)

######################################exercises
for (i in seq(1,100)){
    y <- c(rep(0,18), rep(1,10))
    fit <- glm(y ~ t(m[i,,drop=FALSE]), family=binomial)
    pval <- summary(fit)$coefficients[2,4]
    ypred <- predict(fit)
    intercept <- summary(fit)$coefficients[1,1]
    slope <- summary(fit)$coefficients[2,1]
    # Code below is a by hand predict function
    prob <- rep(NA, 28)
    pred <- rep(0,28)
    for (j in seq(1,28)){
        y <- intercept + slope * tbl_clean[i,j]
        prob[j] <- sigmoid(y)
        pred[j] <- (prob[j] >= 0.5)
    }

    tp <- sum( pred[19:28]==1 )
    fp <- sum( pred[1:18] == 1 )
    tn <- sum( pred[1:18]==0 )
    fn <- sum( pred[19:28]==0 )

    recall <- tp /(tp + fn)
    precision <- tp /(tp +fp)

    # cat('\n',rownames(tbl_clean)[i], precision, recall)
}




### hard stuff

a <- matrix(c(1, 2, 0, 7, 1, 5), nrow=2)
print(a %*% t(a))
print(t(a) %*% a)
as <- svd(a, nu=nrow(a), nv=ncol(a))
approx1 <- as$d[1] * as$u[,1,drop=FALSE] %*% as$v[1,,drop=FALSE]
approx2 <- as$d[1] * as$u[,1,drop=FALSE] %*% as$v[1,,drop=FALSE] + as$d[2] * as$u[,2,drop=FALSE] %*% as$v[2,,drop=FALSE]

msvd <- svd(m, nu=nrow(m), nv=ncol(m))

pc1 <- t(msvd$u[,1,drop=FALSE]) %*% m
pc2 <- t(msvd$u[,2,drop=FALSE]) %*% m
plot(pc1[1:18], pc2[1:18], col="blue",
     xlim=c(min(pc1), max(pc1)), ylim=c(min(pc2), max(pc2)))
points(pc1[19:28], pc2[19:28], col="orange")
