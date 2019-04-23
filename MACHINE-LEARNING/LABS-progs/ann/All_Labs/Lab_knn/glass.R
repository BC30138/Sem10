library(kknn)

data(glass)
myGlass <- glass[,-1]
n <- dim(myGlass)[1]
A_rand <- myGlass[ order(runif(n)), ]
nt <- as.integer(n*0.9)
glassTrain <- A_rand[1:nt, ]
glassTest <- A_rand[(nt+1):n, ]
sizeOfTrain <- dim(glassTrain)[1]

example <- data.frame("RI" = 1.516,"Na" = 11.7, "Mg" = 1.01, "Al" = 1.19, "Si" = 72.59, "K" = 0.43,"Ca" = 11.44, "Ba" = 0.02, "Fe" = 0.1, "Type" = "")
perem <- kknn(Type~., glassTrain, example)
print(fitted(perem))

train1 <- train.kknn(Type ~ ., glassTrain, kmax = floor(sqrt(sizeOfTrain) + 10),kernel = c("triangular", "rectangular", "epanechnikov", "optimal"), distance = 1)
train2 <- train.kknn(Type ~ ., glassTrain, kmax = floor(sqrt(sizeOfTrain) + 10),kernel = c("triangular", "rectangular", "epanechnikov", "optimal"), distance = 2)

print(train1)
print(train2)

par(mfrow = c(1, 2))
plot(train1, type = "b", main = "distance = 1")
plot(train2, type = "b", main = "distance = 2")

resList <- list()
for (i in 1:9) {
  glassTrainWithoutParam <- glassTrain[, -1*i]
  glassTestWithoutParam <- glassTest[, -1*i]
  print(glassTestWithoutParam)
  perem <- kknn(Type~., glassTrainWithoutParam, glassTestWithoutParam)
  myTable <- table(fitted(perem), glassTestWithoutParam$Type)
  resList[i] <- (myTable[1,1] + myTable[2,2] + myTable[3,3] + myTable[4,4] + myTable[5,5] + myTable[6,6]) / sum(myTable)   
}

plot(1:9, resList, type = "b",
     xlab = "Excluded class",
     ylab = "Success probability")




