library(lmridge)
library(datasets)
library(xts)
library(MASS)
library(datasets)

RegLab <- function() {
    value <- list()
    attr(value, "class") <- "RegLab"
    value
}

reglab1.RegLab <- function(obj) {
    data_frame <- read.csv("data/reglab1.csv")
    model <- lm(z~., data = data_frame)
    print(summary(model))

    model <- lmridge(z~., data = data_frame, K = seq(0,0.1,0.01))
    print(rstats1(model))
}

reglab2.RegLab <- function(obj) {
    data_frame <- read.csv("data/reglab2.csv")

    r2 <- vector()
    formulas <- vector()
    tmp_ind <- 0
    for (k in 1:(ncol(data_frame) - 1)) {
        features_to_use <- combn(names(data_frame[,-1]), k)
        for (f_set in 1:ncol(features_to_use)) {
            tmp_ind <- tmp_ind + 1
            formulas[tmp_ind] <- paste("y", "~", paste(features_to_use[,f_set], collapse = "+"))
            model <- lm(formula(formulas[tmp_ind]), data = data_frame)
            r2[tmp_ind] <- summary(model)$r.squared
        }
    }

    r2_frame <- data.frame(formulas, r2)
    r2_frame <- r2_frame[order(r2_frame$r2),]
    print(r2_frame)
}

cygage.RegLab <- function(obj) {
    data_frame <- read.csv("data/cygage.csv")
    model = lm(calAge ~ Depth, data = data_frame, weights=data_frame$Weight)
    print(summary(model))
}

longley.RegLab <- function(obj) {
    data_frame <- read.csv("data/longley.csv")

    lm_model <- lm(Employed ~., data = data_frame)
    print(summary(lm_model))

    data_frame <- data_frame[,-5]
    splitted_df <- split_data_train_test(data_frame, 0.5)
    train_set <- splitted_df$train_set
    test_set <- splitted_df$test_set

    lambda <- vector()
    for (i in 0:25) {
        lambda[i + 1] <- 10 ^ (-1 + 0.2 * i)
    }

    model <- lmridge(Employed~., data = train_set, K = lambda)
    print(rstats1(model))
    png("results/Reg/longley.png", width = 800)
    plot(model)
    dev.off()
}

eustockmark.RegLab <- function(obj) {
    data(EuStockMarkets)
    data_frame <- EuStockMarkets
    data_frame <- zoo(data_frame)
    data_frame <- fortify.zoo(data_frame)
    names(data_frame) <- c("Year", "DAX", "SMI", "CAC", "FTSE")

    png("results/Reg/stcokmark_data.png", width = 800)
    plot(data_frame$Year, data_frame$DAX, type = "l", lwd = 3, pch=16, col = "red", xlab = "Year", ylab = "Val", main = "EuStockMarkets dataset")
    lines(data_frame$Year, data_frame$SMI, type = "l", lwd = 3, pch=16, col = "blue")
    lines(data_frame$Year, data_frame$CAC, type = "l", lwd = 3, pch=16, col = "green")
    lines(data_frame$Year, data_frame$FTSE, type = "l", lwd = 3, pch=16, col = "orange")
    legend('topleft', names(data_frame)[-1] ,
        lty=1, col=c('red', 'blue', 'green',' orange'), cex=1.1)
    dev.off()

    DAX_model = lm(DAX ~ Year, data = data_frame)
    SMI_model = lm(SMI ~ Year, data = data_frame)
    CAC_model = lm(CAC ~ Year, data = data_frame)
    FTSE_model = lm(FTSE ~ Year, data = data_frame)

    png("results/Reg/stockmark_reg_DAX.png", width = 800)
    plot(data_frame$Year, data_frame$DAX,
        type = "l", lwd = 3, pch=16, col = "red",
        xlab = "Year", ylab = "Val", main = "DAX")
    abline(DAX_model, lwd = 3, col = "blue")
    legend('topleft', c("Actual data", "Reg line"),
        lty=1, col=c('red', 'blue'), cex=1.1)
    dev.off()

    png("results/Reg/stockmark_reg_SMI.png", width = 800)
    plot(data_frame$Year, data_frame$SMI,
        type = "l", lwd = 3, pch=16, col = "red",
        xlab = "Year", ylab = "Val", main = "SMI")
    abline(SMI_model, lwd = 3, col = "blue")
    legend('topleft', c("Actual data", "Reg line"),
        lty=1, col=c('red', 'blue'), cex=1.1)
    dev.off()

    png("results/Reg/stockmark_reg_CAC.png", width = 800)
    plot(data_frame$Year, data_frame$CAC,
        type = "l", lwd = 3, pch=16, col = "red",
        xlab = "Year", ylab = "Val", main = "CAC")
    abline(CAC_model, lwd = 3, col = "blue")
    legend('topleft', c("Actual data", "Reg line"),
        lty=1, col=c('red', 'blue'), cex=1.1)
    dev.off()

    png("results/Reg/stockmark_reg_FTSE.png", width = 800)
    plot(data_frame$Year, data_frame$FTSE,
        type = "l", lwd = 3, pch=16, col = "red",
        xlab = "Year", ylab = "Val", main = "FTSE")
    abline(FTSE_model, lwd = 3, col = "blue")
    legend('topleft', c("Actual data", "Reg line"),
        lty=1, col=c('red', 'blue'), cex=1.1)
    dev.off()

    png("results/Reg/stockmark_reg_lines.png", width = 800)
    plot(data_frame$Year, data_frame$DAX, type = "n", xlab = "Year", ylab = "Val")
    abline(DAX_model, lwd = 3, col = "red")
    abline(SMI_model, lwd = 3, col = "blue")
    abline(CAC_model, lwd = 3, col = "green")
    abline(FTSE_model, lwd = 3, col = "orange")
    legend('topleft', names(data_frame)[-1] ,
        lty=1, col=c('red', 'blue', 'green',' orange'), cex=1.1)
    dev.off()
}

JnJ.RegLab <- function(obj) {
    data(JohnsonJohnson)
    data_frame_full <- get_full_df(JohnsonJohnson)
    data_frame_qtr <- get_df_with_qtr(JohnsonJohnson)

    png("results/Reg/JnJ_qtr.png", width = 800)
    plot(data_frame_qtr$Year, data_frame_qtr$Qtr1, type = "o", lwd = 3, pch=16, col = "red", xlab = "Year", ylab = "Profit")
    lines(data_frame_qtr$Year, data_frame_qtr$Qtr2, type = "o", lwd = 3, pch=16, col = "blue")
    lines(data_frame_qtr$Year, data_frame_qtr$Qtr3, type = "o", lwd = 3, pch=16, col = "green")
    lines(data_frame_qtr$Year, data_frame_qtr$Qtr4, type = "o", lwd = 3, pch=16, col = "orange")
    legend('topleft', names(data_frame_qtr)[-1] ,
        lty=1, col=c('red', 'blue', 'green',' orange'), cex=1.1)
    dev.off()

    png("results/Reg/JnJ_reg_line_full.png", width = 800)
    plot(data_frame_full$Year, data_frame_full$Val,
        type = "o", lwd = 3, pch=16, col = "red",
        xlab = "Year", ylab = "Profit", main = "Full year")
    f_model = lm(Val~., data = data_frame_full)
    abline(f_model, lwd = 3, col = "blue")
    legend('topleft', c("Actual data", "Reg line"),
        lty=1, col=c('red', 'blue'), cex=1.1)
    dev.off()

    png("results/Reg/JnJ_reg_line_qtr1.png", width = 800)
    plot(data_frame_qtr$Year, data_frame_qtr$Qtr1,
        type = "o", lwd = 3, pch=16, col = "red",
        xlab = "Year", ylab = "Profit", main = "Qtr1")
    qtr1_model = lm(Qtr1~Year, data = data_frame_qtr)
    abline(qtr1_model, lwd = 3, col = "blue")
    legend('topleft', c("Actual data", "Reg line"),
        lty=1, col=c('red', 'blue'), cex=1.1)
    dev.off()

    png("results/Reg/JnJ_reg_line_qtr2.png", width = 800)
    plot(data_frame_qtr$Year, data_frame_qtr$Qtr2,
        type = "o", lwd = 3, pch=16, col = "red",
        xlab = "Year", ylab = "Profit", main = "Qtr2")
    qtr2_model = lm(Qtr2~Year, data = data_frame_qtr)
    abline(qtr2_model, lwd = 3, col = "blue")
    legend('topleft', c("Actual data", "Reg line"),
        lty=1, col=c('red', 'blue'), cex=1.1)
    dev.off()

    png("results/Reg/JnJ_reg_line_qtr3.png", width = 800)
    plot(data_frame_qtr$Year, data_frame_qtr$Qtr3,
        type = "o", lwd = 3, pch=16, col = "red",
        xlab = "Year", ylab = "Profit", main = "Qtr3")
    qtr3_model = lm(Qtr3~Year, data = data_frame_qtr)
    abline(qtr3_model, lwd = 3, col = "blue")
    legend('topleft', c("Actual data", "Reg line"),
        lty=1, col=c('red', 'blue'), cex=1.1)
    dev.off()

    png("results/Reg/JnJ_reg_line_qtr4.png", width = 800)
    plot(data_frame_qtr$Year, data_frame_qtr$Qtr4,
        type = "o", lwd = 3, pch=16, col = "red",
        xlab = "Year", ylab = "Profit", main = "Qtr4")
    qtr4_model = lm(Qtr4~Year, data = data_frame_qtr)
    abline(qtr4_model, lwd = 3, col = "blue")
    legend('topleft', c("Actual data", "Reg line"),
        lty=1, col=c('red', 'blue'), cex=1.1)
    dev.off()

    png("results/Reg/JnJ_reg_lines.png", width = 800)
    plot(data_frame_qtr$Year, data_frame_qtr$Qtr1, type = "n", xlab = "Year", ylab = "Profit")
    abline(qtr1_model, lwd = 3, col = "red")
    abline(qtr2_model, lwd = 3, col = "blue")
    abline(qtr3_model, lwd = 3, col = "green")
    abline(qtr4_model, lwd = 3, col = "orange")
    legend('topleft', names(data_frame_qtr)[-1] ,
        lty=1, col=c('red', 'blue', 'green',' orange'), cex=1.1)
    dev.off()

    test_year <- data.frame(Year=c(2016, 2016.25, 2016.5, 2016.75))
    res_year <- predict(f_model, test_year)
    cat("2016 full:\n")
    print(summary(res_year))

    test_qtr <- data.frame(Year=c(2016))
    res_qtr1 <- predict(qtr1_model, test_qtr)
    cat("2016 qtr1:\n")
    print(summary(res_qtr1))

    res_qtr2 <- predict(qtr2_model, test_qtr)
    cat("2016 qtr2:\n")
    print(summary(res_qtr2))

    res_qtr3 <- predict(qtr3_model, test_qtr)
    cat("2016 qtr3:\n")
    print(summary(res_qtr3))

    res_qtr4 <- predict(qtr4_model, test_qtr)
    cat("2016 qtr4:\n")
    print(summary(res_qtr4))
}

sunspotyear <- function(obj) {
    data(sunspot.year)
    data_frame <- sunspot.year
    data_frame <- data.frame(seq(1700, 1988, 1), data_frame)
    names(data_frame) <- c("Year", "Num")

    png("results/Reg/sunspotyear_data.png", width = 800)
    plot(data_frame$Year, data_frame$Num, type = "l", lwd = 3, pch=16, col = "red", xlab = "Year", ylab = "Num", main = "Sunspot.year dataset")
    dev.off()

    model = lm(Num ~ Year, data = data_frame)
    png("results/Reg/sunspotyear_reg.png", width = 800)
    plot(data_frame$Year, data_frame$Num,
        type = "l", lwd = 3, pch=16, col = "red",
        xlab = "Year", ylab = "Num", main = "Line reg")
    abline(model, lwd = 3, col = "blue")
    legend('topleft', c("Actual data", "Reg line"),
        lty=1, col=c('red', 'blue'), cex=1.1)
    dev.off()
}

UKgas <- function(obj) {
    data_frame <- read.csv("data/UKgas.csv")[,-1]
    names(data_frame) <- c("Year", "Val")
    quarters <- rep(seq(1:4), nrow(data_frame)/4)
    data_frame_qtr <- data.frame(Val = data_frame[,-1], Q = quarters)
    Q1 <- data_frame_qtr[data_frame_qtr$Q == 1,]
    Q2 <- data_frame_qtr[data_frame_qtr$Q == 2,]
    Q3 <- data_frame_qtr[data_frame_qtr$Q == 3,]
    Q4 <- data_frame_qtr[data_frame_qtr$Q == 4,]
    data_frame_qtr <- data.frame(Year = seq(1960, 1986, 1),
                                 Qtr1 = Q1$Val, Qtr2 = Q2$Val,
                                 Qtr3 = Q3$Val, Qtr4 = Q4$Val)

    png("results/Reg/UKgas_qtr.png", width = 800)
    plot(data_frame_qtr$Year, data_frame_qtr$Qtr1, type = "o", lwd = 3, pch=16, col = "red", xlab = "Year", ylab = "Vol", main = "UKgas dataset")
    lines(data_frame_qtr$Year, data_frame_qtr$Qtr2, type = "o", lwd = 3, pch=16, col = "blue")
    lines(data_frame_qtr$Year, data_frame_qtr$Qtr3, type = "o", lwd = 3, pch=16, col = "green")
    lines(data_frame_qtr$Year, data_frame_qtr$Qtr4, type = "o", lwd = 3, pch=16, col = "orange")
    legend('topleft', names(data_frame_qtr)[-1] ,
        lty=1, col=c('red', 'blue', 'green',' orange'), cex=1.1)
    dev.off()

    png("results/Reg/UKgas_reg_line_full.png", width = 800)
    plot(data_frame$Year, data_frame$Val,
        type = "o", lwd = 3, pch=16, col = "red",
        xlab = "Year", ylab = "Vol", main = "Full year")
    f_model = lm(Val~., data = data_frame)
    abline(f_model, lwd = 3, col = "blue")
    legend('topleft', c("Actual data", "Reg line"),
        lty=1, col=c('red', 'blue'), cex=1.1)
    dev.off()

    png("results/Reg/UKgas_reg_line_qtr1.png", width = 800)
    plot(data_frame_qtr$Year, data_frame_qtr$Qtr1,
        type = "o", lwd = 3, pch=16, col = "red",
        xlab = "Year", ylab = "Vol", main = "Qtr1")
    qtr1_model = lm(Qtr1~Year, data = data_frame_qtr)
    abline(qtr1_model, lwd = 3, col = "blue")
    legend('topleft', c("Actual data", "Reg line"),
        lty=1, col=c('red', 'blue'), cex=1.1)
    dev.off()

    png("results/Reg/UKgas_reg_line_qtr2.png", width = 800)
    plot(data_frame_qtr$Year, data_frame_qtr$Qtr2,
        type = "o", lwd = 3, pch=16, col = "red",
        xlab = "Year", ylab = "Vol", main = "Qtr2")
    qtr2_model = lm(Qtr2~Year, data = data_frame_qtr)
    abline(qtr2_model, lwd = 3, col = "blue")
    legend('topleft', c("Actual data", "Reg line"),
        lty=1, col=c('red', 'blue'), cex=1.1)
    dev.off()

    png("results/Reg/UKgas_reg_line_qtr3.png", width = 800)
    plot(data_frame_qtr$Year, data_frame_qtr$Qtr3,
        type = "o", lwd = 3, pch=16, col = "red",
        xlab = "Year", ylab = "Vol", main = "Qtr3")
    qtr3_model = lm(Qtr3~Year, data = data_frame_qtr)
    abline(qtr3_model, lwd = 3, col = "blue")
    legend('topleft', c("Actual data", "Reg line"),
        lty=1, col=c('red', 'blue'), cex=1.1)
    dev.off()

    png("results/Reg/UKgas_reg_line_qtr4.png", width = 800)
    plot(data_frame_qtr$Year, data_frame_qtr$Qtr4,
        type = "o", lwd = 3, pch=16, col = "red",
        xlab = "Year", ylab = "Vol", main = "Qtr4")
    qtr4_model = lm(Qtr4~Year, data = data_frame_qtr)
    abline(qtr4_model, lwd = 3, col = "blue")
    legend('topleft', c("Actual data", "Reg line"),
        lty=1, col=c('red', 'blue'), cex=1.1)
    dev.off()

    png("results/Reg/UKgas_reg_lines.png", width = 800)
    plot(data_frame_qtr$Year, data_frame_qtr$Qtr1, type = "n", xlab = "Year", ylab = "Vol", main = "Reg lines")
    abline(qtr1_model, lwd = 3, col = "red")
    abline(qtr2_model, lwd = 3, col = "blue")
    abline(qtr3_model, lwd = 3, col = "green")
    abline(qtr4_model, lwd = 3, col = "orange")
    legend('topleft', names(data_frame_qtr)[-1] ,
        lty=1, col=c('red', 'blue', 'green',' orange'), cex=1.1)
    dev.off()

    test_year <- data.frame(Year=c(2016, 2016.25, 2016.5, 2016.75))
    res_year <- predict(f_model, test_year)
    cat("2016 full:\n")
    print(summary(res_year))

    test_qtr <- data.frame(Year=c(2016))
    res_qtr1 <- predict(qtr1_model, test_qtr)
    cat("2016 qtr1:\n")
    print(summary(res_qtr1))

    res_qtr2 <- predict(qtr2_model, test_qtr)
    cat("2016 qtr2:\n")
    print(summary(res_qtr2))

    res_qtr3 <- predict(qtr3_model, test_qtr)
    cat("2016 qtr3:\n")
    print(summary(res_qtr3))

    res_qtr4 <- predict(qtr4_model, test_qtr)
    cat("2016 qtr4:\n")
    print(summary(res_qtr4))
}

carsset <- function(obj) {
    data_frame <- cars

    png("results/Reg/cars_data.png")
    plot(data_frame, col='red', pch=20, cex=2, main="cars dataset",
	xlab="Speed", ylab="Dist")
    dev.off()

    png("results/Reg/cars_reg_line.png", width = 800)
    plot(data_frame,
        type = "o", lwd = 3, pch=16, col = "red",
        xlab = "Speed", ylab = "Dist", main = "Reg line")
    model = lm(dist~speed, data = data_frame)
    abline(model, lwd = 3, col = "blue")
    legend('topleft', c("Actual data", "Reg line"),
        lty=1, col=c('red', 'blue'), cex=1.1)
    dev.off()

    test <- data.frame(speed=c(40))
    res <- predict(model, test)
    cat("speed = 40:\n")
    print(summary(res))
}