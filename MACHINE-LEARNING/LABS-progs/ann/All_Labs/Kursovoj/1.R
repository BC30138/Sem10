library(e1071)
library(adabag)
library(rpart) 
library(Rtsne)
library(cluster)
library(glmnet)
library(autoencoder)

SourceData <- read.csv("C:/Users/anna_fox/Documents/UNIVERSE/4 курс/2 semester/Нейронные_сети/All_Labs/Kursovoj/Indian Liver Patient Dataset (ILPD).csv",stringsAsFactors = TRUE)

findErrorValues <- function(x, initialSelection, n, method) {
    idx <- sample(1:n, n*x)
    train <- initialSelection[idx, ]
    testCheck <- initialSelection[-idx, ]
    test <- testCheck[,-10]
    if (method == "svm") {
      svmModelLinear <- svm(Select ~ ., data = train, type = "C-classification", cost = 1, kernel = "linear")  
      predictions <- predict(svmModelLinear, test)  
      myTable <- table(testCheck$"Select", predictions) 
      return(myTable[2] + myTable[3]) / sum(myTable)
    }
    else if (method == "bagging"){
      train$Select <- as.factor(train$Select)
      baggingModel <- bagging(Select ~.,data = train, mfinal = 10, maxdepth = 5)
      predictions <- predict.bagging(baggingModel, newdata = testCheck)  
      return(predictions$error)
    }
    else{
      train$Select <- as.factor(train$Select)
      boostingModel <- boosting(Select ~.,data = train, mfinal = 10, maxdepth = 5)
      predictions <- predict.boosting(boostingModel, newdata = testCheck)  
      return(predictions$error)
    }
}

getBestKernel <- function(train, testCheck, kernels){
  test <- testCheck[,-10]
  errorList <- list()
  for (i in 1:length(kernels)){
    svmModelLinear <- svm(Select ~ ., data = train, type = "C-classification", cost = 1, kernel = kernels[i])  
    predictions <- predict(svmModelLinear, test)  
    myTable <- table(testCheck$"Select", predictions) 
    errorList[i] <- (myTable[2] + myTable[3]) / sum(myTable)
  }
  return(kernels[unlist(which.min(errorList))])
}

getBestMFinalBagging <- function(train,test,mfinal){
  resList <- list()
  for (i in 1:length(mfinal)) {
    model <- bagging(Select ~.,data = train, mfinal = mfinal[i], maxdepth = 5)
    predictions <- predict.bagging(model, newdata = test)  
    resList[i] <- predictions$error 
  }
  return(resList)
}

getBestMFinalBoosting <- function(train,test,mfinal){
  resList <- list()
  for (i in 1:length(mfinal)) {
    model <- boosting(Select ~.,data = train, mfinal = mfinal[i], maxdepth = 5)
    predictions <- predict.boosting(model, newdata = test)  
    resList[i] <- predictions$error 
  }
  return(resList)
}
############################################################################################
##SVM
############################################################################################

SourceData <- SourceData[,-10]
n <- dim(SourceData)[1]
x <- seq(0.5, 0.9, 0.05)
num <- length(x)
errorValues <- list()
for (i in 1:num) {
  errorValues[i] <- findErrorValues(x[i], SourceData, n, "svm")
}

#График зависимости ошибки от размера обучающей выборки
plot(x, errorValues,
    xlab = "Volume of training sample, %",
    ylab = "Error value")

#Нашли разбиение с наименьшей ошибкой (доля обучающей выборки)
split <- x[unlist(which.min(errorValues))]
idx <- sample(1:n, n*split)
trainDataSvm <- SourceData[idx, ]
testDataSvm <- SourceData[-idx, ]

############################################################################################
##Visual
############################################################################################
train_data <- unique(trainDataSvm)
train_data$Sex <- as.numeric(as.factor(train_data$Sex))
tsne <- Rtsne(as.matrix(train_data))
plot(tsne$Y,pch = 22, bg = c("blue","yellow"))
############################################################################################
##Visual
############################################################################################

#Нашли ядро с наименьшей ошибкой
kernel <- getBestKernel(trainDataSvm,testDataSvm,c("linear","radial","sigmoid","polynomial"))

svmModelLinear <- svm(Select ~ ., data = trainDataSvm, type = "C-classification", cost = 1, kernel = kernel)  
predictions <- predict(svmModelLinear, testDataSvm[,-10])  
myTable <- table(testData$"Select", predictions) 
errSvm <- (myTable[2] + myTable[3]) / sum(myTable)


############################################################################################
##BAGGING
############################################################################################
errorValues <- list()
for (i in 1:num) {
  errorValues[i] <- findErrorValues(x[i], SourceData, n, "bagging")
}

#График зависимости ошибки от размера обучающей выборки
plot(x, errorValues,
     xlab = "Volume of training sample, %",
     ylab = "Error value")

#Нашли разбиение с наименьшей ошибкой (доля обучающей выборки)
split <- x[unlist(which.min(errorValues))]
idx <- sample(1:n, n*split)
trainDataBagging <- SourceData[idx, ]
testDataBagging <- SourceData[-idx, ]

mfinal <- seq(1,6,5)
trainDataBagging$Select <- as.factor(trainDataBagging$Select)
resList <- getBestMFinalBagging(trainDataBagging,testDataBagging,mfinal)

plot(mfinal,resList,    
     col = "red",
     xlab = "Number of trees",
     ylab = "Classification error")

#Нашли количество деревьев с наименьшей ошибкой
treeNumberBag <- mfinal[unlist(which.min(resList))]

baggingModel <- bagging(Select ~.,data = trainDataBagging, mfinal = treeNumberBag, maxdepth = 5)
predictions <- predict.bagging(baggingModel, newdata = testDataBagging)  
errBagging <- predictions$error

############################################################################################
##BOOSTING
############################################################################################
errorValues <- list()
for (i in 1:num) {
  errorValues[i] <- findErrorValues(x[i], SourceData, n, "boosting")
}

#График зависимости ошибки от размера обучающей выборки
plot(x, errorValues,
     xlab = "Volume of training sample, %",
     ylab = "Error value")

#Нашли разбиение с наименьшей ошибкой (доля обучающей выборки)
split <- x[unlist(which.min(errorValues))]
idx <- sample(1:n, n*split)
trainDataBoosting <- SourceData[idx, ]
testDataBoosting <- SourceData[-idx, ]

trainDataBoosting$Select <- as.factor(trainDataBoosting$Select)
resList <- getBestMFinalBoosting(trainDataBoosting,testDataBoosting,mfinal)

plot(mfinal,resList,    
     col = "red",
     xlab = "Number of trees",
     ylab = "Classification error")

#Нашли количество деревьев с наименьшей ошибкой
treeNumberBoost <- mfinal[unlist(which.min(resList))]

boostingModel <- boosting(Select ~.,data = trainDataBoosting, mfinal = treeNumberBoost, maxdepth = 5)
predictions <- predict.boosting(boostingModel, newdata = testDataBoosting)  
errBoosting <- predictions$error

############################################################################################
##CLUSTER
############################################################################################
cl <- clara(SourceData[,-10], 2,metric = c("euclidean"))
t <- table(cl$clustering,SourceData$Select)
errClara <- sum(diag(t))/sum(t)
plot(cl)

data <- SourceData
data$Sex <- as.numeric(as.factor(data$Sex))
kkk <- kmeans(data[,-10],2,iter.max = 10)
t <- table(kkk$cluster,SourceData$Select)
errKMeans <- sum(diag(t))/sum(t)
 
dendogramma <- agnes(SourceData)
plot(dendogramma)

############################################################################################
##LASSO
############################################################################################
x <- as.matrix(data[,-10])
y <- data[,10]
glm = glmnet(x, y, family = "binomial", alpha = 1)
lassoResult <- as.matrix(glm$beta)

############################################################################################
##AUTOENCODER 
############################################################################################

testData$Sex <- as.numeric(as.factor(testData$Sex))
trainData$Sex <- as.numeric(as.factor(trainData$Sex))
encoder <- autoencode(as.matrix(data[,-10]),
                         N.hidden = 20,
                         epsilon = 0,
                         lambda = 0.0002,
                         beta = 6,
                         rho = 0.9,
                         unit.type = "tanh",
                         rescale.flag = TRUE)

predictions <- predict.autoencoder(encoder,as.matrix(data[,-10]),hidden.output = TRUE)
predFrame <- as.data.frame(predictions$X.output)
autoEncodedData <- tibble::add_column(predFrame,data$Select)

tsne <- Rtsne(as.matrix(unique(autoEncodedData)),perplexity = 20)
plot(tsne$Y,pch = 22, bg = c("blue","yellow"))

#Поменяли имя колонки (класс)
colnames(autoEncodedData)[which(names(autoEncodedData) == "data$Select")] <- "Select"
autoEncodedData$Select <- as.factor(autoEncodedData$Select)

#Разбили выборку на обучающую и тестирующую
idx <- sample(1:n, n*split)
trainData <- autoEncodedData[idx, ]
testData <- autoEncodedData[-idx, ]

#BAGGING
baggingModel <- bagging(Select ~.,data = trainData, mfinal = treeNumberBag, maxdepth = 5)
predictions <- predict.bagging(baggingModel, newdata = testData)  
errBagging2 <- predictions$error

#BOOSTING
boostingModel <- boosting(Select ~.,data = trainData, mfinal = treeNumberBoost, maxdepth = 5)
predictions <- predict.boosting(boostingModel, newdata = testData)  
errBoosting2 <- predictions$error

#SVM
svmModelLinear <- svm(Select ~ ., data = trainData, type = "C-classification", cost = 1, kernel = kernel)  
predictions <- predict(svmModelLinear, testData[,-21])  
myTable <- table(testData$"Select", predictions) 
errSvm <- (myTable[2] + myTable[3]) / sum(myTable)


############################################################################################
##AUTOENCODER
############################################################################################

testData$Sex <- as.numeric(as.factor(testData$Sex))
trainData$Sex <- as.numeric(as.factor(trainData$Sex))
encoder <- autoencode(as.matrix(data[,-10]),
                      N.hidden = 5,
                      epsilon = 0,
                      lambda = 0.0002,
                      beta = 6,
                      rho = 0.9,
                      unit.type = "tanh",
                      rescale.flag = TRUE)

predictions <- predict.autoencoder(encoder,as.matrix(data[,-10]),hidden.output = TRUE)
predFrame <- as.data.frame(predictions$X.output)
autoEncodedData <- tibble::add_column(predFrame,data$Select)

#Поменяли имя колонки (класс)
colnames(autoEncodedData)[which(names(autoEncodedData) == "data$Select")] <- "Select"
autoEncodedData$Select <- as.factor(autoEncodedData$Select)

#Разбили выборку на обучающую и тестирующую
idx <- sample(1:n, n*split)
trainData <- autoEncodedData[idx, ]
testData <- autoEncodedData[-idx, ]

#BAGGING
baggingModel <- bagging(Select ~.,data = trainData, mfinal = treeNumberBag, maxdepth = 5)
predictions <- predict.bagging(baggingModel, newdata = testData)  
errBagging3 <- predictions$error

#BOOSTING
boostingModel <- boosting(Select ~.,data = trainData, mfinal = treeNumberBoost, maxdepth = 5)
predictions <- predict.boosting(boostingModel, newdata = testData)  
errBoosting3 <- predictions$error

#SVM
svmModelLinear <- svm(Select ~ ., data = trainData, type = "C-classification", cost = 1, kernel = kernel)  
predictions <- predict(svmModelLinear, testData[,-21])  
myTable <- table(testData$"Select", predictions) 
errSvm3 <- (myTable[2] + myTable[3]) / sum(myTable)

############################################################################################
##AUTOENCODER
############################################################################################
testData$Sex <- as.numeric(as.factor(testData$Sex))
trainData$Sex <- as.numeric(as.factor(trainData$Sex))
encoder <- autoencode(as.matrix(data[,-10]),
                      N.hidden = 20,
                      epsilon = 0.5,
                      lambda = 0.0002,
                      beta = 6,
                      rho = 0.9,
                      unit.type = "tanh",
                      rescale.flag = TRUE)

predictions <- predict.autoencoder(encoder,as.matrix(data[,-10]),hidden.output = TRUE)
predFrame <- as.data.frame(predictions$X.output)
autoEncodedData <- tibble::add_column(predFrame,data$Select)

#Поменяли имя колонки (класс)
colnames(autoEncodedData)[which(names(autoEncodedData) == "data$Select")] <- "Select"
autoEncodedData$Select <- as.factor(autoEncodedData$Select)

#Разбили выборку на обучающую и тестирующую
idx <- sample(1:n, n*split)
trainData <- autoEncodedData[idx, ]
testData <- autoEncodedData[-idx, ]

#BAGGING
baggingModel <- bagging(Select ~.,data = trainData, mfinal = treeNumberBag, maxdepth = 5)
predictions <- predict.bagging(baggingModel, newdata = testData)  
errBagging4 <- predictions$error

#BOOSTING
boostingModel <- boosting(Select ~.,data = trainData, mfinal = treeNumberBoost, maxdepth = 5)
predictions <- predict.boosting(boostingModel, newdata = testData)  
errBoosting4 <- predictions$error

#SVM
svmModelLinear <- svm(Select ~ ., data = trainData, type = "C-classification", cost = 1, kernel = kernel)  
predictions <- predict(svmModelLinear, testData[,-21])  
myTable <- table(testData$"Select", predictions) 
errSvm4 <- (myTable[2] + myTable[3]) / sum(myTable)
