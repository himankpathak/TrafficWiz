import cv2
import argparse
import numpy as np

videopath = "videos/traffic3.mp4"

fweightpath = "models/yolov3.weights"
fclasspath = "models/yolov3.txt"
fconfigpath = "models/yolov3.cfg"

vcount=0
classes = None
COLORS = None

def getCustomColor(classid):
	if classid == 0:        #person
		return (0,255,0)
	elif classid == 1:      #bicycle
		return (0,255,0)
	elif classid == 2:      #car
		return (255,0,0)
	elif classid == 3:      #bike
		return (0,0,255)
	elif classid == 4:      #bus
		return (255,0,0)
	elif classid == 6:      #truck
		return (255,0,0)
	else:                   #others
		return (255,255,255)

def get_output_layers(net):

	layer_names = net.getLayerNames()
	output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

	return output_layers


def draw_prediction(img, class_id, confidence, x, y, x_plus_w, y_plus_h,isfull=True):

	global vcount
	label = str(classes[class_id])

	#color = COLORS[class_id]
	if isfull:
		color = getCustomColor(class_id)
		vcount+=1
	else:
		color = (150,200,40)

	cv2.rectangle(img, (x,y), (x_plus_w,y_plus_h), color, 2)
	cv2.putText(img, label, (x-10,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

def draw_indices(img,data):
	indices = data[1]
	boxes = data[0]
	class_ids = data[2]
	confidences = data[3]
	for i in indices:
		if class_ids[i[0]] in [0,1,2,3,4,6]:
			i = i[0]
			box = boxes[i]
			x = box[0]
			y = box[1]
			w = box[2]
			h = box[3]
			draw_prediction(img, class_ids[i], confidences[i], round(x), round(y), round(x+w), round(y+h))
	return img;

def yolo(image,wpath,clpath,conpath,conf_threshold = 0.5):
	Width = image.shape[1]
	Height = image.shape[0]
	scale = 0.00392

	global classes,COLORS

	classes = None
	with open(clpath, 'r') as f:
		classes = [line.strip() for line in f.readlines()]

	COLORS = np.random.uniform(0, 255, size=(len(classes), 3))
	net = cv2.dnn.readNet(wpath, conpath)

	blob = cv2.dnn.blobFromImage(image, scale, (416,416), (0,0,0), True, crop=False)

	net.setInput(blob)

	outs = net.forward(get_output_layers(net))

	class_ids = []
	confidences = []
	boxes = []
	nms_threshold = 0.4

	for out in outs:
		for detection in out:
			scores = detection[5:]
			class_id = np.argmax(scores)
			confidence = scores[class_id]
			if confidence > conf_threshold:
				center_x = int(detection[0] * Width)
				center_y = int(detection[1] * Height)
				w = int(detection[2] * Width)
				h = int(detection[3] * Height)
				x = center_x - w / 2
				y = center_y - h / 2
				class_ids.append(class_id)
				confidences.append(float(confidence))
				boxes.append([x, y, w, h])

	indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)
	return [boxes,indices,class_ids,confidences]


def process(frame):
	global vcount
	vcount=0
	img = frame;
	full = yolo(frame,fweightpath,fclasspath,fconfigpath)
	img = draw_indices(frame,full)
	return img;


def main():
	global vcount
	cap = cv2.VideoCapture(videopath)

	while(True):
		ret, frame = cap.read()
		abcd = process(frame)

		cv2.putText(abcd,str(vcount),(1650,1020), cv2.FONT_HERSHEY_SIMPLEX, 4,(255,255,255),4,cv2.LINE_AA)
		abcd = cv2.pyrDown(abcd)
		cv2.imshow('frame',abcd)

		if cv2.waitKey(1) & 0xFF == ord('q'):
			break


if __name__ == '__main__':
	main()
