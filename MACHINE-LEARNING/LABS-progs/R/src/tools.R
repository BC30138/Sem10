library(zoo)

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

vehicle <- function(obj) {
    UseMethod("vehicle")
}

vehicle.default <- function(obj) {
    cat("'Vehicle' dataset should be init in lab's object\n")
}

reglab1 <- function(obj) {
    UseMethod("reglab1")
}

reglab1.default <- function(obj) {
    cat("'reglab1' dataset should be init in lab's object\n")
}

reglab2 <- function(obj) {
    UseMethod("reglab2")
}

reglab2.default <- function(obj) {
    cat("'reglab2' dataset should be init in lab's object\n")
}

cygage <- function(obj) {
    UseMethod("cygage")
}

cygage.default <- function(obj) {
    cat("'cygage' dataset should be init in lab's object\n")
}

longley <- function(obj) {
    UseMethod("longley")
}

longley.default <- function(obj) {
    cat("'longley' dataset should be init in lab's object\n")
}

eustockmark <- function(obj) {
    UseMethod("eustockmark")
}

eustockmark.default <- function(obj) {
    cat("'eustockmark' dataset should be init in lab's object\n")
}

JnJ <- function(obj) {
    UseMethod("JnJ")
}

JnJ.default <- function(obj) {
    cat("'JnJ' dataset should be init in lab's object\n")
}

sunspotyear <- function(obj) {
    UseMethod("sunspotyear")
}

sunspotyear.default <- function(obj) {
    cat("'sunspotyear' dataset should be init in lab's object\n")
}

UKgas <- function(obj) {
    UseMethod("UKgas")
}

UKgas.default <- function(obj) {
    cat("'UKgas' dataset should be init in lab's object\n")
}

carsset <- function(obj) {
    UseMethod("carsset")
}

carsset.default <- function(obj) {
    cat("'carsset' dataset should be init in lab's object\n")
}

plutonset <- function(obj) {
    UseMethod("plutonset")
}

plutonset.default <- function(obj) {
    cat("'plutonset' dataset should be init in lab's object\n")
}

generated <- function(obj) {
    UseMethod("generated")
}

generated.default <- function(obj) {
    cat("'generated' dataset should be init in lab's object\n")
}

votesset <- function(obj) {
    UseMethod("votesset")
}

votesset.default <- function(obj) {
    cat("'votesset' dataset should be init in lab's object\n")
}

animals <- function(obj) {
    UseMethod("animals")
}

animals.default <- function(obj) {
    cat("'animals' dataset should be init in lab's object\n")
}

seeds <- function(obj) {
    UseMethod("seeds")
}

seeds.default <- function(obj) {
    cat("'seeds' dataset should be init in lab's object\n")
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

get_full_df <- function(data_frame) {
    new_frame <- zoo(data_frame)
    new_frame <- fortify.zoo(new_frame)
    colnames(new_frame) <- c("Year", "Val")
    return(new_frame)
}

get_df_with_qtr <- function(data_frame) {
    new_frame <- data.frame(yq = yearqtr(index(data_frame)))
    new_frame <- data.frame(do.call('rbind', strsplit(as.character(new_frame$yq),' ',fixed=TRUE)), Val = data_frame)
    Q1 <- new_frame[new_frame$X2 == "Q1",]
    Q2 <- new_frame[new_frame$X2 == "Q2",]
    Q3 <- new_frame[new_frame$X2 == "Q3",]
    Q4 <- new_frame[new_frame$X2 == "Q4",]
    new_frame$X1 <- as.numeric(levels(new_frame$X1))[new_frame$X1]
    new_frame <- data.frame(new_frame$X1[!duplicated(new_frame$X1)], Q1$Val, Q2$Val, Q3$Val, Q4$Val)
    colnames(new_frame) <- c("Year", "Qtr1", "Qtr2", "Qtr3", "Qtr4")
    return(new_frame)
}
