#!/usr/bin/env zsh

python2 ./expand-filter.py >| expanded.md
while [[ $(wc -w < expanded.txt) -lt 50000 ]] ; do if [[ $(wc -l < expanded.txt) -gt 0 ]] ; then mv expanded{,_old}.md ; fi ; cat expanded_old.md | fmt | python2 ./expand-filter.py | fmt > expanded.md ; echo -e ".\c" ; done

sed 's/^$/\n/g' -i expanded.md
