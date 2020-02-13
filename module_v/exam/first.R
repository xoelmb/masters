# first <- matrix(c(1,-1), nrow=2)
# second <- matrix(c(1,1), nrow=2)
# matr <-matrix(c(1,3,3,1), ncol=2)
# eigens <- eigen(matr)
# print(eigens)
# print(matr%*%second)
# print(eigens$values[1]*second)
#
# print(matr%*%first)
# print(eigens$values[2]*first)

func <- function(x){
  return(x[1]^2+(x[2]-1)^2)
}

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

test_point <- c(1,1)
delta <- 1e-06
print(grad(func, test_point, delta))

# gradient_descent <- function(f, x, delta){
#     lambda <- 0.01
#     while(lambda > delta){
#         df <- grad(f,x,delta)
#         x2 <- x - lambda * df
#         if ((f(x2) >= f(x)) | is.nan(f(x2)) ){
#             lambda <- lambda / 2
#             next
#         } else {
#             x <- x2;
#             lambda <- 1.1 * lambda
#         }
#     }
#     return(x)
# }
#
#
# gradient_descent(func, test_point, delta)