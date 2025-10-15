import os
import csv
from src.utils import save_stats, get_parameters, configs
from src.model import solutions
from src.heuristics import lns_matheuristic, ils_matheuristic

folder_path = "dataset/r_15_30_30_70"

def run_all(dataset_dir, configs, output_csv):
    with open(output_csv, mode="a", newline="") as f:
        writer = None

        for folder in sorted(os.listdir(dataset_dir)):
            folder_path = os.path.join(dataset_dir, folder)
            if not os.path.isdir(folder_path):
                continue

            for filename in sorted(os.listdir(folder_path)):
                if filename.startswith("r_") and filename.endswith(".txt"):
                    instance_path = os.path.join(folder_path, filename)
                    instance_name = filename
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



def run_one_folder(folder_path):
    with open("results/results_2.csv", mode="a", newline="") as f:
        writer = None
        for filename in sorted(os.listdir(folder_path)):
            if filename.startswith("r_") and filename.endswith(".txt"):
                instance_path = os.path.join(folder_path, filename)
                instance_name = filename
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

run_one_folder(folder_path)