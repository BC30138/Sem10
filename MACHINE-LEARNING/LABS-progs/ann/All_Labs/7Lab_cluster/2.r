x1 = rnorm(100, mean = 200, sd = 60)
y1 = rnorm(100, mean = 10, sd = 10)

x2 = rnorm(100, mean = 10, sd = 20)
y2 = rnorm(100, mean = 400, sd = 200)

x3 = rnorm(100, mean = 200, sd = 50)
y3 = rnorm(100, mean = 800, sd = 10)

x = as.matrix(c(x1,x2, x3))
y = as.matrix(c(y1,y2, y3))

A <- cbind(x,y)
par(mfrow = c(1,4))
cl <- clara(A, 3, metric = c("manhattan"), stand = TRUE )
plot(A, col = cl$clustering, xlab = "x", ylab = "y")
title("manhattan, TRUE")

cl <- clara(A, 3, metric = c("manhattan"), stand = FALSE)
plot(A, col = cl$clustering, xlab = "x", ylab = "y")
title("manhattan, FALSE")

cl <- clara(A, 3, metric = c("euclidean"), stand = TRUE)
plot(A, col = cl$clustering, xlab = "x", ylab = "y")
title("euclidean, TRUE")

cl <- clara(A, 3, metric = c("euclidean"), stand = FALSE)
plot(A, col = cl$clustering, xlab = "x", ylab = "y")
title("euclidean, FALSE")
