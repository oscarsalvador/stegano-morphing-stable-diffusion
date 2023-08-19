SRC_IMG="src.jpg"
DST_IMG="dst.jpg"
FOLDER="project"
ITERATIONS=100

docker compose build 

echo -e "\n\n\nFacemorpher generating frames"
rm -rf $FOLDER/facemorph-frames
docker compose run --rm facemorpher bash -c "facemorpher \
  --src $SRC_IMG \
  --dest $DST_IMG \
  --num $ITERATIONS \
  --out_frames facemorph-frames \
  --background=transparent"


# python morpher.py --src full_img/source_image-0.jpg --dst full_img/destination_image-0.jpg --out here --frames frames --morph face --iterations 10
OPTIONS=("full" "head" "face")
for MORPH in "${OPTIONS[@]}"; do
  docker compose run --rm morph bash -c "python /morphing/morpher.py \
    --src $SRC_IMG \
    --dst $DST_IMG \
    --out morphing/$MORPH \
    --frames facemorph-frames \
    --morph $MORPH \
    --iterations $ITERATIONS"
done

