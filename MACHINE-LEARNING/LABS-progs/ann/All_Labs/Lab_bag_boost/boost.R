#install.packages("adabag")
library(adabag)
library(rpart) 
library(mlbench) 
### �������� ����� ������ Vehicle: 
data(Vehicle) 
### ����������� ������ ������� �����������, ������� ������ � ��������� ������� (�� ����� ����� 2/3l, 
###��� l - ����� ����������� � ������ ������ Vehicle) 
l <- length(Vehicle[,1]) 
sub <- sample(1:l,7*l/10)  
### ������� ������������ ����� �������� � ��������� adaboost.M1, ������ 25: 
mfinal <- c(1,11,21,31,41,51,61,71,81,91,101,111,121,131,141,151,161,171,181,191,201,211,221,231,241,251,261,271,281,291,301) 
#mfinal <- c(1,11,21)
resList <- list()
maxdepth <- 5
for (i in 1:length(mfinal)){
  Vehicle.adaboost <- boosting(Class ~.,data=Vehicle[sub,], mfinal=mfinal[i], maxdepth=maxdepth) 
  Vehicle.adaboost.pred <- predict.boosting(Vehicle.adaboost, newdata=Vehicle[-sub, ]) 
  resList[i] <- Vehicle.adaboost.pred$error 
}

plot(mfinal,resList,
     col = "red",
     xlab = "Number of trees",
     ylab = "Classification error")