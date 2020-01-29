#' computes gradient of function f at point x
#'
#' @param f function from R^n -> R
#' @param x point in R^n
#' @param delta
grad <- function(f, x, delta){
    n <- length(x)
    f0 <- f(x)
    df <- vector("numeric", n)
    for (i in seq(1,n)){
        tmp <- x[i]
        x[i] <- x[i] + delta
        df[i] <- (f(x) - f0) / delta
        x[i] <- tmp
    }
    return(df)
}


#' gradient descent
#'
#' @param f
#' @param x
#' @param delta
gradient_descent <- function(f, x, delta){
    lambda <- 0.01
    while(lambda > delta){
        df <- grad(f,x,delta)
        x2 <- x - lambda * df
        if ((f(x2) >= f(x)) | is.nan(f(x2)) ){
            lambda <- lambda / 2
            next
        } else {
            x <- x2;
            lambda <- 1.1 * lambda
        }
        #cat(sprintf("descent:%.4f\t%.4f\n", x, lambda))
    }
    return(x)
}



tbl <- read.table("~/data/tbl-macro-tcell.txt.gz", as.is=TRUE, row.names=1)
print(dim(tbl))
tbl_bool <- (tbl > 0)
tbl_clean <- log10(tbl[rowSums(tbl_bool)> 10, ] + 1e-5)
print(dim(tbl_clean))

sigmoid <- function(x){
    return(exp(x) /(1 + exp(x)))
}



## 18 macrophages, 10 t cells
## data from blueprint project
y <- c(rep(0, 18), rep(1, 10))
m <- as.matrix(tbl_clean)

pval <- summary(fit)$coefficients[2,4]
i <- 1
fit       <- glm(y ~ t(m[i,,drop=FALSE]), family=binomial)
ypred <- predict(fit)
intercept <- summary(fit)$coefficients[1,1]
slope     <- summary(fit)$coefficients[2,1]
prob <- rep(NA,  28)
pred <- rep(0, 28)
for (j in seq(1, 28)){
    y <- intercept + slope * tbl_clean[i, j]
    cat(sigmoid(y), sigmoid(ypred[j]),"\n")
    print(sigmoid(y))
    prob[j] <- sigmoid(y)
    pred[j] <- (prob[j] >= 0.5)
}

png("boxplot-regression.png")
boxplot(prob[1:18],prob[19:28], border=c("blue","orange"))
stripchart(list(prob[1:18],prob[19:28]), add=TRUE,
           vertical=TRUE, pch=20, method="jitter")
dev.off()

tp <- sum( pred[19:28]==1 )
fp <- sum( pred[1:18] == 1 )
tn <- sum( pred[1:18]==0 )
fn <- sum( pred[19:28]==0 )

recall <- tp /(tp + fn)
precision <- tp /(tp +fp)

print(recall)
print(precision)


## now what happens if I use all the genes in the model

##y <- c(rep(0, 18), rep(1, 10))
##fitall <- glm(y ~ as.matrix(tbl_clean), family=binomial)

## plot precision-recall for 10 genes

a <- matrix(c(1, 2, 0, 7, 1, 5), nrow=2)
print(a %*% t(a))
print(t(a) %*% a)
as <- svd(a, nu=nrow(a), nv=ncol(a))
approx1 <- as$d[1] * as$u[,1,drop=FALSE] %*% as$v[1,,drop=FALSE]
approx2 <- as$d[1] * as$u[,1,drop=FALSE] %*% as$v[1,,drop=FALSE] + as$d[2] * as$u[,2,drop=FALSE] %*% as$v[2,,drop=FALSE]
print(approx1)
print(approx2)
print(norm(a - approx1, "F"))
m <- as.matrix(tbl_clean)
if (!exists("msvd")){
    msvd <- svd(m, nu=nrow(m), nv=ncol(m))
}

pc1 <- t(msvd$u[,1,drop=FALSE]) %*% m                                                                                                                
pc2 <- t(msvd$u[,2,drop=FALSE]) %*% m
plot(pc1[1:18], pc2[1:18], col="blue",
     xlim=c(min(pc1), max(pc1)), ylim=c(min(pc2), max(pc2)))
points(pc1[19:28], pc2[19:28], col="orange")         
