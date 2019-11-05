# TrafficWiz

TrafficWiz is an unlawful traffic activity detection and monitoring system. Video footage from street cameras is directly processed by TrafficWiz using OpenCV with YOLO. Culprits detected in the footage are then issued challan/fine automatically by reading the number plates of the vehicle using pytesseract.

## Requirements

- Python 3.6
- Flask = 1.1.1
- OpenCV = 4.1.1
- numpy = 1.17.2
- pytesseract = 0.3

Use Anaconda as a package manager to easily set up the environment before running the application.

