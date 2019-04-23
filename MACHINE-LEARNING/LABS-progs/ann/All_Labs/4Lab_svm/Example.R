library(e1071)
area.pallete = function(n = 3)  
{    
  cols = rainbow(n)   
  cols[1:3] = c("PaleGreen", "PaleTurquoise", "Pink")    
  return(cols) 
}  
symbols.pallete = c("Green", "Blue", "Red")  
dataIris = iris[c("Petal.Width", "Petal.Length", "Species")]  
plot(Petal.Width ~ Petal.Length, dataIris, col = Species)  
set.seed(0) 
trainIdx = sample(nrow(dataIris), nrow(dataIris) / 2, replace = FALSE) 
dataIrisTrain = dataIris[trainIdx, ]  
dataIrisTrainObjects = dataIris[trainIdx, c("Petal.Width", "Petal.Length")]  
dataIrisTestObjects = dataIris[-trainIdx, c("Petal.Width", "Petal.Length")]  
svmModelLinear = svm(Species ~ ., data = dataIrisTrain, type = "C-classification", cost = 1, kernel = "linear")  
plot(svmModelLinear, dataIrisTrain, grid = 250, symbolPalette = symbols.pallete, color.palette = area.pallete)  
predictionsTrain = predict(svmModelLinear, dataIrisTrainObjects)  
table(dataIrisTrain$"Species", predictionsTrain)  

predictionsTest = predict(svmModelLinear, dataIrisTestObjects)  
table(dataIrisTest$"Species", predictionsTest) 

svmModelRBF = svm(Species ~ ., data = dataIrisTrain, type = "C-classification", cost = 1, kernel = "radial", gamma = 1)  
plot(svmModelRBF, dataIrisTrain, grid = 250, symbolPalette = symbols.pallete, color.palette = area.pallete) 
predictionsTrain = predict(svmModelLinear, dataIrisTrainObjects)  
table(dataIrisTrain$"Species", predictionsTrain) 

predictionsTest = predict(svmModelLinear, dataIrisTestObjects)  
table(dataIrisTest$"Species", predictionsTest) 