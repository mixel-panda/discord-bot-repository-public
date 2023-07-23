#!/bin/bash
output=$(/opt/games/7days/listplayers.sh);
number=$(echo "$output" | grep "in the game" | grep -Eo "[0-9]{1,4}");
if [ "$number" -eq "0" ]; then
  shutdown -h now;
fi;