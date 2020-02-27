# sh.x dumper for bash, version 1.0

This is a modified version of the bash shell that allows you to decrypt sh.x (shc compiled) scripts. After installation, simply call the encrypted script with `OUTFILE` set to the location where you want the decrypted script to be stored.

## Usage
`OUTFILE=./decrypted.sh ./encrypted.sh.x`

## Compilation
`./configure`

`make -j$(nproc) || make`

## Installation
`sudo mv /bin/bash /bin/bash.bak && sudo cp ./bash /bin/bash`

## Uninstallation
`sudo rm /bin/bash`

`sudo mv /bin/bash.bak /bin/bash`

`sudo chmod a+x /bin/bash`

## Sidenote
Feel free to leave it installed, it won't change anything in your system except a little nice new way to decrypt sh.x scripts!
