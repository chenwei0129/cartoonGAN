# cartoonGAN

This is the cartoonGAN[1] implement, which can cartoonize any image, even webcam(real time), to cartoon style.



For image(png、gif or mp4)

    Step1
    Put the image you want to cartoonize to the folder “image”.

    Step2
    Input the command.
    Python cartoonGAN.py --file_name {your image name} -–model_number {choose the appropriate model} --down_size {x for width/x and height/x}

    Ex:python cartoonGAN.py --file_name test0.jpg --model_number 0 --down_size 2

    Ps:There are 8 weights(0~7) in the folder "models", you need to choose the model number according to the image or environment for the better result.
    Ps:Somtimes, we need to down sample the input image due to the memory space.

    Step3
    Go to the folder “cartoon_result”, there is the cartoonized image.
    .png → .png
    .gif → .gif
    .mp4 → .gif


For webcam(real time)

    Step1
    Connect the USB webcam to your computer.

    Step2
    Input the command.
    Python cartoonGAN.py --model_number {choose the appropriate model} --down_size {x for width/x and height/x}

    Ex:python cartoonGAN.py --model_number 0 --down_size 1

    Ps:There are 8 weights(0~7) in the folder "models", you need to choose the model number according to the image or environment for the better result.
    Ps:Somtimes, we need to down sample the input image due to the memory space.
    
    **You can key in 'q' or 'c' when running the program to exit or capture the image to .png, respectively.**
    **You can capture image again and again.**

    Step3
    Go to the folder “cartoon_result”, there is the cartoonized image.
    webcam → .gif
    Go to the folder “capture”, there are the cartoonized images.
    webcam frame → .png


Folder "capture"

    When you use USB webcam, you can key in 'c' to capture the image, and it will be in the folder.

Folder "cartoonGAN_generator"

    The architecture of cartoonGAN is in the folder.

Folder "cartoon_png" and "gif2png/1"

    When you process gif, there are some steps to finish.
    
    Step1
    
        Transfer the input gif to many png images in the folder "gif2png/1.
    
    Step2
    
        Use cartonGAN to cartoonize the images in "gif2png/1", and put them in the folder "cartoon_png".
    
    Step3
    
        Transfer the images in "cartoon_png" to a gif, and put it in "cartoon_result".

Folder "cartoon_result"

    For any type of input image, the result of cartoonized image(.png or .gif) will be in the folder.

Folder "function"

    All program about processing image(png, gif, mp4 and webcam) are in the folder.

Folder "image"

    All the input image should be there.

reference

    [1]Chen, Y., Lai, Y.K., Liu, Y.J.: CartoonGAN: generative adversarial networks for photo cartoonization. In: Proceedings 31st Meeting of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, CVPR 2018, Salt Lake City, UT, United States, pp. 9465–9474 (2018)
