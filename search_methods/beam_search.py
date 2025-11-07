from search_methods.heuristics import sokoban_heuristic
import os
import heapq

def beam_search(map_obj, beam_width=20, heuristic=sokoban_heuristic, max_iterations=10000):

    # Inițializăm beam-ul și setul de stări vizitate
    beam = [(heuristic(map_obj), [map_obj])]  # Fiecare element este (scor, listă de stări)
    visited = set()
    visited.add(map_obj.serialize_state())  # Serializăm starea inițială
    iterations = 0
    toal_steps = 0

    while beam and iterations < max_iterations:
        iterations += 1
        successors = []

        # Iterăm prin fiecare stare din beam
        for _, path in beam:
            current_state = path[-1]

            # Verificăm dacă starea curentă este soluția
            if current_state.is_solved():
                return path, toal_steps  # Soluția a fost găsită

            # Generăm succesorii stării curente
            for neighbor in current_state.get_neighbours():
                toal_steps += 1
                state_id = neighbor.serialize_state()
                if state_id in visited:
                    continue  # Evităm stările deja vizitate
                visited.add(state_id)

                # Calculăm costul pentru succesor
                cost = heuristic(neighbor)
                successors.append((cost, path + [neighbor]))

        if not successors:
            break  # Dacă nu mai există stări de explorat, ieșim din buclă

        # Selectăm beam_width cei mai buni succesori
        beam = heapq.nsmallest(beam_width, successors, key=lambda x: x[0])

    return None, toal_steps # Dacă nu s-a găsit soluție