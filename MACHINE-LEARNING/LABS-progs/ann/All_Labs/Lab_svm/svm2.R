#��� ��������� C, ���� �� ������ ������� ���� ����� �������� �� � ����� ����.

library(e1071)

A_train <- read.table("C:/Users/anna_fox/Documents/UNIVERSE/4 ����/2 semester/���������_����/All_Labs/4Lab_svm/svmdata2.txt", stringsAsFactors = TRUE)
A_test <- read.table("C:/Users/anna_fox/Documents/UNIVERSE/4 ����/2 semester/���������_����/All_Labs/4Lab_svm/svmdata2test.txt", stringsAsFactors = TRUE)
A_trainObjects <- A_train[,-3]
A_testObjects <- A_test[,-3]

area.pallete = function(n = 2)  
{    
  cols = rainbow(n)   
  cols[1:2] = c("olivedrab3", "firebrick1")      
  return(cols) 
} 

symbols.pallete = c("darkolivegreen", "darkred")   

svmModelLinear = svm(Colors ~ ., data = A_train, type = "C-classification", cost = 1, kernel = "linear")  
#plot(svmModelLinear, A_train, grid = 250, symbolPalette = symbols.pallete, color.palette = area.pallete)  
predictionsTrain = predict(svmModelLinear, A_trainObjects)  
table(A_train$"Colors", predictionsTrain)  

plot(svmModelLinear, A_test, grid = 250, symbolPalette = symbols.pallete, color.palette = area.pallete)  
predictionsTrain2 = predict(svmModelLinear, A_testObjects)  
table(A_test$"Colors", predictionsTrain2) 