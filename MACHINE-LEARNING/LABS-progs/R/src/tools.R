glass <- function(obj) {
UseMethod("glass")
}

tic_tac_toe <- function(obj) {
UseMethod("tic_tac_toe")
}

tic_tac_toe.default <- function(obj) {
cat("'Tic-tac-toe' data-set should be init in lab's object\n")
}

glass.default <- function(obj) {
cat("'Glass' data-set should be init in lab's object\n")
}

split_data_train_test <- function(input_frame, train_ratio) {
    input_frame <- input_frame[sample(nrow(input_frame)),]
    smp_size <- floor(train_ratio * nrow(input_frame))
    set.seed(123)
    train_ind <- sample(seq_len(nrow(input_frame)), size = smp_size)
    return(list("test_set" = input_frame[-train_ind, ], "train_set" = input_frame[train_ind, ]))
}

plot_vol_error <- function(ratio, accuracy,path) {
    png(path)
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
            accuracy <- accuracy + get_accuracy(fitted(model), test_set$V10)
        }
        accuracy_list[train_ind] <- accuracy / repeats
    }
    return(accuracy_list)
}

get_accuracy <- function(fitted_model, test_set_y) {
    conf_matrix <- table(fitted_model,test_set_y)
    return( 1 - ((conf_matrix[2] + conf_matrix[3]) / sum(conf_matrix)) )
}