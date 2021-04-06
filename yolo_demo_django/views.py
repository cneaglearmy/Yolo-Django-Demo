from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage

import sys
sys.path.insert(0, 'darknet/python')
import darknet
import cv2

net = darknet.load_net(b"darknet/cfg/yolov3-tiny.cfg", b"darknet/yolov3/yolov3-tiny.weights", 0)
meta = darknet.load_meta(b"darknet/cfg/coco.data")
fs = FileSystemStorage()

def index(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)

        r = darknet.detect(net, meta, uploaded_file_url[1:].encode('utf-8'))

        im = cv2.imread(uploaded_file_url[1:])
        print(uploaded_file_url)
        try:
            for res in r:
                cv2.rectangle(im, (int(res[2][0] - res[2][2]/2), int(res[2][1] - res[2][3]/2)), (int(res[2][0] + res[2][2]/2), int(res[2][1] + res[2][3]/2)), (0, 255, 0), 1)
                cv2.putText(im, res[0].decode('utf-8'), (int(res[2][0] - res[2][2]/2), int(res[2][1] - res[2][3]/2)), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 0, 0), 1, cv2.LINE_AA)
        except Exception as e:
            print(e)
        yoloImg = (uploaded_file_url[1:]).split('.');
        yoloImg = yoloImg[0] + "_yolo." + yoloImg[1]
        cv2.imwrite(yoloImg,im)
        yoloImg = '/' + yoloImg;

        return render(request, 'simple_upload.html', {
            'uploaded_file_url': uploaded_file_url,
            'yoloImg': yoloImg
        })

    return render(request, 'simple_upload.html')
