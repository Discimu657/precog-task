import random
import json
import os

def generate_groups(base_chars, num_groups, min_size=3, max_size=8):
    groups = set()
    while len(groups) < num_groups:
        size = random.randint(min_size, max_size)
        group = ''.join(random.choices(base_chars, k=size))
        groups.add(group)
    return list(groups)

def generate_string(groups, num_insertions, base_chars, max_additional_rules=5):
    current = ''
    insertion_indices = []
    additional_rules = []
    operation_indices = []
    max_attempts = 20

    for _ in range(num_insertions):
        if not groups:
            break

        attempts = 0
        inserted = False

        while not inserted and attempts < max_attempts:
            # Group insertion
            group = random.choice(groups)
            group_index = groups.index(group)
            pos = random.randint(0, len(current))
            candidate = current[:pos] + group + current[pos:]

            # Check for conflicts with other groups
            conflict = False
            for g in groups:
                if g != group and g in candidate:
                    conflict = True
                    break

            if not conflict:
                current = candidate
                insertion_indices.append(group_index)
                operation_indices.append(group_index)
                inserted = True

                # Additional rule generation
                if len(additional_rules) < max_additional_rules and len(current) >= 5:
                    start = random.randint(0, len(current) - 5)
                    substring = current[start:start+5]
                    
                    # Generate conflict-free small group
                    new_small_group = None
                    for _ in range(5):  # Max attempts for small group
                        new_length = random.randint(2, 4)
                        candidate_group = ''.join(random.choices(base_chars, k=new_length))
                        while True :
                            if candidate_group not in groups:
                                break 
                            else :
                                candidate_group-''.join(random.choice(base_chars,k=new_length))

                        # Check conflicts with ALL existing groups and rules
                        valid = True
                        for g in groups + [r["src"] for r in additional_rules]:
                            if (candidate_group in g or g in candidate_group):
                                valid = False
                                break
                        
                        if valid:
                            new_small_group = candidate_group
                            break
                    
                    if new_small_group:
                        # Add rule and apply substitution
                        additional_rules.append({"src": new_small_group, "tgt": substring})
                        current = current.replace(substring, new_small_group, 1)
                        operation_indices.append(len(groups) + len(additional_rules) - 1)

            else:
                attempts += 1

    return current, operation_indices, additional_rules

def generate_puzzle(problem_id, base_chars=None, num_groups=3, min_group_size=3, max_group_size=5, num_insertions=5):
    if base_chars is None:
        base_chars = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~")
    
    groups = generate_groups(base_chars, num_groups, min_group_size, max_group_size)
    generated_string, operation_indices, additional_rules = generate_string(groups, num_insertions, base_chars)
    
    transitions = [{"src": g, "tgt": ""} for g in groups] + additional_rules
    solution_steps = operation_indices[::-1]
    
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
        save_to_json(puzzle, "puzzles/medium/problem", puzzle_filename)
        
        solution_data = {"problem_id": problem_id, "solution": solution}
        solution_filename = f"solution_{problem_id}.json"
        save_to_json(solution_data, "puzzles/medium/solution", solution_filename)