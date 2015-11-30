#!/usr/bin/env zsh

availableFilters="austro\nbrooklyn\nchef\ncockney\ndrawl\nfudd\njethro\njive\nkraut\npansy\npirate\nredneck\nvalspeak\nwarez"
function rfilt() {
	$(echo -e $availableFilters | shuf -n 1)
}

(
	echo "#include names.gg"
	(fortune plotto | # tee /dev/stderr | 
		grep '[A-Za-z]' | 
		tr '\n' '\a' | tr '\r' '\a'| 
		sed 's/ *([^)]*) *//g;s/"/\\\"/g;s/,/\\\,/g' | 
		
		sed 's/\([ABS]-*[N0-9]*[ ,.\\]\)/$$\1/g;s/\(\$\$[AB]\)-\([0-9]\)/\1_\2/g;'
		echo) | 
		(
			ax=""
			while read -r x ; do 
				echo "$x" | 
					sed 's/\(\$\$[A-Za-z0-9_][A-Za-z0-9_]*\)/\n\1\n/g' | grep '\$' | sed 's/^\$\$//;s/$/:=$fullName/' 
				ax="$ax $x"
			done 
			echo "A00:=$ax"
		) | sort | uniq 
	echo
) | ggc | python2 | sed 's/ \\ / /g;s/\\ *$//;s/\*//g;s/^ [ \\,\t]*//;s/[\a ]*-[\a ]*//;s/\\ /\n/g;s/\a/\n/g' | rfilt
