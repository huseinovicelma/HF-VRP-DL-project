# V11: elimina archi impossibili per limiti di pescaggio a vuoto
def add_vi1(m, I0, S, L_dict, ships, X):
    for i in I0:
        for j in I0:
            if i != j:
                for k in S:
                    if L_dict[(j, k)] < ships[int(k[1:])-1]['draft_empty']:
                        m.addConstr(X[i, j, k] == 0)

# V12: elimina archi impossibili per limiti di capacità
def add_vi2(m, I0, X, S, demand, capacity):
    for i in I0:
        for j in I0:
            if i != j:
                for k in S:
                    if demand[j] > capacity[k]:
                        m.addConstr(X[i, j, k] == 0)

def add_vi3(m, Y, I, S, L_dict, ships):
    # V13: elimina assegnazioni impossibili per limiti di pescaggio a vuoto
    for i in I:
        for k in S:
            if L_dict[(i, k)] < ships[int(k[1:])-1]['draft_empty']:
                m.addConstr(Y[i, k] == 0)

def add_vi4(m, Y, I, S, demand, capacity):
    # V14: elimina assegnazioni impossibili per limiti di capacità
    for i in I:
        for k in S:
            if demand[i] > capacity[k]:
                m.addConstr(Y[i, k] == 0)                    