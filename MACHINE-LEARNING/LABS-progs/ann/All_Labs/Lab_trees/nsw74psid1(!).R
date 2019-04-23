
library(tree)
library(maptree)
library(DAAG)
library(e1071)

data(nsw74psid1)
m <- dim(nsw74psid1)[1]
ns.tr <- tree(re78 ~., nsw74psid1)
draw.tree(ns.tr, cex = 0.7)
ns.tr
summary(ns.tr)


