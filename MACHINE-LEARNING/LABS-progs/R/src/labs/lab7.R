library(cluster)

ClusterLab <- function() {
    value <- list()
    attr(value, "class") <- "ClusterLab"
    value
}

plutonset <- function(obj) {
    data(pluton)
    data_frame <- pluton[,-c(1,2)]
    model_1 <- kmeans(data_frame, 3, iter.max = 1)
    model_1000 <- kmeans(data_frame, 3, iter.max = 1000)
    model_2000 <- kmeans(data_frame, 3, iter.max = 2000)
    png("results/Cluster/pluton_clustering.png", width = 800)
    plot(data_frame, col = model_1$cluster)
    points(data_frame, col = model_1000$cluster, cex = 4)
    points(data_frame, col = model_2000$cluster, cex = 7)
    dev.off()
}

generated <- function(obj) {
    clust_1_x <- rnorm(100, mean = 200, sd = 60)
    clust_1_y <- rnorm(100, mean = 10, sd = 10)
    clust_2_x <- rnorm(100, mean = 10, sd = 20)
    clust_2_y <- rnorm(100, mean = 400, sd = 200)
    clust_3_x <- rnorm(100, mean = 200, sd = 50)
    clust_3_y <- rnorm(100, mean = 800, sd = 10)

    x <- as.matrix(c(clust_1_x, clust_2_x, clust_3_x))
    y <- as.matrix(c(clust_1_y, clust_2_y, clust_3_y))

    data_frame <- data.frame(x,y)

    png("results/Cluster/generated.png")
    par(mfrow = c(2,2))
    model <- clara(data_frame, 3, metric = c("manhattan"), stand = TRUE )
    plot(data_frame, col = model$clustering, xlab = "x", ylab = "y")
    title("manhattan, TRUE")

    model <- clara(data_frame, 3, metric = c("manhattan"), stand = FALSE)
    plot(data_frame, col = model$clustering, xlab = "x", ylab = "y")
    title("manhattan, FALSE")

    model <- clara(data_frame, 3, metric = c("euclidean"), stand = TRUE)
    plot(data_frame, col = model$clustering, xlab = "x", ylab = "y")
    title("euclidean, TRUE")

    model <- clara(data_frame, 3, metric = c("euclidean"), stand = FALSE)
    plot(data_frame, col = model$clustering, xlab = "x", ylab = "y")
    title("euclidean, FALSE")
    dev.off()
}

votesset <- function(obj) {
    data(vores.repub)
    png("results/Cluster/votes.png", 900)
    plot(agnes(votes.repub))
    dev.off()
}

animals <- function(obj) {
    data(animals)
    png("results/Cluster/animals.png", 900)
    plot(agnes(animals))
    dev.off()
}

seeds <- function(obj) {
    data_frame <- read.table("data/seeds_dataset.data")
    model <- kmeans(data_frame, 3)
    png("results/Cluster/seeds.png")
    plot(data_frame, col = model$cluster)
    dev.off()
}