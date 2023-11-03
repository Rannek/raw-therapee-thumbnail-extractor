import os
import struct
from PIL import Image
import numpy as np

# Function to try reading the image data based on width, height, and header offset
def try_reading_image_data(file, width, height, header_offset):
    file.seek(header_offset)
    try:
        image_data = file.read(width * height * 3)
        if len(image_data) < width * height * 3:
            # If the read data is too short, it's not a valid image
            return None
        image_array = np.frombuffer(image_data, dtype=np.uint8).reshape((height, width, 3))
        return image_array
    except (OverflowError, ValueError):
        return None

# Function to find the largest possible image in the .rtti file
def find_largest_image(rtti_file_path):
    with open(rtti_file_path, 'rb') as file:
        file_content = file.read()
        header_end_index = file_content.find(b'\n')
        if header_end_index == -1:
            return None, None, None

        largest_image = None
        largest_dimensions = (0, 0)
        for offset in range(header_end_index + 1, len(file_content) - struct.calcsize('<II'), 4):
            for dimensions_multiplier in range(1, 4):
                try:
                    width, height = struct.unpack_from('<II', file_content, offset=offset)
                    width *= dimensions_multiplier
                    height *= dimensions_multiplier
                    if 0 < width <= 10000 and 0 < height <= 10000 and width * height > largest_dimensions[0] * largest_dimensions[1]:
                        # Try to read the image data with these dimensions
                        image_array = try_reading_image_data(file, width, height, offset + struct.calcsize('<II'))
                        if image_array is not None:
                            largest_image = image_array
                            largest_dimensions = (width, height)
                except struct.error:
                    break  # Reached the end of the file or invalid data

        return largest_image, largest_dimensions, offset + struct.calcsize('<II') if largest_image is not None else None

# Directory containing .rtti files
current_dir = os.getcwd()

# Iterate over all files in the directory
for filename in os.listdir(current_dir):
        rtti_file_path = os.path.join(current_dir, filename)
        largest_image, dimensions, header_offset = find_largest_image(rtti_file_path)
        if largest_image is not None:
            image_rgb = Image.fromarray(largest_image, 'RGB')
            base_filename = os.path.splitext(filename)[0]
            output_image_rgb_path = os.path.join(current_dir, f"{base_filename}_thmb.png")
            image_rgb.save(output_image_rgb_path)
            print(f"The largest extracted image ({dimensions[0]}x{dimensions[1]}) has been saved to {output_image_rgb_path}")
        else:
            print(f"No valid image found in {filename}")