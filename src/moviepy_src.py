print('Creating animation')

import glob
import moviepy.editor as mpy

gif_name = system
fps = frate
file_list = sorted(glob.glob(system+'/*.png')) # Get all the pngs in the current directory
clip = mpy.ImageSequenceClip(file_list, fps=1./fps)
#clip = clip.resize(height=360)
clip.write_gif(system+'/'+system+'.gif')
clip.write_videofile(system+'/'+system+'.mp4')

print('Your animation is ready in '+system+'/'+system+'.gif')
