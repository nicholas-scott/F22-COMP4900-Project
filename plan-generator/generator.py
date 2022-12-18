import re
import random 
import time

##TODO:  Make the parking spots be chosen based on parking capacity.
## On run this will overwrite thisplans  file.
generatedPlanFile = '../plans/01_plan.xml'
networkXMLFile = '../networks/01-double-round-network.xml'
 
generatedPlanFile = '../plans/02_plan.xml'
networkXMLFile = '../networks/02-1-point-5-lane-roundabout-network.xml'

generatedPlanFile = '../plans/03_plan.xml'
networkXMLFile = '../networks/03-4-way-intersection-network.xml'
 

secondsIn4Hours = 14400
driverId = 0 

randomSeed = 4900
plansGenerated = 10
# The node id's of nodes representing where people start their
# journey at the start of the day, and where they will end their journey.
# Bronson North, Sunnyside, Bronson South, Colonel By South
homeStartIds = [901065319, 6818021169, 9451397933, 5171288980]
homeEndIds = [901057238, 6818021169, 901068674, 5171288980]

homeStart2Ids = [901065319, 901065319, 6818021169, 6818021169, 9451397933, 901057238, 5171288980,901057848, 5171288980, 6818021169]
homeEnd2Ids = [901068674, 6818021169, 901057238, 901068674, 901057238, 6818021169, 901057848, 5171288980, 6818021169, 5171288980]

#P6 + P18, P7, P5  P3, P9, UC, P1 (lib above+underground)
parkingCapacity=[1700, 350, 205, 265, 850, 50, 243]
parkingIds=[5590646577, 9451397933, 1034655817, 1435788939, 1435894774, 10199274343, 5707081812]
parkingInd= [i for i in range(len(parkingIds))]

parkingSum = sum(parkingCapacity)
parkingProb = [value / parkingSum for value in parkingCapacity] ## a proportion of all parking spots on campus  


# P6, Red House, Field House, p3, p9, UC, lib

class Node:
  def __init__(self, x, y):
    self.x = x
    self.y = y

def generate(id):
    home = random.randint(0, len(homeStartIds) -1)
    work = random.choices(parkingInd, weights=parkingProb)[0]
    currTime = time.gmtime(id)                  ## This spawns them every second. Perhaps it can be tweeked
    timeString = f'{currTime.tm_hour:02d}:{currTime.tm_min:02d}:{currTime.tm_sec:02d}'
    timeSpentHours= random.randint(1, 8)        ## 1 to 8 hours
    
    f.write(f'\t<person id="{driverId}">\n')
    f.write(f'\t\t<plan selected= "yes">\n')
    f.write(f'\t\t\t<activity type="h" x="{allNodes[homeStartIds[home]].x}" y="{allNodes[homeStartIds[home]].y}" end_time="{timeString}">\n')
    f.write(f'\t\t\t</activity>\n')
    f.write(f'\t\t\t<leg mode="car">\n')
    f.write(f'\t\t\t</leg>\n')
    f.write(f'\t\t\t<activity type="w" x="{allNodes[parkingIds[work]].x}" y="{allNodes[parkingIds[work]].y}" max_dur="0{timeSpentHours}:00:00">\n')
    f.write(f'\t\t\t</activity>\n')
    f.write(f'\t\t\t<leg mode="car">\n')
    f.write(f'\t\t\t</leg>\n')
    f.write(f'\t\t\t<activity type="h" x="{allNodes[homeEndIds[home]].x}" y="{allNodes[homeEndIds[home]].y}" >\n')
    f.write(f'\t\t\t</activity>\n')
    f.write(f'\t\t</plan>\n')
    f.write(f'\t</person>\n') 

def generate2(id):
    home = random.randint(0, len(homeStart2Ids) -1)
    work = random.choices(parkingInd, weights=parkingProb)[0]
    currTime = time.gmtime(id)                  ## This spawns them every second. Perhaps it can be tweeked
    timeString = f'{currTime.tm_hour:02d}:{currTime.tm_min:02d}:{currTime.tm_sec:02d}'
    f.write(f'\t<person id="{driverId}">\n')
    f.write(f'\t\t<plan selected= "yes">\n')
    f.write(f'\t\t\t<activity type="h" x="{allNodes[homeStart2Ids[home]].x}" y="{allNodes[homeStart2Ids[home]].y}" end_time="{timeString}">\n')
    f.write(f'\t\t\t</activity>\n')
    f.write(f'\t\t\t<leg mode="car">\n')
    f.write(f'\t\t\t</leg>\n')
    f.write(f'\t\t\t<activity type="h" x="{allNodes[homeEnd2Ids[home]].x}" y="{allNodes[homeEnd2Ids[home]].y}" >\n')
    f.write(f'\t\t\t</activity>\n')
    f.write(f'\t\t</plan>\n')
    f.write(f'\t</person>\n') 
    

## Open network file to retrieve node information
file1 = open(networkXMLFile, 'r')
Lines = file1.readlines()
## Key is node idea, value is Node 
allNodes = {}

for line in Lines:
    if(line.startswith("	</nodes>")):
        break

    values = re.findall("\d+\.?\d+", line)

    if(len(values) == 3):
        allNodes[int(values[0])] = Node(values[1], values[2])

file1.close() 


## Generate the plans
## Using an xml writter would be cleaner.
f = open(generatedPlanFile, "w+")
f.write('<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE population SYSTEM "http://www.matsim.org/files/dtd/population_v6.dtd">\n<population>\n')

random.seed(randomSeed)

  
for second in range(secondsIn4Hours):
    currTime = time.gmtime(second)
    isCarleton = random.randint(0, 1)
    if(second < 3600 and second % 3 == 0):
        if(isCarleton):
            generate(second)
        else:
            generate2(second)
        driverId += 1
        
    elif(second < 7200 and second >= 3600 and second % 8 == 0):
        if(isCarleton):
            generate(second)
        else:
            generate2(second)
        driverId += 1
       
    elif(second < 10800 and second >= 7200 and second % 15 == 0):
        if(isCarleton):
            generate(second)
        else:
            generate2(second)
        driverId += 1
      
    elif(second % 8 == 0):
        if(isCarleton):
            generate(second)
        else:
            generate2(second)
        driverId += 1
        
    

f.write(f'</population>')


f.close()