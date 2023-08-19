SRC_IMG=$1
MORPHS_DIR=$2
RESULT_DIR=$3

echo $SRC_IMG $MORPHS_DIR $RESULT_DIR

cd /detect-diff
# python prepare_csv.py --src /project/destination_image.png --morphs /project/morphing/
python prepare_csv.py --src $SRC_IMG --morphs $MORPHS_DIR

# exit

cd /dmimagedetection
# python main.py --data_dir /project/morphing/ --out_dir /project/diff_results --csv_file /detect-diff/detect-diff.csv
python main.py --data_dir $MORPHS_DIR --out_dir $RESULT_DIR --csv_file /detect-diff/detect-diff.csv