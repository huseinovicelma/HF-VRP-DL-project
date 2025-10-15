from src.parse import parse_instance
from src.model import solutions
from src.heuristics import lns_matheuristic, ils_matheuristic
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




instance_path = f"dataset/r_50/r_50_70_30_70_4.txt"
params = get_parameters(instance_path)
_ , _ , model_results_ils = ils_matheuristic(*params)
print_stats(model_results_ils, title=f"Instance - ILS with No VI")