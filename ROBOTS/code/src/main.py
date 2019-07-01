"""main file"""
import progressbar
from tools import plot_map
from tools import plot_paths
from tools import plot_heuristic_d
from tools import plot_pheromone
from tools import plot_time_correlation
from tools import generate_tables
from tools import plot_path
from graph import Graph
from ant import EAlg
from planning import planning

EALG_OBJ = EAlg(
    50,
    10,
    1.0,
    1.0,
    0.9,
    50
)

def main_test():
    """Main function \n
        Result of this I will use for report"""
    sizes = (25, 50, 100, 250, 500, 1000)
    targets_numbers = (5, 10, 20, 50)
    prog_bar_it = [0]
    max_val = sum(targets_numbers) * len(sizes) * 10
    bar_ = [progressbar.ProgressBar(maxval=max_val).start()]
    for size in sizes:
        for targets_num in targets_numbers:
            time_file_path = "data/time/" + str(size) + "x" + str(size) + "/" + str(targets_num) + ".data"
            file = open(time_file_path, "w+")
            file.write("size: " + str(size) + "\n")
            file.write("targets_num: " + str(targets_num) + "\n")
            file.write("Map\tAntTime\tPlanTime\tFullTime" + "\n")
            ant_times = []
            plan_times = []
            full_times = []
            opt_paths = []
            graphs = []
            for map_it in range(10):
                graph = Graph(size, size, 0.3, 0.1)
                graph.generate()
                path, _, alg_time = planning(prog_bar_it, bar_, graph, EALG_OBJ, targets_num)
                opt_paths.append(path)
                graphs.append(graph)
                ant_times.append(alg_time["AntColony"])
                plan_times.append(alg_time["Planning"])
                full_times.append(alg_time["Whole"])
                file.write(str(map_it) + "\t" + str(alg_time["AntColony"]) + "\t" + str(alg_time["Planning"]) + "\t" + str(alg_time["Whole"]) + "\n")
            ant_times_sort = ant_times
            ant_times_sort.sort()
            ant_idx = ant_times.index(ant_times_sort[4])

            plan_times_sort = plan_times
            plan_times_sort.sort()
            plan_idx = plan_times.index(plan_times_sort[4])

            full_times_sort = full_times
            full_times_sort.sort()
            full_idx = full_times.index(full_times_sort[4])

            file.write("mean map by ant:" + "\t" + str(ant_times[ant_idx]) + "\t" + str(plan_times[ant_idx]) + "\t" + str(full_times[ant_idx]) + "\n")
            file.write("mean map by plan:" + "\t" + str(ant_times[plan_idx]) + "\t" + str(plan_times[plan_idx]) + "\t" + str(full_times[plan_idx]) + "\n")
            file.write("mean map by full:" + "\t" + str(ant_times[full_idx]) + "\t" + str(plan_times[full_idx]) + "\t" + str(full_times[full_idx]) + "\n")
            file.close()

            plot_file_name = "data/mean_paths/" + str(size) + "x" + str(size) + "/" + str(targets_num) + ".png"
            plot_paths(graphs[full_idx], opt_paths[full_idx], plot_file_name)

def examples_of_data():
    """Necessary for report"""
    sizes = [250, 500]
    end_points = [[200, 180],
               [300, 100]]
    for it, _ in enumerate(sizes):
        graph = Graph(sizes[it], sizes[it], 0.3, 0.1)
        graph.generate()
        graph.init_pheromone_n_heuristics(end_points[it])
        caption = str(sizes[it]) + "x" + str(sizes[it])
        plot_heuristic_d(graph, "data/heuristics_example/heuristic_d_" + caption + ".png")
        plot_pheromone(graph, "data/heuristics_example/pheromone_" + caption + ".png")
        # plot_map(graph, "data/maps_example/" + caption + ".png")

def dev_test():
    """Function for development \n
        I use it for testing components"""
    size = 1000
    graph = Graph(size, size, 0.3, 0.2)
    graph.generate()
    prog_bar_it = [0]
    max_val = 50
    bar_ = [progressbar.ProgressBar(maxval=max_val).start()]
    opt_paths, _, alg_time = planning(prog_bar_it, bar_, graph, EALG_OBJ, 50)
    print(alg_time)
    plot_paths(graph, opt_paths, "data/mean_paths/test.png")

def single_path_test():
    """plot single paths for different maps"""
    sizes = [250, 500]
    robots = [[50, 80],
              [200, 460]]
    targets = [[200, 180],
               [300, 100]]
    file = open("data/path_example/costs.data", "w+")
    for it, _ in enumerate(sizes):
        graph = Graph(sizes[it], sizes[it], 0.3, 0.2)
        graph.generate()
        path, cost = EALG_OBJ.get_path(graph, robots[it], targets[it])
        caption = str(sizes[it]) + "x" + str(sizes[it])
        plot_path(graph, path, "data/path_example/" + caption + ".png")
        file.write(caption + ":\t" + str(cost) + "\n")
    file.close()

def time_correlation():
    """plot surface with mean times by ready data"""
    sizes = (25, 50, 100, 250, 500, 1000)
    targets_numbers = (5, 10, 20, 50)
    plot_time_correlation(sizes, targets_numbers)
    generate_tables(sizes, targets_numbers)

# single_path_test()
# examples_of_data()
# dev_test()
# main_test()
time_correlation()
