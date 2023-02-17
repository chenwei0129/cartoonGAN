# cartoonGAN

# *This is the cartoonGAN[1] implement, which can cartoonize any image, even webcam(real time), to cartoon style.*

## For image(png、gif or mp4)
*ps : The gif in folder "image" is downloaded from [2]*

    Step1
    
        Put the image you want to cartoonize to the folder “image”.

    Step2
    
        Input the command.
        Python cartoonGAN.py --file_name {your image name} -–model_number {choose the appropriate model} --down_size {x for width/x and height/x}

        Ex:python cartoonGAN.py --file_name test0.jpg --model_number 0 --down_size 2

    Step3
    
        Go to the folder “cartoon_result”, there is the cartoonized image.
            .png → .png
            .gif → .gif
            .mp4 → .mp4

    Ps:There are 8 weights(0~7) in the folder "models", you need to choose the model number according to the image or environment for the better result.
       It is recommended to use number 1 or 3 (model_1.pth or model_3.pth).
    Ps:Somtimes, we need to down sample the input image due to the memory space.


## For webcam(real time)

    Step1
    
        Connect the USB webcam to your computer.

    Step2
    
        Input the command.
        Python cartoonGAN.py --model_number {choose the appropriate model} --down_size {x for width/x and height/x}

        Ex:python cartoonGAN.py --model_number 0 --down_size 1
        
    step3
    
        Key in 'q' or 'c' when running the program to exit or capture the image to .png, respectively.
        ** You can capture image again and again. **
        
    Step4
    
        Go to the folder “cartoon_result”, there is the cartoonized image.
            webcam → .mp4
        Go to the folder “capture”, there are the cartoonized images.
            webcam frame → .png

    Ps:There are 8 weights(0~7) in the folder "models", you need to choose the model number according to the image or environment for the better result.
       It is recommended to use number 1 or 3 (model_1.pth or model_3.pth).
    Ps:Somtimes, we need to down sample the input image due to the memory space.
    

## Folder
* __*capture*__  

    When you use USB webcam, you can key in 'c' to capture the image, and it will be in the folder.

* __*cartoonGAN_generator*__
    
    The architecture of cartoonGAN is in the folder.

* __*cartoon_png and gif2png/1*__
    
    When you process gif, there are some steps to finish.

        1. Transfer the input gif to many png images in to the folder "gif2png/1.
        2. Use cartonGAN to cartoonize the images in "gif2png/1", and put them in the folder "cartoon_png".
        3. Transfer the images in "cartoon_png" to a gif, and put it in "cartoon_result".

* __*cartoon_result*__
    
    For any type of input image, the result of cartoonized image(png、gif or mp4) will be in the folder.

* __*function*__
    
    All program about processing image(png, gif, mp4 and webcam) are in the folder.

* __*image*__
    
    All the input image should be there.

## reference
    [1]Chen, Y., Lai, Y.K., Liu, Y.J.: CartoonGAN: generative adversarial networks for photo cartoonization. In: Proceedings 31st Meeting of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, CVPR 2018, Salt Lake City, UT, United States, pp. 9465–9474 (2018)
    
    [2]https://bestanimations.com/Nature/Mountains/Mountains.html
