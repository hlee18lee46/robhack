import os
import glob
from PIL import Image, ImageDraw, ImageFont

# Define the folder where images are stored
image_folder = "C:/Users/Han Lee/OneDrive - Georgia Institute of Technology/thieves"

# Function to get the most recent image
def get_latest_image(folder):
    image_files = glob.glob(os.path.join(folder, "*.*"))  # Get all files
    image_files = [f for f in image_files if f.lower().endswith(('.png', '.jpg', '.jpeg'))]  # Filter images
    
    if not image_files:
        print("No images found in the folder.")
        return None
    
    latest_image = max(image_files, key=os.path.getctime)  # Get most recent file
    return latest_image

# Function to overlay text on the image
def add_text_to_image(image_path, output_path):
    try:
        img = Image.open(image_path)

        # Resize without ANTIALIAS (Pillow 10+ does this automatically)
        img = img.resize((800, 600))

        draw = ImageDraw.Draw(img)
        
        # Set font and size (make sure Arial.ttf is available or change the font path)
        try:
            font = ImageFont.truetype("arial.ttf", 60)  # Adjust size as needed
        except IOError:
            font = ImageFont.load_default()

        # Define text and position
        text = "Thief EXPOSED!\nSHARED to Cloud"
        text_x, text_y = 50, 50  # Adjust position

        # Add text with a red color and white outline
        outline_color = "white"
        text_color = "red"
        
        for offset in range(-2, 3):  # Creates an outline effect
            draw.text((text_x + offset, text_y), text, font=font, fill=outline_color)
            draw.text((text_x, text_y + offset), text, font=font, fill=outline_color)

        draw.text((text_x, text_y), text, font=font, fill=text_color)  # Main text

        # Save new image
        img.save(output_path)
        print(f"Modified image saved at: {output_path}")

    except Exception as e:
        print(f"Error processing image: {e}")

# Main execution
latest_image = get_latest_image(image_folder)

if latest_image:
    output_image_path = os.path.join(image_folder, "EXPOSED_thief.jpg")
    add_text_to_image(latest_image, output_image_path)
else:
    print("No image found to process.")
