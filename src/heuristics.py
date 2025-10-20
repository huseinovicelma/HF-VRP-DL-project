import random
import time
from src.model import build_model, solve_model
import time

def lns_matheuristic(I, I0, S, Q, q, L, t, c, r, ITERMAX=50, MAXNOIMPROVE=10, m_remove=5, alpha=1.5, timelimit=15):

    start = time.time()

    model = build_model(I, I0, S, Q, q, L, t, c, r, use_vi1=False, use_vi2=False, use_vi3=False, use_vi4=False, timelimit=15)

    model_results, X, Y = solve_model(model)

    omega_best = {}
    for (i, j, s), var in X.items():
        omega_best[f"X[{i},{j},{s}]"] = var.X
    omega_best_obj = model_results['ObjVal']
    model_results_best = model_results
    no_improve = 0

    for iter in range(ITERMAX):
        if no_improve >= MAXNOIMPROVE:
            break

        omega_R = omega_best.copy()

        I_R = set(random.sample(I, m_remove))


        for i in list(I_R):
            nu_i = min(t[i][j] for j in I if j != i)
            rho_i = alpha * nu_i
            for j in I:
                if j not in I_R and t[i][j] <= rho_i:
                    I_R.add(j)

        model_rebuild = build_model(I, I0, S, Q, q, L, t, c, r,
                                    use_vi1=False, use_vi2=False, use_vi3=False, use_vi4=False,
                                    timelimit=timelimit)

        Xr = model_rebuild._X

        for (i, j, s) in Xr.keys():
            varname = f"X[{i},{j},{s}]"
            if varname in omega_R and i not in I_R and j not in I_R:
                Xr[i, j, s].lb = Xr[i, j, s].ub = omega_R[varname]

        model_results_new, X_new, Y_new = solve_model(model_rebuild)

        if X_new is None:
            continue
            
        omega_new = {}
        for (i, j, s), var in X_new.items():
            omega_new[f"X[{i},{j},{s}]"] = var.X
        omega_new_obj = model_results_new["ObjVal"]

        if omega_new_obj < omega_best_obj:
            omega_best = omega_new
            omega_best_obj = omega_new_obj
            model_results_best = model_results_new
            no_improve = 0
        else:
            no_improve += 1
        
    end = time.time()
    model_results_best['RuntimeTotal'] = end - start

    
    return omega_best, omega_best_obj, model_results_best


def ils_matheuristic(I, I0, S, Q, q, L, t, c, r, ITERMAX=50, MAXNOIMPROVE=10,
                     m_remove=5, alpha=1.5, timelimit=15):
    
    start = time.time()

    model = build_model(I, I0, S, Q, q, L, t, c, r,
                        use_vi1=False, use_vi2=False, use_vi3=False, use_vi4=False,
                        timelimit=timelimit)
    model_results, X, Y = solve_model(model)

    omega_best = {}
    for (i, j, s), var in X.items():
        omega_best[f"X[{i},{j},{s}]"] = var.X
    omega_best_obj = model_results['ObjVal']
    model_results_best = model_results
    no_improve = 0
    
    omega_new = omega_best.copy()
    omega_new_obj = omega_best_obj

    for iter in range(ITERMAX):
        if no_improve >= MAXNOIMPROVE:
            break

        omega_new, omega_new_obj, model_results_new = local_search_ls(I, I0, S, Q, q, L, t, c, r,
                                                   omega_new, m_remove, alpha, timelimit)

        if omega_new_obj < omega_best_obj:
            omega_best, omega_best_obj = omega_new, omega_new_obj
            model_results_best = model_results_new
            no_improve = 0
        else:

            omega_new, omega_new_obj, model_results_new = diversification_div(I, I0, S, Q, q, L, t, c, r,
                                                           omega_best, m_remove, alpha, timelimit)
            
            if omega_new_obj < omega_best_obj:
                omega_best, omega_best_obj = omega_new, omega_new_obj
                model_results_best = model_results_new
                no_improve = 0
            else:
                no_improve += 1
    
    end = time.time()
    model_results_best['RuntimeTotal'] = end - start

    return omega_best, omega_best_obj, model_results_best


def local_search_ls(I, I0, S,Q, q, L, t, c, r, omega_current, m_remove=5, alpha=1.5, timelimit=15):

    lambdas = []
    for i in I:
        lambda_i = max(max(t[i]), max(row[i] for row in t))  
        lambdas.append((i, lambda_i)) 

    lambdas.sort(key=lambda x: x[1], reverse=True)
    I_R = {i for i, _ in lambdas[:m_remove]}

    for i in list(I_R):
        nu_i = min(t[i][j] for j in I if j != i)
        rho_i = alpha * nu_i
        for j in I:
            if j not in I_R and t[i][j] <= rho_i:
                I_R.add(j)

    model_rebuild = build_model(I, I0, S, Q, q, L, t, c, r,
                                use_vi1=False, use_vi2=False, use_vi3=False, use_vi4=False,
                                timelimit=timelimit)
    Xr = model_rebuild._X

    omega_best_arcs = {
        (i, j, s)
        for (i, j, s) in Xr.keys()
        if f"X[{i},{j},{s}]" in omega_current and omega_current[f"X[{i},{j},{s}]"] > 0.5
    }

    omega_R = {(i, j, s) for (i, j, s) in omega_best_arcs if i not in I_R and j not in I_R}

    for (i, j, s) in omega_R:
        Xr[i, j, s].lb = Xr[i, j, s].ub = 1.0

    model_results, X_new, Y_new = solve_model(model_rebuild)

    omega_new = {}
    for (i, j, s), var in X_new.items():
        omega_new[f"X[{i},{j},{s}]"] = var.X
    omega_new_obj = model_results['ObjVal']
    model_results_new = model_results
    
    return omega_new, omega_new_obj, model_results_new


def diversification_div(I, I0, S, Q, q, L, t, c, r, omega_best, m_remove, alpha, timelimit):

    I_R = set(random.sample(I, m_remove))
    
    for i in list(I_R):
        nu_i = min(t[i][j] for j in I if j != i)
        rho_i = alpha * nu_i  
        for j in I:
            if j not in I_R and t[i][j] <= rho_i:
                I_R.add(j)

    model_rebuild = build_model(I, I0, S, Q, q, L, t, c, r,
                                use_vi1=False, use_vi2=False, use_vi3=False, use_vi4=False,
                                timelimit=timelimit)
    Xr = model_rebuild._X

    omega_best_arcs = {
        (i, j, s)
        for (i, j, s) in Xr.keys()
        if f"X[{i},{j},{s}]" in omega_best and omega_best[f"X[{i},{j},{s}]"] > 0.5
    }

    omega_R = {(i, j, s) for (i, j, s) in omega_best_arcs if i not in I_R and j not in I_R}
    

    for (i, j, s) in omega_R:
        Xr[i, j, s].lb = Xr[i, j, s].ub = 1.0

    model_results, X_new, Y_new = solve_model(model_rebuild)

    omega_new = {}
    for (i, j, s), var in X_new.items():
        omega_new[f"X[{i},{j},{s}]"] = var.X
    omega_new_obj = model_results['ObjVal']
    model_results_new = model_results
    
    return omega_new, omega_new_obj, model_results_new
