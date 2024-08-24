from fastcore.all import *
from fastai.vision.all import *

# Training script path
path = Path('bird_or_not')

# Load the data
dls = DataBlock(
    blocks=(ImageBlock, CategoryBlock), 
    get_items=get_image_files, 
    splitter=RandomSplitter(valid_pct=0.2, seed=42),
    get_y=parent_label,
    item_tfms=[Resize(192, method='squish')]
).dataloaders(path, bs=32)

# Initialize and train the model
learn = vision_learner(dls, resnet18, metrics=error_rate)
learn.fine_tune(3)

# Save the model to the mounted volume (outside of Docker container)
model_save_path = Path("/app/output/model.pkl")
learn.export(model_save_path)

print(f"Model saved to: {model_save_path}")
