# RTTI Image Extractor

This Python script automatically extracts the largest possible image from `.rtti` binary files. It reads potential image dimensions, tries to extract corresponding image data, and saves the largest image it can find as a PNG file.

## How It Works

The script scans the binary contents of all `.rtti` files for potential image dimension data. It attempts to read the image data based on these dimensions and, if successful, saves the largest valid image as a PNG file.

# RawTherapee Thumbnail Cache Locations

RawTherapee stores its thumbnails in a cache directory. The location of this cache directory differs between Windows and Linux.

## Windows

C:\Users[YourUserName]\AppData\Local\RawTherapee\cache\

## Linux

/home/[YourUserName]/.cache/RawTherapee/

## Dependencies

Before running the script, you must have Python installed on your system along with the following libraries:

- `Pillow` for image handling.
- `numpy` for efficient array operations.

These can be installed via pip with the following command:


pip install Pillow numpy

# Usage

To use the script:

1. Place the `thumb.py` script in the directory that contains your `.rtti` files.
2. Open your command-line interface (CLI) and navigate to the directory where the script is located.
3. Run the script with the following command:

```bash
python thumb.py
