library(kernlab)
library(e1071)

myFunc <- function(x, initial_selection, n, repeats) {
  funcList <- list()
  for (rep in 1:repeats) {
    idx <- sample(1:n, n*x)
    spamtrain <- initial_selection[idx, ]
    spamtest <- initial_selection[-idx, ]
    model <- naiveBayes(type ~ ., data = spamtrain)
    myTable <- table(predict(model, spamtest), spamtest$type)
    print(myTable)
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
  resList[i] <- myFunc(x[i], spam, n, 5)
}

plot(x, resList,
     type = "b",
     xlab = "Volume of training sample, %",
     ylab = "Error value")

