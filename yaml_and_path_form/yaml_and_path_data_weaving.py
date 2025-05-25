import random
import string
import yaml

# Random utilities
def random_key():
    return ''.join(random.choices(string.ascii_lowercase, k=random.randint(1, 4)))

def random_value():
    choices = [random.randint(1, 100), 
               round(random.uniform(1, 100), 2), 
               ''.join(random.choices(string.ascii_lowercase, k=5)),
               random.choice([True, False])]
    return random.choice(choices)

def generate_random_paths(n, max_depth=5):
    path_map = {}
    all_paths = []

    for _ in range(n):
        depth = random.randint(1, max_depth)
        keys = [random_key() for _ in range(depth)]
        path = ".".join(keys)
        value = random_value()

        if path in path_map:
            print(f"REPLICATED: {path} (overwriting value)")

        path_map[path] = value
        all_paths.append(path)

    return path_map, sorted(set(all_paths))

# Convert dot-paths back to nested dict
def paths_to_yaml(paths):
    root = {}
    for path, value in paths.items():
        keys = path.split('.')
        current = root
        for key in keys[:-1]:
            if key not in current or not isinstance(current[key], dict):
                current[key] = {}
            current = current[key]
        current[keys[-1]] = value
    return root

# Main logic
if __name__ == "__main__":
    N = 20  # or any number of paths you want
    flat_map, path_list = generate_random_paths(N)

    print("\nSorted unique paths:")
    for p in path_list:
        print(f"  {p} = {flat_map[p]}")

    nested_yaml = paths_to_yaml(flat_map)

    print("\nGenerated YAML:")
    print(yaml.dump(nested_yaml, default_flow_style=False))

"""
- Randomly generates N dot-separated paths of varying lengths (up to 5 keys).
- Assigns a random value to each path.
- If a path is repeated, it will:
    - Print REPLICATED: {path}.
    -  Update the existing value with the latest.
- Collects all paths in a list.
- Sorts the paths.
- Converts the flat path-value map back to nested YAML.
- Outputs the final YAML structure.
"""