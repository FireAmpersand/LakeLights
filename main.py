import time
import threading
import mysql.connector
import python.internalLEDs as iLED #Import Inside Class
import python.externalLEDs as eLED #Import Outside Class

#Global Vars
CURRENT_INSIDE_PATTERN = "N/A"
CURRENT_OUTSIDE_PATTERN = "N/A"
CURRENT_INSIDE_POWERED_STATE = "N/A"
CURRENT_OUTSIDE_POWERED_STATE = "N/A"
INTERNAL_THREAD = None
EXTERNAL_THREAD = None

def callSQL(name):
    try:
       mydb = mysql.connector.connect(
         host="192.168.0.251",
         user="root",
         passwd="PassmorePassword",
         database="lakerpidb"
       )

       #Does a call to the sql server for name.
       if name == "Internal":
           mycursor = mydb.cursor()
           mycursor.execute("SELECT * FROM states WHERE Name='Internal'")
           return mycursor.fetchall()
       elif name == 'External':
           mycursor = mydb.cursor()
           mycursor.execute("SELECT * FROM states WHERE Name='External'")
           return mycursor.fetchall()

    except:
        return [0,0,0]

def setState(name, result):
    #Sets the state of the name strip with the sql result.
    global CURRENT_INSIDE_PATTERN
    global CURRENT_OUTSIDE_PATTERN
    global CURRENT_INSIDE_POWERED_STATE
    global CURRENT_OUTSIDE_POWERED_STATE
    if name == 'Internal':
        CURRENT_INSIDE_PATTERN = result[0][2]
        CURRENT_INSIDE_POWERED_STATE = result[0][1]
    elif name == 'External':
        CURRENT_OUTSIDE_PATTERN = result[0][2]
        CURRENT_OUTSIDE_POWERED_STATE = result[0][1]

def initialSetup():
    #Sets up the values on first boot.
    global CURRENT_INSIDE_PATTERN
    global CURRENT_OUTSIDE_PATTERN
    global CURRENT_INSIDE_POWERED_STATE
    global CURRENT_OUTSIDE_POWERED_STATE
    result = callSQL("Internal")
    setState("Internal",result)

    result = callSQL("External")
    setState("External",result)


def needsUpdate(name):
    #Compare local state vs sql state for name. Returns boolean.
    result = callSQL(name)
    if name == 'Internal':
        if CURRENT_INSIDE_PATTERN != result[0][2] or CURRENT_INSIDE_POWERED_STATE != result[0][1]:
            return True
        else:
            return False
    elif name == 'External':
        if CURRENT_OUTSIDE_PATTERN != result[0][2] or CURRENT_OUTSIDE_POWERED_STATE != result[0][1]:
            return True
        else:
            return False


def startPattern(name, pattern):
    if name == 'Internal' and pattern == 'TheaterChase':
        iLED.runTheater() 
    elif name == 'External' and pattern == 'TheaterChase':
        eLED.runTheater()
    elif name == 'Internal' and pattern == 'StaticWhite':
        iLED.staticColor(255,255,255)
    elif name == 'External' and pattern == 'StaticWhite':
        eLED.staticColor(255,255,255)
    elif name == 'Internal' and pattern == 'ColorCycle':
        iLED.runColorCycle()
    elif name == 'Internal':
        iLED.runError()

def modifyThread (name, command):
    #Change the state of a thread either kill or start
    global INTERNAL_THREAD
    global EXTERNAL_THREAD
    if name == 'Internal':
        if command == 'start':
            iLED.MASTER_LOOP = True
            INTERNAL_THREAD = threading.Thread(target=startPattern, args=(name,CURRENT_INSIDE_PATTERN))
            INTERNAL_THREAD.daemon = True
            INTERNAL_THREAD.start()
        elif command == 'kill':
            iLED.MASTER_LOOP = False
            INTERNAL_THREAD.join()
            iLED.turnOff()
    elif name == 'External':
        if command == 'start':
            eLED.MASTER_LOOP = True
            EXTERNAL_THREAD = threading.Thread(target=startPattern, args=(name,CURRENT_OUTSIDE_PATTERN))
            EXTERNAL_THREAD.daemon = True
            EXTERNAL_THREAD.start()
        elif command == 'kill':
            eLED.MASTER_LOOP = False
            EXTERNAL_THREAD.join()
            eLED.turnOff()

def main():
    global CURRENT_INSIDE_POWERED_STATE
    global CURRENT_OUTSIDE_POWERED_STATE
    #Main function
    initialSetup()
    iLED.startUp()
    #If new threads need to be started, start them
    if CURRENT_INSIDE_POWERED_STATE == 'ON':
        modifyThread('Internal', 'start')
    if CURRENT_OUTSIDE_POWERED_STATE == 'ON':
        modifyThread('External', 'start')

    #Main Loop
    while True:
        time.sleep(5)
        #Internal Checks
        if needsUpdate('Internal') == True:
            #Stop the old thread if it is running
            if (not(INTERNAL_THREAD is None)):
               if INTERNAL_THREAD.is_alive() == True:
                  modifyThread('Internal', 'kill')
               else:
                  iLED.turnOff()
            #Update the new values
            setState('Internal', callSQL('Internal'))

            #If the new values are on, then start a new thread
            if CURRENT_INSIDE_POWERED_STATE == 'ON':
                modifyThread('Internal', 'start')

        #External Checks
        if needsUpdate('External') == True:
            #Stop the old thread if it is running
            if (not(EXTERNAL_THREAD is None)):
                if EXTERNAL_THREAD.is_alive() == True:
                    modifyThread('External', 'kill')
                else:
                   eLED.turnOff()
            #Update new values
            setState('External', callSQL('External'))

            #If the new values are on, then start a new thread
            if CURRENT_OUTSIDE_POWERED_STATE == 'ON':
                modifyThread('External', 'start')


main()
