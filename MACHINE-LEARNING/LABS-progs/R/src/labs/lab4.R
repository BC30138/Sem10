library(e1071)

SVMlab <- function() {
    value <- list()
    attr(value, "class") <- "SVMlab"
    value
}

svmdata1.SVMlab <- function(obj) {
    train_set <- read.csv("data/svmdata/svmdata1.csv")
    test_set <- read.csv("data/svmdata/svmdata1test.csv")
    train_set_features <- train_set[,-3]
    test_set_features <- test_set[,-3]

    area.pallete = palette_func
    symbols.pallete = c("blue", "white")

    model = svm(Color ~ ., data = train_set, type = "C-classification", cost = 1, kernel = "linear")

    png("results/SVM/data1_train_set.png", width = 600)
    plot(model, train_set, symbolPalette = symbols.pallete, color.palette = area.pallete)
    dev.off()
    predictions_train = predict(model, train_set_features)
    print(table(train_set$Color, predictions_train))

    png("results/SVM/data1_test_set.png", width = 600)
    plot(model, test_set, symbolPalette = symbols.pallete, color.palette = area.pallete)
    dev.off()
    predictions_test = predict(model, test_set_features)
    print(table(test_set$Color, predictions_test))
}

svmdata2.SVMlab <- function(obj) {
    train_set <- read.csv("data/svmdata/svmdata2.csv")
    test_set <- read.csv("data/svmdata/svmdata2test.csv")
    train_set_features <- train_set[,-3]
    test_set_features <- test_set[,-3]

    area.pallete = palette_func
    symbols.pallete = c("blue", "white")

    model = svm(Colors ~ ., data = train_set, type = "C-classification", cost = 183, kernel = "linear") # нулевая вероятность ошибки в train

    cat("C = 183 ---------\n")

    png("results/SVM/data2_train_set_183.png", width = 600)
    plot(model, train_set, symbolPalette = symbols.pallete, color.palette = area.pallete)
    dev.off()
    predictions_train = predict(model, train_set_features)
    print(table(train_set$Colors, predictions_train))
    cat(sprintf("Accuracy: %f\n\n", get_accuracy(train_set$Colors, predictions_train)))

    png("results/SVM/data2_test_set_183.png", width = 600)
    plot(model, test_set, symbolPalette = symbols.pallete, color.palette = area.pallete)
    dev.off()
    predictions_test = predict(model, test_set_features)
    print(table(test_set$Colors, predictions_test))
    cat(sprintf("Accuracy: %f\n\n", get_accuracy(train_set$Colors, predictions_test)))

    model = svm(Colors ~ ., data = train_set, type = "C-classification", cost = 1, kernel = "linear") # нулевая вероятность ошибки в test

    cat("\nC = 1 -----------\n")

    png("results/SVM/data2_train_set_1.png", width = 600)
    plot(model, train_set, symbolPalette = symbols.pallete, color.palette = area.pallete)
    dev.off()
    predictions_train = predict(model, train_set_features)
    print(table(train_set$Colors, predictions_train))
    cat(sprintf("Accuracy: %f\n\n", get_accuracy(train_set$Colors, predictions_train)))

    png("results/SVM/data2_test_set_1.png", width = 600)
    plot(model, test_set, symbolPalette = symbols.pallete, color.palette = area.pallete)
    dev.off()
    predictions_test = predict(model, test_set_features)
    print(table(test_set$Colors, predictions_test))
    cat(sprintf("Accuracy: %f\n\n", get_accuracy(train_set$Colors, predictions_test)))
}

svmdata3.SVMlab <- function(obj) {
    data_frame <- read.csv("data/svmdata/svmdata3.csv")
    splitted_df <- split_data_train_test(data_frame, 0.7)
    train_set <- splitted_df$train_set
    test_set <- splitted_df$test_set
    test_set_features <- test_set[,-3]

    area.pallete = palette_func
    symbols.pallete = c("blue", "white")

    accuracy_list <- list()
    repeats <- 5
    for(degree_it in 1:10) {
        model = svm(Colors ~ ., data = train_set, type = "C-classification", cost = 1, kernel = "polynomial", degree = degree_it)
        accuracy <- 0.0
        for(it in 1:repeats){
            accuracy <- accuracy + get_accuracy(predict(model, test_set_features), test_set$Colors)
        }
        accuracy_list[degree_it] <- accuracy / repeats
    }

    png("results/SVM/data3_poly_degree.png")
    plot(1:length(accuracy_list), accuracy_list,
        type = "b",
        xlab = "degree",
        ylab = "Accuracy score",
        col="red",
        lwd=3,
        pch=16
        )
    dev.off()

    model = svm(Colors ~ ., data = train_set, type = "C-classification", cost = 1, kernel = "polynomial", degree = 6)
    png("results/SVM/data3_poly.png", width = 600)
    plot(model, test_set, symbolPalette = symbols.pallete, color.palette = area.pallete)
    dev.off()
    cat(sprintf("Polynomial accuracy: %f\n", get_accuracy(test_set$Colors, predict(model, test_set_features))))

    model = svm(Colors ~ ., data = train_set, type = "C-classification", cost = 1, kernel = "radial")
    png("results/SVM/data3_radial.png", width = 600)
    plot(model, test_set, symbolPalette = symbols.pallete, color.palette = area.pallete)
    dev.off()
    cat(sprintf("Radial accuracy: %f\n", get_accuracy(test_set$Colors, predict(model, test_set_features))))

    model = svm(Colors ~ ., data = train_set, type = "C-classification", cost = 1, kernel = "sigmoid", gamma = 1.0)
    png("results/SVM/data3_sigmoid.png", width = 600)
    plot(model, test_set, symbolPalette = symbols.pallete, color.palette = area.pallete)
    dev.off()
    cat(sprintf("Sigmoid accuracy: %f\n", get_accuracy(test_set$Colors, predict(model, test_set_features))))
}


