#install.packages("adabag")
library(adabag)
library(rpart) 
library(mlbench) 
### «агрузим набор данных Vehicle: 
data(Glass) 
### —генерируем вектор номеров прецедентов, которые войдут в обучающую выборку (их число равно 2/3l, 
###где l - число прецедентов в наборе данных Vehicle) 
l <- length(Glass[,1]) 
sub <- sample(1:l,7*l/10)  
#mfinal <- c(1,11,21,31,41,51,61,71,81,91,101,111,121,131,141,151,161,171,181,191,201) 
mfinal <- c(1,11)
resList <- list()
for (i in 1:length(mfinal)) {
  Glass.bagging <- bagging(Type ~.,data=Glass[sub,], mfinal = mfinal[i], maxdepth=5) 
  ###»спользу€ построенную модель, предскажем ответы на прецедентах из набора данных Vehicle с номерами, не вошедшими в sub: 
  Glass.bagging.pred <- predict.bagging(Glass.bagging, newdata = Glass[-sub, ])  
  Glass.bagging.pred[-1] ### ¬ыведем тестовые ошибки, полученные при использовании одиночного дерева 
  ##и ансамбл€ деревьев решений, построенных adaboost.M1 и bagging: 
  resList[i] <- Glass.bagging.pred$error 
}

plot(mfinal,resList,    
     col = "blue",
     xlab = "Number of trees",
     ylab = "Classification error")