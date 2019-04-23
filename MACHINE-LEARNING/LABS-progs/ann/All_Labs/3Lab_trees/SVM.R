library(tree)
library(maptree)

A_train <- read.table("svmdata4.txt", stringsAsFactors = TRUE)
A_test <- read.table("svmdata4test.txt", stringsAsFactors = TRUE)

len.tr <- tree(Colors ~., A_train)
draw.tree(len.tr)

pred <- predict(len.tr, A_test)
n <- dim(pred)[1]
res <- list()

#для проверки, какой результат определился в pred, используем попарное сравнение элементов (какой больше, так цвет и определен)
for (i in 1:n) {
  if(pred[i] > pred[200+i]){
    res[i] <- "green"
  } else {
    res[i] <- "red"
  }
}

trueElements <- 0

for (i in 1:n) {
  if (A_test$Colors[i] != res[i]){
    trueElements <- trueElements + 1
  }
}

final <- trueElements/n
