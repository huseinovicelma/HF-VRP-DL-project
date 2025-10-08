import gurobipy as gp

def valid_inequality_1(m, X, Y, q, L, TOTq, I, S):
    for j in I:
        for s in S:
            m.addConstr(X[0, j, s] <= 1 - (gp.quicksum(q[i] * Y[i, s] for i in I) - L[j-1][s]) / TOTq)

def valid_inequality_2(m, X, Y, q, L, I, S):
    for i in I:
        for j in I:
            if i != j:
                for s in S:
                    if q[i] + q[j] > L[i-1][s]:
                        m.addConstr(X[i, j, s] == 0)

def valid_inequality_3(m, X, Y, q_big, L, p, u, Q, I, S):
    for i in I:
        for s in S:
            m.addConstr(p[s] - (u[i] - 1) * q_big <= L[i-1][s] + Q[s] * (1 - Y[i, s]))

def valid_inequality_4(m, X, Y, q, L, u, Istar, I, S):
    for i in I:
        m.addConstr(u[i] <= Istar)