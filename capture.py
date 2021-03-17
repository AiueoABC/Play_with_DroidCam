import cv2
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
        cmdSender(getBattery)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

        elif key == ord('f'):
            cmdSender(autoFocus)

        elif key == ord('l'):
            cmdSender(toggleLED)

        elif key == ord('+'):
            cmdSender(zoomIn)

        elif key == ord('-'):
            cmdSender(zoomOut)

        elif key == ord('r'):
            cmdSender(fpsRestriction)

    cap.release()
    cv2.destroyAllWindows()
