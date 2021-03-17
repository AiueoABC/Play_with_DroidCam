import cv2
import PySimpleGUI as sg
import urllib.request as urlreq
import sys

PROTOCOL = 'http'  # Keep this
IP = '192.168.0.53'  # Use one in DroidCAM
PORT = '4747'  # Use one in DroidCAM

if len(sys.argv) == 3:
    IP = sys.argv[1]
    PORT = sys.argv[2]

DIRNAME = 'video'
# SIZE320x240 = '?320X240'
# SIZE640x480 = '?640X480'  # Default
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
    fp = urlreq.urlopen(cmd)
    # print('\r' + fp.read().decode("utf8"), end="")
    ret = fp.read().decode("utf8")
    fp.close()
    return ret


"""
GUI Definition
"""
sg.theme('Black')

# define the window layout
layout = [
        [sg.Text('Realtime movie', size=(40, 1), justification='center', font='Helvetica 20', key='-status-')],
        [sg.Button('LED ON/OFF', size=(10, 1), font='Helvetica 14'),
         sg.Button('AutoFocus', size=(10, 1), font='Helvetica 14'),
         sg.Button('Zoom +', size=(10, 1), font='Helvetica 14'),
         sg.Button('Zoom -', size=(10, 1), font='Helvetica 14'),
         sg.Button('FPS Restriction', size=(10, 1), font='Helvetica 14'), ],
        [sg.Image(filename='', key='image')],
        [sg.Button('Exit', size=(10, 1), font='Helvetica 14')]
        ]

# create the window and show it without the plot
window = sg.Window('Realtime movie', layout, location=(800, 400), finalize=True)

if __name__ == '__main__':
    cap = cv2.VideoCapture(cameraURI + DIRNAME)

    while True:
        ret, frame = cap.read()
        window.set_title('Realtime movie --- Battery:' + cmdSender(getBattery) + ' %')
        if ret is True:
            imgbytes = cv2.imencode('.png', frame)[1].tobytes()
            window['image'].update(data=imgbytes)
        event, values = window.read(timeout=2)
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

    window.close()

    cap.release()
    cv2.destroyAllWindows()
