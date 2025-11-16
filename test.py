
from src.model import solutions
from src.heuristics import lns_matheuristic, ils_matheuristic
from src.utils import get_parameters, configs
from src.utils import configs, get_parameters, print_stats

for i in range(3, 6):
    instance_path = f"dataset/r_15_30_30_30/r_15_30_30_30_{i}.txt"
    params = get_parameters(instance_path)

    for name, (vi1, vi2, vi3, vi4) in configs.items():
        model_results_base = solutions(params, vi1, vi2, vi3, vi4)
        print_stats(model_results_base, title=f"Instance {i} - Base Model with {name}")
    _ , _ , model_results_lns = lns_matheuristic(*params)
    print_stats(model_results_lns, title=f"Instance {i} - LNS with No VI")
    _ , _ , model_results_ils = ils_matheuristic(*params)
    print_stats(model_results_ils, title=f"Instance {i} - ILS with No VI")

