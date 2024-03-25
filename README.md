# A Plaque Test for Redundancies in Relational Data - Reproduction Package

This is a reproduction package for the paper "A Plaque Test for Redundancies in Relational Data" by Christoph Köhnen, Stefan Klessinger, Jens Zumbrägel and Stefanie Scherzinger, 
published in the QDB workshop co-located with VLDB 2023.
It contains a program code as a submodule and experiments on real-world datasets, executed with this program.

This reproduction package provides a Docker container.

The datasets are located in the directory ``experiments/tables``, the original results in the directory ``experiments/results``.

## Setting up the reproduction package
Clone the reproduction package and the program code using the parameter ``--recurse-submodules``:
````shell
git clone https://github.com/sdbs-uni-p/plaque_test.git --recurse-submodules
````
You can set up the package on the host system or on a docker container.

### Setup on host system
Enter the submodule, set up the program and copy the jar file into the folder ``experiments``:
````shell
cd relational_information_content
mvn clean install
cd ..
cp relational_information_content/target/relational_information_content-1.0-SNAPSHOT-jar-with-dependencies.jar experiments/relational_information_content.jar
````

### Setting up a docker container
````shell
docker build -t plaque_test_experiments .
docker run -it plaque_test_experiments
````

## Running the experiments
On the host system or in the docker container, enter the experiments folder and run the experiments:
````shell
cd experiments
./run_experiments.sh
````

Optionally, a description can be added:
* ``--description <description>``: A description to appear in the name of the results folder. The default is the empty string.

The experiments can take several hours. To reduce the runtime, use the provided options:
* ``--threads <number>``: Multiple experiments are parallelized in ``<number>`` threads. The default value is 1.
* ``--timeout <seconds>``: Each entropy computation aborts after ``<seconds>`` seconds. The default value is 86400 seconds, i.e., 24 hours.
* ``--skip-entropy-calc <boolean>``: Only produces charts using the results in the folder ``results`` if ``<boolean>`` is true. The default value is false.

The results of the experiments are saved in the folder ``results_<description>_threads_<number>_timeout_<seconds>s`` or ``results_<description>_skip_entropy_calculations``.

## Folder structure
The repository consists of the folders ``relational_information_content`` and ``experiments``.

### The folder ``relational_information_content``
This folder contains the [relational information content program code](https://github.com/sdbs-uni-p/relational_information_content) as a submodule.

To run the experiments on a specified version, enter this folder and checkout this version.

### The folder ``experiments``
This folder consists of the following components:
* Python scripts to run the relational information content program for experiments and to create charts.
* The script ``run_experiments.sh`` to run all the experiments and create charts.
* The folder ``tables`` containing the data and configuration files.
* The folder ``results`` with the original experiment results. It contains:
  * The files ``accuracy.pdf`` and ``accuracy_compact.pdf`` which plot the sufficient number of iterations for the Monte Carlo method to achieve an accuracy with a specified confidence.
  * The folders ``adult``, ``echocardiogram``, ``iris`` and ``ncvoter``. Each folder contains a CSV file with the entropy values computed with the Monte Carlo method (100,000 iterations) on an excerpt consisting of the first 150 rows (or all 132 rows for ``echocardioram``), a CSV file with the runtime of the computation and a PDF file which illustrates the plaque.
  * The folder ``satellites``. The dataset is considered on the first 150 rows only. It contains the following files:
    * ``satellites.pdf``: Illustrates the plaque based on the entropy values computed with the Monte Carlo method (100,000 iterations).
    * ``satellites_monte-carlo-100-000_rows_150.csv``: Contains the entropy values computed with the Monte Carlo method (100,000 iterations).
    * ``satellites_monte-carlo-100-000_rows_150_r109-128.csv``: Contains the entropy values from ``satellites_monte-carlo-100-000_rows_150.csv``, but restricted to the rows from 109 to 128.
    * ``satellites_runtimes.csv``: Contains the runtimes of the Monte Carlo computations for different numbers of rows (e.g., excerpt containing first 10 rows) and iterations.
    * ``satellites_opt-off_runtimes.csv``: Contains the runtimes of the unoptimized computations for different numbers of rows.
    * ``satellites_opt-on_runtimes.csv``: Contains the runtimes of the optimized computations (identify entropy values of 1 directly and reduce the table to its relevant rows and columns) for different numbers of rows.
    * ``satellites_runtimes.pdf`` and ``satellites_runtimes_compact.pdf``: Illustrate the runtimes from ``satellites_runtimes.csv`` in a heatmap.
    * ``satellites_zoom.pdf``: Illustrates the entropies in an excerpt of the satellite dataset.
    * ``satellites_with_zoom.jpg``: Shows the plaque computed with the Monte Carlo method (100,000 iterations) zooming into the aforementioned excerpt.
    * ``satellites_hist.pdf``: Contains a histogram about the frequency of entropy values in the given dataset.
    * ``satellites-monte-carlo-1-000_rows_150.csv`` and ``satellites-monte-carlo-1-000-000_rows_150.csv``: Contain the entropy values computed with the Monte Carlo method for 1,000 resp. 1,000,000 iterations.
    * ``satellites-mc-1000.pdf`` and ``satellites-mc-1000000.pdf``: Illustrate the plaque based on the entropy values in ``satellites-monte-carlo-1-000_rows_150.csv`` resp. ``satellites-monte-carlo-1-000-000_rows_150.csv``.
    * ``satellites_entropy_diffs_hist.pdf``: Contains a histogram about the frequency of differences between the entropies computed in ``satellites_monte-carlo-1-000_rows_150.csv`` and ``satellites_monte-carlo-1-000-000_rows_150.csv``.

After running the experiments, the output folder contains the following files and folders (note that each visualization is only created if the necessary entropy computations are not aborted by a timeout):
* The files ``accuracy.pdf`` and ``accuracy_compact.pdf`` which plot the sufficient number of iterations for the Monte Carlo method to achieve an accuracy with a specified confidence.
* The folders ``adult``, ``echocardiogram``, ``iris`` and ``ncvoter``. Each folder contains a CSV file with the entropy values computed with the Monte Carlo method (100,000 iterations) on an excerpt consisting of the first 150 rows (or all 132 rows for ``echocardioram``), a CSV file with the runtime of the computation and a PDF file which illustrates the plaque.
* The folder ``satellites``. The dataset is considered on the first 150 rows only. It contains the following files:
  * ``satellites_heatmap_entropies.pdf``: Illustrates the plaque based on the entropy values computed with the Monte Carlo method (100,000 iterations).
  * ``satellites_heatmap_entropies_mc-1000.pdf``: Illustrates the plaque based on the entropy values computed with the Monte Carlo method (1,000 iterations).
  * ``satellites_heatmap_entropies_mc-1000000.pdf``: Illustrates the plaque based on the entropy values computed with the Monte Carlo method (1,000,000 iterations).
  * ``satellites_monte-carlo-<iterations>_rows_<num_rows>.csv``: Contains the entropy values computed with the Monte Carlo method (``<iterations>`` iterations), but only on a considered excerpt consisting of the first ``<num_rows>`` rows.
  * ``satellites_opt-off_optimizations-off_rows_<num_rows>.csv``: Contains the entropy values computed without any optimizations, but only on a considered excerpt consisting of the first ``<num_rows>`` rows.
  * ``satellites_opt-on_optimizations-on_rows_<num_rows>.csv``: Contains the entropy values computed with optimizations (identify entropy values of 1 directly and reduce the table to its relevant rows and columns), but only on a considered excerpt consisting of the first ``<num_rows>`` rows.
  * ``satellites_runtimes.csv``: Contains the runtimes of the Monte Carlo computations for different numbers of rows and iterations.
  * ``satellites_opt-off_runtimes.csv``: Contains the runtimes of the unoptimized computations for different numbers of rows.
  * ``satellites_opt-on_runtimes.csv``: Contains the runtimes of the optimized computations for different numbers of rows.
  * ``satellites_runtimes.pdf`` and ``satellites_runtimes_compact.pdf``: Illustrate the runtimes from ``satellites_runtimes.csv`` in a heatmap.
  * ``satellites_zoom.pdf``: Illustrates the entropies in an excerpt of the satellite dataset.
  * ``satellites_hist.pdf``: Contains a histogram about the frequency of entropy values in the given dataset.
  * ``satellites_entropy_diffs_hist.pdf``: Contains a histogram about the frequency of differences between the entropies computed in ``satellites_monte-carlo-1-000_rows_150.csv`` and ``satellites_monte-carlo-1-000-000_rows_150.csv``.

## Datasets
The satellites dataset is retrieved from the input data of the [Metanome tool](https://github.com/HPI-Information-Systems/Metanome/blob/metanome_cli/backendwar/src/main/resources/inputData/WDC_satellites.csv).
The datasets adult, echocardiogram, iris, and ncvoter are retrieved from [HPI Potsdam](https://hpi.de/naumann/projects/repeatability/data-profiling/fds.html).

## About
To reference this work, please use the following BibTeX entry.
````bibtex
@inproceedings{DBLP:conf/vldb/KohnenKZS23,
  author       = {Christoph K{\"{o}}hnen and
                  Stefan Klessinger and
                  Jens Zumbr{\"{a}}gel and
                  Stefanie Scherzinger},
  title        = {A Plaque Test for Redundancies in Relational Data},
  booktitle    = {Joint Proceedings of Workshops at the 49th International Conference
                  on Very Large Data Bases {(VLDB} 2023), Vancouver, Canada, August
                  28 - September 1, 2023},
  series       = {{CEUR} Workshop Proceedings},
  volume       = {3462},
  year         = {2023}
}
````

All artifacts, including source code, data, and scripts, are available on Zenodo, DOI: [10.5281/zenodo.8220684](https://doi.org/10.5281/zenodo.8220684).

The reproduction package was created by Christoph Köhnen. The experimental scripts were created by Stefan Klessinger and Christoph Köhnen.

This work was partly funded by Deutsche Forschungsgemeinschaft (DFG, German Research Foundation) grant #385808805.
