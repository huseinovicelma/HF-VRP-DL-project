from src.parse import parse_instance
import csv
from src.model import solutions
from src.heuristics import lns_matheuristic, ils_matheuristic
from src.utils import save_stats, get_parameters, configs
from src.utils import configs, get_parameters, print_stats

'''for i in range(1, 2):
    instance_path = f"dataset/r_15_30_30_30/r_15_30_30_30_{i}.txt"
    params = get_parameters(instance_path)

    for name, (vi1, vi2, vi3, vi4) in configs.items():
        model_results_base = solutions(params, vi1, vi2, vi3, vi4)
        print_stats(model_results_base, title=f"Instance {i} - Base Model with {name}")
    _ , _ , model_results_lns = lns_matheuristic(*params)
    print_stats(model_results_lns, title=f"Instance {i} - LNS with No VI")
    _ , _ , model_results_ils = ils_matheuristic(*params)
    print_stats(model_results_ils, title=f"Instance {i} - ILS with No VI")'''



with open("results/results_25_70_30_1.csv", mode="a", newline="") as f:
        writer = None
        instance_path = f"dataset/r_25_70_30_70/r_25_70_30_1.txt"
        folder_path = "dataset/r_25_70_30_1"
        instance_name = 'r_25_70_30_1'
        params = get_parameters(instance_path)

        for name, (vi1, vi2, vi3, vi4) in configs.items():
            stats = solutions(params, vi1, vi2, vi3, vi4)
            if writer is None:
                writer = csv.DictWriter(f, fieldnames=["Instance", "Algorithm", "Config"] + list(stats.keys()))
                writer.writeheader()
            save_stats(stats, writer, instance_name, "base", name)

        _, _, stats_lns = lns_matheuristic(*params)
        save_stats(stats_lns, writer, instance_name, "lns", "base")

        _, _, stats_ils = ils_matheuristic(*params)
        save_stats(stats_ils, writer, instance_name, "ils", "base")


with open("results/results_25_70_30_70_1.csv", mode="a", newline="") as f:
        writer = None
        instance_path = f"dataset/r_25_70_30_70/r_25_70_30_70_1.txt"
        folder_path = "dataset/r_25_70_30_70_1"
        instance_name = 'r_25_70_30_70_1'
        params = get_parameters(instance_path)

        for name, (vi1, vi2, vi3, vi4) in configs.items():
            stats = solutions(params, vi1, vi2, vi3, vi4)
            if writer is None:
                writer = csv.DictWriter(f, fieldnames=["Instance", "Algorithm", "Config"] + list(stats.keys()))
                writer.writeheader()
            save_stats(stats, writer, instance_name, "base", name)

        _, _, stats_lns = lns_matheuristic(*params)
        save_stats(stats_lns, writer, instance_name, "lns", "base")

        _, _, stats_ils = ils_matheuristic(*params)
        save_stats(stats_ils, writer, instance_name, "ils", "base")

with open("results/results_25_70_30_70_2.csv", mode="a", newline="") as f:
        writer = None
        instance_path = f"dataset/r_25_70_30_70/r_25_70_30_70_2.txt"
        folder_path = "dataset/r_25_70_30_70_2"
        instance_name = 'r_25_70_30_70_2'
        params = get_parameters(instance_path)

        for name, (vi1, vi2, vi3, vi4) in configs.items():
            stats = solutions(params, vi1, vi2, vi3, vi4)
            if writer is None:
                writer = csv.DictWriter(f, fieldnames=["Instance", "Algorithm", "Config"] + list(stats.keys()))
                writer.writeheader()
            save_stats(stats, writer, instance_name, "base", name)

        _, _, stats_lns = lns_matheuristic(*params)
        save_stats(stats_lns, writer, instance_name, "lns", "base")

        _, _, stats_ils = ils_matheuristic(*params)
        save_stats(stats_ils, writer, instance_name, "ils", "base")

with open("results/results_25_70_30_70_3.csv", mode="a", newline="") as f:
        writer = None
        instance_path = f"dataset/r_25_70_30_70/r_25_70_30_70_3.txt"
        folder_path = "dataset/r_25_70_30_70_3"
        instance_name = 'r_25_70_30_70_3'
        params = get_parameters(instance_path)

        for name, (vi1, vi2, vi3, vi4) in configs.items():
            stats = solutions(params, vi1, vi2, vi3, vi4)
            if writer is None:
                writer = csv.DictWriter(f, fieldnames=["Instance", "Algorithm", "Config"] + list(stats.keys()))
                writer.writeheader()
            save_stats(stats, writer, instance_name, "base", name)

        _, _, stats_lns = lns_matheuristic(*params)
        save_stats(stats_lns, writer, instance_name, "lns", "base")

        _, _, stats_ils = ils_matheuristic(*params)
        save_stats(stats_ils, writer, instance_name, "ils", "base")

with open("results/results_25_70_30_70_4.csv", mode="a", newline="") as f:
        writer = None
        instance_path = f"dataset/r_25_70_30_70/r_25_70_30_70_4.txt"
        folder_path = "dataset/r_25_70_30_70_4"
        instance_name = 'r_25_70_30_70_4'
        params = get_parameters(instance_path)

        for name, (vi1, vi2, vi3, vi4) in configs.items():
            stats = solutions(params, vi1, vi2, vi3, vi4)
            if writer is None:
                writer = csv.DictWriter(f, fieldnames=["Instance", "Algorithm", "Config"] + list(stats.keys()))
                writer.writeheader()
            save_stats(stats, writer, instance_name, "base", name)

        _, _, stats_lns = lns_matheuristic(*params)
        save_stats(stats_lns, writer, instance_name, "lns", "base")

        _, _, stats_ils = ils_matheuristic(*params)
        save_stats(stats_ils, writer, instance_name, "ils", "base")


with open("results/results_25_70_30_70_5.csv", mode="a", newline="") as f:
        writer = None
        instance_path = f"dataset/r_25_70_30_70/r_25_70_30_70_5.txt"
        folder_path = "dataset/r_25_70_30_70_5"
        instance_name = 'r_25_70_30_70_5'
        params = get_parameters(instance_path)

        for name, (vi1, vi2, vi3, vi4) in configs.items():
            stats = solutions(params, vi1, vi2, vi3, vi4)
            if writer is None:
                writer = csv.DictWriter(f, fieldnames=["Instance", "Algorithm", "Config"] + list(stats.keys()))
                writer.writeheader()
            save_stats(stats, writer, instance_name, "base", name)

        _, _, stats_lns = lns_matheuristic(*params)
        save_stats(stats_lns, writer, instance_name, "lns", "base")

        _, _, stats_ils = ils_matheuristic(*params)
        save_stats(stats_ils, writer, instance_name, "ils", "base")

with open("results/results_25_70_30_70_6.csv", mode="a", newline="") as f:
        writer = None
        instance_path = f"dataset/r_25_70_30_70/r_25_70_30_70_6.txt"
        folder_path = "dataset/r_25_70_30_70_6"
        instance_name = 'r_25_70_30_70_6'
        params = get_parameters(instance_path)

        for name, (vi1, vi2, vi3, vi4) in configs.items():
            stats = solutions(params, vi1, vi2, vi3, vi4)
            if writer is None:
                writer = csv.DictWriter(f, fieldnames=["Instance", "Algorithm", "Config"] + list(stats.keys()))
                writer.writeheader()
            save_stats(stats, writer, instance_name, "base", name)

        _, _, stats_lns = lns_matheuristic(*params)
        save_stats(stats_lns, writer, instance_name, "lns", "base")

        _, _, stats_ils = ils_matheuristic(*params)
        save_stats(stats_ils, writer, instance_name, "ils", "base")


with open("results/results_25_70_30_70_7.csv", mode="a", newline="") as f:
        writer = None
        instance_path = f"dataset/r_25_70_30_70/r_25_70_30_70_7.txt"
        folder_path = "dataset/r_25_70_30_70_7"
        instance_name = 'r_25_70_30_70_7'
        params = get_parameters(instance_path)

        for name, (vi1, vi2, vi3, vi4) in configs.items():
            stats = solutions(params, vi1, vi2, vi3, vi4)
            if writer is None:
                writer = csv.DictWriter(f, fieldnames=["Instance", "Algorithm", "Config"] + list(stats.keys()))
                writer.writeheader()
            save_stats(stats, writer, instance_name, "base", name)

        _, _, stats_lns = lns_matheuristic(*params)
        save_stats(stats_lns, writer, instance_name, "lns", "base")

        _, _, stats_ils = ils_matheuristic(*params)
        save_stats(stats_ils, writer, instance_name, "ils", "base")


with open("results/results_25_70_30_70_7.csv", mode="a", newline="") as f:
        writer = None
        instance_path = f"dataset/r_25_70_30_70/r_25_70_30_70_7.txt"
        folder_path = "dataset/r_25_70_30_70_7"
        instance_name = 'r_25_70_30_70_7'
        params = get_parameters(instance_path)

        for name, (vi1, vi2, vi3, vi4) in configs.items():
            stats = solutions(params, vi1, vi2, vi3, vi4)
            if writer is None:
                writer = csv.DictWriter(f, fieldnames=["Instance", "Algorithm", "Config"] + list(stats.keys()))
                writer.writeheader()
            save_stats(stats, writer, instance_name, "base", name)

        _, _, stats_lns = lns_matheuristic(*params)
        save_stats(stats_lns, writer, instance_name, "lns", "base")

        _, _, stats_ils = ils_matheuristic(*params)
        save_stats(stats_ils, writer, instance_name, "ils", "base")


with open("results/results_25_70_30_70_8.csv", mode="a", newline="") as f:
        writer = None
        instance_path = f"dataset/r_25_70_30_70/r_25_70_30_70_8.txt"
        folder_path = "dataset/r_25_70_30_70_8"
        instance_name = 'r_25_70_30_70_8'
        params = get_parameters(instance_path)

        for name, (vi1, vi2, vi3, vi4) in configs.items():
            stats = solutions(params, vi1, vi2, vi3, vi4)
            if writer is None:
                writer = csv.DictWriter(f, fieldnames=["Instance", "Algorithm", "Config"] + list(stats.keys()))
                writer.writeheader()
            save_stats(stats, writer, instance_name, "base", name)

        _, _, stats_lns = lns_matheuristic(*params)
        save_stats(stats_lns, writer, instance_name, "lns", "base")

        _, _, stats_ils = ils_matheuristic(*params)
        save_stats(stats_ils, writer, instance_name, "ils", "base")


with open("results/results_25_70_30_70_9.csv", mode="a", newline="") as f:
        writer = None
        instance_path = f"dataset/r_25_70_30_70/r_25_70_30_70_9.txt"
        folder_path = "dataset/r_25_70_30_70_9"
        instance_name = 'r_25_70_30_70_9'
        params = get_parameters(instance_path)

        for name, (vi1, vi2, vi3, vi4) in configs.items():
            stats = solutions(params, vi1, vi2, vi3, vi4)
            if writer is None:
                writer = csv.DictWriter(f, fieldnames=["Instance", "Algorithm", "Config"] + list(stats.keys()))
                writer.writeheader()
            save_stats(stats, writer, instance_name, "base", name)

        _, _, stats_lns = lns_matheuristic(*params)
        save_stats(stats_lns, writer, instance_name, "lns", "base")

        _, _, stats_ils = ils_matheuristic(*params)
        save_stats(stats_ils, writer, instance_name, "ils", "base")


with open("results/results_25_70_30_70_10.csv", mode="a", newline="") as f:
        writer = None
        instance_path = f"dataset/r_25_70_30_70/r_25_70_30_70_10.txt"
        folder_path = "dataset/r_25_70_30_70_10"
        instance_name = 'r_25_70_30_70_10'
        params = get_parameters(instance_path)

        for name, (vi1, vi2, vi3, vi4) in configs.items():
            stats = solutions(params, vi1, vi2, vi3, vi4)
            if writer is None:
                writer = csv.DictWriter(f, fieldnames=["Instance", "Algorithm", "Config"] + list(stats.keys()))
                writer.writeheader()
            save_stats(stats, writer, instance_name, "base", name)

        _, _, stats_lns = lns_matheuristic(*params)
        save_stats(stats_lns, writer, instance_name, "lns", "base")

        _, _, stats_ils = ils_matheuristic(*params)
        save_stats(stats_ils, writer, instance_name, "ils", "base")


