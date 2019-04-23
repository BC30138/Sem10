library(e1071)

calculate <- function(x, initial_selection, n, repeats) {
  funcList <- list()
  for (rep in 1:repeats){
    initial_selection <- initial_selection[ order(runif(n)), ]
    idx <- sample(1:n, n*x)
    A_train <- initial_selection[idx, ]
    A_test <- initial_selection[-idx, ]
    model <- naiveBayes(V10 ~ ., data = A_train)
    myTable <- table(predict(model, A_test), A_test$V10)
    funcList[rep] <- (myTable[2] + myTable[3]) / sum(myTable)
  }
  return(Reduce("+", funcList)/repeats)
}

A_raw <- read.table("C:/Users/anna_fox/Documents/UNIVERSE/4 курс/2 semester/Нейронные_сети/All_Labs/1Lab/Tic_tac_toe.txt", sep = ",", stringsAsFactors = TRUE)
n <- dim(A_raw)[1]
lengthOfSelection <- dim(A_raw)[1]

x <- seq(0.5, 0.9, 0.05)
num <- length(x)
resList <- list()

for (i in 1:num) {
  resList[i] <- calculate(x[i], A_raw, lengthOfSelection,5)
}

plot(x, resList,
     type = "b",
     xlab = "Volume of training sample, %",
     ylab = "Error value")



