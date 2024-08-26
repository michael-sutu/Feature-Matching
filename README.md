# Image Matcher API

This project is a Flask-based API designed to identify if two images contain the same product, specifically for valuing item worth based on eBay results. It leverages OpenCV's Scale-Invariant Feature Transform (SIFT) algorithm to perform image matching and calculates a dynamic range for pricing based on the matching results.

## Features

- **Image Download and Processing**: The API downloads images from URLs, converts them to grayscale, and computes keypoints and descriptors using the SIFT algorithm.
- **Feature Matching**: Uses brute-force matcher to find matches between keypoints of the input image and other images.
- **Dynamic Range Calculation**: Based on the feature matches and a provided condition, it computes a minimum and maximum value range.

## Installation

To run this project, you'll need Python installed with the following dependencies:

- `Flask`: A lightweight WSGI web application framework.
- `OpenCV`: An open-source computer vision and machine learning software library.

You can install these dependencies using pip:

```bash
pip install flask opencv-python
