#!/bin/bash
source_lady="JulianaMU0"
source_ext=".png"
target_lady="Murka"
target_ext=**.mp4
output_dir="/Users/cyan/MEGA/DF/Output/$source_lady-$target_lady"
mkdir "$output_dir"
for target in /Users/cyan/MEGA/DF/Input/"${target_lady}"/${target_ext}
do
    echo processing "${target}"
    python run.py --execution-provider coreml --headless -s "/Users/cyan/MEGA/DF/Face/${source_lady}${source_ext}" -o "$output_dir" -t "${target}";
done
