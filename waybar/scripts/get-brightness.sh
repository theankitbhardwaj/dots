#!/usr/bin/env zsh
brightnessctl info | grep -oP "(?<=\()\d+(?=%)" | cat
