import cv2
import urllib.request as urlreq
import sys

PROTOCOL = 'http'  # Keep this
IP = '192.168.0.53'  # Use one in DroidCAM
PORT = '4747'  # Use one in DroidCAM

if len[sys.argv] > 3:
    IP = sys.argv[1]
    PORT = sys.argv[2]

DIRNAME = 'video'
# SIZE320x240 = '?320X240'
# SIZE640x480 = '?640X480'  # Default
# SIZE1280x720 = '?1280X720'  # You need PRO license on DroidCAM
# SIZE1920x1080 = '?1920X1080'  # You Need PRO license on DroidCAM

cameraURI = PROTOCOL + '://' + IP + ':' + PORT + '/'

'''
Cam Settings
'''
exposurelockOn = cameraURI + 'cam/1/set_exposure_lock'
exposurelockOff = cameraURI + 'cam/1/unset_exposure_lock'

setwbAuto = cameraURI + '/cam/1/set_wb/auto'  # Default
setwbIncandescent = cameraURI + '/cam/1/set_wb/incandescent'
setwbWarmfluorescent = cameraURI + '/cam/1/set_wb/warm-fluorescent'
setwbTwilight = cameraURI + '/cam/1/set_wb/twilight'
setwbFluorescent = cameraURI + '/cam/1/set_wb/fluorescent'
setwbDaylight = cameraURI + '/cam/1/set_wb/daylight'
setwbCloudydaylight = cameraURI + '/cam/1/set_wb/cloudy-daylight'
setwbShade = cameraURI + '/cam/1/set_wb/shade'

'''
Useful Functions
'''
autoFocus = cameraURI + 'cam/1/af'   # ブラウザでURLをたたくとAF
zoomIn = cameraURI + 'cam/1/zoomin'   # ブラウザでURLをたたくとZoomIn
zoomOut = cameraURI + 'cam/1/zoomout'   # ブラウザでURLをたたくとZoomOut
toggleLED = cameraURI + 'cam/1/led_toggle'  # ブラウザでURLをたたくとLED ON/OFF
fpsRestriction = cameraURI + 'cam/1/fpslimit'  # ブラウザでURLをたたくとFPSを著しく下げる
getBattery = cameraURI + 'battery'  # ブラウザでURLをたたくとバッテリレベルでる


def readHTML(uri):
    fp = urlreq.urlopen(uri)
    print('\r' + fp.read().decode("utf8"), end="")
    fp.close()


if __name__ == '__main__':
    cap = cv2.VideoCapture(cameraURI + DIRNAME)
    # Exposure Lock
    # readHTML(exposurelockOn)
    # Set White-balance
    # readHTML(setwbAuto)

    while True:
        ret, frame = cap.read()
        cv2.imshow('frame', frame)
        readHTML(getBattery)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

        elif key == ord('f'):
            readHTML(autoFocus)

        elif key == ord('l'):
            readHTML(toggleLED)

        elif key == ord('+'):
            readHTML(zoomIn)

        elif key == ord('-'):
            readHTML(zoomOut)

        elif key == ord('r'):
            readHTML(fpsRestriction)

    cap.release()
    cv2.destroyAllWindows()
