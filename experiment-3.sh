HANDPICKED="experiments/handpicked.csv"
OPTIONS=("full" "head" "face")

# load the csv into an array
if [[ ! -z $(tail -n 1 $HANDPICKED) ]]; then
  echo "" >> $HANDPICKED
fi

arr_csv=()
while IFS='\n' read -r line; do
  arr_csv+=("$line")
done < "$HANDPICKED"

for row in "${arr_csv[@]}"; do
  if [[ $row[0] == *"Identifier"* ]]; then
    continue
  fi
  if [[ -z "$row" ]]; then
    continue
  fi

  row=$(echo "$row" | tr -d ' ')
  IFS=',' read -ra row_elems <<< "$row"
  echo "${row_elems[0]}, ${row_elems[1]}, ${row_elems[2]}"



  docker compose run --rm facemorpher bash -c "facemorpher \
    --src /experiments/${row_elems[1]} \
    --dest /experiments/${row_elems[2]} \
    --num 100 \
    --out_frames /experiments/experiment-3-facemorpher-frames/${row_elems[0]}/ \
    --background=transparent"

  OPTIONS=("head")
  for MORPH in "${OPTIONS[@]}"; do
    echo $MORPH ${row_elems[0]} 

    docker compose run --rm morph bash -c "python /morphing/morpher.py \
      --src /experiments/${row_elems[1]} \
      --dst /experiments/${row_elems[2]} \
      --out /experiments/experiment-3/$MORPH-${row_elems[0]} \
      --frames /experiments/experiment-3-facemorpher-frames/${row_elems[0]}/ \
      --morph $MORPH \
      --iterations 100"
  done
done



TEST_DIRS=()
while IFS= read -d $'\0' -r dir; do
  TEST_DIRS+=("'/$dir',")
done < <(find experiments/experiment-3 -mindepth 1 -type d -print0)
TEXT_DIRS="${TEST_DIRS[@]}"
TEXT_DIRS="\"["${TEXT_DIRS%?}"]\""
echo $TEXT_DIRS


mkdir experiments/experiment-2
docker compose run --rm eval bash -c "python /experiments-code/experiment-2-prepare-csv.py \
  --dirs $TEXT_DIRS \
  --output /experiments/experiment-3/sets.csv"

grep "_head_0\.[0-9]*\.png," sets-head.csv | awk -F"_head_0\\.|\\.png," '$2<50{print}' > sets-head-half.csv

docker compose run --rm detect-diff bash -c "python main.py \
  --data_dir /experiments/experiment-3/ \
  --out_dir /experiments/experiment-3-diff-det/ \
  --csv_file /experiments/experiment-3/sets.csv"


docker compose run --rm eval bash -c "python /experiments-code/evaluate-diff-detect-morph.py \
  --csv_dir /experiments/experiment-3-diff-det/"