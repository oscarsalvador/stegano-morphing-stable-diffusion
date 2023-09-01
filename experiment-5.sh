mkdir experiments/experiment-5-arcfaces/

docker compose run --rm eval bash -c "python /experiments-code/combined-detector.py \
  --morph_csv_dir /experiments/experiment-4/output/ \
  --diff_csv_dir /experiments/experiment-3-diff-det/ \
  --filter none \
  --out /experiments/ \
  --copy true "

docker compose run --rm eval bash -c "python /experiments-code/combined-detector.py \
  --morph_csv_dir /experiments/experiment-4/output/ \
  --diff_csv_dir /experiments/experiment-3-diff-det/ \
  --filter full \
  --copy false \
  --out /experiments/"

docker compose run --rm eval bash -c "python /experiments-code/combined-detector.py \
  --morph_csv_dir /experiments/experiment-4/output/ \
  --diff_csv_dir /experiments/experiment-3-diff-det/ \
  --filter head \
  --copy false \
  --out /experiments/"

docker compose run --rm eval bash -c "python /experiments-code/combined-detector.py \
  --morph_csv_dir /experiments/experiment-4/output/ \
  --diff_csv_dir /experiments/experiment-3-diff-det/ \
  --filter face \
  --copy false \
  --out /experiments/"

docker compose run --rm arcfaces bash -c "python /arcfaces/arcfaces.py \
  --people \"[['oscar', ['/project/training/IMG_20230821_141251.jpg']], ['oscar', ['/project/training/IMG_20230821_141315.jpg']], ['oscar', ['/project/training/IMG_20230821_141259.jpg']], ['oscar', ['/project/training/IMG_20230821_141306.jpg']], ['oscar', ['/project/training/IMG_20230821_141344.jpg']]]\" \
  --images_dir /experiments/experiment-5-arcfaces \
  --out_dir /experiments/experiment-5-arcfaces"

docker compose run --rm eval bash -c "python /experiments-code/evaluate-arcfaces.py \
  --csv /experiments/experiment-5-arcfaces/detailed_arcfaces.csv"