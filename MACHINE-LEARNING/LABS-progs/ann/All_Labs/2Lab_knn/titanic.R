library(kknn)

A_train <- read.csv("C:/Users/anna_fox/Documents/UNIVERSE/4 курс/2 semester/Нейронные_сети/All_Labs/1Lab/train.csv", stringsAsFactors = TRUE)
B <- train.kknn(Survived ~ ., 
                A_train[,-1], 
                kmax = dim(A_train)[1],
                kernel = c("triangular", "rectangular", "epanechnikov", "optimal", "inv","gaussian","biweight","triweight","cos"), 
                distance = 1)
print(B)
