from search_methods.heuristics import sokoban_heuristic_ida

def ida_star(map_obj, heuristic=sokoban_heuristic_ida, max_iterations=10000):
    
    def search(path, g, threshold, visited):
        nonlocal total_steps
        node = path[-1]
        f = g + heuristic(node)

        # Incrementăm contorul de pași
        total_steps += 1

        if f > threshold:
            return f  # Returnăm f ca să știm noul threshold minim
        
        if node.is_solved():
            return path # Soluția găsită

        min_threshold = float('inf')

        for neighbor in node.get_neighbours():
            state_id = neighbor.serialize_state()
            if state_id in visited:
                continue
            visited.add(state_id)
            result = search(path + [neighbor], g + 1, threshold, visited)

            if isinstance(result, list):  # Soluția a fost găsită
                return result
            if result < min_threshold:
                min_threshold = result

            visited.remove(state_id)

        return min_threshold

    threshold = heuristic(map_obj)
    path = [map_obj]
    visited = set()
    visited.add(map_obj.serialize_state())
    iterations = 0
    total_steps = 0  # Contor pentru numărul total de pași

    while iterations < max_iterations:
        iterations += 1
        result = search(path, g=0, threshold=threshold, visited=visited)
        if isinstance(result, list):
            return result, total_steps  # Soluția găsită
        if result == float('inf'):
            return None, total_steps  # Nu există soluție
        threshold = result  # Creștem threshold-ul

    return None, total_steps  # Dacă depășim numărul maxim de iterații