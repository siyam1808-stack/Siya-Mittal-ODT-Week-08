from machine import Pin,TouchPad, PWM
import neopixel
import time
import random


np = neopixel.NeoPixel(Pin(21), 16)


pb = Pin(25, Pin.IN, Pin.PULL_UP) 
touch1 = TouchPad(Pin(27, Pin.IN))
touch2 = TouchPad(Pin(13, Pin.IN))
ir = Pin(35, Pin.IN)   


buzzer = PWM(Pin(4))


servo = PWM(Pin(23))
servo.freq(50)


score = 0
reaction_time = 2000  #2sec?
colours = ["red", "blue", "yellow", "green"]


def onnp_led(color):
    for i in range(16):
        np[i] = color
    np.write()

def offnp_led():
    for i in range(16):
        np[i] = (0, 0, 0)
    np.write()

def buzzer_beep(freq):
    buzzer.freq(freq)
    buzzer.duty(512)
    time.sleep(0.2)
    buzzer.duty(0)

def set_servo():
    for i in range (35,110,30):
        servo.duty(i)
        time.sleep(0.3)

def game_over():
    onnp_led((255, 0, 0))
    buzzer_beep(200)
    set_servo()
    print("GAME OVER")
    print("Final Score:", score)
    
    while True:
        pass

while True:
    colour = random.choice(colours)
    success = False

    
    if colour == "red":
        onnp_led((255, 0, 0))
    elif colour == "blue":
        onnp_led((0, 0, 255))
    elif colour == "yellow":
        onnp_led((255, 255, 0))
    elif colour == "green":
        onnp_led((0, 255, 0))

    start = time.ticks_ms()

    while True:

        #red = capacitive touch1
        if colour == "red" and touch1.read() < 300:
            success = True
            break

        #blue = ir sensor
        if colour == "blue" and ir.value() == 0:
            success = True
            break

        #yellow = pb
        if colour == "yellow" and pb.value() == 0:
            success = True
            break

        #green = capacitive touch2 
        if colour == "green" and touch2.read() < 300:
            success = True
            break

        
        if time.ticks_diff(time.ticks_ms(), start) > reaction_time:
            break

    offnp_led()

    if success:
        score += 100
        buzzer_beep(80)
        print("Score :", score)

    else:
        game_over()








