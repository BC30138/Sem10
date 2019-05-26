suppressWarnings(suppressMessages(library(adabag)))
library(mlbench)
library(rpart)

BoostLab <- function() {
    value <- list()
    attr(value, "class") <- "BoostLab"
    value
}

vehicle.BoostLab <- function(obj) {
    data(Vehicle)
    data_frame <- Vehicle
    splitted_df <- split_data_train_test(data_frame, 0.7)
    train_set <- splitted_df$train_set
    test_set <- splitted_df$test_set

    trees_num <- seq(1, 301, 10)
    max_dp <- 5
    error_list <- list()
    for(tree_ind in 1:length(trees_num)) {
        ensemble <- boosting(Class~., data = train_set, mfinal = trees_num[tree_ind], maxdepth = max_dp)
        predict_res <- predict.boosting(ensemble, newdata = test_set)
        error_list[tree_ind] <- predict_res$error
    }

    png("results/Boosting/Vehicle_num_trees.png", width = 800)
    plot(trees_num, error_list,
        type = "b",
        xlab = "Number of trees",
        ylab = "Classification error",
        col="red",
        lwd=3,
        pch=16
        )
    dev.off()
    print(setNames(trees_num, error_list))
}

glass.BoostLab <- function(obj) {
    data(glass)
    data_frame <- glass
    splitted_df <- split_data_train_test(data_frame, 0.7)
    train_set <- splitted_df$train_set
    test_set <- splitted_df$test_set

    trees_num <- seq(1,201,10)
    max_dp = 5
    error_list <- list()
    for(tree_ind in 1:length(trees_num)) {
        ensemble <- bagging(Type~., data = train_set, mfinal = trees_num[tree_ind], maxdepth = max_dp)
        predict_res <- predict.bagging(ensemble, newdata = test_set)
        error_list[tree_ind] <- predict_res$error
    }

    png("results/Boosting/glass_num_trees.png", width = 800)
    plot(trees_num, error_list,
        type = "b",
        xlab = "Number of trees",
        ylab = "Classification error",
        col="red",
        lwd=3,
        pch=16
        )
    dev.off()
    print(setNames(trees_num, error_list))
}
