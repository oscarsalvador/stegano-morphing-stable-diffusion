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
#     --iterations $ITERATIONS"
# done

# # if it crashes due to lack of memory, reduce the batch size
# docker compose run --rm morph bash -c "python /morphing/prepare_csvs.py \
#   --dst $DST_IMG \
#   --morphs /$FOLDER/morphing/ \
#   --batch_size 30"


# rm -rf $FOLDER/det_diff_results
# docker compose run --rm detect-diff bash -c "python main.py \
#   --data_dir /$FOLDER/morphing/ \
#   --out_dir /$FOLDER/det_diff_results \
#   --csv_file /$FOLDER/morphing/detect-diff.csv"


# rm -rf $FOLDER/det_morph_results
# docker compose run --rm detect-morph bash -c "/detect-morph/wrapper.sh \
#   /$FOLDER/morphing \
#   /$FOLDER/det_morph_results"


# mkdir $FOLDER/det_arcfaces
# docker compose run --rm arcfaces bash -c "python /arcfaces/arcfaces.py \
#   --people \"[['diffused', ['/$FOLDER/$SRC_IMG']], ['original', ['/$FOLDER/$DST_IMG']]]\" \
#   --images_dir /$FOLDER/morphing/head \
#   --out_dir /$FOLDER/det_arcfaces"
