tic_tac_toe <- function(obj) {
    UseMethod("tic_tac_toe")
}

tic_tac_toe.default <- function(obj) {
    cat("'Tic-tac-toe' dataset should be init in lab's object\n")
}

email <- function(obj) {
    UseMethod("email")
}

titanic.default <- function(obj) {
    cat("'Email spam' dataset should be init in lab's object\n")
}

glass <- function(obj) {
    UseMethod("glass")
}

glass.default <- function(obj) {
    cat("'Glass' dataset should be init in lab's object\n")
}

titanic <- function(obj) {
    UseMethod("titanic")
}

titanic.default <- function(obj) {
    cat("'Titanic' dataset should be init in lab's object\n")
}

svmdata1 <- function(obj) {
    UseMethod("svmdata1")
}

svmdata1.default <- function(obj) {
    cat("'Svmdata1' dataset should be init in lab's object\n")
}

svmdata2 <- function(obj) {
    UseMethod("svmdata2")
}

svmdata2.default <- function(obj) {
    cat("'Svmdata2' dataset should be init in lab's object\n")
}

svmdata3 <- function(obj) {
    UseMethod("svmdata3")
}

svmdata3.default <- function(obj) {
    cat("'Svmdata3' dataset should be init in lab's object\n")
}

svmdata4 <- function(obj) {
    UseMethod("svmdata4")
}

svmdata4.default <- function(obj) {
    cat("'Svmdata4' dataset should be init in lab's object\n")
}

svmdata5 <- function(obj) {
    UseMethod("svmdata5")
}

svmdata5.default <- function(obj) {
    cat("'Svmdata5' dataset should be init in lab's object\n")
}

svmdata6 <- function(obj) {
    UseMethod("svmdata6")
}

svmdata6.default <- function(obj) {
    cat("'Svmdata6' dataset should be init in lab's object\n")
}

split_data_train_test <- function(input_frame, train_ratio) {
    input_frame <- input_frame[sample(nrow(input_frame)),]
    smp_size <- floor(train_ratio * nrow(input_frame))
    set.seed(123)
    train_ind <- sample(seq_len(nrow(input_frame)), size = smp_size)
    return(list("test_set" = input_frame[-train_ind, ], "train_set" = input_frame[train_ind, ]))
}

plot_vol_error <- function(ratio, accuracy,path) {
    png(path, width = 800)
    plot(ratio, accuracy,
        type = "b",
        xlab = "Volume of training sample",
        ylab = "Accuracy score",
        col="red",
        lwd=3,
        pch=16
        )
    dev.off()
}

get_accuracy_vol_dep <- function(data_frame, train_ratios, func) {
    repeats <- 5
    accuracy_list <- list()
    for (train_ind in 1:length(train_ratios)) {
        accuracy <- 0.0
        splitted_df <- split_data_train_test(data_frame, train_ratios[train_ind])
        test_set <- splitted_df$test_set
        train_set <- splitted_df$train_set
        for (it in 1:repeats) {
            model <- func(train_set, test_set)
            accuracy <- accuracy + get_accuracy(fitted(model), test_set[[ncol(test_set)]])
        }
        accuracy_list[train_ind] <- accuracy / repeats
    }
    return(accuracy_list)
}

get_accuracy <- function(fitted_model, test_set_y) {
    conf_matrix <- table(fitted_model,test_set_y)
    diag_len <- sqrt(length(conf_matrix))
    score <- 0
    for (it in 1:diag_len) {
        score <- score + conf_matrix[it, it]
    }
    return(score / sum(conf_matrix))
}

get_accuracy_class_dep <- function(train_set, test_set, func) {
    accuracy_list <-list()
    repeats <- 5
    for (excl_it in 1:(ncol(train_set) - 1)) {
        train_set_exclude <- train_set[, -1*excl_it]
        test_set_exclude <- test_set[, -1*excl_it]
        accuracy <- 0.0
        for (it in 1:repeats) {
            model <- func(train_set_exclude, test_set_exclude)
            accuracy <- accuracy + get_accuracy(fitted(model), test_set_exclude$Type)
        }
        accuracy_list[excl_it] <- accuracy / repeats
    }
    return(accuracy_list)
}

plot_exc_error <- function(accuracy,path) {
    png(path, width = 800)
    plot(1:length(accuracy), accuracy,
        type = "b",
        xlab = "Excluded class",
        ylab = "Accuracy score",
        col="red",
        lwd=3,
        pch=16
        )
    dev.off()
}

check_data <- function(data_frame) {
    str(data_frame)
    cat("\nMissing values: \n")
    sapply(data_frame, function(x) {sum(is.na(x))})
}

palette_func <- function(n = 2) {
    cols = rainbow(n)
    cols[1:2] = c("olivedrab3", "firebrick1")
    return(cols)
}