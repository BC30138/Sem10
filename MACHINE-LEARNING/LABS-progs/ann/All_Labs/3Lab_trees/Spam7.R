#install.packages("tree")
#install.packages("maptree")
#install.packages("mlbench")
#install.packages("DAAG")

library(tree)
library(maptree)
library(DAAG)

data(spam7)
m <- dim(spam7)[1]
sp.tr <- tree(yesno ~., spam7)
draw.tree(sp.tr, cex = 0.7)
sp.tr

#���������� ������ 6
cv.tree(sp.tr)
plot(cv.tree(sp.tr))

#��� �������� best �� �����������
sp.tr1 <- prune.misclass(sp.tr, best = 5)
#sp.tr1 <- prune.misclass(sp.tr)

#�������� ���� ����� �� ���������
#��������� ��������� �cost-complexity prunning� � ������� ��������� k �� ���������, method = �misclass�
#sp.tr1 <- prune.tree(sp.tr, k = NULL, method = "misclass")
#bc.tr2 <- prune.tree(bc.tr)
#sp.tr1 <- cv.tree(sp.tr, prune.tree)

#sp.tr1 <- prune.misclass(sp.tr) 

draw.tree(sp.tr1, cex = 0.7)

