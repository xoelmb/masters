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

gradient_descent <- function(f,x,delta){
    lambda <- 0.01
    while(lambda>delta){
        df <- grad(f,x,delta)
        x2 <- x - lambda * df
        if ((f(x2) >= f(x)) | is.nan(f(x2))){
            lambda <- lambda / 2
            next
        } else {
            x <- x2;
            lambda <- 1.1 * lambda
        }
    }
    return(x)
}

f1 <- function(x){x^2}
print(grad(f1,1,1e-6))

f2 <- function(x) {cos(log(x))}
x <- seq(0.01, 1, by=0.01)
plot(x, f2(x), col='red', pch=21)
print(sin(log(2))/2) # derivative by hand
print(grad(f2, 2, 1e-6))
print(gradient_descent(f2, 0.2, 1e-6))

f3 <- function(x){log(x[1]^2 + x[2]^2)}
print(grad(f3, c(1,1), 1e-6))

f4 <- function(x){x[1]^2 * x[2]^2}
print(grad(f4, c(1,1), 1e-6))
print(gradient_descent(f4, c(1,1), 1e-6))

f5 <- function(x){
    sin(sqrt(x[1]^2 + x[2]^2))
}
x <- seq(10,10,by=0.1)
y <- seq(10,10,by=0.1)


