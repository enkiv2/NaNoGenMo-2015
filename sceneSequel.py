#!/usr/bin/env python

from random import Random

random=Random()

MAX=20

successWeight=10
complicationWeight=0

world={}
world["start_state"]={"get_museum_uniform":{"probability":0.5, "complications":{"get_smaller_gun": { "probability":0.9 }}}}
world["go_to_gun_store"]={"get_smaller_gun":{"probability":0.7, "complications":{"find_stolen_wallet":{ "probability":0.2}}}}
world["get_smaller_gun"]={}
world["get_museum_uniform"]={"pass_as_museum_employee":{"probability":0.3, "complications":{"heal_leg_wound":{ "probability":0.2}, "escape_museum":{ "probability": 0.7} } } }
world["pass_as_museum_employee"]={"steal_jewels":{"probability":0.7, "complications":{"heal_leg_wound":{ "probability":0.3}, "heal_arm_wound":{ "probability":0.3}, "heal_chest_wound":{ "probability":0.3}}}, "go_to_hospital":{"probability":0.9}}
world["go_to_hospital"]={"heal_leg_wound":{"probability":0.9}, "heal_arm_wound":{"probability":0.9}, "heal_chest_wound":{"probability":0.7}, "escape_museum":{"probability":0.7}}
world["heal_leg_wound"]={"go_to_hospital":{"probability":1}, "get_museum_uniform":{"probability":1}, "get_smaller_gun":{"probability":1}}
world["heal_arm_wound"]={"go_to_hospital":{"probability":1}, "get_museum_uniform":{"probability":1}, "get_smaller_gun":{"probability":1}}
world["heal_chest_wound"]={"go_to_hospital":{"probability":1}, "get_museum_uniform":{"probability":1}, "get_smaller_gun":{"probability":1}}
world["steal_jewels"]={"steal_jewels":{"probability":1, "complicaitons":{}}}
endGoal="steal_jewels"
goalPool={endGoal:1}

cachedRankings={}
stateStack=[]
oldState="None"

def biasedFlip(probability):
	percent=int(probability*100)
	suc=[True]*percent
	fail=[False]*(100-percent)
	suc.extend(fail)
	return random.choice(suc)


def scene(state, goal):
	if(state in world):
		if(goal in world[state]):
			print("SCENE")
			print("Goal: "+goal)
			print("Goalpool: ", goalPool)
			print("State: "+state)
			res=biasedFlip((world[state][goal]["probability"]+successWeight)/2)
			if(res):
				print("Result: success")
				if(goal in goalPool):
					goalPool.pop(goal)
			else:
				print("Result: failure")
			comp=[]
			if("complications" in world[state][goal]):
				for item in world[state][goal]["complications"]:
					if biasedFlip((world[state][goal]["complications"][item]["probability"]+complicationWeight)/2):
						comp.append(item)
						if not (item in goalPool):
							goalPool[item]=1
			print("New complications: ", comp)
			print("")
			return res
	return False

def rankPathByGoal(state, goal, ttl=0):
	print("Examining ranking of "+state+" -> "+goal)
	ranking=0
	if(goal==state): 
		return 1
	if not (goal in world): return 0
	if not (state in world): return 0
	if(state in cachedRankings):
		if(goal in cachedRankings[state]):
			print("Ranking of "+state+" -> "+goal+" is "+str(cachedRankings[state][goal]))
			return cachedRankings[state][goal]
	if (goal in world[state]):
		ranking=world[state][goal]["probability"]
	if(ttl>MAX): 
		print("giving up iterating more than "+str(MAX)+" moves ahead")
		return ranking
	if(ranking<1):
		for item in world[state]:
			if(item!=goal and item!=state):
				ranking+=rankPathByGoal(item, goal, ttl+1)*world[state][item]["probability"]
		if(len(world[state])>0):
			ranking=ranking/len(world[state])
	print("Ranking of "+state+" -> "+goal+" is "+str(ranking))
	if not (state in cachedRankings):
		cachedRankings[state]={}
	cachedRankings[state][goal]=ranking
	print(cachedRankings)
	return ranking
def rankPathByGoalPool(state):
	compositeProb={}
	for item in world[state]:
		compositeProb[item]=0
		for goal in goalPool:
			gr=rankPathByGoal(item, goal)*goalPool[goal]
			print("GoalPool rank for path "+state+" to goal "+goal+" is ",gr)
			compositeProb[item]+=gr
	return compositeProb

def chooseGoal(state):
	compositeProb=rankPathByGoalPool(state)
	poss=[]
	for item in compositeProb:
		if(int(100*compositeProb[item])>0):
			poss.extend([item]*(int(100*compositeProb[item])))
		else:
			print(item + " is impossible", compositeProb[item])
	if(len(poss)>0):
		return random.choice(poss)
	return None

def scenes(state):
	global oldState
	while(len(goalPool)>0):
		goal=chooseGoal(state)
		if(goal==None):
			print("No moves are possible")
			break
		if(scene(state, goal)):
			stateStack.append(state)
			state=goal
		else:
			if(state==oldState):
				state=stateStack.pop()
			else:
				oldState=state
	print("THE END")

scenes("start_state")

