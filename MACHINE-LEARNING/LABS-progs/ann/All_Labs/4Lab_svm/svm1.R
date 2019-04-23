library(e1071)

A_train <- read.table("svmdata1.txt", stringsAsFactors = TRUE)
A_test <- read.table("svmdata1test.txt", stringsAsFactors = TRUE)
A_trainObjects <- A_train[,-3]
A_testObjects <- A_test[,-3]

area.pallete = function(n = 2)  
{    
  cols = rainbow(n)   
  cols[1:2] = c("olivedrab3", "firebrick1")    
  return(cols) 
} 

symbols.pallete = c("darkolivegreen", "darkred")  

svmModelLinear = svm(Color ~ ., data = A_train, type = "C-classification", cost = 1, kernel = "linear")  

plot(svmModelLinear, A_train, symbolPalette = symbols.pallete, color.palette = area.pallete)  
predictionsTrain1 = predict(svmModelLinear, A_trainObjects)  
table(A_train$"Color", predictionsTrain1) 

plot(svmModelLinear, A_test, symbolPalette = symbols.pallete, color.palette = area.pallete)  
predictionsTrain2 = predict(svmModelLinear, A_testObjects)  
table(A_test$"Color", predictionsTrain2) 