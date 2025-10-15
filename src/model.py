import gurobipy as gp
from gurobipy import GRB 
from src.parse import parse_instance
from src.utils import extract_model_stats
from src.valid_inequalities import valid_inequality_1, valid_inequality_2, valid_inequality_3, valid_inequality_4
from src.env_utils import create_env
import time

env = create_env(
    logfile=None,   
    output_flag=False,                
    mip_gap=0.01,               
    presolve=-1            
)


def build_model(I, I0, S, Q, q, L, t, c, r, use_vi1=False, use_vi2=False, use_vi3=False, use_vi4=False, timelimit=600):

    Imax = len(I)


    model = gp.Model("ShipRouting", env=env)

    X = model.addVars(I0, I0, S, vtype=GRB.BINARY, name="X")
    Y = model.addVars(I0, S, vtype=GRB.BINARY, name="Y")
    u = model.addVars(I, vtype=GRB.INTEGER, name="u")
    l = model.addVars(I0, S, vtype=GRB.CONTINUOUS, name="l")
    p = model.addVars(S, vtype=GRB.CONTINUOUS, name="p")

    model.setObjective(
        gp.quicksum(c[s] * t[i][j] * X[i, j, s] for i in I0 for j in I0 for s in S) +
        gp.quicksum(r[i-1][s] * Y[i, s] for i in I for s in S),
        GRB.MINIMIZE
    )

    for i in I:
        model.addConstr(gp.quicksum(Y[i, s] for s in S) == 1)

    for s in S:
        model.addConstr(gp.quicksum(q[i] * Y[i, s] for i in I) <= Q[s])

    for j in I:
        for s in S:
            model.addConstr(gp.quicksum(X[i, j, s] for i in I0 if i != j) ==
                            gp.quicksum(X[j, k, s] for k in I0 if k != j))
            
    for j in I:
        for s in S:
            model.addConstr(gp.quicksum(X[i, j, s] for i in I0 if i != j) == Y[j, s])

    for s in S:
        model.addConstr(
            gp.quicksum(X[0, j, s] for j in I) <= gp.quicksum(Y[j, s] for j in I)
        )
        model.addConstr(
            gp.quicksum(X[0, j, s] for j in I) >= gp.quicksum(Y[j, s] for j in I) / Imax
        )
    
    for i in I:
        for j in I:
            if i != j:
                for s in S:
                    model.addConstr(u[j] >= u[i] + 1 - Imax * (1 - X[i, j, s]))
    
    for i in I:
        for j in I:
            for s in S:
                model.addConstr(l[j, s] >= l[i, s] - q[i] - Q[s] * (1 - X[i, j, s]))
    
    for i in I:
        for s in S:
            model.addConstr(l[i, s] <= L[i-1][s])
    
    for s in S:
        model.addConstr(p[s] == gp.quicksum(q[i] * Y[i, s] for i in I))

    TOTq  = sum(q[1:])  
    q_big = max(q[1:])     
    Qmax  = max(Q)      

    sorted_q = sorted(q[1:])
    cum, Istar = 0, 0
    for demand in sorted_q:
        if cum + demand <= Qmax:
            cum += demand
            Istar += 1
        else:
            break
        
    if use_vi1:
        valid_inequality_1(model, X, Y, q, L, TOTq, I, S)

    if use_vi2:
        valid_inequality_2(model, X, Y, q, L, I, S)

    if use_vi3:
        valid_inequality_3(model, X, Y, q_big, L, p, u, Q, I, S)

    if use_vi4:
        valid_inequality_4(model, X, Y, q, L, u, Istar, I, S)

    model.Params.TimeLimit = timelimit
    model._X = X
    model._Y = Y

    return model

def solve_model(model):
    model.optimize()
    if model.status == GRB.OPTIMAL or model.status == GRB.TIME_LIMIT:
        X = model._X
        Y = model._Y
        stats = extract_model_stats(model)
        return stats, X, Y
    else:
        return None, None, None

def solutions(params, vi1=False, vi2=False, vi3=False, vi4=False):
    start = time.time()
    model_results_base, _, _ = solve_model(build_model(*params,
        vi1, vi2, vi3, vi4, timelimit=600))
    end = time.time()
    model_results_base['RuntimeTotal'] = end - start
    
    return model_results_base