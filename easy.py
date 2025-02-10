import random
import json
import os

def generate_groups(base_chars, num_groups, min_size=1, max_size=3):
    groups = set()
    while len(groups) < num_groups:
        size = random.randint(min_size, max_size)
        group = ''.join(random.choices(base_chars, k=size))
        groups.add(group)
    return list(groups)

def generate_string(groups, num_insertions):
    current = ''
    insertion_indices = []
    max_attempts = 20  

    for _ in range(num_insertions):
        if not groups:
            break

        attempts = 0
        inserted = False

        while not inserted and attempts < max_attempts:
            group = random.choice(groups)
            group_index = groups.index(group)

            pos = random.randint(0, len(current))
            candidate = current[:pos] + group + current[pos:]

            conflict = False
            for g in groups:
                if g != group and g in candidate:
                    conflict = True
                    break

            if not conflict:
                current = candidate
                insertion_indices.append(group_index)
                inserted = True
            else:
                attempts += 1

        if not inserted:
            break

    return current, insertion_indices

def generate_puzzle(problem_id, base_chars=None, num_groups=5, min_group_size=3, max_group_size=5, num_insertions=7):
    if base_chars is None:
        base_chars = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~")
    groups = generate_groups(base_chars, num_groups, min_group_size, max_group_size)
    generated_string, insertion_indices = generate_string(groups, num_insertions)
    solution_steps = insertion_indices[::-1]
    transitions = [{"src": group, "tgt": ""} for group in groups]
    return {
        "problem_id": problem_id,
        "initial_string": generated_string,
        "transitions": transitions
    }, solution_steps

def save_to_json(data, directory, filename):
    os.makedirs(directory, exist_ok=True)
    filepath = os.path.join(directory, filename)
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    for i in range(1,51):
        problem_id = f"{i:03d}"
        puzzle, solution = generate_puzzle(problem_id)
        
        puzzle_filename = f"problem_{problem_id}.json"
        save_to_json(puzzle, "puzzles/easy/problem", puzzle_filename)
        
        solution_data = {"problem_id": problem_id, "solution": solution}
        solution_filename = f"solution_{problem_id}.json"
        save_to_json(solution_data, "puzzles/easy/solution", solution_filename)
        
        print(f"Generated puzzle: {puzzle_filename}")
        print(f"Generated solution: {solution_filename}")
