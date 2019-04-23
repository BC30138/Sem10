library(e1071)

A_train <- read.table("svmdata6.txt", stringsAsFactors = TRUE)
x = A_train$X
y = A_train$Y  
plot(x, y)  
svmModel = svm(x, y, type = "eps-regression", eps = 0.25, cost = 1, kernel = "radial")  
points(x[svmModel$index], y[svmModel$index], col = "red")  
predctions = predict(svmModel, x) 
lines(x, predctions, col = "deeppink4", lwd = 2)  
lines(x, predctions + svmModel$epsilon, col = "gold2")  
lines(x, predctions - svmModel$epsilon, col = "gold2") 