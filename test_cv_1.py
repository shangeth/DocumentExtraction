import pdf2image
import matplotlib.pyplot as plt
import numpy as np
import cv2
from PIL import Image

# pdf_path = 'dataset\[Kotak] Nestle India, October 26, 2018.pdf'
# image = pdf2image.convert_from_path(pdf_path)[0]
# open_cv_image = np.array(image) 

# # Convert RGB to BGR 
# open_cv_image = open_cv_image[:, :, ::-1].copy()
# # plt.imshow(cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2RGB))
# # plt.show()

# img_thr = cv2.threshold(cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY), 128, 255, cv2.THRESH_BINARY_INV)[1]

# thr_y = 200
# y_sum = np.count_nonzero(img_thr, axis=0)
# peaks = np.where(y_sum > thr_y)[0]

# thr_x = 50
# temp = np.diff(peaks).squeeze()
# idx = np.where(temp > thr_x)[0]
# peaks = np.concatenate(([0], peaks[idx+1]), axis=0) + 1

# images = []
# for i in np.arange(peaks.shape[0]):
#     if i == peaks.shape[0]-1:
#         im = open_cv_image[:, peaks[i]:]
#     else:
#         im = open_cv_image[:, peaks[i]:peaks[i+1]]
#     images.append(im)
#     im_pil = Image.fromarray(cv2.cvtColor(im, cv2.COLOR_BGR2RGB))

#     plt.imshow(im_pil)
#     plt.show()

pdf_path = 'dataset\[Kotak] Nestle India, October 26, 2018.pdf'
image = pdf2image.convert_from_path(pdf_path)[0]
# open_cv_image = np.array(image) 

# # Convert RGB to BGR 
# open_cv_image = open_cv_image[:, :, ::-1].copy()
# # plt.imshow(cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2RGB))
# # plt.show()

# img_thr = cv2.threshold(cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY), 128, 255, cv2.THRESH_BINARY_INV)[1]

# thr_x = 200
# x_sum = np.count_nonzero(img_thr, axis=1)
# peaks = np.where(x_sum > thr_x)[0]

# thr_x = 50
# temp = np.diff(peaks).squeeze()
# idx = np.where(temp > thr_x)[0]
# peaks = np.concatenate(([0], peaks[idx+1]), axis=0) + 1

# images = []
# for i in np.arange(peaks.shape[0]):
#     if i == peaks.shape[0]-1:
#         im = open_cv_image[peaks[i]:]
#     else:
#         im = open_cv_image[peaks[i]:peaks[i+1]]
#     images.append(im)
#     im_pil = Image.fromarray(cv2.cvtColor(im, cv2.COLOR_BGR2RGB))

#     plt.imshow(im_pil)
#     plt.show()


def split_horizontal_img(image):
    open_cv_image = np.array(image) 
    open_cv_image = open_cv_image[:, :, ::-1].copy()

    img_thr = cv2.threshold(cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY), 128, 255, cv2.THRESH_BINARY_INV)[1]

    thr_x = 200
    x_sum = np.count_nonzero(img_thr, axis=1)
    peaks = np.where(x_sum > thr_x)[0]

    thr_x = 50
    temp = np.diff(peaks).squeeze()
    idx = np.where(temp > thr_x)[0]
    peaks = np.concatenate(([0], peaks[idx+1]), axis=0) + 1

    images = []
    for i in np.arange(peaks.shape[0]):
        if i == peaks.shape[0]-1:
            im = open_cv_image[peaks[i]:]
        else:
            im = open_cv_image[peaks[i]:peaks[i+1]]
        im_pil = Image.fromarray(cv2.cvtColor(im, cv2.COLOR_BGR2RGB))

        images.append(im_pil)
    return images

def split_vertical_img(image):
    open_cv_image = np.array(image) 
    open_cv_image = open_cv_image[:, :, ::-1].copy()

    img_thr = cv2.threshold(cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY), 128, 255, cv2.THRESH_BINARY_INV)[1]

    thr_y = 200
    y_sum = np.count_nonzero(img_thr, axis=0)
    peaks = np.where(y_sum > thr_y)[0]

    thr_x = 50
    temp = np.diff(peaks).squeeze()
    idx = np.where(temp > thr_x)[0]
    peaks = np.concatenate(([0], peaks[idx+1]), axis=0) + 1

    images = []
    for i in np.arange(peaks.shape[0]):
        if i == peaks.shape[0]-1:
            im = open_cv_image[:, peaks[i]:]
        else:
            im = open_cv_image[:, peaks[i]:peaks[i+1]]
        im_pil = Image.fromarray(cv2.cvtColor(im, cv2.COLOR_BGR2RGB))
        images.append(im_pil)
    return images

def plot_imgs(imgs):
    fig=plt.figure(figsize=(20, 5))
    columns = len(imgs)
    rows = 1
    for i in range(0, columns*rows):
        img = imgs[i]
        fig.add_subplot(rows, columns, i+1)
        plt.imshow(img)
    plt.show()

if __name__ =='__main__':
    pdf_path = 'dataset\[Kotak] Nestle India, October 26, 2018.pdf'
    image = pdf2image.convert_from_path(pdf_path)[0]

    images = split_vertical_img(image)
    plot_imgs(images)