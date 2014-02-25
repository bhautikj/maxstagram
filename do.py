import glob, os, sys

flu = glob.glob('*.JPG')
fll = glob.glob('*.jpg')

fl = fll + flu

mc = int(sys.argv[1])
mt = int(sys.argv[2])

for i, fn in enumerate(fl):
  if i % mt == mc:
    os.system ('python2.7 GenerateN.py ' + fn + ' 100')
