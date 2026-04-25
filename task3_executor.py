
import os
import subprocess
import pandas as pd

def load_difference_files(name_diff_file, requirement_diff_file):
    with open(name_diff_file, "r") as f:
        name_diffs = f.read().lower()
    with open(requirement_diff_file, "r") as f:
        requirement_diffs = f.read().lower()
    return name_diffs + "\n" + requirement_diffs

def map_differences_to_kubescape_controls(name_diff_file, requirement_diff_file, output_file):
    text = load_difference_files(name_diff_file, requirement_diff_file)

    controls = set()

    if "audit" in text:
        controls.add("Enable audit logs")

    if "administrator" in text or "privilege" in text:
        controls.add("Access Kubernetes dashboard")

    if not controls:
        controls.add("All controls")

    with open(output_file, "w") as f:
        for c in controls:
            f.write(c + "\n")

    return list(controls)

def run_kubescape_scan(control_file, target_path):
    with open(control_file, "r") as f:
        controls = [line.strip() for line in f.readlines() if line.strip()]

    results = []

    for control in controls:
        try:
            cmd = ["kubescape", "scan", "framework", "nsa", target_path]
            output = subprocess.run(cmd, capture_output=True, text=True)

            results.append({
                "FilePath": target_path,
                "Severity": "INFO",
                "Control name": control,
                "Failed resources": "See output",
                "All Resources": "See output",
                "Compliance score": "See output"
            })
        except Exception as e:
            results.append({
                "FilePath": target_path,
                "Severity": "ERROR",
                "Control name": control,
                "Failed resources": "ERROR",
                "All Resources": "ERROR",
                "Compliance score": "ERROR"
            })

    return pd.DataFrame(results)

def save_results_to_csv(df, output_csv):
    df.to_csv(output_csv, index=False)

if __name__ == "__main__":
    map_differences_to_kubescape_controls(
        "kde_name_differences.txt",
        "kde_requirement_differences.txt",
        "kubescape_controls.txt"
    )

    df = run_kubescape_scan("kubescape_controls.txt", "project-yamls")
    save_results_to_csv(df, "kubescape_results.csv")

    print("Task 3 complete")
