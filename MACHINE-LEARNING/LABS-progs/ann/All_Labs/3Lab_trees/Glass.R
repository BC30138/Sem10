
library(tree)
library(maptree)
library(mlbench)

data(Glass)
m <- dim(Glass)[1]
Glass <- Glass[,-1]
bc.tr <- tree(Type ~., Glass)
draw.tree(bc.tr, cex = 0.7)
bc.tr
summary(bc.tr)
#обрезаем дерево от узла 103, 31 так как оба выходящих узла принадлежат классу 1,2
bc.tr1 <- snip.tree(bc.tr, nodes = c(31, 103))
draw.tree(bc.tr1, cex = 0.7)
bc.tr2 <- prune.tree(bc.tr, k = 10)
#bc.tr2 <- prune.tree(bc.tr)
draw.tree(bc.tr2, cex = 0.7)

example <- data.frame("RI" = 1.516,"Na" = 11.7, "Mg" = 1.01, "Al" = 1.19, "Si" = 72.59, "K" = 0.43,"Ca" = 11.44, "Ba" = 0.02, "Fe" = 0.1, "Type" = "")
predict(bc.tr, example)