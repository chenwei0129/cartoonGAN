import torch
import torch.nn as nn
import torch.nn.functional as F
from torch import sigmoid

class ConvBNReLU(nn.Sequential):
    def __init__(self, in_planes, out_planes, kernel_size=3, stride=1, padding=0):
        super(ConvBNReLU, self).__init__(
          nn.Conv2d(in_planes, out_planes, kernel_size, stride, padding),
          nn.BatchNorm2d(out_planes),
          nn.ReLU())

class TransConvBNReLU(nn.Sequential):
    def __init__(self, in_planes, out_planes, kernel_size=3, stride=1, padding=0):
        super(TransConvBNReLU, self).__init__(
          nn.Conv2d(in_planes, out_planes, kernel_size, stride, padding),
          nn.BatchNorm2d(out_planes),
          nn.ReLU())

class ConvBN(nn.Sequential):
    def __init__(self, in_planes, out_planes, kernel_size=3, stride=1, padding=0):
        super(ConvBN, self).__init__(
          nn.Conv2d(in_planes, out_planes, kernel_size, stride, padding),
          nn.BatchNorm2d(out_planes))

class ResidualBlock(nn.Module):
  def __init__(self):
    super(ResidualBlock, self).__init__()
    self.ConvBNReLU1 = ConvBNReLU(in_planes=256, out_planes=256, kernel_size=3, stride=1, padding=1)
    self.ConvBN1     = ConvBN    (in_planes=256, out_planes=256, kernel_size=3, stride=1, padding=1)
    self.myop = nn.quantized.FloatFunctional()
  def forward(self, x):
    output = self.ConvBN1(self.ConvBNReLU1(x))
    output = self.myop.add(output, x)
    return output

class Generator(nn.Module):
    def __init__(self):
      super(Generator, self).__init__()
      self.quant = torch.quantization.QuantStub()
      self.ConvBNReLU1 = ConvBNReLU(in_planes=3, out_planes=64, kernel_size=7, stride=1, padding=3)
      
      # down-convolution #
      self.conv_2 = nn.Conv2d(in_channels=64, out_channels=128, kernel_size=3, stride=2, padding=1)
      self.ConvBNReLU2 = ConvBNReLU(in_planes=128, out_planes=128, kernel_size=3, stride=1, padding=1)
      
      self.conv_4 = nn.Conv2d(in_channels=128, out_channels=256, kernel_size=3, stride=2, padding=1)
      self.ConvBNReLU3 = ConvBNReLU(in_planes=256, out_planes=256, kernel_size=3, stride=1, padding=1)
      
      # residual blocks #
      residualBlocks = []
      for l in range(8):
        residualBlocks.append(ResidualBlock())
      self.res = nn.Sequential(*residualBlocks)
      
      # up-convolution #
      self.conv_6 = nn.ConvTranspose2d(in_channels=256, out_channels=128, kernel_size=3, stride=2, padding=1, output_padding=1)
      self.TransConvBNReLU1 = TransConvBNReLU(in_planes=128, out_planes=128, kernel_size=3, stride=1, padding=1)

      self.conv_8 = nn.ConvTranspose2d(in_channels=128, out_channels=64, kernel_size=3, stride=2, padding=1, output_padding=1)
      self.TransConvBNReLU2 = TransConvBNReLU(in_planes=64, out_planes=64, kernel_size=3, stride=1, padding=1)
      
      self.conv_10 = nn.Conv2d(in_channels=64, out_channels=3, kernel_size=7, stride=1, padding=3)
      self.dequant = torch.quantization.DeQuantStub()

    def forward(self, x):
      x = self.quant(x)
      x = self.ConvBNReLU1(x)
      
      x = self.ConvBNReLU2(self.conv_2(x))
      x = self.ConvBNReLU3(self.conv_4(x))
      
      x = self.res(x)
      x = self.TransConvBNReLU1(self.conv_6(x))
      x = self.TransConvBNReLU2(self.conv_8(x))

      x = self.conv_10(x)

      x = sigmoid(x)
      x = self.dequant(x)

      return x
    
    def fuse_model(self):
        for m in self.modules():
            if type(m) == ConvBNReLU:
                torch.quantization.fuse_modules(m, ['0', '1', '2'], inplace=True) #conv + bn + relu
            if type(m) == ConvBN:
                torch.quantization.fuse_modules(m, ['0', '1'], inplace=True) #conv + bn + relu
            if type(m) == TransConvBNReLU:
                torch.quantization.fuse_modules(m, ['0', '1', '2'], inplace=True) #conv + bn + relu

