import freelancer_main as fr
import glob
import os
ddir = "/home/sfdr/Desktop/projects/Needle Pad OpenCV"
os.chdir(ddir)
fs = glob.glob("*.jpg")

for f in fs:
    r = fr.runfind(f, True)
