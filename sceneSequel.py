#!/usr/bin/env python

from random import Random
import sys

random=Random()

MAX=5

successWeight=0.1
complicationWeight=0.7

world={}
world["go about it the obvious way"]={"get a museum uniform":{"probability":0.5, "complications":{"get a smaller gun": { "probability":0.9 }}}}
world["go_to_gun_store"]={"get a smaller gun":{"probability":0.7, "complications":{"find my stolen wallet":{ "probability":0.2}}}}
world["get a smaller gun"]={}
world["get a museum uniform"]={"pass as a museum employee":{"probability":0.3, "complications":{"heal my leg wound":{ "probability":0.2}, "escape the museum":{ "probability": 0.7} } } }
world["pass as a museum employee"]={"steal them jewels":{"probability":0.7, "complications":{"heal my leg wound":{ "probability":0.3}, "heal my arm wound":{ "probability":0.3}, "heal my chest wound":{ "probability":0.3}}}, "go to the hospital":{"probability":0.9}}
world["go to the hospital"]={"heal my leg wound":{"probability":0.9}, "heal my arm wound":{"probability":0.9}, "heal my chest wound":{"probability":0.7}, "escape the museum":{"probability":0.7}}
world["heal my leg wound"]={"go to the hospital":{"probability":1}, "get a museum uniform":{"probability":1}, "get a smaller gun":{"probability":1}}
world["heal my arm wound"]={"go to the hospital":{"probability":1}, "get a museum uniform":{"probability":1}, "get a smaller gun":{"probability":1}}
world["heal my chest wound"]={"go to the hospital":{"probability":1}, "get a museum uniform":{"probability":1}, "get a smaller gun":{"probability":1}}
world["steal them jewels"]={"steal them jewels":{"probability":1, "complicaitons":{}}}

endGoal="steal them jewels"


goalPool={endGoal:1}
complicationList=[]

cachedRankings={}
stateStack=[]
oldState="None"

oldmsg=""
def printmsg(msg):
	global oldmsg
	if(msg!=oldmsg):
		sys.stdout.write(msg)
	oldmsg=msg

def biasedFlip(probability):
	percent=int(probability*100)
	suc=[True]*percent
	fail=[False]*(100-percent)
	suc.extend(fail)
	return random.choice(suc)


def scene(state, goal):
	if(state in world):
		if(goal in world[state]):
			#printmsg("SCENE")
			#printmsg("Goal: "+goal)
			printmsg("So, I have to "+goal+". ")
			#printmsg("Goalpool: ", goalPool)
			for item in goalPool:
				if(item!=goal):
					printmsg("I also have to "+item+". ")
			#printmsg("State: "+state)
			printmsg("Right now, I'm trying to "+state+". ")
			res=biasedFlip((world[state][goal]["probability"]+successWeight)/2)
			if(res):
				#printmsg("Result: success")
				printmsg("\n\nI totally succeeded in my attempt to "+goal+" by trying to "+state+". Yay! ")
				if(goal in goalPool):
					printmsg("Now I no longer need to "+goal+". ")
					goalPool.pop(goal)
			else:
				printmsg("\n\nI failed to "+goal+" while trying to "+state+". Bummer. ")
				#printmsg("Result: failure")
			comp=[]
			if("complications" in world[state][goal]):
				found=False
				for item in world[state][goal]["complications"]:
					if biasedFlip((world[state][goal]["complications"][item]["probability"]+complicationWeight)/2):
						comp.append(item)
						if not (item in goalPool):
							printmsg("Now I have to "+ item+"")
							goalPool[item]=1
						else:
							printmsg("Now I have to "+ item+", again")
						if (found):
							printmsg(", too")
						printmsg(". ")
						found=True
				found=False
				for item in goalPool:
					if(not (item in comp)):
						printmsg("I ")
						if(found):
							printmsg("also ")
						printmsg("still need to "+item+". ")
						found=True
			#printmsg("New complications: ", comp)
			printmsg("\n\n")
			return res
	return False

def rankPathByGoal(state, goal, ttl=0):
	if(state in complicationList and (not (state in goalPool))):
		return 0
	#printmsg("Examining ranking of "+state+" -> "+goal)
	printmsg("So, I thought, what if I tried to "+goal+" by trying to "+state+"... ")
	ranking=0
	if(goal==state): 
		return 1
	if not (goal in world): return 0
	if not (state in world): return 0
	if(state in cachedRankings):
		if(goal in cachedRankings[state]):
			#printmsg("Ranking of "+state+" -> "+goal+" is "+str(cachedRankings[state][goal]))
			if(goal in goalPool and int(cachedRankings[state][goal]*10)>0):
				printmsg("I already figured that if I tried to "+goal+" by trying to "+state+" I'd only have about a "+str(int(cachedRankings[state][goal]*10))+" in 10 chance of succeeding. ")
			return cachedRankings[state][goal]
	if (goal in world[state]):
		ranking=world[state][goal]["probability"]
	if(ttl>MAX): 
		#printmsg("giving up iterating more than "+str(MAX)+" moves ahead")
		printmsg("Geez, this is complicated. I can't think more than "+str(MAX)+" moves ahead!\n\n")
		return ranking
	if(ranking<1):
		found=False
		for item in world[state]:
			if(item!=goal and item!=state):
				rpg=rankPathByGoal(item, goal, ttl+1)*world[state][item]["probability"]
				ranking+=rpg
				if(int(rpg*10)>0):
					if(found):
						printmsg("On the other hand, if I try to "+item+" it'll give me a "+str(int(rpg*10))+" in 10 chance of succeeding. ")
					else:
						printmsg("If I'm trying to "+state+", what if In order to "+goal+", I tried to "+item+". That has about a "+str(int(rpg*10))+" in 10 chance of working. ")
					found=True
		if(len(world[state])>0):
			ranking=ranking/len(world[state])
	if(goal in goalPool and int(ranking*10)>0):
		printmsg("So, I figured, if I tried to "+goal+" by trying to "+state+" I'd have maybe a "+str(int(ranking*100))+"% chance of succeding. ")
	#printmsg("Ranking of "+state+" -> "+goal+" is "+str(ranking))
	if not (state in cachedRankings):
		printmsg("I'll try to remember that. \n\n")
		cachedRankings[state]={}
	cachedRankings[state][goal]=ranking
	#printmsg(cachedRankings)
	return ranking
def rankPathByGoalPool(state):
	compositeProb={}
	for item in world[state]:
		compositeProb[item]=0
		for goal in goalPool:
			gr=rankPathByGoal(item, goal)*goalPool[goal]
			#printmsg("GoalPool rank for path "+state+" to goal "+goal+" is ",gr)
			compositeProb[item]+=gr
	return compositeProb

def chooseGoal(state):
	compositeProb=rankPathByGoalPool(state)
	poss=[]
	for item in compositeProb:
		if(int(100*compositeProb[item])>0):
			poss.extend([item]*(int(100*compositeProb[item])))
		else:
			printmsg("It turns out there's no way to "+endGoal+" by trying to "+item+" after you already tried to "+state+". \n\n")
	if(len(poss)>0):
		return random.choice(poss)
	return None

def scenes(state):
	global oldState
	printmsg("This is the story of that time I decided to try and "+endGoal+".\n\n")
	while(len(goalPool)>0 and state!=endGoal):
		goal=chooseGoal(state)
		if(goal==None):
			printmsg("\n\nThere's nothing left for me to do. I give up on trying to "+endGoal+".\n\n")
			break
		printmsg("\n\nSo, since I'm trying to "+state+" I decided to "+endGoal+" by trying to "+goal+". ")
		if(scene(state, goal)):
			stateStack.append(state)
			state=goal
		else:
			if(state==oldState and len(stateStack)>0):
				state=stateStack.pop()
			else:
				oldState=state
	printmsg("THE END")

def composeComplicationList():
	global complicationList
	for i in world:
		for j in world[i]:
			if "complications" in world[i][j]:
				for k in world[i][j]["complications"]:
					complicationList.append(k)
def init():
	composeComplicationList()
init()
scenes("go about it the obvious way")

