import time
import threading
import mysql.connector
import python.internalLEDs as iLED #Import Inside Class
#import python.externalLEDs as eLED #Import Outside Class

#Global Vars
CURRENT_INSIDE_PATTERN = "N/A"
CURRENT_OUTSIDE_PATTERN = "N/A"
CURRENT_INSIDE_POWERED_STATE = "N/A"
CURRENT_OUTSIDE_POWERED_STATE = "N/A"
INTERNAL_THREAD = ""
EXTERNAL_THREAD = ""

def callSQL(name):

    mydb = mysql.connector.connect(
      host="bumblebee.fireampersand.ca",
      port="10069",
      user="root",
      passwd="tester",
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

def modifyThread (name, command):
    #Change the state of a thread either kill or start
    global INTERNAL_THREAD
    global EXTERNAL_THREAD
    if name == 'Internal':
        if command == 'start':
            INTERNAL_THREAD = threading.Thread(target=startPattern, args=(name,CURRENT_INSIDE_PATTERN))
            INTERNAL_THREAD.daemon = True
            INTERNAL_THREAD.start()
        elif command == 'kill':
            INTERNAL_THREAD.terminate()
    elif name == 'External':
        if command == 'start':
            EXTERNAL_THREAD = threading.Thread(target=startPattern, args=(name,CURRENT_OUTSIDE_PATTERN))
            EXTERNAL_THREAD.daemon = True
            EXTERNAL_THREAD.start()
        elif command == 'kill':
            EXTERNAL_THREAD.terminate()

def main():
    #Main function
    initialSetup()
    iLED.runStartup()
    #If new threads need to be started, start them
    if CURRENT_INSIDE_POWERED_STATE == 'ON':
        modifyThread('Internal', 'start')
    if CURRENT_OUTSIDE_POWERED_STATE == 'ON':
        modifyThread('External', 'start')

    #Main Loop
    while True:
        time.sleep(5)
        print(CURRENT_INSIDE_PATTERN + " | " + callSQL('Internal')[0][2])
        print(needsUpdate('Internal'))
        #Internal Checks
        if needsUpdate('Internal') == True:
            #Stop the old thread if it is running
            if INTERNAL_THREAD.is_alive() == True:
                modifyThread('Internal', kill)
            #Update the new values
            setState('Internal', callSQL('Internal'))

            #If the new values are on, then start a new thread
            if CURRENT_INTERNAL_POWERED_STATE == 'ON':
                modifyThread('Internal', 'start')

        #External Checks
        if needsUpdate('External') == True:
            #Stop the old thread if it is running
            if EXTERNAL_THREAD.is_alive() == True:
                modifyThread('External', 'kill')
            #Update new values
            setState('External', callSQL('External'))

            #If the new values are on, then start a new thread
            if CURRENT_OUTSIDE_POWERED_STATE == 'ON':
                modifyThread('External', 'start')


main()
