
library(tree)
library(maptree)

names <- c("Id", "Age", "Sight", "Astigmatism", "Tears", "Type")

A_raw <- read.table("Lenses.txt", stringsAsFactors = TRUE, col.names = names )
A_raw <- A_raw[,-1]

len.tr <- tree(Type ~., A_raw)
draw.tree(len.tr)

example <- data.frame("Age" = 2,"Sight" = 1, "Astigmatism" = 2, "Tears" = 1)
predict(len.tr, example)