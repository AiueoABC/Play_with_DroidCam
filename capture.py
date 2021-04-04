import copy
import cv2
from PIL import Image, ImageTk
import PySimpleGUI as sg
import urllib.request as urlreq
import time

PROTOCOL = 'http'  # Keep this
IP = '192.168.0.53'  # Use one in DroidCAM
PORT = '4747'  # Use one in DroidCAM

'''
Read IP/PORT settings
'''
ask_settings = True
try:
    with open('./capture_settings.dat') as f:
        l_strip = [s.strip() for s in f.readlines()]
        for data in l_strip:
            if 'ip' in data:
                IP = data.split('=')[1]
            elif 'port' in data:
                PORT = data.split('=')[1]
            elif 'ask_settings' in data and 'False' in data:
                ask_settings = False
except Exception as e:
    print(e)

'''
GUI IP/PORT Setting
'''
if ask_settings:
    layout = [
        [sg.Text('IP/PORT Setting')],
        [sg.Text('IP', size=(15, 1)), sg.InputText(IP)],
        [sg.Text('PORT', size=(15, 1)), sg.InputText(PORT)],
        [sg.Submit(button_text='Check'), sg.Submit(button_text='Next')]
    ]
    settingwindow = sg.Window('IP/PORT Setting', layout, location=(800, 400), finalize=True)
    while True:
        event, values = settingwindow.read()
        if event in (None, 'Next'):
            IP = values[0]
            PORT = values[1]
            break
        if event == 'Check':
            IP = values[0]
            PORT = values[1]
            show_message = 'Your settings are;\n'
            show_message += "IP: " + IP + '\n'
            show_message += "PORT: " + PORT
            sg.popup(show_message)
    settingwindow.close()

DIRNAME = 'video'
SIZE320x240 = '?320X240'
SIZE640x480 = '?640X480'  # Default
# SIZE1280x720 = '?1280X720'  # You need PRO license on DroidCAM
# SIZE1920x1080 = '?1920X1080'  # You Need PRO license on DroidCAM

cameraURI = PROTOCOL + '://' + IP + ':' + PORT + '/'

'''
Cam Settings Commands
'''
# Exposure
exposurelockOn = cameraURI + 'cam/1/set_exposure_lock'
exposurelockOff = cameraURI + 'cam/1/unset_exposure_lock'

# White Balance
setwbAuto = cameraURI + 'cam/1/set_wb/auto'  # Default
setwbIncandescent = cameraURI + 'cam/1/set_wb/incandescent'  # Incandescent mode
setwbWarmfluorescent = cameraURI + 'cam/1/set_wb/warm-fluorescent'  # Warmfluorescent mode
setwbTwilight = cameraURI + 'cam/1/set_wb/twilight'  # Twilight mode
setwbFluorescent = cameraURI + 'cam/1/set_wb/fluorescent'  # Florescent mode
setwbDaylight = cameraURI + 'cam/1/set_wb/daylight'  # Daylight mode
setwbCloudydaylight = cameraURI + 'cam/1/set_wb/cloudy-daylight'  # Cloudy mode
setwbShade = cameraURI + 'cam/1/set_wb/shade'  # Shade mode

'''
Useful Functions Commands
'''
autoFocus = cameraURI + 'cam/1/af'   # Execute Auto-Focus
zoomIn = cameraURI + 'cam/1/zoomin'   # Execute Zoom-in
zoomOut = cameraURI + 'cam/1/zoomout'   # Execute Zoom-out
toggleLED = cameraURI + 'cam/1/led_toggle'  # Change LED light ON/OFF
fpsRestriction = cameraURI + 'cam/1/fpslimit'  # Execute FPS restriction
getBattery = cameraURI + 'battery'  # Ask BAT level


def cmdSender(cmd):
    ret = ''
    try:
        fp = urlreq.urlopen(cmd)
        ret = fp.read().decode("utf8")
        fp.close()
    except Exception as e:
        print(e)
    return ret


"""
GUI Definition
"""
sg.theme('Black')

# define the window layout
layout = [
        [sg.Text('DroidCam Movie', size=(40, 1), justification='center', font='Helvetica 20', key='-status-')],
        [sg.Button('LED ON/OFF', size=(12, 2), font='Helvetica 14'),
         sg.Button('AutoFocus', size=(12, 2), font='Helvetica 14'),
         sg.Button('Zoom +', size=(12, 2), font='Helvetica 14'),
         sg.Button('Zoom -', size=(12, 2), font='Helvetica 14'),
         sg.Button('FPS Restriction', size=(12, 2), font='Helvetica 14'), ],
        [sg.Button('Exp.Lock ON', size=(12, 2), font='Helvetica 14'),
         sg.Button('Exp.Lock OFF', size=(12, 2), font='Helvetica 14'),
         sg.Button('WB Settings...', size=(12, 2), font='Helvetica 14'),
         sg.Button('640X480', size=(12, 2), font='Helvetica 14'),
         sg.Button('320X240', size=(12, 2), font='Helvetica 14'),],
        [sg.Image(filename='', key='image')],
        [sg.Button('Exit', size=(10, 1), font='Helvetica 14')]
        ]
wbsetter_layout = [
                    [sg.Button('Auto WB', size=(15, 2), font='Helvetica 14'),
                     sg.Button('Incandescent', size=(15, 2), font='Helvetica 14'),
                     sg.Button('Warm Fluorescent', size=(15, 2), font='Helvetica 14'),
                     sg.Button('Twilight', size=(15, 2), font='Helvetica 14'), ],
                    [sg.Button('Florescent', size=(15, 2), font='Helvetica 14'),
                     sg.Button('Daylight', size=(15, 2), font='Helvetica 14'),
                     sg.Button('Cloudy', size=(15, 2), font='Helvetica 14'),
                     sg.Button('Shade', size=(15, 2), font='Helvetica 14'), ],
                    [sg.Button('Done', size=(10, 1), font='Helvetica 14')]
                    ]


def wbSetting():
    newlayout = copy.deepcopy(wbsetter_layout)  # bc you can't reuse layout defined before
    wbwindow = sg.Window('White Balance Settings', newlayout, location=(800, 400), finalize=True)
    while True:
        event, values = wbwindow.read(timeout=5)
        if event in (None, 'Done'):
            break
        elif event == 'Auto WB':
            cmdSender(setwbAuto)
        elif event == 'Incandescent':
            cmdSender(setwbIncandescent)
        elif event == 'Warm Fluorescent':
            cmdSender(setwbWarmfluorescent)
        elif event == 'Twilight':
            cmdSender(setwbTwilight)
        elif event == 'Florescent':
            cmdSender(setwbFluorescent)
        elif event == 'Daylight':
            cmdSender(setwbDaylight)
        elif event == 'Cloudy':
            cmdSender(setwbCloudydaylight)
        elif event == 'Shade':
            cmdSender(setwbShade)
    wbwindow.close()
    del newlayout


# create the window and show it without the plot
window = sg.Window('Realtime movie', layout, location=(800, 400), finalize=True, element_justification='center')

if __name__ == '__main__':
    cap = cv2.VideoCapture(cameraURI + DIRNAME + SIZE640x480)
    # cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('B', 'G', 'R', '3'))
    # cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('H', '2', '6', '4'))  # Not sure this works
    # cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('Y', 'U', 'Y', 'V'))
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    while cap.isOpened():
        ret, frame = cap.read()
        if ret is True:
            window['image'].update(data=cv2.imencode('.png', frame)[1].tobytes())
            # cv2.imshow('DroidCamImage', frame)
            window.set_title('Realtime movie --- Battery:' + cmdSender(getBattery) + ' %')
        event, values = window.read(timeout=1)
        if event in (None, 'Exit'):
            break

        elif event == 'AutoFocus':
            cmdSender(autoFocus)

        elif event == 'LED ON/OFF':
            cmdSender(toggleLED)

        elif event == 'Zoom +':
            cmdSender(zoomIn)

        elif event == 'Zoom -':
            cmdSender(zoomOut)

        elif event == 'FPS Restriction':
            cmdSender(fpsRestriction)

        elif event == 'Exp.Lock ON':
            cmdSender(exposurelockOn)

        elif event == 'Exp.Lock OFF':
            cmdSender(exposurelockOff)

        elif event == 'WB Settings...':
            wbSetting()

        elif event == '640X480':
            cap.release()
            time.sleep(1)
            cap = cv2.VideoCapture(cameraURI + DIRNAME + SIZE640x480)
            cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('H', '2', '6', '4'))

        elif event == '320X240':
            cap.release()
            time.sleep(1)
            cap = cv2.VideoCapture(cameraURI + DIRNAME + SIZE320x240)
            cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('H', '2', '6', '4'))

        """
        To Clear Buffers... I know this is stupid.
        """
        cap.read(), cap.read(), cap.read()

    window.close()

    cap.release()
    cv2.destroyAllWindows()
