library(e1071)

A_train <- read.table("svmdata3.txt", stringsAsFactors = TRUE)
A_trainObjects <- A_train[,-3]

area.pallete = function(n = 2)
{
  cols = rainbow(n)
  cols[1:2] = c("olivedrab3", "firebrick1")
  return(cols)
}

symbols.pallete = c("darkolivegreen", "darkred")

svmModelPoly = svm(Colors ~ ., data = A_train, type = "C-classification", cost = 1, kernel = "polynomial", degree = 8)
#plot(svmModelPoly, A_train, grid = 250, symbolPalette = symbols.pallete, color.palette = area.pallete)
predictionsTrain = predict(svmModelPoly, A_trainObjects)
table(A_train$"Colors", predictionsTrain)

svmModelRadial = svm(Colors ~ ., data = A_train, type = "C-classification", cost = 1, kernel = "radial")
plot(svmModelRadial, A_train, grid = 250, symbolPalette = symbols.pallete, color.palette = area.pallete)
predictionsTrain = predict(svmModelRadial, A_trainObjects)
table(A_train$"Colors", predictionsTrain)

svmModelSigmoid = svm(Colors ~ ., data = A_train, type = "C-classification", cost = 1, kernel = "sigmoid", gamma = 0.5)
plot(svmModelSigmoid, A_train, grid = 250, symbolPalette = symbols.pallete, color.palette = area.pallete)
predictionsTrain = predict(svmModelSigmoid, A_trainObjects)
table(A_train$"Colors", predictionsTrain)