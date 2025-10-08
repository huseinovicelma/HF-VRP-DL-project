

def extract_block(label, lines):
    block = []
    for i, line in enumerate(lines):
        if line.startswith(label):
            if "[" in line and "]" in line:
                content = line.split("[", 1)[1].split("]", 1)[0]
                block.append(content)
                break
            elif "[" in line and "]" not in line:
                # Prima riga parziale
                partial = line.split("[", 1)[1].strip()
                if partial:
                    block.append(partial)
                j = i + 1
                while j < len(lines):
                    line_j = lines[j].strip().replace("]", "")
                    if line_j:
                        block.append(line_j)
                    if "]" in lines[j]:
                        break
                    j += 1
                break
            elif line.endswith(":"):
                j = i + 1
                while j < len(lines):
                    line_j = lines[j].strip().replace("[", "").replace("]", "")
                    if line_j:
                        block.append(line_j)
                    if "]" in lines[j]:
                        break
                    j += 1
                break
    return block


def parse_instance(path):
    with open(path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    Q = list(map(int, extract_block("Q:", lines)[0].split()))
    q = list(map(int, extract_block("q:", lines)))
    L = [list(map(int, row.split())) for row in extract_block("L:", lines)]
    coord = [list(map(float, row.split())) for row in extract_block("coord:", lines)]
    c = list(map(float, extract_block("c:", lines)[0].split()))
    r = [list(map(float, row.split())) for row in extract_block("r:", lines)]
    I = list(range(1, len(q)))
    I0 = list(range(len(q)))
    S = list(range(len(Q)))

    return I, I0, S, Q, q, L, coord, c, r
