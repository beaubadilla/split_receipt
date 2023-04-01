# April 1, 2023
- Happy April Fool's Day!
- Added `issues.md`
- Added CLAHE to ocr.py
- CLAHE and grayscale can both help or hinder the ability to find corners, depending on the background of the photo

## Next TODO
- change implementation to try both CLAHE and grayscale
    ```
    # Pseudo
    Apply CLAHE
    Apply blur
    Apply threshold/bw
    Apply morphology
    find corners
    save corners
    "reset" img to original
    Apply grayscale
    Apply blur
    Apply threshold/bw
    Apply morphology
    find corners
    save corners
    Figure out which set of corners is "more like a rectangle"
    ```
    -   Info to figure out which set of corners is better
        e.g. curry.jpg
        3024 x 4032
        [array([378,   0], dtype=int32), top left
        array([ 467, 4031], dtype=int32),bottom left
        array([2343, 4031], dtype=int32), bottom right
        array([2149,    0], dtype=int32)] top right
            - two lowest of arr[1] means top
            - two highest of arr[0] means right
            - two highest of arr[1] means bottom
            - twi lowest of arr[0] means left
        
        To have a better idea how much of a leeway between adjacent corners,
        |467-378| = 89
        89 / 3024 = 0.02943 == 2.943%

# March 25, 2023

- Explored Contrast Limited Adaptive Histogram Equalization (CLAHE)
    - A bright photo will have all its pixels confined to a relatively high value. Picture a histogram that is thin and tall. CLAHE will essentially normalize it, spreading the values so the histogram is shorter and wider.
    - Addresses: glare/bright spots in picture that make it more difficult to find corners.
    - Use: reducing glare in picture.
    - Resources: [OpenCV](https://docs.opencv.org/3.1.0/d5/daf/tutorial_py_histogram_equalization.html)

- Understand Morphology
    - Basic Forms: dilation, erosion
    - normally performed on **binary** images
    - Resources: [OpenCV](https://docs.opencv.org/4.x/d9/d61/tutorial_py_morphological_ops.html)

- Understand Contour Approximation
    - Resources: 
        - [PyImageSearch](https://pyimagesearch.com/2021/10/06/opencv-contour-approximation/): great animation

- Understand Kernel
    - > A matrix that represents how you should combine a window of n-by-n pixels to get a single pixel value
    - Resources:
        - [stackoverflow - opencv-understanding-kernel](https://stackoverflow.com/questions/16655962/opencv-understanding-kernel)

- Understand Threshold
    - Resources:
        - [OpenCV](https://docs.opencv.org/4.x/d7/d4d/tutorial_py_thresholding.html)

## Next TODO

Add CLAHE into ocr.py, continue finishing ocr.py overall.

Resources to look further into
- [how-to-force-approxpolydp-to-return-only-the-best-4-corners](https://stackoverflow.com/questions/13028961/how-to-force-approxpolydp-to-return-only-the-best-4-corners-opencv-2-4-2)
- [how-to-detect-a-rectangle-and-square-in-an-image-using-opencv-python](https://www.tutorialspoint.com/how-to-detect-a-rectangle-and-square-in-an-image-using-opencv-python)