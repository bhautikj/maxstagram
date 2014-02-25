#!/usr/bin/env python
# Copyright 2013 Mayank Lahiri
# mlahiri@gmail.com
# Released under the BSD License
"""Generates a series of random photo filters and processes 
   a set of photos with them, generating nice output in output/index.html.
"""
from random import uniform
from sys import argv
from gen_operator import GenOperator, GenLayeredOperator, GenBlend
from image_processor import ProcessImage
from runner import Run, GetTimer, ResetTimer
from html_index_writer import StartHTML, WriteHTML, EndHTML
import os
import glob,json


def main(argv):
  if len(argv) < 1:
    print 'Usage: GenerateFilters.py <one or more image files>'
    exit(1)

  # Check for ImageMagick in the path
  if 0 != Run('convert'):
    print 'ImageMagick\'s "convert" does not seem to be in your path.'
    print 'In Debian/Ubuntu, type: sudo apt-get install imagemagick'
    exit(1)

  # Create output directory and empty it out
  try:
    if not os.path.exists('output'):
      os.mkdir('output')
    #if not os.path.isdir('output'):
      #print 'You already have a file called "output" in the current directory.'
      #print 'Delete it. Now.'
      #exit(1)
    #for fname in os.listdir('output'):
      #os.remove('output/' + fname)
  except:
    print 'Could not empty out the "output" directory. Do it yourself.'
    exit(1)

  # Generate resized square source images from files specified on command line
  # Use lossless PNG as the intermediate file format
  
  print argv
  infile = argv[0]
  outfile = 'output/' + os.path.basename(infile).replace('.jpg', '') + '.640.orig.jpg'

                #'-thumbnail 640x640^',
                #'-extent 640x640',
  
  if 0 != Run(('convert',
                '"' + infile + '"',
                '-auto-level',
                '-auto-orient',
                '-gravity center',
                '-quality 98',
                '-resize "640>"',
                outfile)):
    print 'Cannot resize', infile, 'to save to', outfile
    exit(1)
    
  print 'INPUT:', infile, '=>', outfile
  print outfile

  numRuns = int(argv[1])
  

  ## Generate filters
  for filter_idx in range(0, numRuns):
    ## Increasing the number of operators allows for more complex filters at
    ## the cost of increased computational requirements.
    num_operators = int(uniform(1, 20))
    filterop = GenOperator(num_operators)
    blendop = GenBlend()
    print '''
#=================================================================
#FILTER: {filterop}
#BLEND:  {blendop}
#=================================================================
#'''.format(**locals())
    
    ## Process each input file with the filter
    #ResetTimer()
    def runner(fn): return ProcessImage(fn, 'output/', filterop, blendop, filter_idx, 640)
    runner(outfile)

  os.system('cp ' + infile + ' output/')
  # TODO: FIX GLOB!
  fl = glob.glob("output/"+os.path.basename(infile).replace('.jpg', '')+"*")
  dct = { "orig" : os.path.basename(infile) }
  compset = []
  for fn in fl:
    compset.append(os.path.basename(fn))
  dct["testset"] = compset
  
  f = open('output/' + os.path.basename(infile) + ".json", 'w')
  f.write(json.dumps(dct))
  f.close()

if __name__ == '__main__':
  main(argv[1:])
