#!/usr/bin/env zsh
while [[ $(wc -w < orgasmotron.md) -lt 50000 ]] ; do  ggc orgasmotron.gg | python2 >> orgasmotron.md; done
sed 's/^$/\n/g' -i orgasmotron.md 
