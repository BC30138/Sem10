### lab2: kknn ###
source("src/tools.R")

library(kknn)

KnnLab <- function() {
    value <- list()
    attr(value, "class") <- "KnnLab"
    value
}

tic_tac_toe.KnnLab <- function(obj) {
    data_frame <- read.csv("data/Tic_tac_toe.data", header=FALSE, stringsAsFactors = TRUE)

    train_ratios <- seq(0.1, 0.9, 0.1)
    clf <- function(tr_set, te_set) {
        return(kknn(V10~., tr_set, te_set, k = 25, kernel = "optimal"))
    }

    accuracy_list <- get_accuracy_vol_dep(data_frame, train_ratios, clf)

    plot_vol_error(train_ratios, accuracy_list, "results/kknn/tic_tac_toe.png")
}

glass.KnnLab <- function(obj) {
    data(glass)
    data_frame <- glass[,-1]
    splitted_df <- split_data_train_test(data_frame, 0.9)
    train_set <- splitted_df$train_set
    test_set <- splitted_df$test_set

    test_sample <- data.frame("RI" = 1.516,
                              "Na" = 11.7,
                              "Mg" = 1.01,
                              "Al" = 1.19,
                              "Si" = 72.59,
                              "K" = 0.43,
                              "Ca" = 11.44,
                              "Ba" = 0.02,
                              "Fe" = 0.1,
                              "Type" = "")

    print(fitted(kknn(Type~., train_set, test_sample)))

    model_d_1 <- train.kknn(Type ~ ., train_set,
            kmax = 25,
            kernel = c("triangular", "rectangular",
                       "epanechnikov", "optimal"),
            distance = 1)

    model_d_2 <- train.kknn(Type ~ ., train_set,
            kmax = 25,
            kernel = c("triangular", "rectangular",
                       "epanechnikov", "optimal"),
            distance = 2)

    print(model_d_1)
    print(model_d_2)

    png("results/kknn/glass_distance.png",
        width = 960,
        height = 480,)
    par(mfrow = c(1, 2))
    plot(model_d_1,
         type = "b",
         main = "distance = 1",
         lwd=3)
    plot(model_d_2,
         type = "b",
         main = "distance = 2",
         lwd=3)
    dev.off()

    clf <- function(tr_set, te_set) {
        return(kknn(Type~., tr_set, te_set, distance = 1, k = 5))
    }

    accuracy_list <- get_accuracy_class_dep(train_set, test_set, clf)

    plot_exc_error(accuracy_list, "results/kknn/glass_class_exclude.png")
}

svmdata4.KnnLab <- function(obj) {
    train_set <- read.csv("data/svmdata/svmdata4.csv")

    cross_valid_model <- train.kknn(Colors ~ .,
                         train_set,
                         kmax = 15,
                         kernel = c("triangular", "rectangular",
                                    "epanechnikov", "optimal", "inv"),
                         distance = 1)

    print(cross_valid_model)

    png("results/kknn/svmdata.png", width = 960)
    par(mfrow = c(1, 2))
    plot(train_set$X1, train_set$X2,
        col = ifelse(train_set$Colors == 'green', "green", "red"),
        xlab = "X1",
        ylab = "X2",
        main = "input_frame",
        lwd=3)
    plot(cross_valid_model,
        type="b",
        main="Analysis",
        lwd=3)
    dev.off()
}

titanic.KnnLab <- function(obj) {
    train_set <- read.csv("data/titanic/train.csv", stringsAsFactors = T)
    cross_valid_model <- train.kknn(Survived ~ .,
                train_set[,-1],
                kmax = 40,,
                kernel = c("triangular", "rectangular", "epanechnikov", "optimal", "inv","gaussian","biweight","triweight","cos"),
                distance = 1)
    print(cross_valid_model)

    png("results/kknn/titanic.png")
    plot(cross_valid_model,
        type="b",
        lwd=3)
    dev.off()
}