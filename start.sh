#! /usr/bin/env sh

set -e

echo "
            dddddddd                                    bbbbbbbb
            d::::::d                                    b::::::b                                      tttt
            d::::::d                                    b::::::b                                   ttt:::t
            d::::::d                                    b::::::b                                   t:::::t
            d:::::d                                      b:::::b                                   t:::::t
    ddddddddd:::::d   aaaaaaaaaaaaa     ggggggggg   gggggb:::::bbbbbbbbb       ooooooooooo   ttttttt:::::ttttttt
  dd::::::::::::::d   a::::::::::::a   g:::::::::ggg::::gb::::::::::::::bb   oo:::::::::::oo t:::::::::::::::::t
 d::::::::::::::::d   aaaaaaaaa:::::a g:::::::::::::::::gb::::::::::::::::b o:::::::::::::::ot:::::::::::::::::t
d:::::::ddddd:::::d            a::::ag::::::ggggg::::::ggb:::::bbbbb:::::::bo:::::ooooo:::::otttttt:::::::tttttt
d::::::d    d:::::d     aaaaaaa:::::ag:::::g     g:::::g b:::::b    b::::::bo::::o     o::::o      t:::::t
d:::::d     d:::::d   aa::::::::::::ag:::::g     g:::::g b:::::b     b:::::bo::::o     o::::o      t:::::t
d:::::d     d:::::d  a::::aaaa::::::ag:::::g     g:::::g b:::::b     b:::::bo::::o     o::::o      t:::::t
d:::::d     d:::::d a::::a    a:::::ag::::::g    g:::::g b:::::b     b:::::bo::::o     o::::o      t:::::t    tttttt
d::::::ddddd::::::dda::::a    a:::::ag:::::::ggggg:::::g b:::::bbbbbb::::::bo:::::ooooo:::::o      t::::::tttt:::::t
 d:::::::::::::::::da:::::aaaa::::::a g::::::::::::::::g b::::::::::::::::b o:::::::::::::::o      tt::::::::::::::t
  d:::::::::ddd::::d a::::::::::aa:::a gg::::::::::::::g b:::::::::::::::b   oo:::::::::::oo         tt:::::::::::tt
   ddddddddd   ddddd  aaaaaaaaaa  aaaa   gggggggg::::::g bbbbbbbbbbbbbbbb      ooooooooooo             ttttttttttt
                                                 g:::::g
                                     gggggg      g:::::g
                                     g:::::gg   gg:::::g
                                      g::::::ggg:::::::g
                                       gg:::::::::::::g
                                         ggg::::::ggg
                                            gggggg             "

echo "Starting Dagbot"


FILE=/configuration.yml
if  [ -z "$token" ]; then
      if test -f "$FILE"; then
          echo "$FILE exists."
      else
          echo "No env vars or configuration.yml found. Exiting"
          exit 1
      fi
else
      echo "Generating Config.yml from enviroment vraibles"
      python3 gen-config.py
      cat configuration.yml
      echo "Generated Config"

fi

exec python3 -m dagbot

echo "App Was exited"



