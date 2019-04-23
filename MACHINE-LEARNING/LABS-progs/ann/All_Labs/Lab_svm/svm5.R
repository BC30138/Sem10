#В чем заключается переобучение?

library(e1071)

A_train <- read.table("svmdata5.txt", stringsAsFactors = TRUE)
A_test <- read.table("svmdata5test.txt", stringsAsFactors = TRUE)
A_trainObjects <- A_train[,-3]
A_testObjects <- A_test[,-3]

area.pallete = function(n = 2)  
{    
  cols = rainbow(n)   
  cols[1:2] = c("PaleGreen", "Pink")    
  return(cols) 
} 

symbols.pallete = c("Green", "Red")  

svmModelPoly = svm(Colors ~ ., data = A_train, type = "C-classification", cost = 1, kernel = "polynomial", gamma = 30)  
#plot(svmModelPoly, A_test, grid = 250, symbolPalette = symbols.pallete, color.palette = area.pallete)  
predictionsTrain1 = predict(svmModelPoly, A_testObjects)  
table(A_test$"Colors", predictionsTrain1)  

svmModelRadial = svm(Colors ~ ., data = A_train, type = "C-classification", cost = 1, kernel = "radial", gamma = 40)  
#plot(svmModelRadial, A_test, grid = 250, symbolPalette = symbols.pallete, color.palette = area.pallete)  
predictionsTrain2 = predict(svmModelRadial, A_testObjects)  
table(A_test$"Colors", predictionsTrain2)  

svmModelSigmoid = svm(Colors ~ ., data = A_train, type = "C-classification", cost = 1, kernel = "sigmoid")  
#plot(svmModelSigmoid, A_test, grid = 250, symbolPalette = symbols.pallete, color.palette = area.pallete)  
predictionsTrain3 = predict(svmModelSigmoid, A_testObjects)  
table(A_test$"Colors", predictionsTrain3) 