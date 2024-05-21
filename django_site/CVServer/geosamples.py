from ultralytics import YOLO
import cv2 as cv
import numpy as np
import copy
from CVServer.geosample_model import get_model
import base64

# Load a model
# model = YOLO('./CVServer/geosample_models/best.pt')  # Load a pretrained model

# CAPTIONING_PROMPT = """
# Given the following base64 encoded image of a rock geosmpale, please identify the following properties of the image and respond in json format
# [rock_color, rock_size, rock_description, rock_type]

# Example response:
# { rock_color: "red", rock_size: "10cm", rock_description: "an igneous rock with a red coloring and rough texture. likely has a high iron content", rock_type: "igneous"}
# """

CAPTIONING_PROMPT = "Give a description of the rock in the image and say its color, shape, and type be as brief as possible in the response."


def encode_image_to_base64(file_path):
    with open(file_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')
    return base64_image

def find_rocks(img, generate_caption=False, prompting=None):
    model = get_model()
    print("Starting prediction...")
    # Predict using the model
    results = model.predict(img)

    # Assuming the first result is what we need
    result = results[0]
    
    # Accessing the original image
    img_no_label = copy.deepcopy(result.orig_img)
    img = result.orig_img

    # Filter rocks based on the confidence and size of their bounding box
    rock_boxes = [box for box in result.boxes if result.names[box.cls[0].item()] == 'detect' and box.conf.item() >= 0.90]
    rock_boxes.sort(key=lambda box: (box.xyxy[0][2] - box.xyxy[0][0]) * (box.xyxy[0][3] - box.xyxy[0][1]), reverse=True)
    print(f"Total rocks detected with >= 90% accuracy: {len(rock_boxes)}")

    # Select top three largest rocks with >= 90% accuracy
    top_3_rocks = rock_boxes[:3]

    # Draw rectangle around each of the top three rocks
    for box in top_3_rocks:
        cords = box.xyxy[0].tolist()
        cords = [round(x) for x in cords]

        img = cv.rectangle(img, (cords[0], cords[1]), (cords[2], cords[3]), (255, 0, 0), 20)
        confidence = round(100 * box.conf.item(), 2)

        # Set text properties
        text = f"{confidence}%"
        font = cv.FONT_HERSHEY_SIMPLEX
        font_scale = 1
        color = (255, 255, 255)  # White
        thickness = 2
        cv.putText(img, text, (cords[0], cords[1] - 10), font, font_scale, color, thickness)

    # Save the image with rectangles
    new_filename = f"temp_rock_output.jpg"
    # Save the image with rectangles
    cv.imwrite(new_filename, img)

    caption = {"type": "No caption generated"}
    if not top_3_rocks:
        rock_com = [0, 0]
    else:        
        cords = top_3_rocks[0].xyxy[0].tolist()               
        cords = [round(x) for x in cords]        
        rock_com = [(cords[0]+cords[2])//2, (cords[1]+cords[3])//2]    
        # return [[200,200]], "This is a cup"

        # Caption identified portion
        if generate_caption and prompting:
            cropped_img = img_no_label[cords[1]:cords[3], cords[0]:cords[2]]
            new_crop_filename = f"temp_rock_cropped_output.jpg"
            cv.imwrite(new_crop_filename, cropped_img)
            
            base64_image = encode_image_to_base64(new_crop_filename)
            
            caption = prompting.execute_command_image(CAPTIONING_PROMPT, base64_image)

    return [rock_com], caption
