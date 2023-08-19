MORPH_DIR=$1
OUTPUT_DIR=$2

if [[ "$MORPH_DIR" != */ ]]; then
  MORPH_DIR="$MORPH_DIR/"
fi

if [[ "$OUTPUT_DIR" != */ ]]; then
  OUTPUT_DIR="$OUTPUT_DIR/"
fi


mkdir $OUTPUT_DIR
for file in $(find $MORPH_DIR -name "detect-morph*.csv" | sort); do
  NAME=$(echo $file | rev | cut -d "/" -f1 | rev | cut -d "." -f1)
  python test.py --test_csv $file \
    --model_path casia_smdd.pth \
    --output_path $OUTPUT_DIR$NAME"_results.csv" | tee >(grep threshold > $OUTPUT_DIR$NAME"_threshold.txt")
done