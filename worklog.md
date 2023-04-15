# April 9, 2023
- imread(img, 0) vs cv2.cvtColor(img, cv2.COLORBGR2GRAY)
    - tl;dr If original image was taken as grayscale, use imread(). Otherwise, use cv2Color()
    - not 1:1, but 99% similar
- different Page Segmentation Modes (PSM) for Pytesseract
    - mode (4) is definitely the one we want to use as it is recognizes text line-by-line/row-wise
    - mode(5) might be of use, since it is mode (4) but for vertical text. Can be used if our photo is not rotated properly. However, mode (0) can provide metadata to fix rotation

# April 8, 2023
## Wandering Thoughts
- Receipts will always be white/light colored, so we should have a process for light-on-light-bg vs light-on-dark-bg
    - same with photos with bright spots vs no bright spots

- order_points
- best corner angle
- proper orientation improves results (duh), even on a pixel-level
- CLAHE process working, but mixed results, as expected, depending on the background of the photo

## Next TODO
- get grayscale process working
- improve set of transformations before image_to_string()

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
            - two lowest of arr[0] means left
        
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