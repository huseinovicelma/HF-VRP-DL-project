import csv

def save_results(filename, results):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['istanza', 'algoritmo', 'status', 'costo', 'tempo_sec'])
        for row in results:
            writer.writerow(row)