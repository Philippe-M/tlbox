#!/usr/bin/env python
# -*-coding:UTF-8 -*

from flask import Flask, render_template, request, send_file
import os

app = Flask(__name__)
app.config["CACHE_TYPE"] = "null"
app.secret_key = os.urandom(24)

fileseq = filefolder = awb = metering = ev = exposure = sharpness = brightness = contrast = saturation = iso = imxfix = quality = raw = width = height = hflip = vflip = timelapse_active = False
tlFolderRoot = "/media/usb/"

@app.route('/')
def acceuil():
    return render_template('index.html')

@app.route('/takepicture', methods=['POST'])
def takepicture():
    if request.method == 'POST':    
        fileseq = request.form['fileseq']
        filefolder = request.form['filefolder']
        awb = request.form['awb']
        metering = request.form['metering']
        ev = request.form['ev']
        exposure = request.form['exposure']
        sharpness = request.form['sharpness']
        brightness = request.form['brightness']
        contrast = request.form['contrast']
        saturation = request.form['saturation']
        iso = request.form['iso']
        imxfx = request.form['imxfx']
        quality = request.form['quality']
        raw = request.form.getlist('raw')
        width = request.form['width']
        height = request.form['height']
        hflip = request.form.getlist('hflip')
        vflip = request.form.getlist('vflip')
        timelapse_active = request.form.getlist('timelapse_active')
        timelapse = request.form['timelapse']
        timeout = request.form['timeout']
                       
        command = "raspistill -v"
        command += " --awb '" + str(awb) + "'" # Define WB
        command += " --metering '" + str(metering) + "'" # Define Metering Mode
        command += " --ev " + str(ev) # Define the Exposure Adjustment
        command += " --exposure '" + str(exposure) + "'" # Define Exposure Mode
        command += " --sharpness " + str(sharpness) # Define Image Sharpness
        command += " --brightness " + str(brightness) # Define Image Brightness
        command += " --contrast " + str(contrast) # Define Image Contrast
        command += " --saturation " + str(saturation) # Define Image Saturation
        command += " --ISO " + str(iso) # Define Image ISO            
        command += " --imxfx '" + str(imxfx) + "'" # Define Image Effect
        command += " --quality " + str(quality) # Define Image Quality
        command += " --width " + str(width) # Define output image width
        command += " --height " + str(height) # Define output image height
        
        if hflip:
            command += " --hflip"
        if vflip:
            command += " --vflip"
            
        if raw:
            command += " --raw"

        # TimeLapse parameter
        if timelapse_active:
            folder = tlFolderRoot + "images/timelapse/" + str(filefolder)
            if not os.path.exists(folder):
                os.makedirs(folder)
            command += " --timelapse " + timelapse
            command += " --timeout " + timeout
            command += " --output " + folder + "/\05%d.jpg"

            os.system(command)
            return render_template('takepicture.html', timelapse_active=True, timelapse=timelapse, timeout=timeout)
        else:
            folder = "images/" + str(filefolder)
            if not os.path.exists(folder):
                os.makedirs(folder)

            command += " --output '" + folder + "/" + str(fileseq) + ".jpg'"
            os.system(command)
            return render_template('takepicture.html', fileFolder=str(filefolder), filePicture=str(fileseq) + ".jpg")
    else:
        return render_template('index.html')

@app.route('/images/<fileFolder>/<filePicture>')
def images(fileFolder, filePicture):
    return send_file("images/" + fileFolder + "/" + filePicture, "image/jpeg")

if __name__== '__main__' :
    app.run(host="0.0.0.0", debug=True)