#!/usr/bin/env python

from random import Random
import sys

random=Random()

MAX=5

successWeight=0.1
complicationWeight=0.7

world={}
world["go about it the obvious way"]={"get a museum uniform":{"probability":0.5, "complications":{"get a smaller gun": { "probability":0.9 }}}, "go to the ninja supply store":{"probability":1}, "go to the gun store":{"probability":1}}
world["go to gun store"]={"get a smaller gun":{"probability":0.7, "complications":{"find my stolen wallet":{ "probability":0.2}, "success_descr":["The gun store carried an antique gun intended for defending women on bicycles against dogs in the late nineteenth century. ", "The gun store carried a half-scale airsoft dart gun version of a Walther PPK, and poison darts. "]}, "descr":["The gun store was a tiny brick building by the side of the highway, in the bad part of town. "], "success_descr":["The owner glared at me, and then at my ID, and then back at me. Then he grunted, accepted my cash, and handed me the new gun. "], "failure_descr":["After banging on the locked door for ten minutes, I noticed a tiny sign at the lower left hand corner of the window embedded in the door. It had hours. It turns out, this store is closed on Tuesdays. "]}, "goal_reqs":{"or":["get a smaller gun"]}}
world["get a smaller gun"]={"go to gun store":{"probability":1}, "go about it the obvious way":{"probability":1}, "pass as a museum employee":{"probability":0.3}}
world["get a museum uniform"]={"pass as a museum employee":{"probability":0.3, "complications":{"heal my leg wound":{ "probability":0.2}, "escape the museum":{ "probability": 0.7} } }, "descr":["The costume shop was tucked into a strip mall down town, between a laundromat and a chinese take-out place. It smelled like soap. "], "success_descr":["There was a perfect museum employee uniform sitting on the rack to the left of the entrance. "], "failure_descr":["After looking through the racks several times, I finally decided to ask the cashier -- a wrinkled but plump old woman with a puff of curly white hair -- if she carried museum employee uniforms. She shook her head, and I left, dejected. "]}
world["pass as a museum employee"]={"steal them jewels":{"probability":0.7, "complications":{"heal my leg wound":{ "probability":0.3}, "heal my arm wound":{ "probability":0.3}, "heal my chest wound":{ "probability":0.3}}}, "go to the hospital":{"probability":0.9}, "reqs":{"or":["get a museum uniform"]}}
world["go to the ninja supply store"]={"get a smaller gun":{"probability":0.4, "success_descr":["In the glass display case, there was a poison dart gun that looked like a fountain pen. I bought six! "], "failure_descr":["The cashier claimed that they had a moral aversion to projectile weapons, and thus did not carry them. "]}, "purchase a black leather catsuit":{"probability":0.7, "success_descr":["A beautiful black leather catsuit greeted me from the rack to the left of the doorway. "], "failure_descr":["All the black leather catsuits they had in stock were sized for literal cats. ", "All the black leather cat suits they had in stock were way too big for me. ", "All their black leather catsuits were covered in shiny chrome studs and buckles, and wouldn't help me disappear into the night at all. "]}, "purchase a grappling hook":{"probability":0.7, "success_descr":["There was a grappling hook with two hundred feet of rope sitting right behind the counter, on display. ", "I spent twenty minutes looking through the discount bin, before finding an absolutely perfect grappling hook for thirty cents. When I went up to pay for it, the cashier waved me off -- no charge. "],"failure_descr":["\"Are there any grappling hooks in stock?\" The cashier, impassive behind his mask, shook his head slowly in response to my question. Then, after a moment of staring at me, he threw a smoke bomb at his feet. I found myself outside the shop, which was now locked. "]}, "descr":["The ninja supply shop was in the middle of the second floor of the mall, between a Hot Topic and a Zappo's. It was dimly lit, and the scuffed floors had a fake tatami-pattern print. There was a wad of gum stuck to the doorway. "], "failure_descr":["The shutter was shut, and a great big lock hung from the side of it. ", "The door was shut and locked, and a sign said \"Back at 2:00\". It was four. I waited until six. "],"success_descr":["As I entered, a machine emitted a little beep to indicate that customers were about. The cashier appeared out of a plume of smoke behind the counter. "]}
world["purchase a black leather catsuit"]={"sneak into the museum at night":{"probability":0.8}, "go to the ninja supply store":{"probability":1}}
world["purchase a grappling hook"]={"sneak into the museum at night":{"probability":0.9}, "go to the ninja supply store":{"probability":1}}
world["sneak into the museum at night"]={"steal them jewels":{"probability":0.8, "complications":{"heal my leg wound":{"probability":0.3},"heal my arm wound":{ "probability":0.3}, "heal my chest wound":{ "probability":0.3}}}, "go to the hospital":{"probability":0.9}, "reqs":{"or":["purchase a black leather catsuit", "purchase a grappling hook"]}}
world["go to the hospital"]={"heal my leg wound":{"probability":0.9}, "heal my arm wound":{"probability":0.9}, "heal my chest wound":{"probability":0.7}, "escape the museum":{"probability":0.7},"goal_reqs":{"or":["heal my leg wound", "heal my arm wound", "heal my chest wound"]}}
world["heal my leg wound"]={"go to the hospital":{"probability":1}, "get a museum uniform":{"probability":1}, "get a smaller gun":{"probability":1}, "go to the ninja supply store":{"probability":1}}
world["heal my arm wound"]={"go to the hospital":{"probability":1}, "get a museum uniform":{"probability":1}, "get a smaller gun":{"probability":1}, "go to the ninja supply store":{"probability":1}}
world["heal my chest wound"]={"go to the hospital":{"probability":1}, "get a museum uniform":{"probability":1}, "get a smaller gun":{"probability":1}, "go to the ninja supply store":{"probability":1}}
world["steal them jewels"]={"steal them jewels":{"probability":1, "complications":{}}}

endGoal="steal them jewels"


goalPool={endGoal:1}
complicationList=[]
completed=[]

cachedRankings={}
stateStack=[]
oldState="None"

blacklist=["descr", "success_descr", "failure_descr", "reqs", "goal_reqs"]

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
			#printmsg("So, I have to "+goal+". ")
			#printmsg("Goalpool: ", goalPool)
			for item in goalPool:
				if(item!=goal):
					printmsg("I also have to "+item+". ")
			#printmsg("State: "+state)
			#printmsg("Right now, I'm trying to "+state+". ")
			if("descr" in world[state][goal]):
				printmsg(random.choice(world[state][goal]["descr"]))
			res=biasedFlip((world[state][goal]["probability"]+successWeight)/2)
			if("reqs" in world[goal]):
				if "and" in world[goal]["reqs"]:
					tmp=True
					for item in world[goal]["reqs"]["and"]:
						if(not item in completed):
							printmsg("I failed to "+goal+" because I need to "+item+" first. ")
							tmp=False
					if(not tmp):
						res=False
				if "or" in world[goal]["reqs"]:
					tmp=False
					for item in world[goal]["reqs"]["or"]:
						if(item in completed):
							tmp=True
					if(not tmp):
						printmsg("I failed to "+goal+" because I need to "+(" or ".join(world[goal]["reqs"]["or"]))+" first.")
						res=False
			if(res):
				#printmsg("Result: success")
				if("success_descr" in world[state][goal]):
					printmsg(random.choice(world[state][goal]["success_descr"]))
				elif("success_descr" in world[goal]):
					printmsg(random.choice(world[goal]["success_descr"]))
				else:
					printmsg("\n\nI totally succeeded in my attempt to "+goal+" by trying to "+state+". Yay! ")
				if(goal in goalPool):
					printmsg("Now I no longer need to "+goal+". ")
					goalPool.pop(goal)
				if(not (goal in completed)):
					completed.append(goal)
			else:
				if("failure_descr" in world[state][goal]):
					printmsg(random.choice(world[state][goal]["failure_descr"]))
				elif("failure_descr" in world[goal]):
					printmsg(random.choice(world[goal]["failure_descr"]))
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
	if (state in blacklist):
		return 0
	#printmsg("Examining ranking of "+state+" -> "+goal)
	ranking=0
	if(goal==state): 
		return 1
	if not (goal in world): return 0
	if not (state in world): return 0
	if "goal_reqs" in world[state]:
		if "and" in world[state]["goal_reqs"]:
			tmp=True
			for item in world[state]["goal_reqs"]:
				tmp2=False
				for item2 in goalPool:
					if(item==item2):
						tmp2=True
				if(not tmp2 or not tmp):
					tmp=False
			if(not tmp):
				return 0
		if "or" in world[state]["goal_reqs"]:
			tmp=False
			for item in world[state]["goal_reqs"]:
				for item2 in goalPool:
					if(item==item2):
						tmp=True
			if(not tmp):
				return 0
	printmsg("So, I thought, what if I tried to "+goal+" by trying to "+state+"... ")
	if(state in cachedRankings):
		if(goal in cachedRankings[state]):
			#printmsg("Ranking of "+state+" -> "+goal+" is "+str(cachedRankings[state][goal]))
			if(goal in goalPool and int(cachedRankings[state][goal]*10)>0):
				printmsg("I already figured that if I tried to "+goal+" by trying to "+state+" I'd only have about a "+str(int(cachedRankings[state][goal]*10))+" in 10 chance of succeeding. ")
			return cachedRankings[state][goal]
	if (goal in world[state]):
		if("probability" in world[state][goal]):
			ranking=world[state][goal]["probability"]
		else:
			return 0
	if(ttl>MAX): 
		#printmsg("giving up iterating more than "+str(MAX)+" moves ahead")
		printmsg("Geez, this is complicated. I can't think more than "+str(MAX)+" moves ahead!\n\n")
		return ranking
	if(ranking<1):
		found=False
		for item in world[state]:
			if(item!=goal and item!=state):
				if("probability" in world[state][item] and item not in blacklist):
					rpg=rankPathByGoal(item, goal, ttl+1)*world[state][item]["probability"]
					ranking+=rpg
					if(int(rpg*10)>0):
						if(found):
							printmsg("On the other hand, if I try to "+item+" it'll give me a "+str(int(rpg*10))+" in 10 chance of succeeding. ")
						else:
							printmsg("If I'm trying to "+state+", what if in order to "+goal+", I tried to "+item+". That has about a "+str(int(rpg*10))+" in 10 chance of working. ")
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
	if(state in world):
		for item in world[state]:
			if(item not in blacklist):
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
		#printmsg("\n\nSo, since I'm trying to "+state+" I decided to "+endGoal+" by trying to "+goal+". ")
		if("descr" in world[goal]):
			printmsg(random.choice(world[goal]["descr"]))
		if(scene(state, goal)):
			stateStack.append(state)
			state=goal
		else:
			if(state==oldState and len(stateStack)>0):
				state=stateStack.pop()
			else:
				oldState=state
	printmsg("THE END\n\n")

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

