import random
import string
import yaml

def random_key():
    return random.choice(string.ascii_lowercase)  # Just 1 character

def random_value():
    choices = [
        random.randint(1, 100),
        round(random.uniform(1, 100), 2),
        ''.join(random.choices(string.ascii_lowercase, k=5)),
        random.choice([True, False])
    ]
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

if __name__ == "__main__":
    N = 20  # Number of random paths to generate
    flat_map, path_list = generate_random_paths(N)

    print("\nSorted unique paths:")
    for p in path_list:
        print(f"  {p} = {flat_map[p]}")

    nested_yaml = paths_to_yaml(flat_map)

    print("\nGenerated YAML:")
    print(yaml.dump(nested_yaml, default_flow_style=False))

"""
# N = 2000
REPLICATED: i (overwriting value)
REPLICATED: t (overwriting value)
:
REPLICATED: x.w (overwriting value)
:
REPLICATED: e (overwriting value)

Sorted unique paths:
  a = 99
  a.b = 75.89
  a.b.r.v = 81
  a.d.d = qvaxt
  a.e.f.i = aahil
:
  h.i.t = False
:
  s.e.x = eenmx
:
  z.z.s = jovmx
  z.z.x.o = 36.82

Generated YAML:
a:
  b:
    r:
      v: 81
  d:
    d: qvaxt
  e:
    f:
      i: aahil
    g:
      e:
        q: false
:
  h: false
  i:
    e:
      s: 36.2
    m: 72.41
    s: iahfl
  l: false
:
  m:
    w:
      n: 1.9
    z:
      j:
        r: 69.81
:
  w: 67.09
:
  y:
    n:
      a: 75.14
    q:
      f:
        t: false
  z:
    s: jovmx
    x:
      o: 36.82

"""