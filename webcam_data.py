import cv2
import time
from is_military import predict
from is_military_resnet import *
from send_data import post_request, get_location


def cv_to_pil_img(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return Image.fromarray(img)


cv2.namedWindow("webcam")
vc = cv2.VideoCapture(0)

net = cv2.dnn.readNetFromCaffe('models/bvlc_googlenet.prototxt', 'models/bvlc_googlenet.caffemodel')
rows = open('synset_words.txt').read().strip().split("\n")
classes = [r[r.find(" ") + 1:].split(",")[0] for r in rows]

time.sleep(2)

if vc.isOpened():
    rval, frame = vc.read()
else:
    rval = False


#resnet
model = modified_resnet50()
model.load_state_dict(torch.load('model_best.pth.tar', map_location='cpu')['state_dict'])

begin = time.time()
http = urllib3.PoolManager()
while rval:
    print("step:", (time.time() - begin))
    cv2.imshow("webcam", frame)
    rval, frame = vc.read()
    wasFound = predict(frame, net, classes)
    if wasFound:
        ping_server(http)
    key = cv2.waitKey(20)
    if key == 27:
        break
cv2.destroyWindow("webcam")