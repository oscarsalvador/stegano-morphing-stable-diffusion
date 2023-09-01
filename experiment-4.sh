OPTIONS=("full" "head" "face")

for MORPH in "${OPTIONS[@]}"; do
  mkdir -p experiments/experiment-4/input
  docker compose run --rm eval bash -c "python /experiments-code/experiment-4.prepare-csvs.py \
    --dir /experiments/experiment-3/ \
    --output /experiments/experiment-4/input/ \
    --handpicked /experiments/handpicked.csv \
    --filter $MORPH"
done

for MORPH in "${OPTIONS[@]}"; do
  mkdir -p experiments/experiment-4/output
  # for file in $(ls experiments/experiment-4/input/ | grep $MORPH | grep "0-50" | sort); do
  for file in $(ls experiments/experiment-4/input/ | grep $MORPH | sort); do
    # echo $file
    NAME=$(echo $file | rev | cut -d "/" -f1 | rev | cut -d "." -f1)

    TEST_CSV="/experiments/experiment-4/input/$NAME.csv"
    OUTPUT_PATH="/experiments/experiment-4/output/$NAME"

    docker compose run --rm detect-morph bash -c "python test.py --test_csv $TEST_CSV \
      --model_path casia_smdd.pth \
      --output_path $OUTPUT_PATH\"_results.csv\" | tee >(grep threshold > $OUTPUT_PATH\"_threshold.txt\")"
  done
done


docker compose run --rm eval bash -c "python /experiments-code/evaluate-morph-det.py \
  --csv_dir /experiments/experiment-4/output/"