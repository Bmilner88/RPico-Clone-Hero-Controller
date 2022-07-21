# Raspberry Pi Pico Keyboard Controller for Clone Hero
# Using CircuitPython 6.2.0-rc.0
# Using Adafruit USB_HID Library

import time
import board
import machine
import digitalio
import usb_hid
from adafruit_hid.gamepad import Gamepad
from analogio import AnalogIn

gamepad = Gamepad(usb_hid.devices)

board_led = digitalio.DigitalInOut(board.LED)
led1 = digitalio.DigitalInOut(board.GP18)
led2 = digitalio.DigitalInOut(board.GP19)
led3 = digitalio.DigitalInOut(board.GP20)
led4 = digitalio.DigitalInOut(board.GP21)

if(board_led.value == True):
    led1.toggle()
    led2.toggle()
    led3.toggle()
    led4.toggle()

gamepad.find_device()

# frets
sdaPIN = machine.pin(28) # data OR D
sclPIN = machine.pin(27) # clk OR C
# V goes to GP36
# G goes to GP33

i2c = machine.I2C(0, sda=sdaPIN, scl=sclPIN, freq=400000)

print('Scanning i2c bus')
devices = i2c.scan()

if len(devices) == 0:
    print("No i2c device !")
else:
    print('i2c devices found:', len(devices))

for device in devices:
    print('Decimal address: ', device, ' | Hexa address: ', hex(device))

# strum bar
btn_up = digitalio.DigitalInOut(board.GP7)
btn_up.direction = digitalio.Direction.INPUT
btn_up.pull = digitalio.Pull.DOWN

btn_down = digitalio.DigitalInOut(board.GP8)
btn_down.direction = digitalio.Direction.INPUT
btn_down.pull = digitalio.Pull.DOWN

# misc. buttons
btn_start = digitalio.DigitalInOut(board.GP10)
btn_start.direction = digitalio.Direction.INPUT
btn_start.pull = digitalio.Pull.DOWN

btn_select = digitalio.DigitalInOut(board.GP11)
btn_select.direction = digitalio.Direction.INPUT
btn_select.pull = digitalio.Pull.DOWN

# whammy
ana_whammy = AnalogIn(board.GP26)
# RED WIRE IS NOT GROUND

# set the buttons
buttons = {
    1 : btn_green,
    2 : btn_red,
    3 : btn_yellow,
    4 : btn_blue,
    5 : btn_orange,
    6 : btn_start,
    7 : btn_select,
    8 : btn_up,
    9 : btn_down
}

# sets the range from -127 to 127
def setToJoyStickRange(stickVal):
    return int(stickVal * 127 * 2 -127)

# sets a dead zone for the whammy bar
# if the whammy value is below the specified whammy value, then return the specified whammy value
def whammyDeadZone(whammyVal):
    whammyDeadZoneVal = -90
    whammyVal = setToJoyStickRange(whammyVal)
    if(whammyVal < whammyDeadZoneVal):
        return whammyDeadZoneVal
    else:
        return whammyVal

# rounds down the joystick value to the value specified
def roundStickVal(stickVal):
    roundDownVal = 20
    return int(stickVal / roundDownVal) * roundDownVal
while True:
    for gamenum, button in buttons.items():
        if button.value:
            gamepad.press_buttons(gamenum)
        else:
            gamepad.release_buttons(gamenum)

    # the limit on each analog stick is by the first value
    # make limit -127 to 127
    # adjust your joystick until limits are -127 to 127