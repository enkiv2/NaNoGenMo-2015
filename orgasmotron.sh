#!/usr/bin/env zsh
while [[ $(wc -w < orgasmotron.txt) -lt 50000 ]] ; do  ggc orgasmotron.gg | python2 >> orgasmotron.txt; done
