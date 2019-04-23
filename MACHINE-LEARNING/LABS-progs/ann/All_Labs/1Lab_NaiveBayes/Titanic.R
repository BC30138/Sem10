
library(e1071)

A_train <- read.csv("C:/Users/anna_fox/Documents/UNIVERSE/4 курс/2 semester/Нейронные_сети/All_Labs/1Lab/train.csv", stringsAsFactors = TRUE)
A_test <- read.csv("C:/Users/anna_fox/Documents/UNIVERSE/4 курс/2 semester/Нейронные_сети/All_Labs/1Lab/test.csv", stringsAsFactors = TRUE)
A_check <- read.csv("C:/Users/anna_fox/Documents/UNIVERSE/4 курс/2 semester/Нейронные_сети/All_Labs/1Lab/gender_submission.csv", stringsAsFactors = TRUE)

A_classifier <- naiveBayes(A_train[,-2], as.factor(A_train$Survived))
A_predicted <- predict(A_classifier, A_test)

myTable <- table(A_predicted, A_check$Survived)
myTable
(myTable[2] + myTable[3])/(dim(A_test)[1])
