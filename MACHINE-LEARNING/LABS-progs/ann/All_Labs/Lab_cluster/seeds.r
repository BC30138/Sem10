A <- read.table("seeds_dataset.txt")
cl <- kmeans(A, 3)
plot(A, col = cl$cluster)