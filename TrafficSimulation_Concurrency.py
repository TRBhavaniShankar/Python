import time
import random
import threading
import sys

#Initializing
barrier = threading.Barrier(7)
Astraight,Aright,Aleft = 0,0,0
Bstraight,Bright,Bleft = 0,0,0
Cstraight,Cright,Cleft = 0,0,0
Dstraight,Dright,Dleft = 0,0,0
countC,countD = 0,0
bv1Right = False

#Direction to be assigned to vehicles randomly
randDirection = ["straight", "right", "left"]

#Initiallizing locks. The intersection between the signals are divided
# into 4 cells which are interconnection cells
lock1 = threading.Lock()    #Intersection in front of forword of A's road
lock2 = threading.Lock()    #Intersection in front of forword of B's road
lock3 = threading.Lock()    #Intersection in front of forword of C's road
lock4 = threading.Lock()    #Intersection in front of forword of D's road

lockA = threading.Lock()    #Lock to perform any count increment or decrement A's count
lockB = threading.Lock()    #Lock to perform any count increment or decrement B's count
lockC = threading.Lock()    #Lock to perform any count increment or decrement C's count
lockD = threading.Lock()    #Lock to perform any count increment or decrement D's count

#initial traffic like to East-West
trafficlight = "EW"
signalLock = threading.Lock()

#class to create an object for vehicle
class vehicle:
    def __init__(self, name, road, direction, nameDirection):
        self.name = name
        self.road = road
        self.direction = direction
        self.nameDirection = nameDirection

#Main function which threads executs
def trafficController(tID):

    #Declaring global variables
    global Astraight,Aright,Aleft
    global Bstraight,Bright,Bleft
    global Cstraight,Cright,Cleft
    global Dstraight,Dright,Dleft
    global lockA,lockB,lockC,lockD
    global countC,countD
    global trafficlight, bv1Right

    #check the count of all the vehicles along with their direction
    if tID.nameDirection == "Astraight":
        lockA.acquire()
        Astraight += 1
        lockA.release()
    elif tID.nameDirection == "Aright":
        lockA.acquire()
        Aright += 1
        lockA.release()
    elif tID.nameDirection == "Aleft":
        lockA.acquire()
        Aleft += 1
        lockA.release()

    elif tID.nameDirection == "Bstraight":
        lockB.acquire()
        Bstraight += 1
        lockB.release()
    elif tID.nameDirection == "Bright":
        lockB.acquire()
        Bright += 1
        if tID.name == "bv1" and tID.direction == "right":
            bv1Right = True
        lockB.release()
    elif tID.nameDirection == "Bleft":
        lockB.acquire()
        Bleft += 1
        lockB.release()

    elif tID.nameDirection == "Cstraight":
        lockC.acquire()
        Cstraight += 1
        lockC.release()
    elif tID.nameDirection == "Cright":
        lockC.acquire()
        Cright += 1
        lockC.release()
    elif tID.nameDirection == "Cleft":
        lockC.acquire()
        Cleft += 1
        lockC.release()

    elif tID.nameDirection == "Dstraight":
        lockD.acquire()
        Dstraight += 1
        lockD.release()
    elif tID.nameDirection == "Dright":
        lockD.acquire()
        Dright += 1
        lockD.release()
    elif tID.nameDirection == "Dleft":
        lockD.acquire()
        Dleft += 1
        lockD.release()

    print("I'm",tID.name,"--------->","moving in ",tID.direction,"direction")
    #wait until all the threads have updated their counts
    barrier.wait()

    while(True):
        #If moving in East-West direction
        if trafficlight == "EW":

            #A moving in right direction
            if tID.nameDirection == "Aright":

                lock1.acquire()
                try:
                    print("Im ", tID.name," now in transition")
                finally :
                    print("*****done****** Im ", tID.name,
                          ": I traversed in right direction......Now im moving in the road D")
                    lock1.release()

                    lockA.acquire()
                    Aright -= 1
                    lockA.release()


                    break

            # A moving in straight direction
            elif tID.nameDirection == "Astraight":

                lock1.acquire()
                lock4.acquire()
                lock1.release()

                try :
                    print("Im ", tID.name," now in transition")
                finally :
                    print("*****done****** Im ", tID.name,
                          ": I traversed in straight direction......Now im moving in the road C")
                    lock4.release()

                    lockA.acquire()
                    Astraight -= 1
                    lockA.release()

                    break

            # A moving in left direction
            elif tID.nameDirection == "Aleft":

                lock1.acquire()
                lock4.acquire()
                lock1.release()

                lock3.acquire()
                lock4.release()

                try :
                    print("Im ", tID.name," now in transition")
                finally :
                    print("*****done****** Im ", tID.name,
                          ": I traversed in left direction......Now im moving in the road B")
                    lock3.release()

                    lockA.acquire()
                    Aleft -= 1
                    lockA.release()
                    break

            # B moving in right direction
            elif bv1Right is True and tID.nameDirection == "Bright":

                #wait for 3 secs before taking a right in red signal
                time.sleep(3)
                #check if no one is coming from other direction, if no one move a head or wait for 3 more secs
                while Cstraight != 0 and Cleft != 0:
                    time.sleep(3)

                lock2.acquire()
                try:
                    print("Im ", tID.name," now in transition")
                finally:
                    print("*****done****** Im ", tID.name,
                          ": I traversed in right direction......Now im moving in the road A and I waited for 3 seconds"
                          " and took a right turn when the signal infront of me was red")
                    lock2.release()
                    lockB.acquire()
                    Bright -= 1
                    lockB.release()

                    break

            # C moving in straight direction
            elif tID.nameDirection == "Cstraight":
                lock3.acquire()
                lock2.acquire()
                lock3.release()

                try:
                    print("Im ", tID.name," now in transition")
                finally:
                    print("*****done****** Im ", tID.name,
                          ": I traversed in stright direction......Now im moving in the road A")
                    lock2.release()
                    lockC.acquire()
                    Cstraight -= 1
                    lockC.release()

                    break

            # C moving in right direction
            elif tID.nameDirection == "Cright":
                lock3.acquire()
                try:
                    print("Im ", tID.name," now in transition")
                finally :
                    print("*****done****** Im ", tID.name,
                          ": I traversed in right direction......Now im moving in the road B")
                    lock3.release()

                    lockC.acquire()
                    Cright -= 1
                    lockC.release()

                    break

            # C moving in left direction
            elif tID.nameDirection == "Cleft":
                lock3.acquire()
                lock2.acquire()
                lock3.release()

                lock1.acquire()
                lock2.release()
                try:
                    print("Im ", tID.name," now in transition")
                finally:
                    print("*****done****** Im ", tID.name,
                          ": I traversed in left direction......Now im moving in the road D")
                    lock1.release()

                    lockC.acquire()
                    Cleft =-1
                    lockC.release()

                    break

            # D moving in right direction
            elif tID.nameDirection == "Dright":

                # wait for 3 secs before taking a right in red signal
                time.sleep(3)
                # check if no one is coming from other direction, if no one move a head or wait for 3 more secs
                while Astraight != 0 and Aleft != 0:
                    time.sleep(3)

                lock4.acquire()
                try:
                    print("Im ", tID.name," now in transition")
                finally :
                    print("*****done****** Im ", tID.name,
                          ": I traversed in right direction......Now im moving in the road C and I waited for 3 seconds"
                          " and took a right turn when the signal infront of me was red")
                    lock4.release()
                    lockD.acquire()
                    Dright -= 1
                    lockD.release()

                    break

            #time to transition from Green to Red(yellow light) which I have taken as 5 secs
            time.sleep(5)

            #change the signal to green in Nort-South
            signalLock.acquire()
            trafficlight = "NS"
            signalLock.release()

        #If moving in North-South direction
        elif trafficlight == "NS":

            #B moving in right direction, onces which were waiting behind BV1,
            # if BV1 did not move in right direction in EW signal direction
            if tID.nameDirection == "Bright":

                lock2.acquire()
                try:
                    print("Im ", tID.name," now in transition")
                finally:
                    print("*****done****** Im ", tID.name,
                          ": I traversed in right direction......Now im moving in the road A")
                    lock2.release()

                    lockB.acquire()
                    Bright -= 1
                    lockB.release()

                    break

            # B moving in straight direction
            elif tID.nameDirection == "Bstraight":
                lock2.acquire()
                lock1.acquire()
                lock2.release()

                try:
                    print("Im ", tID.name," now in transition")
                finally:
                    print("*****done****** Im ", tID.name,
                          ": I traversed in straight direction......Now im moving in the road D")
                    lock1.release()

                    lockB.acquire()
                    Bstraight -= 1
                    lockB.release()

                    break

            # B moving in left direction
            elif tID.nameDirection == "Bleft":
                lock2.acquire()
                lock1.acquire()
                lock2.release()

                lock4.acquire()
                lock1.release()
                try:
                    print("Im ", tID.name," now in transition")
                finally:
                    print("*****done****** Im ", tID.name,
                          ": I traversed in left direction......Now im moving in the road C")
                    lock4.release()

                    lockB.acquire()
                    Bleft =-1
                    lockB.release()

                    break

            # D moving in left direction
            elif tID.nameDirection == "Dleft":
                lock4.acquire()
                lock3.acquire()
                lock4.release()

                lock2.acquire()
                lock3.release()
                try:
                    print("Im ", tID.name," now in transition")
                finally:
                    print("*****done****** Im ", tID.name,
                          ": I traversed in left direction......Now im moving in the road A")
                    lock2.release()

                    lockD.acquire()
                    Dleft =-1
                    lockD.release()

                    break

            # D moving in straight direction
            elif tID.nameDirection == "Dstraight":
                lock4.acquire()
                lock3.acquire()
                lock4.release()

                try:
                    print("Im ", tID.name," now in transition")
                finally:
                    print("*****done****** Im ", tID.name,
                          ": I traversed in straight direction......Now im moving in the road B")
                    lock3.release()

                    lockD.acquire()
                    Dstraight -= 1
                    lockD.release()

                    break

#naming roads
roadA = "A"
roadB = "B"
roadC = "C"
roadD = "D"

# creating vehicles for A
for i in range(1, 4):
    ID = "av" + str(i)
    dir = random.choice(randDirection)
    nameDirection = "A"+dir
    tID = vehicle(ID, roadA, dir, nameDirection)
    t = threading.Thread(target=trafficController, args=[tID])
    t.start()

# creating vehicles for B
for i in range(1, 3):
    ID = "bv" + str(i)
    dir = random.choice(randDirection)
    nameDirection = "B"+dir
    tID = vehicle(ID, roadB, dir, nameDirection)
    t = threading.Thread(target=trafficController, args=[tID])
    t.start()

# creating a vehicle for C
dir = random.choice(randDirection)
tID = vehicle("cv1", roadC, dir, "C"+dir)
t = threading.Thread(target=trafficController, args=[tID])
t.start()

# creating a vehicle for D
dir = random.choice(randDirection)
tID = vehicle("dv1", roadD, dir, "D"+dir)
t = threading.Thread(target=trafficController, args=[tID])
t.start()
