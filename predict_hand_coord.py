from typing import Tuple
import cv2
import mediapipe as mp
import numpy as np
from PIL import Image, ImageOps
from torch import Tensor
from torchvision.transforms import functional as f



hands = mp.solutions.hands.Hands(
    model_complexity=0, static_image_mode=False, max_num_hands=2, min_detection_confidence=0.8
)


def preprocess(img: np.ndarray) -> Tuple[Tensor, Tuple[int, int], Tuple[int, int]]:
    """
    Preprocess image for model input
    Parameters
    ----------
    img: np.ndarray
        Input image
    """
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(img)
    width, height = image.size

    image = ImageOps.pad(image, (max(width, height), max(width, height)))
    padded_width, padded_height = image.size
    image = image.resize((320, 320))

    img_tensor = f.pil_to_tensor(image)
    img_tensor = f.convert_image_dtype(img_tensor)
    img_tensor = img_tensor[None, :, :, :]
    return img_tensor, (width, height), (padded_width, padded_height)


def predict(img):
    processed_frame, size, padded_size = preprocess(img)

    results = hands.process(img[:, :, ::-1])
    if results.multi_hand_landmarks:
        hand_coord = results.multi_hand_landmarks[0].landmark[9]

        width, height = size
        padded_width, padded_height = padded_size
        scale = max(width, height) / 320

        padding_w = abs(padded_width - width) // (2 * scale)
        # padding_h = abs(padded_height - height) // (2 * scale)

        x = hand_coord.x
        # y = hand_coord.y

        abs_x = int(x * 320)
        # abs_y = int(y * 320)

        original_x = int(abs_x * scale + padding_w)
        # original_y = int(abs_y * scale + padding_h)


        return original_x
