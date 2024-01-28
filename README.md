# Pexels Image Transformer

This repository contains a Python script that interacts with the Pexels API to download images and then applies various transformations to create abstract art. 

![abstract_art_1706373451](https://github.com/oscarpark0/pexels-image-transformer/assets/115663638/eaa1d1a3-1bdc-4bf4-8fdb-b1b335e5c3a4)![abstract_art_1706405133](https://github.com/oscarpark0/pexels-image-transformer/assets/115663638/1436e32c-cf6f-4d32-814a-673bdc740810)


## Dependencies
- `requests`: For making HTTP requests to the Pexels API.
- `PIL`: Python Imaging Library, to work with images.
- `io`: For handling byte streams.
- `random`: For generating random values.
- `sys`: For interacting with the Python interpreter.
- `time`: For time-related functionality.

## Installation
1. Clone the repository using 

```bash
git clone https://github.com/your_username/pexels-image-transformer.git
```

2. Install the required dependencies using 

```bash
pip install -r requirements.txt
```

3. Obtain a Pexels API key from [Pexels](https://www.pexels.com/api/).

## Usage
1. Run the script using 

```bash
python pexels_image_transformer.py
```

2. The script will download images from Pexels, apply various transformations, and create abstract art images.

3. The final abstract art image will be saved with a unique filename based on the current timestamp.

## Overview
The script interacts with the Pexels API to download an image, then applies a series of random transformations to the image. These transformations include flipping, enhancing color, brightness, contrast, applying filters, and color transformations. 

The script then blends the transformed images onto a canvas to create a final abstract art image. It applies color correction to boost saturation and saves the final abstract art image with a unique filename.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
- The Pexels API for providing access to a vast library of high-quality images.
- The Python community for developing and maintaining the `PIL` library and other dependencies.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

This README provides an overview of the repository, how to install and use the script, its dependencies, license information, acknowledgments, contribution guidelines, and support information.
