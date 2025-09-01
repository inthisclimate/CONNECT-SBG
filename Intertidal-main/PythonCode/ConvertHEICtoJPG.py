import os
from PIL import Image
import pillow_heif

# Register HEIF opener
pillow_heif.register_heif_opener()

# Set paths
source_folder = "/Users/kylamonique/Desktop/JPLFiles/SpectralEvolution/FieldData/PV0504/Quadrat Images" #Folder for HEIC inputs
destination_folder = "/Users/kylamonique/Desktop/JPLFiles/SpectralEvolution/FieldData/PV0504/Quadrat Images/JPG" #Folder for JPG outputs
os.makedirs(destination_folder, exist_ok=True)

# Convert all HEIC files
for filename in os.listdir(source_folder):
    if filename.lower().endswith(".heic"):
        heic_path = os.path.join(source_folder, filename)
        jpg_filename = os.path.splitext(filename)[0] + ".jpg"
        jpg_path = os.path.join(destination_folder, jpg_filename)

        try:
            image = Image.open(heic_path)
            image.save(jpg_path, "JPEG")
            print(f"Converted: {filename} -> {jpg_filename}")
        except Exception as e:
            print(f"Failed to convert {filename}: {e}")
