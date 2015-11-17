#!/usr/bin/env zsh
article=0
touch pkdpitches.md
echo "# PKD Pitches For Screenwriters, Volume 1\n\n" > pkdpitches.md
echo "## Introduction\n\n" >> pkdpitches.md
echo "* Because the works of Phillip K. Dick are popular with screenwriters for a source of pitches but are rarely properly adapted beyond the pitch level, here is a list of film pitches based on the works of Phillip K. Dick, without the pesky story in the way. * \n\n" >> pkdpitches.md
while [[ $(wc -w < pkdpitches.md) -lt 50000 ]] ; do  
	article=$((article+1))
	echo -e "\n\n== Pitch #$article ==\n\n">> pkdpitches.md
	ggc pkdpitches.gg | python >> pkdpitches.md
done
