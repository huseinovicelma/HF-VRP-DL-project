import math

def parse_block(lines, start):
    block = []
    i = start
    while i < len(lines):
        l = lines[i].strip()
        if l.startswith('['):
            l = l[1:]
        if l.endswith(']'):
            l = l[:-1]
            if l.strip() == '':
                break
        if l != '':
            block.append(l)
        if lines[i].strip().endswith(']'):
            break
        i += 1
    return block, i

def read_instance(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()

    # Q
    idx_Q = next(i for i, l in enumerate(lines) if l.strip().startswith('Q:'))
    Q_block, _ = parse_block(lines, idx_Q+1)
    Q = [int(x) for x in ' '.join(Q_block).split()]

    # q
    idx_q = next(i for i, l in enumerate(lines) if l.strip().startswith('q:'))
    q_block, _ = parse_block(lines, idx_q+1)
    q = [int(x) for x in ' '.join(q_block).split()]

    # L
    idx_L = next(i for i, l in enumerate(lines) if l.strip().startswith('L:'))
    L_block, _ = parse_block(lines, idx_L+1)
    L = [[int(x) for x in l.split()] for l in L_block]

    # coord
    idx_coord = next(i for i, l in enumerate(lines) if l.strip().startswith('coord:'))
    coord_block, _ = parse_block(lines, idx_coord+1)
    coord = [[int(x) for x in l.split()] for l in coord_block]

    # c
    idx_c = next(i for i, l in enumerate(lines) if l.strip().startswith('c:'))
    c_line = lines[idx_c].split(':')[1].replace('[','').replace(']','').strip()
    c = [float(x) for x in c_line.split()]

    # r
    idx_r = next(i for i, l in enumerate(lines) if l.strip().startswith('r:'))
    r_block, _ = parse_block(lines, idx_r+1)
    r = [[float(x) for x in l.split()] for l in r_block]

    num_ports = len(coord)
    num_ships = len(Q)

    ports = []
    for i in range(num_ports):
        ports.append({
            'id': f'P{i+1}',
            'x': coord[i][0],
            'y': coord[i][1],
            'demand': q[i],
            'draft_limit': min(L[i]) if i < len(L) else 9999
        })

    ships = []
    for k in range(num_ships):
        ships.append({
            'id': f'N{k+1}',
            'capacity': Q[k],
            'cost_per_unit': c[k] if k < len(c) else 1.0,
            'draft_empty': r[0][k] if len(r) > 0 else 4.0,
            'draft_per_unit': 0.02
        })

    # Calcolo delle distanze (t_ij)
    distances = {}
    for i in range(num_ports):
        for j in range(num_ports):
            pi, pj = ports[i], ports[j]
            dist = math.sqrt((pi['x'] - pj['x'])**2 + (pi['y'] - pj['y'])**2)
            distances[(pi['id'], pj['id'])] = round(dist, 2)

    return ships, ports, distances, q, Q, c, r, L
