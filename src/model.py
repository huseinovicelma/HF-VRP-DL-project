# src/model.py

from gurobipy import Model, GRB, quicksum
from .valid_inequalities import add_vi1, add_vi2, add_vi3, add_vi4

def build_model(data, vi_flags, fixed_arcs=None):
    ships, ports, distances, q, Q, c, r, L = data
    port_ids = [p['id'] for p in ports]
    depot = port_ids[0]
    ship_ids = [s['id'] for s in ships]
    I0 = port_ids
    I = port_ids[1:]
    S = ship_ids

    demand = {p['id']: p['demand'] for p in ports}
    capacity = {s['id']: s['capacity'] for s in ships}
    cost = {s['id']: s['cost_per_unit'] for s in ships}
    t = distances
    r_is = {}
    for i in port_ids:
        for k in ship_ids:
            r_is[(i, k)] = ships[int(k[1:])-1]['draft_empty']
    L_dict = {}
    for i, p in enumerate(ports):
        for k in ship_ids:
            L_dict[(p['id'], k)] = L[i][int(k[1:])-1] if i < len(L) and int(k[1:])-1 < len(L[i]) else 9999

    m = Model("HF-VRP-DL")
    m.setParam('OutputFlag', 0)

    # Variabili
    X = m.addVars(I0, I0, S, vtype=GRB.BINARY, name="X")
    Y = m.addVars(I, S, vtype=GRB.BINARY, name="Y")
    l = m.addVars(I0, S, vtype=GRB.CONTINUOUS, name="l")
    u = m.addVars(I, S, vtype=GRB.INTEGER, lb=1, ub=len(I), name="u")

    # Funzione obiettivo
    m.setObjective(
        quicksum(cost[k] * t[i, j] * X[i, j, k] for i in I0 for j in I0 for k in S if i != j) +
        quicksum(r_is[(i, k)] * Y[i, k] for i in I for k in S),
        GRB.MINIMIZE
    )

    # (2) Ogni porto servito da una sola nave
    for i in I:
        m.addConstr(quicksum(Y[i, k] for k in S) == 1)

    # (3) Capacità nave
    for k in S:
        m.addConstr(quicksum(demand[i] * Y[i, k] for i in I) <= capacity[k])

    # (4) Flusso: ogni porto visitato da una nave deve essere raggiunto
    for j in I:
        for k in S:
            m.addConstr(quicksum(X[i, j, k] for i in I0 if i != j) == Y[j, k])

    # (5) Flusso: ogni porto visitato da una nave deve essere lasciato
    for i in I:
        for k in S:
            m.addConstr(quicksum(X[i, j, k] for j in I0 if j != i) == Y[i, k])

    # (6) Ogni nave entra ed esce dal deposito solo se serve almeno un porto
    for k in S:
        m.addConstr(quicksum(X[depot, j, k] for j in I) == quicksum(Y[j, k] for j in I))
        m.addConstr(quicksum(X[j, depot, k] for j in I) == quicksum(Y[j, k] for j in I))

    # (8) Subtour elimination (MTZ-like)
    for i in I:
        for j in I:
            if i != j:
                for k in S:
                    m.addConstr(u[i, k] - u[j, k] + len(I) * X[i, j, k] <= len(I) - 1)
    # (9) Carico nave in ingresso nei porti
    for i in I:
        for j in I:
            if i != j:
                for k in S:
                    m.addConstr(l[j, k] >= l[i, k] - demand[j] * X[i, j, k] - capacity[k] * (1 - X[i, j, k]))

    # (10) Limite di carico massimo per accedere al porto
    for i in I:
        for k in S:
            m.addConstr(l[i, k] <= L_dict[(i, k)])

    # (11) Carico nave in uscita dal deposito
    for k in S:
        m.addConstr(l[depot, k] == quicksum(demand[i] * Y[i, k] for i in I))


    # Valid inequalities (attivabili con vi_flags)
    if vi_flags.get('vi1', False):
        add_vi1(m, I0, S, L_dict, ships, X)
    if vi_flags.get('vi2', False):
        add_vi2(m, I0, X, S, demand, capacity)
    if vi_flags.get('vi3', False):
        add_vi3(m, Y, I, S, L_dict, ships)
    if vi_flags.get('vi4', False):
        add_vi4(m, Y, I, S, demand, capacity)

    if fixed_arcs is not None:
        for (i, j, k) in fixed_arcs:
            m.addConstr(X[i, j, k] == 1)

    return m