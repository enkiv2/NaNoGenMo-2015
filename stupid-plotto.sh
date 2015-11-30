#!/usr/bin/env zsh
touch stupid-plotto.md
echo "# Stupid Plotto\n\n## Introduction\n\nStupid Plotto is a collection of plotto-generated stories expanded as stupidly as possible. Names are substituted randomly. Footnotes and plotto-specific notation are stripped. Style is introduced using gnu talkfilters.\n\n##Stories\n\n" >> stupid-plotto.md
count=0
while [[ $(wc -w < stupid-plotto.md) -lt 50000 ]] ; do
	count=$((count+1))
	echo "### Story #$count" >> stupid-plotto.md
	./plotto.sh >> stupid-plotto.md
done

