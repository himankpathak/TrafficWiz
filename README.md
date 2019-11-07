# TrafficWiz

TrafficWiz is an unlawful traffic activity detection and monitoring system. Video footage from street cameras is directly processed by TrafficWiz using OpenCV with YOLO. Culprits detected in the footage are then issued challan/fine automatically by reading the number plates of the vehicle using pytesseract.

## Requirements

- Python 3.6
- Flask = 1.1.1
- OpenCV = 4.1.1
- numpy = 1.17.2
- pytesseract = 0.3

Use Anaconda as a package manager to easily set up the environment before running the application.

## Setup

Download the model [weights](https://drive.google.com/file/d/1OElmPFZOKx90K2qmcoCHGviG_lq316el/view) and place the models folder in the root directory.
Download the [static](https://drive.google.com/file/d/1xemdHTKmo86I2fePn9piGmJuVz3U0me0/view) files and place the static folder in the root directory.

## Running the app

- Make sure you have models and static folder in the root directory
- Start the flask server with `$ python app.py` in the root folder of the project
- Navigate to `localhost:5000`

