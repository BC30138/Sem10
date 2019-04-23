library(kernlab)
library(kknn)

calculate <- function(x, initial_selection, n, repeats) {
  funcList <- list()
  for (rep in 1:repeats){
    initial_selection <- initial_selection[ order(runif(n)), ]
    idx <- sample(1:n, n*x)
    A_train <- initial_selection[idx, ]
    A_test <- initial_selection[-idx, ]
    model <- kknn(type~., A_train, A_test, k = floor(sqrt(dim(A_train)[1])), kernel = "optimal")
    myTable <- table(fitted(model), A_test$type)
    funcList[rep] <- (myTable[2] + myTable[3]) / sum(myTable)
  }
  return(Reduce("+", funcList)/repeats)
}

data(spam)
#spam[0:1,]
n <- dim(spam)[1]
x <- seq(0.5, 0.9, 0.05)
num <- length(x)
resList <- list()
for (i in 1:num){
  resList[i] <- calculate(x[i], spam, n, 5)
}

plot(x, resList,
     type = "b",
     xlab = "Volume of training sample, %",
     ylab = "Error value")

