import re
import random
import time

##TODO:  Make the parking spots be chosen based on parking capacity.

## On run this will overwrite thisplans  file.
generatedPlanFile = '../plans/01_plan.xml'
networkXMLFile = '../networks/01_carleton_network.xml'
randomSeed = 4900

# The node id's of nodes representing where people start their
# journey at the start of the day, and where they will end their journey.
homeStart = [1435066125, 901063900, 1435066119, 901068597]
homeEnd = [905117452, 901069328, 901063167, 901068597]

#parkingCapacity = [900,900,900,900,1200,1200,200,200,300,300,600]

# The node id's of nodes representing where people will park at Carleton
# 0, 1 Athletics, 2, 3 field house, 4, 5 P4 , 6, 7 uc parking, 8 co op parking, 9 south lib parking, Garage 9
parking = [8581420024, 1034655817, 9451397931, 9451397931, 3071803288, 5590646581, 10199274341, 10199274342, 1435788933, 5707082427, 2924096375]


class Node:
  def __init__(self, x, y):
    self.x = x
    self.y = y

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
f = open(generatedPlanFile, "w+")
f.write('<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE population SYSTEM "http://www.matsim.org/files/dtd/population_v6.dtd">\n<population>\n')

random.seed(randomSeed)

for id in range(500):
    home = random.randint(0, len(homeStart) -1)
    work = random.randint(0, len(parking) -1)   ## this can be changed to account for parking lot capacity
    currTime = time.gmtime(id)                  ## This spawns them every second. Perhaps it can be tweeked
    timeString = f'{currTime.tm_hour:02d}:{currTime.tm_min:02d}:{currTime.tm_sec:02d}'
    f.write(f'\t<person id="{id}">\n')
    f.write(f'\t\t<plan selected= "yes">\n')
    f.write(f'\t\t\t<activity type="h" x="{allNodes[homeStart[home]].x}" y="{allNodes[homeStart[home]].y}" end_time="{timeString}">\n')
    f.write(f'\t\t\t</activity>\n')
    f.write(f'\t\t\t<leg mode="car">\n')
    f.write(f'\t\t\t</leg>\n')
    f.write(f'\t\t\t<activity type="w" x="{allNodes[parking[work]].x}" y="{allNodes[parking[work]].y}" max_dur="04:00:00">\n')
    f.write(f'\t\t\t</activity>\n')
    f.write(f'\t\t\t<leg mode="car">\n')
    f.write(f'\t\t\t</leg>\n')
    f.write(f'\t\t\t<activity type="h" x="{allNodes[homeEnd[home]].x}" y="{allNodes[homeEnd[home]].y}" >\n')
    f.write(f'\t\t\t</activity>\n')
    f.write(f'\t\t</plan>\n')
    f.write(f'\t</person>\n')

f.write(f'</population>')


f.close()