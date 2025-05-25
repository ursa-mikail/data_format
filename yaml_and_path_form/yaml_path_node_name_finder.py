import yaml

def read_yaml_file(file_path):
    with open(file_path, 'r') as f:
        return yaml.safe_load(f)

def yaml_to_paths(d, prefix=''):
    paths = {}
    for k, v in d.items():
        full_key = f"{prefix}.{k}" if prefix else k
        if isinstance(v, dict):
            paths.update(yaml_to_paths(v, full_key))
        else:
            paths[full_key] = v
    return paths

'''
def find_paths_with_keyword(flat_paths, keyword):
    results = []
    for path in flat_paths:
        parts = path.split('.')
        if keyword in parts:
            highlighted = '.'.join([f">>{p}<<" if p == keyword else p for p in parts])
            results.append(highlighted)
    return results
'''
def find_paths_with_keyword(flat_paths, keyword):
    results = []
    for path, value in flat_paths.items():
        parts = path.split('.')
        if keyword in parts:
            highlighted = '.'.join([f">>{p}<<" if p == keyword else p for p in parts])
            results.append((highlighted, value))
    return results


if __name__ == "__main__":
    # Load YAML file
    data = read_yaml_file("input.yaml")

    # Flatten YAML to dot-paths
    flat = yaml_to_paths(data)

    # Search for keyword in paths
    keyword = 'c'
    matches = find_paths_with_keyword(flat, keyword)

    # Print matches
    print(f"Paths containing keyword '{keyword}':")
    for path, value in matches:
        print(f"  {path} = {value}")

"""
Paths containing keyword 'c':
  a.b.>>c<<.d = 1
  f.g.>>c<<.h = 3
  i.j.>>c<< = 4
"""  
