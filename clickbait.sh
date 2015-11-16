#!/usr/bin/env zsh
article=0
touch clickbait.md
while [[ $(wc -w < clickbait.md) -lt 50000 ]] ; do  
	article=$((article+1))
	echo -e "== Article #$article ==\n\n">> clickbait.md
	ggc clickbait.gg | python >> clickbait.md
done
