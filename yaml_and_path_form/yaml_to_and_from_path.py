import yaml

# --------- Conversion: YAML -> dot-path ---------
def yaml_to_paths(d, prefix=''):
    paths = {}
    for k, v in d.items():
        full_key = f"{prefix}.{k}" if prefix else k
        if isinstance(v, dict):
            paths.update(yaml_to_paths(v, full_key))
        else:
            paths[full_key] = v
    return paths

# --------- Conversion: dot-path -> YAML ---------
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

# --------- Read YAML from file ---------
def read_yaml_file(file_path):
    with open(file_path, 'r') as f:
        return yaml.safe_load(f)

# --------- Write YAML to file ---------
def write_yaml_file(data, file_path):
    with open(file_path, 'w') as f:
        yaml.dump(data, f, default_flow_style=False)

# --------- Example Usage ---------
if __name__ == "__main__":
    # Input YAML (as a Python dict for simplicity)
    sample_yaml = {
        'a': {
            'b': {
                'c': {
                    'd': 42
                },
                'e': 'hello'
            },
            'f': True
        },
        'x': 3.14
    }

    write_yaml_file(sample_yaml, "output.yaml")

    del sample_yaml
    # Read YAML
    sample_yaml = read_yaml_file("output.yaml")

    print("Original YAML:")
    print(yaml.dump(sample_yaml, default_flow_style=False))

    # Convert YAML to dot-path
    flat = yaml_to_paths(sample_yaml)
    print("\nYAML to path format:")
    for k, v in flat.items():
        print(f"{k} = {v}")

    # Convert back to YAML
    reconstructed = paths_to_yaml(flat)
    print("\nReconstructed YAML:")
    print(yaml.dump(reconstructed, default_flow_style=False))


"""
Original YAML:
a:
  b:
    c:
      d: 42
    e: hello
  f: true
x: 3.14


YAML to path format:
a.b.c.d = 42
a.b.e = hello
a.f = True
x = 3.14

Reconstructed YAML:
a:
  b:
    c:
      d: 42
    e: hello
  f: true
x: 3.14
"""