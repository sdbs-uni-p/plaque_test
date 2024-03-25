#!/bin/bash

description=""
timeout_seconds=86400
threads=1
skip_ent_calc=false

i=1
while [ $i -lt $# ]
do
  if [ "${!i}" == "--description" ]
  then i=$((i+1)); description=${!i}
  elif [ "${!i}" == "--timeout" ]
  then i=$((i+1)); timeout_seconds=${!i}
  elif [ "${!i}" == "--threads" ]
  then i=$((i+1)); threads=${!i}
  elif [ "${!i}" == "--skip-entropy-calc" ]
  then i=$((i+1)); skip_ent_calc=${!i}
  else echo "\"${!i}\" not a valid command"; exit 1
  fi
  i=$((i+1))
done

if [ $i -eq $# ]
then echo "\"${!i}\" not a valid command or parameter missing"; exit 1
fi

if [[ ! "$description" =~ ^[0-9A-Za-z_-]*$ ]]
then echo "Description can only contain letters, numbers, '_' and '-'"; exit 1
fi

results_dir_new="results$(if [ "$description" != "" ]; then echo "_$description"; fi)_\
$(if [ "$skip_ent_calc" == true ]; then echo "skip_entropy_calculations"; else echo "threads_${threads}_timeout_${timeout_seconds}s"; fi)"

j=1
finished=false
results_dir_new_prefix="$results_dir_new"
while [ "$finished" == false ]
do
  if [ -d "$results_dir_new" ]
  then j=$((j+1)); results_dir_new="${results_dir_new_prefix}($j)"
  else finished=true
  fi
done

mkdir -p "$results_dir_new"

if [ "$skip_ent_calc" == true ]
then results_dir="results"
elif [ "$skip_ent_calc" == false ]
then
  results_dir="$results_dir_new"
  python3 run-experiments.py "$results_dir" $timeout_seconds $threads \
    tables/echocardiogram/config.json \
    tables/ncvoter/config.json \
    tables/adult/config.json \
    tables/iris/config.json \
    tables/satellites/config_opt-on.json \
    tables/satellites/config_opt-off.json \
    tables/satellites/config.json
else echo "skip_entropy_calc not set correctly"; rm -r "$results_dir_new"; exit 1
fi
wait

python3 heatmap_runtimes.py satellites "${results_dir}/satellites/satellites_runtimes.csv" "$results_dir_new"

mc_sat=${results_dir}/satellites/satellites_monte-carlo-100-000_rows_150.csv
mc_adult=${results_dir}/adult/adult_monte-carlo-100-000_rows_150.csv
mc_echo=${results_dir}/echocardiogram/echocardiogram_monte-carlo-100-000_rows_132.csv
mc_iris=${results_dir}/iris/iris_monte-carlo-100-000_rows_150.csv
mc_ncvoter=${results_dir}/ncvoter/ncvoter_monte-carlo-100-000_rows_150.csv

mc_sat_1000=${results_dir}/satellites/satellites_monte-carlo-1-000_rows_150.csv
mc_sat_1000000=${results_dir}/satellites/satellites_monte-carlo-1-000-000_rows_150.csv

if test -f "$mc_sat"
then python3 histogram.py satellites "$mc_sat" "$results_dir_new"
fi

if test -f "$mc_sat_1000" && test -f "$mc_sat_1000000"
then
  python3 histogram_entropy_diffs.py satellites "$mc_sat_1000" "$mc_sat_1000000" "$results_dir_new"
  python3 heatmap_entropies.py satellites "$mc_sat_1000" "$results_dir_new" desc "mc-1000"
  python3 heatmap_entropies.py satellites "$mc_sat_1000000" "$results_dir_new" desc "mc-1000000"
fi

if test -f "$mc_sat"
then python3 heatmap_entropies.py satellites "$mc_sat" "$results_dir_new" zoom results/satellites/satellites_monte-carlo-100-000_rows_150_r109-128.csv tables/satellites/satellites_zoom.csv
fi

if test -f "$mc_adult"
then python3 heatmap_entropies.py adult "$mc_adult" "$results_dir_new"
fi

if test -f "$mc_echo"
then python3 heatmap_entropies.py echocardiogram "$mc_echo" "$results_dir_new"
fi

if test -f "$mc_iris"
then python3 heatmap_entropies.py iris "$mc_iris" "$results_dir_new"
fi

if test -f "$mc_ncvoter"
then python3 heatmap_entropies.py ncvoter "$mc_ncvoter" "$results_dir_new"
fi

python3 accuracy.py "$results_dir_new"
