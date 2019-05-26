library(MASS)

RegLab <- function() {
    value <- list()
    attr(value, "class") <- "RegLab"
    value
}

reglab1.RegLab <- function(obj) {
    data_frame <- read.csv("data/reglab1.csv")

    # png("results/Reg/reglab1_lin.png")
    # model <- lm(z~., data = data_frame)
    # plot(z~., data = data_frame,
    #     col="red",
    #     pch=16)
    # abline(model, col = "blue", lwd=3)
    # dev.off()
    # print(summary(model))

    png("results/Reg/reglab1_ridge.png")
    model <- lm.ridge(z~., data = data_frame)
    # plot(model)
    plot(z~., data = data_frame,
        col="red",
        pch=16)
    abline(model, col = "blue", lwd=3)
    dev.off()
}