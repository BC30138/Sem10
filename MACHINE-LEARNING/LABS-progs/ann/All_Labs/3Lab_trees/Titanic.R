
library(tree)
library(maptree)
library(mlbench)

A_trai <- read.csv("train.csv", sep = ",", stringsAsFactors = TRUE)
A_test <- read.csv("test.csv", sep = ",", stringsAsFactors = TRUE)
A_RealDateForTest <- read.csv("gender_submission.csv", sep = ",", stringsAsFactors = TRUE)

A_train <- A_trai[, -1]
A_train$Name <- NULL
A_train$Ticket <- NULL
#A_train$Cabin <- NULL

surv.tr <- tree(Survived ~., A_train)
draw.tree(surv.tr, cex = 0.7)

pred <- predict(surv.tr, A_test)

n <- dim(A_test)[1]
res <- list()

#для проверки, какой результат определился в pred, проверяем, больше ли значение 0.5 (выжил) или нет
for (i in 1:n) {
  if (pred[i] >= 0.5) {
    res[i] <- 1
  } 
  else {
    res[i] <- 0
  }
}

#проверяем, совпали ли предполагаемые выжившие с реальными
trueElements <- 0

for (i in 1:n) {
  if (A_RealDateForTest$Survived[i] != res[i]) {
    trueElements <- trueElements + 1
  }
}

final <- trueElements/n