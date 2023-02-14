import torch
from torchvision import transforms
import torch.nn as nn
import torch.nn.functional as F
from torch import sigmoid
import cv2
import time
import numpy as np
import sys
import shutil
import os
import imageio
import argparse
from cartoonGAN_generator import Net

parser = argparse.ArgumentParser(description='cartoonGAN')
parser.add_argument('--file_name', type=str, default=None,
                    help='the file to cartoonize(jpg、png、gif、mp4、None for webcam)')
parser.add_argument('--model_number', type=int, default=0,
                    help='model number to load')
parser.add_argument('--down_size', type=int, default=1,
                    help='parameter to down size')
args = parser.parse_args()

checkpoint_dir = './models/'

down_size = args.down_size

padding = 1

device = torch.device('cpu')

if torch.cuda.is_available():
  device = torch.device('cuda')
  print("GPU available")
else:
  print("No cuda available")

checkpoint = torch.load(checkpoint_dir+'model_'+str(args.model_number)+'.pth', map_location=torch.device(device))
cartoonGAN = Net.Generator()
cartoonGAN.to(device)
cartoonGAN.load_state_dict(checkpoint['g_state_dict'])

cartoonGAN.eval()

print("\nUsing cartoonGAN to transform image to cartoon style")

#########################################################################
##                                                                     ##
##                        process mp4 or webcam                        ##
##                                                                     ##
#########################################################################
c = 0
if args.file_name[-4:] == '.mp4':
  cap = cv2.VideoCapture('./test_video/'+mp4_file_name)
else:
  capture_dir = './capture/'
  shutil.rmtree(capture_dir)
  os.mkdir(capture_dir)
  cap = cv2.VideoCapture(0)

v_fps = cap.get(cv2.CAP_PROP_FPS)

video_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
video_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
video_width = int(video_width/down_size)
video_height = int(video_height/down_size)

cartoon_list = []

while(True):
  ret, frame = cap.read()
  
  if frame is None:
    break
  
  img_real = cv2.resize(frame, (video_width, video_height))
  img_pad = cv2.copyMakeBorder(img_real, padding, padding, padding, padding, cv2.BORDER_CONSTANT, value=(0, 0, 0))
  img = transforms.ToTensor()(img_pad)
  img = img.unsqueeze(0)
  img = img.to(device)

  with torch.no_grad():
    cartoonGAN.eval()
    cartoon_img = cartoonGAN(img)
  
  cartoon_img_show = np.transpose(cartoon_img[0].detach().cpu().numpy(), (1, 2, 0))
  cartoon_img_show_256 = cartoon_img_show.dot(255)
  cartoon_img_show_256 = cartoon_img_show_256.astype(np.uint8)
  
  cv2.imshow('frame', cartoon_img_show_256)
  
  cartoon_img_show_256_RGB = cv2.cvtColor(cartoon_img_show_256, cv2.COLOR_BGR2RGB)
  cartoon_list.append(cartoon_img_show_256_RGB)
  
  key = cv2.waitKey(1)
  if key == ord('q') and args.file_name == None:
      exit()
  elif key == ord('c') and args.file_name == None:
      print('save photo')
      num = '%02d' % c
      c = c + 1
      cv2.imwrite(capture_dir+'cartoon_'+str(num)+'.png', cartoon_img_show_256)
  

cap.release()
cv2.destroyAllWindows()

print("\noutput gif")
cartoon_result_dir = './cartoon_result/'
shutil.rmtree(cartoon_result_dir)
os.mkdir(cartoon_result_dir)
imageio.mimsave(cartoon_result_dir+'cartoon.gif', cartoon_list, fps=v_fps)
