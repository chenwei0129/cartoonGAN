import torch
import cv2
import time
import argparse
from cartoonGAN_generator import Net
from function import function

parser = argparse.ArgumentParser(description='cartoonGAN')
parser.add_argument('--file_name', type=str, default=None,
                    help='the file to cartoonize(jpg、png、gif、mp4、None for webcam)')
parser.add_argument('--model_number', type=int, default=0,
                    help='model number to load')
parser.add_argument('--down_size', type=int, default=1,
                    help='parameter to down size')
args = parser.parse_args()

checkpoint_dir = './model_G/'

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
cartoonGAN.fuse_model()

if args.file_name == None:
  cap, capture_dir = function.webcam_prepare()
elif args.file_name[-4:] == '.mp4':
  cap = function.mp4_prepare(args.file_name)
elif args.file_name[-4:] == '.gif':
  total, duration, test_images = function.gif_prepare(args.file_name)
else:
  pass

print("\nUsing cartoonGAN to transform image to cartoon style")

if args.file_name == None:
  function.webcam_mp4_ex(args.file_name, capture_dir, cap, cartoonGAN, down_size, padding, device)
elif args.file_name[-4:] == '.mp4':
  function.webcam_mp4_ex(args.file_name, None, cap, cartoonGAN, down_size, padding, device)
elif args.file_name[-4:] == '.gif':
  function.gif_ex(args.file_name, total, duration, test_images, padding, cartoonGAN, device)
else:
  function.png_ex(args.file_name, padding, cartoonGAN, device)
