library(kknn)

data(glass)
myGlass <- glass[,-1]
n <- dim(myGlass)[1]
A_rand <- myGlass[ order(runif(n)), ]
nt <- as.integer(n*0.9)
glassTrain <- A_rand[1:nt, ]
glassTest <- A_rand[(nt+1):n, ]
sizeOfTrain <- dim(glassTrain)[1]

model <- kknn(Type ~ ., glassTrain, glassTest, k = 22,kernel = "triangular", distance = 1)

myTable <- table(fitted(model), glassTest$Type)
funcList <- (myTable[2] + myTable[3]) / sum(myTable)

myTable



