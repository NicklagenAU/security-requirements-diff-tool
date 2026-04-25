
import os
from task2_comparator import load_yaml_file, compare_kde_names, compare_kde_requirements

def test_load_yaml_file():
    data = load_yaml_file("cis-r1-kdes.yaml")
    assert isinstance(data, dict)

def test_compare_kde_names():
    result = compare_kde_names("cis-r1-kdes.yaml", "cis-r2-kdes.yaml", "test_names_output.txt")
    assert isinstance(result, list)
    assert os.path.exists("test_names_output.txt")

def test_compare_kde_requirements():
    result = compare_kde_requirements("cis-r1-kdes.yaml", "cis-r2-kdes.yaml", "test_requirements_output.txt")
    assert isinstance(result, list)
    assert os.path.exists("test_requirements_output.txt")
