import cv2
import argparse
import numpy as np

videopath = "videos/traffic3.mp4"

fweightpath = "models/yolov3.weights"
fclasspath = "models/yolov3.txt"
fconfigpath = "models/yolov3.cfg"

hweightpath = "models/helmet/yolov3-obj_2400.weights"
hclasspath = "models/helmet/obj.names"
hconfigpath = "models/helmet/yolov3-obj.cfg"

vcount=0
classes = None
COLORS = None
def readfromframe(vid,frame):
	_,t = vid.read();
	vid.set(cv2.CAP_PROP_POS_FRAMES, frame)

def getCustomColor(classid):
	global vcount
	
	if classid == 0:        #person
		return (0,255,0)
	elif classid == 1:      #bicycle
		return (0,255,0)
	elif classid == 2:      #car
		vcount+=1
		return (255,0,0)
	elif classid == 3:      #bike
		vcount+=1
		return (0,0,255)
	elif classid == 4:      #bus
		vcount+=1
		return (255,0,0)
	elif classid == 6:      #truck
		vcount+=1
		return (255,0,0)
	else:                   #others
		return (255,255,255)

def get_output_layers(net):

	layer_names = net.getLayerNames()
	output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

	return output_layers


def draw_prediction(img, class_id, confidence, x, y, x_plus_w, y_plus_h,classes,isfull=True):

	label = str(classes[class_id])

	#color = COLORS[class_id]
	if isfull:
		color = getCustomColor(class_id)
	else:
		color = (150,200,40)

	cv2.rectangle(img, (x,y), (x_plus_w,y_plus_h), color, 2)
	cv2.putText(img, label, (x-10,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

def draw_indices(img,data,classes):
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
			draw_prediction(img, class_ids[i], confidences[i], round(x), round(y), round(x+w), round(y+h),classes)
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

def crop_persons(frame,data):
	indices = data[1]
	boxes = data[0]
	class_ids = data[2]
	confidences = data[3]
	persons=[];
	locs=[]
	for i in indices:
		i = i[0]
		box = boxes[i]
		x = int(box[0])
		y = int(box[1])
		w = int(box[2])
		h = int(box[3])

		if class_ids[i] == 0:
			persons.append(frame[y:y+h, x:x+w])
			locs.append([x,y,w,h])
	return persons,locs;
		#draw_prediction(img, class_ids[i], confidences[i], round(x), round(y), round(x+w), round(y+h))
	#return img;


def getbikes(frame,data):
	indices = data[1]
	boxes = data[0]
	class_ids = data[2]
	confidences = data[3]
	bikes=[];
	locs=[]
	for i in indices:
		i = i[0]
		box = boxes[i]
		x = int(box[0])
		y = int(box[1])
		w = int(box[2])
		h = int(box[3])

		if class_ids[i] == 3:
			bikes.append(frame[y:y+h, x:x+w])
			locs.append([x,y,w,h])
	return bikes,locs;

def ishelmetpresent(person_img):
	helmet = yolo(person_img,hweightpath,hclasspath,hconfigpath,conf_threshold=0.5)
	if(len(helmet[0])!=0):
		return helmet;
	else:
		return False;

def getRatiowh(box):
	return box[2]/box[3];

def center(box):
	x,y,w,h = box
	return [(x+w)/2,(y+h)/2]

def dist(p1,p2):
	return ((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)**0.5;

def islistNear(box,blist,threshx,threshy):
	c = center(box)
	minv = 100000000;
	minvy = -1;
	for b in blist:
		cl = center(b)
		dx = abs(cl[0]-c[0])
		dy = cl[1]-c[1]
		if dx<minv:
			minv=dx;
			minvy = dy;
	#print("mins:",minv,minvy)
	if minv<threshx*box[2] and minvy>0 and minvy<=box[3]*threshy:
		#print("threshes:",threshx*box[2],box[3]*threshy)
		return True;
	else:
		return False;

def isonBike(man,bikes):
	g = getRatiowh(man)
	possible = False;
	if g<1.3 and g>0.6:
		possible = True
	if possible == True:
		if islistNear(man,bikes,0.3,1.5):
			return True;
		else: return False;
	else: return False;

def process(frame):
	global vcount
	global classes
	vcount=0
	img = frame;
	full = yolo(frame,fweightpath,fclasspath,fconfigpath)

	persons,locs = crop_persons(frame,full)
	bikes,blocs = getbikes(frame,full)
	non_hel =[[],[],[],[]];
	for p,l in zip(persons,locs):
		x,y,w,h = l
		if(isonBike(l,blocs)):
			hel = ishelmetpresent(p)
			if(hel==False):
				cv2.rectangle(frame, (x,y), (x+w,y+h), (0,0,255), 2)
			else:
				cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 2)
		else:
			cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)

	with open(fclasspath, 'r') as f:
		classes = [line.strip() for line in f.readlines()]
	img = draw_indices(frame,full,classes)
	cv2.putText(frame,str(vcount),(1700,1050), cv2.FONT_HERSHEY_SIMPLEX, 4,(255,255,255),4,cv2.LINE_AA)
	return img

def getVcount():
	global vcount
	return vcount

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
