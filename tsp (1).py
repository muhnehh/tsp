import math
import random
import sys
import tsplib95

def load_problem(file_path):
    problem = tsplib95.load(file_path)

    city_coords = {}
    for node_id, (x, y) in problem.node_coords.items():
        city_coords[int(node_id)] = (float(x), float(y))

    name = getattr(problem, "name", None)
    size = problem.dimension
    edge_type = getattr(problem, "edge_weight_type", None)

    return city_coords, name, size, edge_type


def dist_euclidean(p, q):
    dx = p[0] - q[0]
    dy = p[1] - q[1]
    return int(round(math.hypot(dx, dy)))


def tour_len(tour, city_coords):
    n = len(tour)
    total = 0
    for i in range(n):
        a = tour[i]
        b = tour[(i + 1) % n]
        total += dist_euclidean(city_coords[a], city_coords[b])
    return total


def nn_tour(city_coords, start_city, rng):
    unvisited = set(city_coords.keys())
    unvisited.remove(start_city)

    tour = [start_city]
    current = start_city

    while unvisited:
        nxt = min(unvisited, key=lambda c: dist_euclidean(city_coords[current], city_coords[c]))
        tour.append(nxt)
        unvisited.remove(nxt)
        current = nxt

    return tour

def best_2opt_once_full(tour, city_coords):
    best = tour
    best_len = tour_len(tour, city_coords)
    n = len(tour)

    for i in range(n - 1):
        for j in range(i + 2, n):
            if i == 0 and j == n - 1:
                continue
            candidate = tour[:i + 1] + tour[i + 1:j + 1][::-1] + tour[j + 1:]
            L = tour_len(candidate, city_coords)
            if L < best_len:
                best, best_len = candidate, L

    return best, (best is not tour)


def best_insert_once_full(tour, city_coords):
    best = tour
    best_len = tour_len(tour, city_coords)
    n = len(tour)

    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            candidate = tour[:]
            city = candidate.pop(i)
            candidate.insert(j, city)
            L = tour_len(candidate, city_coords)
            if L < best_len:
                best, best_len = candidate, L

    return best, (best is not tour)


def sample_2opt_once(tour, city_coords, tries=1000, rng=None):
    if rng is None:
        rng = random

    base_len = tour_len(tour, city_coords)
    n = len(tour)

    for _ in range(tries):
        i = rng.randint(0, n - 3)
        j = rng.randint(i + 2, n - 1)
        if i == 0 and j == n - 1:
            continue

        candidate = tour[:i + 1] + tour[i + 1:j + 1][::-1] + tour[j + 1:]
        if tour_len(candidate, city_coords) < base_len:
            return candidate, True

    return tour, False


def sample_insert_once(tour, city_coords, tries=1000, rng=None):
    if rng is None:
        rng = random

    base_len = tour_len(tour, city_coords)
    n = len(tour)

    for _ in range(tries):
        i = rng.randrange(n)
        j = rng.randrange(n)
        if i == j:
            continue

        candidate = tour[:]
        city = candidate.pop(i)
        candidate.insert(j, city)
        if tour_len(candidate, city_coords) < base_len:
            return candidate, True

    return tour, False


def climb_hill(city_coords, restarts=20, seed=42, verbose=True):
    rng = random.Random(seed)
    all_cities = list(city_coords.keys())
    n = len(all_cities)
    use_fast_mode = (n >= 150)

    best_overall_tour = None
    best_overall_len = float("inf")

    for r in range(restarts):
        start_city = rng.choice(all_cities)
        tour = nn_tour(city_coords, start_city, rng)

        if verbose:
            print(f"\nrestart {r + 1}/{restarts}")
            print(f" start city: {start_city}")
            print(f" start length: {tour_len(tour, city_coords)}")
            print(" mode:", "FAST (sampled neighborhoods, n ≥ 150)" if use_fast_mode
                  else "FULL (exhaustive neighborhoods, n < 150)")

        improved = True
        step = 0
        while improved:
            step += 1
            if use_fast_mode:
                tour2, ok2 = sample_2opt_once(tour, city_coords, tries=1000, rng=rng)
                if ok2:
                    tour = tour2
                    if verbose:
                        print(f"  step {step}: 2-opt* -> {tour_len(tour, city_coords)}")
                    continue

                tourI, okI = sample_insert_once(tour, city_coords, tries=1000, rng=rng)
                if okI:
                    tour = tourI
                    if verbose:
                        print(f"  step {step}: insert* -> {tour_len(tour, city_coords)}")
                    continue

                improved = False  
            else:
                tour2, ok2 = best_2opt_once_full(tour, city_coords)
                if ok2:
                    tour = tour2
                    if verbose:
                        print(f"  step {step}: 2-opt  -> {tour_len(tour, city_coords)}")
                    continue

                tourI, okI = best_insert_once_full(tour, city_coords)
                if okI:
                    tour = tourI
                    if verbose:
                        print(f"  step {step}: insert -> {tour_len(tour, city_coords)}")
                    continue

                improved = False  

        final_len = tour_len(tour, city_coords)
        if verbose:
            print(f"  done improving after {step - 1} steps")
            print(f"  final length this restart: {final_len}")

        if final_len < best_overall_len:
            best_overall_len = final_len
            best_overall_tour = tour
            if verbose:
                print("  new best overall")

    return best_overall_tour, best_overall_len

def solve_file(file_path, num_restarts):
    city_coords, prob_name, size, edge_type = load_problem(file_path)

    print("Problem:", prob_name)
    print("Cities:", size)
    print("Edge type:", edge_type)
    print("Restarts:", num_restarts)

    best_tour, best_length = climb_hill(
        city_coords,
        restarts=num_restarts,
        seed=42,
        verbose=True
    )

    print("\nBEST TOUR LENGTH:", best_length)
    print("TOUR ORDER      :", best_tour)


def main():
    if len(sys.argv) < 2:
        print("Usage: python tsp_hill_climb.py <file.tsp> [restarts]")
        print("Example: python tsp_hill_climb.py eil51.tsp 200")
        sys.exit(0)

    file_path = sys.argv[1]
    if len(sys.argv) >= 3:
        num_restarts = int(sys.argv[2])
    else:
        num_restarts = 20  # default

    solve_file(file_path, num_restarts)


if __name__ == "__main__":
    main()
