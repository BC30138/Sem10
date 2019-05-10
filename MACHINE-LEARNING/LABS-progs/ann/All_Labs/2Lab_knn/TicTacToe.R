library(kknn)

calculate <- function(x, initial_selection, n, repeats) {
  funcList <- list()
  for (rep in 1:repeats){
    initial_selection <- initial_selection[ order(runif(n)), ]
    idx <- sample(1:n, n*x)
    A_train <- initial_selection[idx, ]
    A_test <- initial_selection[-idx, ]
    model <- kknn(V10~., A_train, A_test, k = 25, kerne0l = "optimal")
    myTable <- table(fitted(model), A_test$V10)
    funcList[rep] <- (myTable[2] + myTable[3]) / sum(myTable)
  }
  return(Reduce("+", funcList)/repeats)
}

A_raw <- read.table("C:/Users/anna_fox/Documents/UNIVERSE/4 ����/2 semester/���������_����/All_Labs/1Lab/Tic_tac_toe.txt", sep = ",", stringsAsFactors = TRUE)
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



