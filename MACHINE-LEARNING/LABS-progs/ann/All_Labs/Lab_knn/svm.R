library(kknn)

A_train <- read.table("C:/Users/anna_fox/Documents/UNIVERSE/4 курс/2 semester/Нейронные_сети/All_Labs/2Lab/svmdata4.txt", stringsAsFactors = TRUE)
A_test <- read.table("C:/Users/anna_fox/Documents/UNIVERSE/4 курс/2 semester/Нейронные_сети/All_Labs/2Lab/svmdata4test.txt", stringsAsFactors = TRUE)

A_result <- train.kknn(Colors ~ ., 
                         A_train, 
                         kmax = floor(sqrt(dim(A_train)[1]))+5, 
                         kernel = c("triangular", "rectangular", "epanechnikov", "optimal", "inv"), 
                         distance = 1)
print(A_result)

par(mfrow = c(1, 2))
plot(A_train$X1, A_train$X2,
     col = ifelse(A_train$Colors == 'green', "green", "red"),
     xlab = "X1", ylab = "X2")
plot(A_result)