# Copyright 2013 Mayank Lahiri
# mlahiri@gmail.com
# Released under the BSD License
"""Applies a photo filter to an image using ImageMagick."""
from runner import Run
from os import path, unlink

def ProcessImage(filename, output_filebase, filterop, blendop, filter_id, outdim = 640, quality = 80):
  #print filename
  if output_filebase[-1:] != '/':
    output_filebase += '/'
  basename = path.basename(filename)
  basename = basename.replace('.orig.jpg', '')
  #while basename[-4:] == '.jpg' or basename[-4:] == '.png':
    #basename = basename[:-4]  
    
  # Generate the FX layer as a lossless PNG
  fx_file = ''.join((output_filebase,
                     'fx-',
                     str(filter_id),
                     '-',
                     basename,
                     '.png'))
  if 0 != Run(('convert',
               filename,
               filterop,
               fx_file)):
    return None
  
  # Combine the FX layer with the original image
  #out_file = ''.join((output_filebase,
                      #'img-',
                      #str(filter_id),
                      #'-',
                      #basename,
                      #'.jpg'))
  out_file = output_filebase + basename + "." + str(filter_id) + ".maxstagram.jpg"
  #out_file = output_filebase + "." + basename + "." + str(filter_id)
  if 0 != Run(('convert',
               fx_file,
               filename,
               blendop,
               '-resize ' + str(outdim) + 'x' + str(outdim),
               '-normalize',
               '-quality ' + str(quality),
               out_file)):
    return None

  unlink(fx_file)
  return out_file

