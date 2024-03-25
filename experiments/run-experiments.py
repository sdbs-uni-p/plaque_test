import datetime
import json
import os
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

temp_dir = "tmp"


def get_args(config, res_dir, experiment, rows):
    csv_name = config["input"]
    input = csv_name
    experiment_name = (config["name"] + "_" + experiment["name"] + "_rows_" + str(rows)).replace(" ", "-")
    outdir = f'{res_dir}/{config["outdir"]}'
    if rows > 0:
        # create temporary csv file with specified number of rows
        input = f"{temp_dir}/{experiment_name}.csv"
        if not os.path.exists(input.rsplit("/", 1)[0]):
            os.makedirs(input.rsplit("/", 1)[0], exist_ok=True)
        with open(input, "w") as f:
            with open(csv_name, "r") as original:
                for i in range(rows):
                    f.write(next(original))

    args = ["java", "-jar", "relational_information_content.jar", input]

    if experiment["find fds"]:
        args.append("--find-fds")
    args.append("--name")
    args.append(f"{outdir}/{experiment_name}.csv")
    if experiment["optimizations"]:
        args.append("-i")
        args.append("-s")
    if experiment["monte carlo"] > 0:
        args.append("-r")
        args.append(str(experiment["monte carlo"]))

    for fd in experiment["fds"]:
        args.append(fd)

    return args, experiment_name


def run_experiment(config, res_dir, timeout, experiment, rows):
    args, experiment_name = get_args(config, res_dir, experiment, rows)
    start = datetime.datetime.now()
    print(f"{start}: {experiment_name} started")
    proc = subprocess.Popen(args, start_new_session=True)
    try:
        proc.wait(timeout=timeout)
        end = datetime.datetime.now()
        runtime = datetime.datetime.timestamp(end) - datetime.datetime.timestamp(start)
        print(f"{end}: {experiment_name} finished in {runtime} seconds")
        return [experiment_name, experiment["monte carlo"], rows, int(runtime * 1000)]
    except subprocess.TimeoutExpired:
        end = datetime.datetime.now()
        runtime = datetime.datetime.timestamp(end) - datetime.datetime.timestamp(start)
        print(f"{end}: {experiment_name} timed out after {runtime} seconds")
        proc.kill()
        return [experiment_name, experiment["monte carlo"], rows, "timeout"]


def run_experiments(conf_paths, res_dir, timeout, workers):
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir, exist_ok=True)

    configs = []
    names = []
    for conf_path in conf_paths:
        with open(conf_path, "r") as f:
            config = json.load(f)
            configs.append(config)
            names.append(config["name"])
        if not os.path.exists(f'{res_dir}/{config["outdir"]}'):
            os.makedirs(f'{res_dir}/{config["outdir"]}', exist_ok=True)

    if len(names) != len(set(names)):
        raise Exception("ambiguous naming, check names in config files")

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(run_experiment, config, res_dir, timeout, experiment, rows)
                   for config in configs for rows in config["rows"] for experiment in config["experiments"]]

    for config in configs:
        runtimes = [["experiment", "monte carlo", "rows", "runtime"]]
        for future in as_completed(futures):
            result = future.result()
            if "_".join(result[0].split("_")[:-3]) == config["name"]:
                runtimes.append(result)
        with open(f'{res_dir}/{config["outdir"]}/{config["name"]}_runtimes.csv', "w") as f:
            for row in runtimes:
                f.write(",".join(map(str, row)) + "\n")

    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)


if __name__ == "__main__":
    results_dir = sys.argv[1]
    timeout_seconds = int(sys.argv[2])
    threads = int(sys.argv[3])
    config_paths = tuple(sys.argv[4:])
    run_experiments(config_paths, results_dir, timeout_seconds, threads)
