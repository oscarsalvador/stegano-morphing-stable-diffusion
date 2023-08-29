SUBJECT=$1
SUBJECT_CLASS=$2
INSTANCE_DATA_DIR=$3
OUTPUT_DIR=$4
CLASS_DATA_DIR=$5
TRAINING_IMAGES_DIR=$6
# MODEL_WEIGHT_PAIRS=$7
MODEL_NAME=$7

# echo $@


python /dreambooth/prepare.py \
  --subject $SUBJECT \
  --subject_class $SUBJECT_CLASS \
  --instance_data_dir $INSTANCE_DATA_DIR \
  --output_dir $OUTPUT_DIR \
  --class_data_dir $CLASS_DATA_DIR

cp $TRAINING_IMAGES_DIR/* $INSTANCE_DATA_DIR$SUBJECT

python /dreambooth/prepare.py -p \
  --subject $SUBJECT \
  --subject_class $SUBJECT_CLASS \
  --instance_data_dir $INSTANCE_DATA_DIR \
  --output_dir $OUTPUT_DIR \
  --class_data_dir $CLASS_DATA_DIR



# script download now handled in dockerfile
# if [ ! -f train_dreambooth.py ]; then
#   # wget -q https://github.com/ShivamShrirao/diffusers/raw/main/examples/dreambooth/train_dreambooth.py
#   wget -q https://github.com/huggingface/diffusers/blob/main/examples/dreambooth/train_dreambooth.py
# # fi

# MODEL_NAME="runwayml/stable-diffusion-v1-5"
# MODEL_NAME="runwayml/stable-diffusion-inpainting"
# MODEL_NAME="stabilityai/stable-diffusion-2-base"
# MODEL_NAME="stabilityai/stable-diffusion-2-1"

WEIGHTS_DIR=$OUTPUT_DIR"800"
CKPT_DIR="$WEIGHTS_DIR/$SUBJECT.ckpt"
CONCEPTS_LIST_DIR=$(echo $INSTANCE_DATA_DIR | awk -v RS="data" 'NR==1{print}')
CONCEPTS_LIST_PATH=$CONCEPTS_LIST_DIR"concepts_list.json"


# python3 /dreambooth/train_inpainting_dreambooth.py 

python3 /diffusers/train_dreambooth.py \
  --pretrained_model_name_or_path=$MODEL_NAME \
  --pretrained_vae_name_or_path="stabilityai/sd-vae-ft-mse" \
  --output_dir=$OUTPUT_DIR \
  --revision="fp16" \
  --with_prior_preservation --prior_loss_weight=1.0 \
  --seed=1337 \
  --resolution=512 \
  --train_batch_size=1 \
  --train_text_encoder \
  --mixed_precision="fp16" \
  --use_8bit_adam \
  --gradient_accumulation_steps=1 \
  --learning_rate=1e-6 \
  --lr_scheduler="constant" \
  --lr_warmup_steps=0 \
  --num_class_images=50 \
  --sample_batch_size=4 \
  --max_train_steps=800 \
  --save_interval=10000 \
  --save_sample_prompt="photo of $SUBJECT man" \
  --concepts_list=$CONCEPTS_LIST_PATH


echo -e "\n\n\n"

# if [ ! -f convert_diffusers_to_original_stable_diffusion.py ]; then
#   wget -q https://github.com/ShivamShrirao/diffusers/raw/main/scripts/convert_diffusers_to_original_stable_diffusion.py
# fi


# --half => Whether to convert to fp16, takes half the space (2GB).
python /diffusers/convert_diffusers_to_original_stable_diffusion.py \
  --model_path $WEIGHTS_DIR \
  --checkpoint_path $CKPT_DIR \
  --half

echo "MODEL SAVED AS A CKPT IN $CKPT_DIR"

