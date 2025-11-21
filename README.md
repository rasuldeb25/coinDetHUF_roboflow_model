# Parallel Processing Coin Counter

## Overview

The **Parallel Processing Coin Counter** is a desktop application designed to detect, count, and calculate the total value of coins from an image. It utilizes the YOLOv8 (You Only Look Once) object detection model to identify specific coin denominations and provides a visual summary of the results. The application is built using Python and provides a user-friendly Graphical User Interface (GUI).

This tool is specifically configured to recognize Hungarian Forint (Ft) coins, including 5, 10, 50, 100, and 200 denominations.

## Features

*   **Image Upload**: Users can upload images in standard formats (.jpg, .jpeg, .png) directly through the GUI.
*   **Object Detection**: leverages a pre-trained YOLO model (`weights.pt`) to accurately detect coins within the image.
*   **Visual Feedback**:
    *   Draws bounding boxes around detected coins.
    *   Labels each coin with its denomination and detection confidence score.
    *   Uses distinct colors for different coin denominations for easy visual differentiation.
*   **Automated Counting**: Automatically counts the number of coins for each denomination.
*   **Total Value Calculation**: Computes the total monetary value of all detected coins.
*   **Summary Report**: Displays a detailed side-panel report listing the count and subtotal for each coin type, as well as the grand total.

## Technologies Used

*   **Python**: The core programming language.
*   **Tkinter**: Used for building the Graphical User Interface (GUI).
*   **Ultralytics YOLOv8**: The state-of-the-art object detection model used for identifying coins.
*   **OpenCV (cv2)**: Used for image processing, drawing bounding boxes, and handling image data.
*   **Pillow (PIL)**: Python Imaging Library, used for image manipulation and displaying images within the Tkinter interface.

## Prerequisites

*   Python 3.8 or higher
*   An environment capable of running Tkinter (usually included with standard Python installations).

## Installation

1.  **Clone the Repository**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Install Dependencies**
    It is recommended to use a virtual environment.
    ```bash
    pip install -r requirements.txt
    ```

    *Note: If `requirements.txt` is not available, you can manually install the key packages:*
    ```bash
    pip install ultralytics opencv-python Pillow
    ```

3.  **Verify Model File**
    Ensure the `weights.pt` file is present in the root directory of the project. This file contains the trained model parameters necessary for coin detection.

## Usage

1.  **Run the Application**
    Execute the main script from your terminal:
    ```bash
    python app.py
    ```

2.  **Operate the GUI**
    *   Click the **"📂 Upload Image"** button at the top of the window.
    *   Select an image file containing coins from your file system.
    *   The application will process the image and display the results.
        *   The main view shows the image with detected coins highlighted.
        *   The right sidebar shows a summary of counts and the total value in Forints (Ft).

## Supported Currency

The application is currently trained to recognize the following Hungarian Forint denominations:

*   **5 Ft** (Gold/Orange)
*   **10 Ft** (Light Silver/Blue)
*   **50 Ft** (Lime Green)
*   **100 Ft** (Purple/Pinkish)
*   **200 Ft** (Bright Red)

## Project Structure

*   `app.py`: The main entry point of the application. Contains the GUI logic and integration with the YOLO model.
*   `weights.pt`: The pre-trained YOLOv8 model weights file.
*   `requirements.txt`: List of Python dependencies required to run the project.
*   `test_imges/`: Directory containing sample images for testing purposes.

## License

This project is open-source and available for use.
