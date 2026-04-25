
import yaml
import os

def load_yaml_file(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{file_path} not found")
    with open(file_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise ValueError("Input YAML must be a dictionary")
    return data

def flatten_kdes(data):
    kde_map = {}
    for section, elements in data.items():
        if isinstance(elements, dict):
            for _, value in elements.items():
                if isinstance(value, dict):
                    name = value.get("name")
                    requirements = value.get("requirements", [])
                    if isinstance(name, str):
                        kde_map[name.strip()] = set(str(r).strip() for r in requirements)
    return kde_map

def compare_kde_names(yaml_file1, yaml_file2, output_file):
    data1 = flatten_kdes(load_yaml_file(yaml_file1))
    data2 = flatten_kdes(load_yaml_file(yaml_file2))
    differences = []

    for name in sorted(set(data1.keys()) - set(data2.keys())):
        differences.append(f"{name},PRESENT-IN-{yaml_file1},ABSENT-IN-{yaml_file2}")

    for name in sorted(set(data2.keys()) - set(data1.keys())):
        differences.append(f"{name},ABSENT-IN-{yaml_file1},PRESENT-IN-{yaml_file2}")

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(differences) if differences else "NO DIFFERENCES IN REGARDS TO ELEMENT NAMES")

    return differences

def compare_kde_requirements(yaml_file1, yaml_file2, output_file):
    data1 = flatten_kdes(load_yaml_file(yaml_file1))
    data2 = flatten_kdes(load_yaml_file(yaml_file2))
    differences = []

    for name in sorted(set(data1.keys()).union(set(data2.keys()))):
        if name not in data1:
            differences.append(f"{name},ABSENT-IN-{yaml_file1},PRESENT-IN-{yaml_file2},NA")
        elif name not in data2:
            differences.append(f"{name},ABSENT-IN-{yaml_file2},PRESENT-IN-{yaml_file1},NA")
        else:
            for req in sorted(data1[name] - data2[name]):
                differences.append(f"{name},ABSENT-IN-{yaml_file2},PRESENT-IN-{yaml_file1},{req}")
            for req in sorted(data2[name] - data1[name]):
                differences.append(f"{name},ABSENT-IN-{yaml_file1},PRESENT-IN-{yaml_file2},{req}")

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(differences) if differences else "NO DIFFERENCES IN REGARDS TO ELEMENT REQUIREMENTS")

    return differences
