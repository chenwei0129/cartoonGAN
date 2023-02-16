import numpy as np
import torch
from torchvision import transforms
from torch.utils.data import DataLoader
from torchvision.datasets import ImageFolder
import matplotlib.pyplot as plt
from PIL import Image
import shutil
import os
import cv2
from torchvision import transforms
import imageio

def get_avg_fps(PIL_Image_object):
    """ Returns the average framerate of a PIL Image object """
    PIL_Image_object.seek(0)
    frames = duration = 0
    while True:
        try:
            frames += 1
            duration += PIL_Image_object.info['duration']
            PIL_Image_object.seek(PIL_Image_object.tell() + 1)
        except EOFError:
            return frames / duration * 1000
    return None

def save_cartoon_png_result(c, pngDir, output):
  image_output = output.detach().cpu().numpy()
  image_output = np.transpose(image_output, (1, 2, 0))
  num = '%03d' % c
  path_output = pngDir + str(num) + ".png"
  plt.imsave(path_output, image_output)

def gif_prepare(name):
  L = 0 - len(name)
  gifFileName = './image/' + name
  im = Image.open(gifFileName)

  gif_width  = im.size[0]
  gif_height = im.size[1]

  pngDir = "./gif2png/1/"
  shutil.rmtree(pngDir)
  os.mkdir(pngDir)
  total = 0

  try:
      while True:
        total = total + 1
        current = im.tell()
        num = '%03d' % current
        im.save(pngDir+'/'+str(num)+'.png')
        im.seek(current+1)
  except EOFError:
      pass

  print("total png = ",end="")
  print(total)
  duration = 1/get_avg_fps(im)
  print("duration  = ",end="")
  print(duration)

  print("\nconstruct cartoonGAN and pre-process image(png)")

  transformer = transforms.Compose([transforms.ToTensor()])
  test_dataset = ImageFolder('./gif2png/', transformer)
  test_dataloader = DataLoader(test_dataset, total, shuffle=False, num_workers=0)
  test_images = next(iter(test_dataloader))[0]
  return total, duration, test_images

def webcam_prepare():
  capture_dir = './capture/'
  shutil.rmtree(capture_dir)
  os.mkdir(capture_dir)
  cap = cv2.VideoCapture(0)
  return cap, capture_dir

def mp4_prepare(name):
  cap = cv2.VideoCapture('./image/'+name)
  return cap

def webcam_mp4_ex(name, capture_dir, cap, cartoonGAN, down_size, padding, device):
  v_fps = cap.get(cv2.CAP_PROP_FPS)

  video_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
  video_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
  video_width = int(video_width/down_size)
  video_height = int(video_height/down_size)

  capture_num = 0

  cartoon_result_dir = './cartoon_result/'
  shutil.rmtree(cartoon_result_dir)
  os.mkdir(cartoon_result_dir)

  fourcc = cv2.VideoWriter_fourcc(*'mp4v')
  out = cv2.VideoWriter(cartoon_result_dir+'cartoon.mp4', fourcc, float(v_fps), (video_width+4, video_height+4))
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
  
    out.write(cartoon_img_show_256)
  
    key = cv2.waitKey(1)
    if key == ord('q') and name == None:
        break
    elif key == ord('c') and name == None:
        print('save photo')
        num = '%02d' % capture_num
        capture_num = capture_num + 1
        cv2.imwrite(capture_dir+'cartoon_'+str(num)+'.png', cartoon_img_show_256)
  

  cap.release()
  out.release()
  cv2.destroyAllWindows()

def gif_ex(name, total, duration, test_images, padding, cartoonGAN, device):
  pngDir = './cartoon_png/'
  shutil.rmtree(pngDir)
  os.mkdir(pngDir)
  with torch.no_grad():
    for i in range(total):
      cartoonGAN.eval()
      img = np.transpose(test_images[i:i+1][0].detach().cpu().numpy(), (1, 2, 0))
      img = img.dot(255)
      img = img.astype(np.uint8)
      img = cv2.copyMakeBorder(img, padding, padding, padding, padding, cv2.BORDER_CONSTANT, value=(0, 0, 0))
      img = transforms.ToTensor()(img)
      img = img.unsqueeze(0)
      img = img.to(device)
      cartoonGAN.eval()
      cartoon_img = cartoonGAN(img)
      try:
          save_cartoon_png_result(i, pngDir, cartoon_img[0])
      except EOFError:
          pass

  print("\noutput gif\n")

  images = []

  filenames = os.listdir(pngDir)
  filenames.sort()

  for filename in filenames:
    img = imageio.imread(pngDir+filename)
    images.append(img)

  pngDir = "./cartoon_result/"
  shutil.rmtree(pngDir)
  os.mkdir(pngDir)

  imageio.mimsave(pngDir+"cartoon_"+name, images, duration=duration)

def png_ex(name, padding, cartoonGAN, device):
  img = cv2.imread('./image/'+name)
  img = cv2.copyMakeBorder(img, padding, padding, padding, padding, cv2.BORDER_CONSTANT, value=(0, 0, 0))
  img = transforms.ToTensor()(img)
  img = img.unsqueeze(0)
  img = img.to(device)
  with torch.no_grad():
    cartoonGAN.eval()
    cartoon_img = cartoonGAN(img)

  cartoon_img = np.transpose(cartoon_img[0].detach().cpu().numpy(), (1, 2, 0))
  cartoon_img = cartoon_img.dot(255)
  cartoon_img = cartoon_img.astype(np.uint8)
  
  pngDir = "./cartoon_result/"
  shutil.rmtree(pngDir)
  os.mkdir(pngDir)

  cv2.imwrite(pngDir+"cartoon_"+name, cartoon_img)

