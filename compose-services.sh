SRC_IMG="src.jpg"
DST_IMG="dst.jpg"
FOLDER="project"
ITERATIONS=100

# docker compose build 

# echo -e "\n\n\nFacemorpher generating frames"
# rm -rf $FOLDER/facemorph-frames
# docker compose run --rm facemorpher bash -c "facemorpher \
#   --src $SRC_IMG \
#   --dest $DST_IMG \
#   --num $ITERATIONS \
#   --out_frames facemorph-frames \
#   --background=transparent"


# OPTIONS=("full" "head" "face")
# for MORPH in "${OPTIONS[@]}"; do
#   docker compose run --rm morph bash -c "python /morphing/morpher.py \
#     --src $SRC_IMG \
#     --dst $DST_IMG \
#     --out morphing/$MORPH \
#     --frames facemorph-frames \
#     --morph $MORPH \
#     --iterations $ITERATIONS; \
#     python /morphing/prepare_csvs.py \
#       --src $SRC_IMG \
#       --morphs /$FOLDER/morphing/"
# done


# rm -rf $FOLDER/diff_results
# docker compose run --rm detect-diff bash -c "python main.py \
#   --data_dir /$FOLDER/morphing/ \
#   --out_dir /$FOLDER/diff_results \
#   --csv_file /$FOLDER/morphing/detect-diff.csv"


