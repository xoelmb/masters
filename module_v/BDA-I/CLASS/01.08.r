v <- runif(10)
#print(v)
#plot(v)

v <- c(1,2,3)
v <- log(c(1,2,3))
#print(v)

m <- matrix(runif(10), nrow=5)
#print(m)
#image(m)

m1 <- matrix(c(1,2,3,4), nrow=2)
m2 <- matrix(c(5,6,7,8), nrow=2)
#print(m1+m2)
#print(m1*m2)
#print(m1-m2)
#print(m1%*%m2)

v1 <- c(1,2)
v2 <- c(1,2,3)
#print(v1+v2)

m3 <- matrix(c(1,2), nrow=2)
m4 <- matrix(c(1,0,0,1), nrow=2)
#print(m4%*%m3)

m5 <- matrix(c(1,2,3), nrow=1)
m6 <- matrix(c(1,2,3), nrow=3)
#print(m5%*%m6)

m7 <- matrix(c(1,2,3,4), nrow=2)
#print(t(m7))


# this is the squared length or dot product of a vector.
# It's also called the projection of one vector over another one.
# print(m5%*%t(m5))


m8 <- matrix(c(2,1,3,0), nrow=2)
m9 <- matrix(c(1,2,0,7,1,5), nrow=2)
#print(m8%*%m9)

# Inverse of a matrix times the matrix will return an identity matrix.
# Not all matrices are invertible
# If the matrix is invertible, solve function will return the inverse:
m10 <- matrix(c(1,0,0,2,1,0,-1,-1,-1), nrow=3)
# print(solve(m10))
# print(solve(m10)%*%m10)
# print(m10%*%solve(m10))

# Finding eigenvalue/vector
m11 <- matrix(c(1,2,-1,4), nrow=2)
l <- eigen(m11)
print(m11%*%l$vectors)
# The result is the eigenvector columns multiplied by the eigenvalues. Each of the columns of the eigenvectors are one
# eigenvector that correspond to each of the eigenvalues. Each eigenvector-eigenvalue is a solution that satisfies the
# condition A*v = lambda*v