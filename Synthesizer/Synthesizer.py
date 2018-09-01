#!/usr/bin/env python  
from mingus.midi import fluidsynth
from mingus.containers.note import Note
import mraa
import time 

fluidsynth.init('/home/root/FluidR3_GM.sf2', "alsa")    
button0 = mraa.Gpio(0)
button1 = mraa.Gpio(1)
button2 = mraa.Gpio(2)
button3 = mraa.Gpio(3)
button4 = mraa.Gpio(4)
button5 = mraa.Gpio(5)
button6 = mraa.Gpio(6)
button7 = mraa.Gpio(7)
button8 = mraa.Gpio(8)
button9 = mraa.Gpio(9)
button10 = mraa.Gpio(10)
button11 = mraa.Gpio(11)
button12 = mraa.Gpio(12)
button13 = mraa.Gpio(13)

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

counter0 = 127;
counter1 = 127;
counter2 = 127;
counter3 = 127;
counter4 = 127;
counter5 = 127;
counter6 = 127;
counter7 = 127;
counter8 = 127;
counter9 = 127;
	
oldval0 = 0
oldval1 = 0
oldval2 = 0
oldval3 = 0
oldval4 = 0
oldval5 = 0
oldval6 = 0
oldval7 = 0
oldval8 = 0
oldval9 = 0

instrument = 0

while True:
    time.sleep(0.05)
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
    
	
    if buttonState9 == 0 and oldval9 == 1:
        instrument +=1
        print("\t\t\t\t", instrument)
        fluidsynth.set_instrument(0, instrument)
        oldval9 = 0
    elif buttonState9 == 1 and oldval9 == 0:
        ##fluidsynth.play_Note(n)
        oldval9 = 1
	    
    if buttonState0 == 0:
        if buttonState1 == 0 and oldval1 == 1:
            oldval1 = 0
            n1 = Note("A-4")
            n1.channel = 0
            n1.velocity = counter1
            fluidsynth.play_Note(n1)
            print("APASAT", counter1)
        elif buttonState1 == 1:
            oldval1 = 1
            counter1 -= 1
            ##time.sleep(0.005)
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
            print("APASAT", counter3)
        elif buttonState3 == 1:
            oldval3 = 1
            counter3 -= 1
            ##time.sleep(0.005)
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
            print("APASAT", counter5)
        elif buttonState5 == 1:
            oldval5 = 1
            counter5 -= 1
            ##time.sleep(0.005)
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
            print("APASAT", counter7)
        elif buttonState7 == 1:
            oldval7 = 1
            counter7 -= 1
            ##time.sleep(0.005)
            if counter7 == 0:
                counter7 += 1
            print (counter7)
    elif buttonState6 == 1:
        counter7 = 127	
		

    ##if buttonState8 == 0:
    ##    if buttonState9 == 0 and oldval9 == 1:
    ##        oldval9 = 0
    ##        n9 = Note("E-5")
    ##        n9.channel = 0
    ##        n9.velocity = counter9
    ##        fluidsynth.play_Note(n9)
    ##        print("APASAT", counter9)
    ##    elif buttonState9 == 1:
    ##        oldval9 = 1
    ##        counter9 -= 1
    ##        ##time.sleep(0.005)
    ##        if counter9 == 0:
    ##            counter9 += 1
    ##        print (counter9)
    ##elif buttonState8 == 1:
    ##    counter9 = 127	
		
##while True:
##    time.sleep(0.05)
##    buttonState = button1.read()
##    buttonState2 = button2.read()
##    buttonState3 = button3.read() 
##    buttonState4 = button4.read() 
##    buttonState5 = button5.read() 
##    buttonState6 = button6.read() 
##    buttonState7 = button7.read() 	
##    fluidsynth.set_instrument(0, 3)
##	
##    if buttonState == 0:
##        if buttonState2 == 0 and oldval2 == 1:
##            oldval2 = 0
##            fluidsynth.play_Note(60,0,counter)
##            print("APASAT", counter)
##        elif buttonState2 == 1:
##            oldval2 = 1
##            counter -= 1
##            ##time.sleep(0.005)
##            if counter == 0:
##                counter += 1
##            print (counter)
##
##        if buttonState3 == 0 and oldval3 == 1:
##            oldval3 = 0
##            fluidsynth.play_Note(62,0,counter)
##            print("APASAT", counter)
##        elif buttonState3 == 1:
##            oldval3 = 1
##            counter -= 1
##            ##time.sleep(0.005)
##            if counter == 0:
##                counter += 1
##            print (counter)	
##
##        if buttonState4 == 0 and oldval4 == 1:
##            oldval4 = 0
##            fluidsynth.play_Note(64,0,counter)
##            print("APASAT", counter)
##        elif buttonState4 == 1:
##            oldval4 = 1
##            counter -= 1
##            ##time.sleep(0.005)
##            if counter == 0:
##                counter += 1
##            print (counter)	
##
##        if buttonState5 == 0 and oldval5 == 1:
##            oldval5 = 0
##            fluidsynth.play_Note(66,0,counter)
##            print("APASAT", counter)
##        elif buttonState5 == 1:
##            oldval5 = 1
##            counter -= 1
##            ##time.sleep(0.005)
##            if counter == 0:
##                counter += 1
##            print (counter)	
##
##        if buttonState6 == 0 and oldval6 == 1:
##            oldval6 = 0
##            fluidsynth.play_Note(68,0,counter)
##            print("APASAT", counter)
##        elif buttonState6 == 1:
##            oldval6 = 1
##            counter -= 1
##            ##time.sleep(0.005)
##            if counter == 0:
##                counter += 1
##            print (counter)	
##
##    elif buttonState == 1:
##        counter = 127
##
	
##    if buttonState2 == 0 and oldval2 == 1:
##        fluidsynth.play_Note(n2)
##        oldval2 = 0
##    elif buttonState2 == 1 and oldval2 == 0:
##        ##fluidsynth.play_Note(n2)
##        oldval2 = 1
##		
##    if buttonState3 == 0 and oldval3 == 1:
##        fluidsynth.play_Note(n3)
##        oldval3 = 0
##    elif buttonState3 == 1 and oldval3 == 0:
##        ##fluidsynth.play_Note(n2)
##        oldval3 = 1
##		
##    if buttonState4 == 0 and oldval4 == 1:
##        fluidsynth.play_Note(n4)
##        oldval4 = 0
##    elif buttonState4 == 1 and oldval4 == 0:
##        ##fluidsynth.play_Note(n2)
##        oldval4 = 1
##		
##    if buttonState5 == 0 and oldval5 == 1:
##        fluidsynth.play_Note(n5)
##        oldval5 = 0
##    elif buttonState5 == 1 and oldval5 == 0:
##        ##fluidsynth.play_Note(n2)
##        oldval5 = 1
##		
##    if buttonState6 == 0 and oldval6 == 1:
##        fluidsynth.play_Note(n6)
##        oldval6 = 0
##    elif buttonState6 == 1 and oldval6 == 0:
##        ##fluidsynth.play_Note(n2)
##        oldval6 = 1
##		
##    if buttonState7 == 0 and oldval7 == 1:
##        fluidsynth.play_Note(n7)
##        oldval7 = 0
##    elif buttonState7 == 1 and oldval7 == 0:
##        ##fluidsynth.play_Note(n2)
##        oldval7 = 1