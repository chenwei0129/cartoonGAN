# cartoonGAN

This is the cartoonGAN, which can cartoonize any image, even webcam(real time), to cartoon style.



For image(.png, .gif or .mp4)

    Step1
    Put the image you want to cartoonize to the folder “image”.

    Step2
    Input the command.
    Python cartoonGAN.py --file_name {your image name} -–model_number {choose the appropriate model}

    Ex: python cartoonGAN.py --file_name test0.jpg --model_number 0

    Ps:You need to choose the model number according to the image or environment for the better result.

    Step3
    Go to the folder “result”, there is the cartoonized image.
    .png → .png
    .gif → .gif
    .mp4 → .gif


For webcam(real time)
    Step1
    Connect the USB webcam to computer.

    Step2
    Input the command.
    Python cartoonGAN.py --model_number {choose the appropriate model}

    Ex: python cartoonGAN.py --model_number 0

    Ps:You need to choose the model number according to the image or environment for the better result.

    Step3
    Go to the folder “result”, there is the cartoonized image.
    webcam → .gif

reference

Chen, Y., Lai, Y.K., Liu, Y.J.: CartoonGAN: generative adversarial networks for photo cartoonization. In: Proceedings 31st Meeting of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, CVPR 2018, Salt Lake City, UT, United States, pp. 9465–9474 (2018)
