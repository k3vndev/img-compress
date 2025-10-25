from PIL import Image
import os

def compress_image(input_path, output_path, quality=85):
    """
    Compress an image and save it to the specified output path.

    :param input_path: Path to the input image file.
    :param output_path: Path to save the compressed image file.
    :param quality: Quality of the compressed image (1-100).
    """
    # Open the image file
    with Image.open(input_path) as img:
        # Save the image with the specified quality
        img.save(output_path, "WEBP", quality=quality)


# Extract all the images on this path
input_directory = "./"
output_directory = "./compressed_images/"

os.makedirs(output_directory, exist_ok=True)

for filename in os.listdir(input_directory):
    if filename.lower().endswith(('.png')):
        input_path = os.path.join(input_directory, filename)

        webp_filename = filename[0:-3] + 'webp'
        output_path = os.path.join(output_directory, webp_filename)


        compress_image(input_path, output_path, quality=85)
        print(f"Compressed {webp_filename} and saved to {output_directory}")