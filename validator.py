import json
import os

def validate_solution(initial_string, transitions, solution):
    current = initial_string
    for step in solution:
        if step >= len(transitions):
            return False 
        rule = transitions[step]
        src, tgt = rule["src"], rule["tgt"]
        if src not in current:
            return False  
        current = current.replace(src, tgt, 1)
    return current == ""  

def validate_all_solutions(problem_dir, solution_dir):
    valid_count = 0

    for solution_file in os.listdir(solution_dir):
        if not solution_file.endswith(".json"):
            continue

        solution_path = os.path.join(solution_dir, solution_file)
        with open(solution_path, "r", encoding="utf-8") as f:
            solution_data = json.load(f)

        problem_id = solution_data["problem_id"]
        problem_path = os.path.join(problem_dir, f"problem_{problem_id}.json")

        if not os.path.exists(problem_path):
            continue

        with open(problem_path, "r", encoding="utf-8") as f:
            problem_data = json.load(f)

        if validate_solution(
            problem_data["initial_string"],
            problem_data["transitions"],
            solution_data["solution"]
        ):
            valid_count += 1

    return valid_count

if __name__ == "__main__":
    difficulties = ["easy", "medium"]
    for diff in difficulties:
        problem_dir = f"puzzles/{diff}/problem"
        solution_dir = f"puzzles/{diff}/solution"
        valid_count = validate_all_solutions(problem_dir, solution_dir)
        print(f"No of valid {diff} problems: {valid_count}")
