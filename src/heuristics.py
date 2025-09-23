import random
import time

# =========================
# Funzioni di supporto
# =========================

def remove_arcs(solution, nodes):
    # Rimuove tutti gli archi entranti e uscenti dai nodi in 'nodes'
    new_arcs = set()
    for (i, j, k) in solution['arcs']:
        if i not in nodes and j not in nodes:
            new_arcs.add((i, j, k))
    return {'arcs': new_arcs, 'cost': solution['cost']}

def solve_overconstrained(data, build_model, fixed_arcs):
    # Costruisci e risolvi il modello con alcuni archi fissati a 1
    m = build_model(data, vi_flags={},fixed_arcs=fixed_arcs)
    m.optimize()
    if m.status == 2:
        arcs = set()
        for v in m.getVars():
            if v.varName.startswith("X[") and v.x > 0.5:
                # Estrai indici da varName tipo X[P1,P2,N1]
                idx = v.varName[2:-1].split(',')
                arcs.add(tuple(idx))
        return {'arcs': arcs, 'cost': m.objVal}
    else:
        return {'arcs': set(), 'cost': float('inf')}

def initial_solution(data, build_model):
    # Soluzione iniziale: modello esatto senza archi fissati
    m = build_model(data, vi_flags={})
    m.optimize()
    if m.status == 2:
        arcs = set()
        for v in m.getVars():
            if v.varName.startswith("X[") and v.x > 0.5:
                idx = v.varName[2:-1].split(',')
                arcs.add(tuple(idx))
        return {'arcs': arcs, 'cost': m.objVal}
    else:
        return {'arcs': set(), 'cost': float('inf')}

# =========================
# ALGORITHM 4: Diversification DIV
# =========================
def diversification_DIV(solution, ports, t, rho, m_pert, build_model, data):
    IR = set()
    OmegaR = solution['arcs'].copy()
    I = set(ports)
    # Step 3-6: Randomly select m_pert ports
    for _ in range(m_pert):
        candidates = list(I - IR)
        if not candidates:
            break
        j = random.choice(candidates)
        IR.add(j)
    # Step 7-11: Add close ports
    for i in IR.copy():
        for j in I - IR:
            if t[i][j] <= rho[i]:
                IR.add(j)
    # Step 12-14: Remove arcs entering/exiting IR from OmegaR
    OmegaR = set([arc for arc in OmegaR if arc[0] not in IR and arc[1] not in IR])
    # Step 15-16: Fissa archi attivi in OmegaR a 1 e risolvi modello over-constrained
    Omega_new = solve_overconstrained(data, build_model, fixed_arcs=OmegaR)
    return Omega_new

# =========================
# ALGORITHM 2: Intensification INT
# =========================
def intensification_INT(solution, ports, t, rho, m_pert, build_model, data):
    # Simile a DIV ma scegli i porti in modo deterministico (es: quelli con costo maggiore)
    IR = set()
    OmegaR = solution['arcs'].copy()
    I = set(ports)
    # Step 3-6: Scegli i m_pert porti con grado uscente maggiore
    port_scores = {j: sum(1 for arc in OmegaR if arc[0] == j) for j in I}
    sorted_ports = sorted(port_scores, key=port_scores.get, reverse=True)
    for j in sorted_ports[:m_pert]:
        IR.add(j)
    # Step 7-11: Add close ports
    for i in IR.copy():
        for j in I - IR:
            if t[i][j] <= rho[i]:
                IR.add(j)
    # Step 12-14: Remove arcs entering/exiting IR from OmegaR
    OmegaR = set([arc for arc in OmegaR if arc[0] not in IR and arc[1] not in IR])
    Omega_new = solve_overconstrained(data, build_model, fixed_arcs=OmegaR)
    return Omega_new

# =========================
# ALGORITHM 3: Reconstruction REC
# =========================
def reconstruction_REC(solution, ports, t, rho, m_pert, build_model, data):
    # Scegli m_pert porti a caso e rimuovi solo gli archi uscenti
    IR = set()
    OmegaR = solution['arcs'].copy()
    I = set(ports)
    for _ in range(m_pert):
        candidates = list(I - IR)
        if not candidates:
            break
        j = random.choice(candidates)
        IR.add(j)
    # Step 7-11: Add close ports
    for i in IR.copy():
        for j in I - IR:
            if t[i][j] <= rho[i]:
                IR.add(j)
    # Rimuovi solo archi uscenti da IR
    OmegaR = set([arc for arc in OmegaR if arc[0] not in IR])
    Omega_new = solve_overconstrained(data, build_model, fixed_arcs=OmegaR)
    return Omega_new

# =========================
# ALGORITHM 1: LNS Matheuristic
# =========================
def lns_matheuristic(data, build_model, params, algo_type='DIV'):
    ITERMAX = params.get('ITERMAX', 100)
    MAXNOIMPROVE = params.get('MAXNOIMPROVE', 20)
    m_pert = params.get('m_pert', 3)
    ports = [p['id'] for p in data[1]]  # ports from read_instance
    t = {}  # build t[i][j] from data[2]
    for (i, j), v in data[2].items():
        if i not in t:
            t[i] = {}
        t[i][j] = v
    rho = {p: 9999 for p in ports}  # puoi settare valori diversi se vuoi

    iter = 1
    NOIMPROVE = 0
    best_solution = initial_solution(data, build_model)
    solution = best_solution
    best_cost = solution['cost']

    while iter <= ITERMAX and NOIMPROVE <= MAXNOIMPROVE:
        if algo_type == 'DIV':
            Omega_new = diversification_DIV(solution, ports, t, rho, m_pert, build_model, data)
        elif algo_type == 'INT':
            Omega_new = intensification_INT(solution, ports, t, rho, m_pert, build_model, data)
        elif algo_type == 'REC':
            Omega_new = reconstruction_REC(solution, ports, t, rho, m_pert, build_model, data)
        else:
            raise ValueError("algo_type deve essere 'DIV', 'INT' o 'REC'")
        if Omega_new['cost'] < best_cost:
            best_solution = Omega_new
            best_cost = Omega_new['cost']
            NOIMPROVE = 0
        else:
            NOIMPROVE += 1
        solution = Omega_new
        iter += 1
    return best_solution
