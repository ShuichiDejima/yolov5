# https://qiita.com/ryoon025/items/8441b0747782c2486ad1
import shutil
import os
import pathlib

import detect2
import argparse

from flask import Flask, request, render_template, flash, redirect
from werkzeug.utils import secure_filename

import csv


UPLOAD_FOLDER = "img"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
data = []



def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('ファイルがありません')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('ファイルがありません')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            filepath = os.path.join(UPLOAD_FOLDER, filename)

            filen = str(filepath).split("/")
            print(filen[1])
            parser = argparse.ArgumentParser()
            parser.add_argument('--weights', nargs='+', type=str, default='yolov5s.pt', help='model.pt path(s)')
            parser.add_argument('--source', type=str, default='data/images', help='source')  # file/folder, 0 for webcam
            parser.add_argument('--img-size', type=int, default=640, help='inference size (pixels)')
            parser.add_argument('--conf-thres', type=float, default=0.25, help='object confidence threshold')
            parser.add_argument('--iou-thres', type=float, default=0.45, help='IOU threshold for NMS')
            parser.add_argument('--max-det', type=int, default=1000, help='maximum number of detections per image')
            parser.add_argument('--device', default='', help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
            parser.add_argument('--view-img', action='store_true', help='display results')
            parser.add_argument('--save-txt', action='store_true', help='save results to *.txt')
            parser.add_argument('--save-conf', action='store_true', help='save confidences in --save-txt labels')
            parser.add_argument('--save-crop', action='store_true', help='save cropped prediction boxes')
            parser.add_argument('--nosave', action='store_true', help='do not save images/videos')
            parser.add_argument('--classes', nargs='+', type=int, help='filter by class: --class 0, or --class 0 2 3')
            parser.add_argument('--agnostic-nms', action='store_true', help='class-agnostic NMS')
            parser.add_argument('--augment', action='store_true', help='augmented inference')
            parser.add_argument('--update', action='store_true', help='update all models')
            parser.add_argument('--project', default='runs/detect', help='save results to project/name')
            parser.add_argument('--name', default='exp', help='save results to project/name')
            parser.add_argument('--exist-ok', action='store_true', help='existing project/name ok, do not increment')
            parser.add_argument('--line-thickness', default=3, type=int, help='bounding box thickness (pixels)')
            parser.add_argument('--hide-labels', default=False, action='store_true', help='hide labels')
            parser.add_argument('--hide-conf', default=False, action='store_true', help='hide confidences')
            parser.add_argument('--half', type=bool, default=False, help='use FP16 half-precision inference')
            parser.add_argument('--out_label', type=str, default='data', help='label output dir') 
            parser.add_argument('--ant_dat', type=str, default='', help='annotation data') 
            opt = parser.parse_args()
            opt.source = filepath
            print(opt)

            file_detect = detect2.detect(opt)

            print("file_detect" + str(file_detect))
            print(type(filen))
            file_path = file_detect.joinpath(filen[1])
            print(file_path)
            print(type(file_path))
            new_path = shutil.move(file_path, './static/images/'+filen[1])

            new_org_path = shutil.move(filepath, './static/images/org_'+filen[1])


            return render_template("index.html", filen = new_path, org_filen = new_org_path)
#            return render_template("index.html", filen=file_path)
#            return render_template("index.html",answer="")
    
#    return "Tree"
#    return render_template("index.html", answer="test")
    return render_template("index.html", filen="", org_filen = "")



@app.route("/detect")
def detect_ml():
#    return "Test"
#    return render_template("extend.html", title="Flask")
    return render_template("index.html", filen="", org_filen = "")

#    return render_template("index.html",input_from_python= data, filen = filen) # templatesフォルダ内のindex.htmlを表示する


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port="5010")