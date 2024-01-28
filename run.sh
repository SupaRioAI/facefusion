#!/bin/bash
for target in `ls /Users/cyan/MEGA/DF/Input/SigalAcon/**.mp4`
do
    echo "processing $target"
    python app.py --execution-provider coreml --headless -s "/Users/cyan/MEGA/DF/Face/JulianaMU0.png" -o "/Users/cyan/MEGA/DF/Output/JulianaMU0-SigalAcon" -t $target;
done
