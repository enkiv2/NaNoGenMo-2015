#!/usr/bin/env zsh
while [[ $(wc -w < xkcd-1609.md) -lt 50000 ]] ; do  ggc xkcd-1609.gg | python2 >> xkcd-1609.md; done
sed 's/$/\n/g' -i xkcd-1609.md 
