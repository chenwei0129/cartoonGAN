# cartoonGAN

This is the cartoonGAN[1] implement, which can cartoonize any image, even webcam(real time), to cartoon style.



For image(.png, .gif or .mp4)

    Step1
    Put the image you want to cartoonize to the folder “image”.

    Step2
    Input the command.
    Python cartoonGAN.py --file_name {your image name} -–model_number {choose the appropriate model} --down_size {x for width/x and height/x}

    Ex:python cartoonGAN.py --file_name test0.jpg --model_number 0 --down_size 2

    Ps:There are many weight in folder "models", you need to choose the model number according to the image or environment for the better result.
    Ps:Somtimes, we need to down sample the input image due to memory space.

    Step3
    Go to the folder “cartoon_result”, there is the cartoonized image.
    .png → .png
    .gif → .gif
    .mp4 → .gif


For webcam(real time)

    Step1
    Connect the USB webcam to computer.

    Step2
    Input the command.
    Python cartoonGAN.py --model_number {choose the appropriate model} --down_size {x for width/x and height/x}

    Ex:python cartoonGAN.py --model_number 0 --down_size 1

    Ps:There are many weight in folder "models", you need to choose the model number according to the image or environment for the better result.
    Ps:Somtimes, we need to down sample the input image due to memory space.
    
    You can key in 'q' or 'c' when running the program to exit or capture the image to .png, respectively.

    Step3
    Go to the folder “cartoon_result”, there is the cartoonized image.
    webcam → .gif

reference

    [1]Chen, Y., Lai, Y.K., Liu, Y.J.: CartoonGAN: generative adversarial networks for photo cartoonization. In: Proceedings 31st Meeting of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, CVPR 2018, Salt Lake City, UT, United States, pp. 9465–9474 (2018)
