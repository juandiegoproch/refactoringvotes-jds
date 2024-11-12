import csv

def count_votes(file_path):
    vote_counts = {} # renombramiento de variables
    
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader) #skip header
        for row in reader:
            vote_counts = process_row(row, vote_counts)
        printvotes(vote_counts)

    # Renombramiento de variables
    winner = getWinner(vote_counts)
    announceWinner(winner)

def announceWinner(winner):
    if winner is None:
        print("There was a tie")
    else:
        print(f"winner is {winner}")

def getWinner(vote_counts):
    candidates_sorted_by_votes = sorted(vote_counts.items(), key=lambda item: item[1], reverse=True)
    most_votes = candidates_sorted_by_votes[0][1]
    top_candidates = [candidate for candidate, votes in candidates_sorted_by_votes if votes == most_votes]
    if len(top_candidates) != 1: #simplificacion de condicionales
        return None
    return top_candidates[0]

def printvotes(votes): # Extraccion de metodos (Podria querer imprimir los votos en otro momento)
    for candidate, total_votes in votes.items():
        print(f"{candidate}: {total_votes} votes")

def process_row(row, results): # Division de metodos, este procesamiento era muy grande
                               # Seria beneficioso poder testearlo independientemente
    city = row[0]
    candidate = row[1]
    try:
        votes = int(row[2])
    except:
        votes = 0
    
    # Eliminacion de codigo duplicado (entre mi codigo y la libreria estandar de python)
    results.setdefault(candidate, 0)
    results[candidate] += votes
    return results

# Example usage
count_votes('votes.csv')
