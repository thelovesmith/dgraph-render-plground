# Run this script with sentence_transformers 2.5.1 and torch 2.2.0
# Updated for PyTorch 2.x compatibility
# The output format may vary between PyTorch versions 

import os
from sentence_transformers import SentenceTransformer

def download_model():
    """Download and save the all-MiniLM-L6-v2 model locally"""
    
    model_path = "./model"
    
    # Create model directory if it doesn't exist
    os.makedirs(model_path, exist_ok=True)
    
    print("Downloading all-MiniLM-L6-v2 model...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    print(f"Saving model to {model_path}...")
    model.save(model_path)
    
    # Verify the model was saved correctly
    model_files = os.listdir(model_path)
    print(f"Model files saved: {model_files}")
    
    # PyTorch 2.x may use different model file formats
    if 'pytorch_model.bin' in model_files:
        print("✓ Model saved successfully with pytorch_model.bin format")
    elif 'model.safetensors' in model_files:
        print("✓ Model saved successfully with safetensors format (PyTorch 2.x)")
    elif any(f.endswith('.bin') or f.endswith('.safetensors') for f in model_files):
        print("✓ Model saved successfully with PyTorch format")
    else:
        print("⚠ Warning: No recognizable model files found")
        print("  This may still work if the model uses a different format")
    
    print("Model download and save completed!")

if __name__ == "__main__":
    download_model()
