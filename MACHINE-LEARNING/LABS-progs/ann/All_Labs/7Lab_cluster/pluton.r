#install.packages("cluster")
library(cluster)

data(pluton)
pluton <- pluton[,-c(1,2)]
cl <- kmeans(pluton, 3, iter.max = 1)
plot(pluton,col = cl$cluster)
cl2 <- kmeans(pluton, 3, iter.max = 1000)
points(pluton, col = cl2$cluster, cex = 4)
cl3 <- kmeans(pluton, 3, iter.max = 2000)
points(pluton, col = cl3$cluster, cex = 7)

