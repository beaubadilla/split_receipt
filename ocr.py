import configparser
import sys
from typing import Tuple

import cv2  # OpenCV - change image
from matplotlib import pyplot as plt
import numpy as np
from PIL import Image, ImageOps  # PIL (Pillow) - open image
import pytesseract  # Pytesseract - ocr image

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract"

config = configparser.ConfigParser()
config.read("config.ini")
BASE_FP = config["FILES"]["default_path"]
print(BASE_FP)

"""
/static/changes/{change}.{filename}.JPG
"""


def display(im_fp):
    dpi = 80
    im_data = plt.imread(im_fp)
    height, width, *_ = im_data.shape

    figsize = width / float(dpi), height / float(dpi)

    fig = plt.figure(figsize=figsize)
    ax = fig.add_axes([0, 0, 1, 1])

    ax.axis("off")

    ax.imshow(im_data, cmap="gray")

    plt.show()


def cv_display(img):
    resize = resize_with_aspect_ratio(img, 540, 300)
    cv2.imshow("corners", resize)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def transpose(img):
    return ImageOps.exif_transpose(img)


def invert(img):
    """Invert colors, not orientation"""
    return cv2.bitwise_not(img)


def grayscale(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


def bw(img):
    _, bw_img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

    return bw_img


def noise_removal(img):
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.erode(img, kernel, iterations=1)
    img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    img = cv2.medianBlur(img, 3)
    return img


def thin_font(img):
    img = cv2.bitwise_not(img)
    kernel = np.ones((2, 2), np.uint8)
    img = cv2.erode(img, kernel, iterations=1)
    img = cv2.bitwise_not(img)
    return img


def thick_font(img):
    img = cv2.bitwise_not(img)
    # kernel = np.ones((2, 2), np.uint8)
    kernel = np.ones((3, 3), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.bitwise_not(img)
    return img


# Calculate skew angle of an image
def getSkewAngle(cvImage) -> float:
    # https://becominghuman.ai/how-to-automatically-deskew-straighten-a-text-image-using-opencv-a0c30aed83df
    # Prep image, copy, convert to gray scale, blur, and threshold
    newImage = cvImage.copy()
    gray = cv2.cvtColor(newImage, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (9, 9), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Apply dilate to merge text into meaningful lines/paragraphs.
    # Use larger kernel on X axis to merge characters into single line, cancelling out any spaces.
    # But use smaller kernel on Y axis to separate between different blocks of text
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 5))
    dilate = cv2.dilate(thresh, kernel, iterations=5)

    # Find all contours
    contours, hierarchy = cv2.findContours(
        dilate, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE
    )
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    # Find largest contour and surround in min area box
    largestContour = contours[0]
    minAreaRect = cv2.minAreaRect(largestContour)

    # Determine the angle. Convert it to the value that was originally used to obtain skewed image
    angle = minAreaRect[-1]
    if angle < -45:
        angle = 90 + angle
    return -1.0 * angle


def rotateImage(cvImage, angle: float):
    newImage = cvImage.copy()
    (h, w) = newImage.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    newImage = cv2.warpAffine(
        newImage, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE
    )
    return newImage


def deskew(cvImage):
    angle = getSkewAngle(cvImage=cvImage)
    return rotateImage(cvImage, 1.0 * angle)


def remove_border(img):
    contours, heirarchy = cv2.findContours(
        img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    cntsSorted = sorted(contours, key=lambda x: cv2.contourArea(x))
    cnt = cntsSorted[-1]
    x, y, w, h = cv2.boundingRect(cnt)
    crop = img[y : y + h, x : x + w]
    return crop


def missing_borders(img):
    color = [255, 255, 255]
    top, bottom, left, right = [150] * 4
    image_with_border = cv2.copyMakeBorder(
        img, top, bottom, left, right, cv2.BORDER_DEFAULT, value=color
    )
    return image_with_border


def warp_perspective(img):
    width, height, *_ = img.shape

    # Get top-left, top-right, bottom-left, bottom-right points
    tl, bl, br, tr = find_corners(img)
    print(f"{tl}")
    print(f"{tr}")
    print(f"{bl}")
    print(f"{br}")

    point_matrix = np.float32([tl, tr, bl, br])

    cv2.circle(img, (tl[0], tl[1]), 50, (0, 0, 255), cv2.FILLED)
    cv2.circle(img, (tr[0], tr[1]), 50, (0, 255, 0), cv2.FILLED)
    cv2.circle(img, (bl[0], bl[1]), 50, (255, 0, 0), cv2.FILLED)
    cv2.circle(img, (br[0], br[1]), 50, (0, 0, 0), cv2.FILLED)

    resize = resize_with_aspect_ratio(img, 540, 300)
    cv2.imshow("test", resize)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    converted_points = np.float32([[0, 0], [width, 0], [0, height], [width, height]])

    perspective_transform = cv2.getPerspectiveTransform(point_matrix, converted_points)

    warp_perspective = cv2.warpPerspective(img, perspective_transform, (width, height))
    return warp_perspective


def resize_window(img, width, height, name):
    cv2.namedWindow(name, cv2.WINDOW_NORMAL)
    img_resized = cv2.resize(img, (width, height))
    cv2.imshow(name, img_resized)
    cv2.waitKey(0)


def resize_with_aspect_ratio(image, width=None, height=None, inter=cv2.INTER_AREA):
    """This is better than our first pass of resize_window"""
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    return cv2.resize(image, dim, interpolation=inter)


def find_corners(bw_img):
    """
    Thanks https://stackoverflow.com/questions/60941012/how-do-i-find-corners-of-a-paper-when-there-are-printed-corners-lines-on-paper-i
    Algorithm above
    1. Apply grayscale
    2. Apply blur
    3. Apply threshold (i.e. black & white)
    4. Apply morphology
    5. Find contours
    6. Approximate polygon -> 4 vertices that represent corners

    To allow flexibility, we'll skip steps 1-4. Main takeaway is to provide an image where, as best as possible, only 4 contours can be found. Typically will be a black & white image
    """

    # blur image
    # kernal size (ksize) parameter must be high for the images we are using. I think it's because the size of the image is very large?
    blur = cv2.GaussianBlur(gray, (51, 51), 0)
    resize = resize_with_aspect_ratio(blur, 540, 300)
    cv2.imshow("blur", resize)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    # exit()

    # do otsu threshold on gray image
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    resize = resize_with_aspect_ratio(thresh, 540, 300)
    cv2.imshow("thresh", resize)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # apply morphology
    kernel = np.ones((7, 7), np.uint8)
    morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    morph = cv2.morphologyEx(morph, cv2.MORPH_OPEN, kernel)

    # get largest contour
    contours = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]
    area_thresh = 0
    for c in contours:
        area = cv2.contourArea(c)
        if area > area_thresh:
            area_thresh = area
            big_contour = c

    # get perimeter and approximate a polygon
    peri = cv2.arcLength(big_contour, True)
    # note that approxPolyDP looks for any polygon, not specifically a rectangle
    corners = cv2.approxPolyDP(big_contour, 0.04 * peri, True)

    # try
    # from https://stackoverflow.com/questions/71164603/how-to-find-the-best-quadrilateral-to-approximate-an-opencv-contour
    # on second thought, might be doing the exact same thing
    # corners = cv2.approxPolyDP(big_contour, 0.02 * cv2.arcLength(c, True), closed=True)

    corners = [corner[0] for corner in corners]

    # Add blue circles onto image
    for corner in corners:
        x, y = corner.ravel()
        cv2.circle(img, (x, y), 50, (255, 0, 0), -1)
    resize = resize_with_aspect_ratio(img, 540, 300)
    cv2.imshow("corners", resize)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return corners


def clahe(img, clipLimit: float, tileGridSize: Tuple[int, int]):
    """Address glare and bright spots

    A bright photo will have all its pixels confined to a relatively high value. Picture a histogram that is thin and tall. CLAHE will essentially normalize it, spreading the values so the histogram is shorter and wider.
    """
    clahe = cv2.createCLAHE(clipLimit, tileGridSize)
    return clahe.apply(img)


def main():
    args = sys.argv[1:]
    fn = args[0]

    write = len(args) == 1

    name = fn.split("/")[-1].split(".")[0]
    print(f"{fn=}")
    print(f"{name=}")

    fp = BASE_FP + fn
    img = cv2.imread(fp, 0)
    imgs = {"original": img}

    # Find corners
    ## Apply grayscale
    gray = grayscale(img)
    imgs["gray"] = gray

    ## Blur
    ### larger kernel -> larger blur
    kernel = (51, 51)
    blur = cv2.GaussianBlur(gray, kernel, 0)
    imgs["blur"] = blur

    ## Threshold; typically for black & white
    ### Otsu's threshold
    _, bw = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    imgs["bw"] = bw

    # Display all imgs into separate windows
    for name, img in imgs.items():
        resize = resize_with_aspect_ratio(img, 300, 200)
        cv2.imshow(name, resize)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # ocr_result = pytesseract.image_to_string(dilated_img, lang="eng")
    # print(ocr_result)


if __name__ == "__main__":
    main()
