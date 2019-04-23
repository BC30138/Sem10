#Как подобрать C, если на первом графике один точно окажется не в своем поле.

library(e1071)

A_train <- read.table("svmdata4.txt", stringsAsFactors = TRUE)
A_test <- read.table("svmdata4test.txt", stringsAsFactors = TRUE)
A_trainObjects <- A_train[,-3]
A_testObjects <- A_test[,-3]

area.pallete = function(n = 2)  
{    
  cols = rainbow(n)   
  cols[1:2] = c("olivedrab3", "firebrick1")   
  return(cols) 
} 

symbols.pallete = c("darkolivegreen", "darkred")

svmModelPoly = svm(Colors ~ ., data = A_train, type = "C-classification", cost = 1, kernel = "polynomial")  
#plot(svmModelPoly, A_test, grid = 250, symbolPalette = symbols.pallete, color.palette = area.pallete)  
predictionsTrain1 = predict(svmModelPoly, A_testObjects)  
table(A_test$"Colors", predictionsTrain1)  

svmModelRadial = svm(Colors ~ ., data = A_train, type = "C-classification", cost = 1, kernel = "radial")  
#plot(svmModelRadial, A_test, grid = 250, symbolPalette = symbols.pallete, color.palette = area.pallete)  
predictionsTrain2 = predict(svmModelRadial, A_testObjects)  
table(A_test$"Colors", predictionsTrain2)  

svmModelSigmoid = svm(Colors ~ ., data = A_train, type = "C-classification", cost = 1, kernel = "sigmoid")  
#plot(svmModelSigmoid, A_test, grid = 250, symbolPalette = symbols.pallete, color.palette = area.pallete)  
predictionsTrain3 = predict(svmModelSigmoid, A_testObjects)  
table(A_test$"Colors", predictionsTrain3) 