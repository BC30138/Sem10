library(e1071)

n <- 50
n2 <- 100

#generate 2 vectors with given parameters
X1 <- c(rnorm(n, 10, 4), rnorm(n, 20, 3))
X2 <- c(rnorm(n, 14, 4), rnorm(n, 18, 3))

#union 2 vectors and add labels
unionDate <- data.frame(X1, X2, label = c(rep(-1, n), rep(1, n)))

#randomize the set
A_rand <- unionDate[ order(runif(n2)), ]
nt <- as.integer(n2*0.8)
A_train <- A_rand[1:nt, ]
A_test <- A_rand[(nt + 1):(n2), ]

A_classifier <- naiveBayes(A_train[,-3], as.factor(A_train$label))
A_predicted <- predict(A_classifier, A_test)

myTable <- table(A_predicted, A_test$label)
print(myTable)

plot(unionDate$X1, unionDate$X2,
     col = ifelse(unionDate$label == -1, "magenta", "green"),
     xlab = "X1", ylab = "X2")
