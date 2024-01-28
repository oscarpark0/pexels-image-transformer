from flask import Flask, render_template, send_file
from flask import request
from PIL import Image, ImageFilter, ImageEnhance, ImageOps, ImageChops, ImageStat
from io import BytesIO
import random
import sys
import time
import os
import requests

app = Flask(__name__)

PEXELS_API_KEY = os.getenv('PEXELS_API_KEY')

# Function to download an image from Pexels
def download_pexels_image():
    headers = {'Authorization': PEXELS_API_KEY}
    response = requests.get('https://api.pexels.com/v1/curated?per_page=1&page=' + str(random.randint(1, 1000)), headers=headers)

    if response.status_code == 200:
        image_data = response.json()
        image_url = image_data['photos'][0]['src']['large']
        image_response = requests.get(image_url)
        return Image.open(BytesIO(image_response.content))
    else:
        print("Failed to retrieve an image from Pexels. Status Code:", response.status_code)
        return None

# Function to generate a random color
def get_random_color():
    return (random.randint(0, 255), random.randint(0, 200), random.randint(0, 255))

# Function to generate a color based on the pixel's position
def get_position_based_color(x, y, width, height):
    return (int(255 * x / width), int(255 * y / height), 128)

# Function to generate a color based on the pixel's original color
def get_color_based_color(pixel):
    r, g, b = pixel
    return (255 - r, 255 - g, 255 - b)

# Function to apply a color transformation to an image
def color_transform(image):
    width, height = image.size
    pixels = image.load()

    for y in range(height):
        for x in range(width):
            pixel = pixels[x, y]
            color = get_position_based_color(x, y, width, height)
            pixels[x, y] = tuple(map(lambda i: (i * pixel[i]) // 255, range(3)))

    return image

# Function to apply random transformations to an image
def random_transform(image):
    # Apply a series of random transformations
    transformations = [
        lambda img: img.transpose(Image.FLIP_LEFT_RIGHT),
        lambda img: img.transpose(Image.FLIP_TOP_BOTTOM),
       # lambda img: img.transpose(Image.ROTATE_90),
       # lambda img: img.transpose(Image.ROTATE_180),
       # lambda img: img.transpose(Image.ROTATE_270),
        lambda img: ImageEnhance.Color(img).enhance(random.uniform(0.5, 1.5)),
        lambda img: ImageEnhance.Brightness(img).enhance(random.uniform(0.5, 1)),
        lambda img: ImageEnhance.Contrast(img).enhance(random.uniform(0.5, 1.5)),
        lambda img: img.filter(ImageFilter.GaussianBlur(radius=random.randint(0, 2))),
        lambda img: ImageOps.colorize(img.convert('L'), get_random_color(), get_random_color()),
        lambda img: ImageChops.multiply(img, Image.new('RGB', img.size, get_random_color())),
        lambda img: img.filter(ImageFilter.EDGE_ENHANCE_MORE),
        lambda img: color_transform(img)
    ]
    return random.choice(transformations)(image)

# Download and transform images
images = []
for i in range(3):
    image = download_pexels_image()
    if image:
        image.save(f'download_{i}.png')  # Save the downloaded image
        transformed_image = random_transform(image)
        transformed_image.save(f'transformed_{i}.png')  # Save the transformed image
        images.append(transformed_image)

# Verify image count
if 0 < len(images) < 3 :
    print("Could not download all images. Exiting.")
    sys.exit()

# Ensure all images are the same size and mode as the first image
base_size = images[0].size
base_mode = 'RGB'
images = [img.resize(base_size).convert(base_mode) for img in images]

# Create a canvas to blend images onto
combined_image = Image.new(base_mode, base_size, (255, 255, 255))

# Calculate consistent alpha based on the number of images
consistent_alpha = 1.0 / len(images)

# Blend images onto the canvas with consistent alpha
for i, image in enumerate(images):
    combined_image = ImageChops.blend(combined_image, image, alpha=consistent_alpha)
    combined_image.save(f'blended_{i}.png')  # Save the blended image

# Apply a final random transformation to the combined image
final_image = random_transform(combined_image)
final_image.save('final_transformed.png')  # Save the final transformed image

# Apply color correction to boost saturation
enhancer = ImageEnhance.Color(final_image)
final_image = enhancer.enhance(1.5)  # Increase color saturation by 50%

# Generate a unique filename using the current timestamp
unique_filename = f'abart_{int(time.time())}.png'

# Save the final abstract art image with the unique filename
final_image.save(unique_filename)
print(f'saved as "{unique_filename}".')

# Function to download and transform images
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        images = []
        for i in range(3):
            image = download_pexels_image()
            if image:
                image.save(f'static/download_{i}.png')  # Save the downloaded image
                transformed_image = random_transform(image)
                transformed_image.save(f'static/transformed_{i}.png')  # Save the transformed image
                images.append(f'static/transformed_{i}.png')

        if len(images) == 3:
          base_size = Image.open(images[0]).size
          base_mode = 'RGB'
          images = [Image.open(img).resize(base_size).convert(base_mode) for img in images]

          combined_image = Image.new(base_mode, base_size, (255, 255, 255))
          consistent_alpha = 1.0 / len(images)

          for i, image in enumerate(images):
              combined_image = ImageChops.blend(combined_image, image, alpha=consistent_alpha)
              combined_image.save(f'static/blended_{i}.png')

          final_image = random_transform(combined_image)
          final_image.save('static/final_transformed.png')
          enhancer = ImageEnhance.Color(final_image)
          final_image = enhancer.enhance(1.5)

          unique_filename = f'static/{int(time.time())}_abart.png'
          final_image.save(unique_filename)

          return render_template('index.html', images=[unique_filename])

    return render_template('index.html', images=[])

@app.route('/download/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)