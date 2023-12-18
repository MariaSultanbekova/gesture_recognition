import cv2
import torch
import numpy as np
from PIL import Image
from omegaconf import OmegaConf
from torchvision.transforms import functional as f
from constants import targets
from classifier.utils import build_model


conf = OmegaConf.load('clf_config.yaml')

model = build_model(
    model_name=conf.model.name,
    num_classes=len(targets),
    checkpoint=conf.model.get("checkpoint", None),  # !изменить путь при запуске
    device=conf.device,
    pretrained=conf.model.pretrained,
    freezed=conf.model.freezed,
    ff=conf.model.full_frame,
)
model.eval()


def preprocess(img: np.ndarray):
    """
    Preproc image for model input
    Parameters
    ----------
    img: np.ndarray
        input image
    """
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(img)
    width, height = image.size

    image = image.resize((224, 224))

    img_tensor = f.pil_to_tensor(image)
    img_tensor = f.convert_image_dtype(img_tensor)
    img_tensor = img_tensor[None, :, :, :]
    return img_tensor, (width, height)


def predict(frame):
    processed_frame, size = preprocess(frame)

    with torch.no_grad():
        output = model(processed_frame)
    label = output["gesture"].argmax(dim=1)
    return targets[int(label.item())+1]
