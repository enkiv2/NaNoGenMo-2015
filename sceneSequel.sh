#!/usr/bin/env zsh
heist=0
touch badHeists.md
while [[ $(wc -w < badHeists.md) -lt 50000 ]] ; do  
	heist=$((heist+1))
	echo -e "== Heist #$heist ==\n\n">> badHeists.md
	./sceneSequel.py >> badHeists.md
done
