from heapq import heappop, heappush
import itertools

def sokoban_heuristic(state):

    total_cost = 0

    # 1. Matching optim cutii-ținte
    box_positions = [(box.x, box.y) for box in state.boxes.values()]
    target_positions = list(state.targets)
    cost_matrix = [[manhattan_distance(box, target) for target in target_positions] for box in box_positions]

    # Minimum cost matching (greedy)
    used_targets = set()
    for box_costs in cost_matrix:
        min_dist = min((dist for idx, dist in enumerate(box_costs) if idx not in used_targets), default=float('inf'))
        if min_dist != float('inf'):
            best_target_idx = box_costs.index(min_dist)
            used_targets.add(best_target_idx)
            total_cost += min_dist

    # 2. Penalizare pentru cutii blocate sau aproape blocate
    for box in state.boxes.values():
        if is_box_deadlocked(state, box):
            total_cost += 500  # Deadlock major
        elif is_box_cornered(state, box):
            total_cost += 100  # Blocaj parțial

    # 3. Distanță minimă jucător - cutie
    player_pos = (state.player.x, state.player.y)
    player_distances = [manhattan_distance(player_pos, box_pos) for box_pos in box_positions]
    if player_distances:
        total_cost += min(player_distances) // 2 # ponderăm mai puțin agresiv

    return total_cost


def manhattan_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


def is_box_cornered(state, box):
    walls = state.obstacles
    x, y = box.x, box.y
    adjacent = [
        ((x - 1, y), (x, y - 1)),
        ((x - 1, y), (x, y + 1)),
        ((x + 1, y), (x, y - 1)),
        ((x + 1, y), (x, y + 1)),
    ]
    for (a, b) in adjacent:
        if (a in walls or a in state.positions_of_boxes) and (b in walls or b in state.positions_of_boxes):
            if (x, y) not in state.targets:
                return True
    return False


def is_box_deadlocked(state, box):
    x, y = box.x, box.y
    if (x, y) in state.targets:
        return False  # dacă e pe țintă, e ok

    walls = state.obstacles
    # Verifică colțuri (două direcții blocate)
    corner_pairs = [
        ((-1, 0), (0, -1)),
        ((-1, 0), (0, 1)),
        ((1, 0), (0, -1)),
        ((1, 0), (0, 1)),
    ]
    for (dx1, dy1), (dx2, dy2) in corner_pairs:
        pos1 = (x + dx1, y + dy1)
        pos2 = (x + dx2, y + dy2)
        if (pos1 in walls or pos1 in state.positions_of_boxes) and (pos2 in walls or pos2 in state.positions_of_boxes):
            return True

    return False


def sokoban_heuristic_ida(state):
    total_cost = 0

    # 1. Matching optimizat cutii-ținte
    box_positions = [(box.x, box.y) for box in state.boxes.values()]
    target_positions = list(state.targets)

    # Calculăm distanțele Manhattan între fiecare cutie și fiecare țintă
    cost_matrix = [[manhattan_distance(box, target) for target in target_positions] for box in box_positions]

    # Matching minim (greedy)
    used_targets = set()
    for box_costs in cost_matrix:
        min_dist = min((dist for idx, dist in enumerate(box_costs) if idx not in used_targets), default=float('inf'))
        if min_dist != float('inf'):
            best_target_idx = box_costs.index(min_dist)
            used_targets.add(best_target_idx)
            total_cost += min_dist

    # 2. Penalizare pentru cutii blocate
    for box in state.boxes.values():
        if is_box_deadlocked(state, box):
            total_cost += 300  # Penalizare moderată pentru cutii blocate

    # 3. Distanță minimă jucător - cutie
    player_pos = (state.player.x, state.player.y)
    player_distances = [manhattan_distance(player_pos, box_pos) for box_pos in box_positions]
    if player_distances:
        total_cost += min(player_distances)  # Adăugăm distanța minimă

    return total_cost
