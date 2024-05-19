# myapp/ml_model.py

from ultralytics import YOLO

# Initialize the model variable
model = None

def load_model():
    global model
    print("Loading geosample model...\r")
    model = YOLO('./CVServer/geosample_models/best.pt')  # Load a pretrained model    
    print("Model loaded successfully!")

def get_model():
    if model is None:
        raise ValueError("Model is not loaded, please check the configuration.")
    return model