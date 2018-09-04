## Import the libraries.
from mingus.midi import fluidsynth
from mingus.containers.note import Note
import mraa
import time 

## Use a specific soundfont, and a driver.
fluidsynth.init('/home/root/FluidR3_GM.sf2', "alsa") 

## The following buttons are used to implement velocity system.
## Buttons used as counters.
button0 = mraa.Gpio(0)
button2 = mraa.Gpio(2)
button4 = mraa.Gpio(4)
button6 = mraa.Gpio(6)
button8 = mraa.Gpio(8)
button10 = mraa.Gpio(10)
button12 = mraa.Gpio(12)

## Buttons used as playing sounds.
button1 = mraa.Gpio(1)
button3 = mraa.Gpio(3)
button5 = mraa.Gpio(5)
button7 = mraa.Gpio(7)
button9 = mraa.Gpio(9)
button11 = mraa.Gpio(11)
button13 = mraa.Gpio(13)

## Button used to change the instrument.
changeInstrument = mraa.Aio(0)

## Configure buttons as outputs, and set PULL_UP resistors for every button.
button0.dir(mraa.DIR_IN)
button0.mode(mraa.MODE_PULLUP)  
button1.dir(mraa.DIR_IN)
button1.mode(mraa.MODE_PULLUP)
button2.dir(mraa.DIR_IN)
button2.mode(mraa.MODE_PULLUP)
button3.dir(mraa.DIR_IN)
button3.mode(mraa.MODE_PULLUP)
button4.dir(mraa.DIR_IN)
button4.mode(mraa.MODE_PULLUP)
button5.dir(mraa.DIR_IN)
button5.mode(mraa.MODE_PULLUP)
button6.dir(mraa.DIR_IN)
button6.mode(mraa.MODE_PULLUP)
button7.dir(mraa.DIR_IN)
button7.mode(mraa.MODE_PULLUP)
button8.dir(mraa.DIR_IN)
button8.mode(mraa.MODE_PULLUP)
button9.dir(mraa.DIR_IN)
button9.mode(mraa.MODE_PULLUP)
button10.dir(mraa.DIR_IN)
button10.mode(mraa.MODE_PULLUP)
button11.dir(mraa.DIR_IN)
button11.mode(mraa.MODE_PULLUP)
button12.dir(mraa.DIR_IN)
button12.mode(mraa.MODE_PULLUP)
button13.dir(mraa.DIR_IN)
button13.mode(mraa.MODE_PULLUP)

## Counter for every button used to count the volume of note when velocity system is activated.
counter1 = 127;
counter3 = 127;
counter5 = 127;
counter7 = 127;
counter9 = 127;
counter11 = 127;
counter13 = 127;

## In order to push a button and if is kept pushed, the button will be activated only once using these values.	
oldval1 = 0
oldval3 = 0
oldval5 = 0
oldval7 = 0
oldval9 = 0
oldval11 = 0
oldval13 = 0

instrumentOldVal = 0

## Counter used to select a different instrument each time we press the button.
instrument = 0

## The loop which is running all the time.
while True:
    ## After every button pressed, there is a 50 ms delay.
    time.sleep(0.05)
	
	## Read the button states (pressed/released).
    buttonState0 = button0.read() 
    buttonState1 = button1.read()
    buttonState2 = button2.read()
    buttonState3 = button3.read() 
    buttonState4 = button4.read() 
    buttonState5 = button5.read() 
    buttonState6 = button6.read() 
    buttonState7 = button7.read()
    buttonState8 = button8.read()
    buttonState9 = button9.read()
    buttonState10 = button10.read() 
    buttonState11 = button11.read() 
    buttonState12 = button12.read() 
    buttonState13 = button13.read() 	
    changeInstrumentState = changeInstrument.read()
	
	
	## The sequence which is used to select the instrument.
    if changeInstrumentState == 0 and instrumentOldVal == 1:
        instrument +=1
        print("Instrument: ", instrument)
        fluidsynth.set_instrument(0, instrument)
        instrumentOldVal = 0
    elif changeInstrumentState > 0 and instrumentOldVal == 0:
        instrumentOldVal = 1
	
    ## The sequene which is used to bring velocity system to life.    
    if buttonState0 == 0:
        if buttonState1 == 0 and oldval1 == 1:
            oldval1 = 0
            n1 = Note("A-4")
            n1.channel = 0
            n1.velocity = counter1
            fluidsynth.play_Note(n1)
            print("ACTIVATED ", counter1)
        elif buttonState1 == 1:
            oldval1 = 1
            counter1 -= 1
            if counter1 == 0:
                counter1 += 1
            print (counter1)
    elif buttonState0 == 1:
        counter1 = 127

    if buttonState2 == 0:
        if buttonState3 == 0 and oldval3 == 1:
            oldval3 = 0
            n3 = Note("B-4")
            n3.channel = 0
            n3.velocity = counter3
            fluidsynth.play_Note(n3)
            print("ACTIVATED ", counter3)
        elif buttonState3 == 1:
            oldval3 = 1
            counter3 -= 1
            if counter3 == 0:
                counter3 += 1
            print (counter3)
    elif buttonState2 == 1:
        counter3 = 127	

    if buttonState4 == 0:
        if buttonState5 == 0 and oldval5 == 1:
            oldval5 = 0
            n5 = Note("C-5")
            n5.channel = 0
            n5.velocity = counter5
            fluidsynth.play_Note(n5)
            print("ACTIVATED ", counter5)
        elif buttonState5 == 1:
            oldval5 = 1
            counter5 -= 1
            if counter5 == 0:
                counter5 += 1
            print (counter5)
    elif buttonState4 == 1:
        counter5 = 127	

    if buttonState6 == 0:
        if buttonState7 == 0 and oldval7 == 1:
            oldval7 = 0
            n7 = Note("D-5")
            n7.channel = 0
            n7.velocity = counter7
            fluidsynth.play_Note(n7)
            print("ACTIVATED ", counter7)
        elif buttonState7 == 1:
            oldval7 = 1
            counter7 -= 1
            if counter7 == 0:
                counter7 += 1
            print (counter7)
    elif buttonState6 == 1:
        counter7 = 127	
		

    if buttonState8 == 0:
        if buttonState9 == 0 and oldval9 == 1:
            oldval9 = 0
            n9 = Note("E-5")
            n9.channel = 0
            n9.velocity = counter9
            fluidsynth.play_Note(n9)
            print("ACTIVATED ", counter9)
        elif buttonState9 == 1:
            oldval9 = 1
            counter9 -= 1
            if counter9 == 0:
                counter9 += 1
            print (counter9)
    elif buttonState8 == 1:
        counter9 = 127	

    if buttonState10 == 0:
        if buttonState11 == 0 and oldval11 == 1:
            oldval11 = 0
            n11 = Note("F-5")
            n11.channel = 0
            n11.velocity = counter11
            fluidsynth.play_Note(n11)
            print("ACTIVATED ", counter11)
        elif buttonState11 == 1:
            oldval11 = 1
            counter11 -= 1
            if counter11 == 0:
                counter11 += 1
            print (counter11)
    elif buttonState10 == 1:
        counter11 = 127	
		
    if buttonState12 == 0:
        if buttonState13 == 0 and oldval13 == 1:
            oldval13 = 0
            n13 = Note("G-5")
            n13.channel = 0
            n13.velocity = counter13
            fluidsynth.play_Note(n13)
            print("ACTIVATED ", counter13)
        elif buttonState13 == 1:
            oldval13 = 1
            counter13 -= 1
            if counter13 == 0:
                counter13 += 1
            print (counter13)
    elif buttonState12 == 1:
        counter13 = 127	