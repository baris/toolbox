mencoder -quiet "$1" -oac mp3lame -lameopts abr:br=64 -ovc lavc -lavcopts vcodec=mpeg4:vbitrate=300 -vf scale=352:208 -ffourcc DIVX -ofps 15000/1001 -o "$2";
