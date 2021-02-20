from PIL import Image
import cv2
import numpy as np
import matplotlib.pyplot as plt
import pdf2image
from collections import Counter

class ImageTools:
    def __init__(self):
        pass
    
    def __call__(self, img):
        img, xs, ys = self.split_line_regions(img)
        self.plot_imgs([img])
        return self.split_image(img, xs, ys)
        
    def split_line_regions(self, image):
        open_cv_image = np.array(image) 
        img = open_cv_image[:, :, ::-1].copy()
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray,50,150,apertureSize = 3)

        minLineLength=int(open_cv_image.shape[0]*0.4)
        lines = cv2.HoughLinesP(image=edges,rho=1,theta=np.pi/180, 
        threshold=100,lines=np.array([]), minLineLength=minLineLength,maxLineGap=10)

        a,b,c = lines.shape
        xs, ys = [0, open_cv_image.shape[1]], [0, open_cv_image.shape[0]]
        for i in range(a):
            x_st, y_st, x_e, y_e = lines[i][0][0], lines[i][0][1], lines[i][0][2], lines[i][0][3]

            if x_st == x_e:
                xs.append(x_st)
                y_st = 0
                y_e = open_cv_image.shape[1]
            
            if y_st == y_e:
                ys.append(y_st)
                x_st = 0
                x_e = open_cv_image.shape[0]

            im = cv2.line(
                gray, 
                ( x_st, y_st), (x_e, y_e), 
                (0, 0, 255), 3, cv2.LINE_AA)

        return Image.fromarray(cv2.cvtColor(im, cv2.COLOR_BGR2RGB)), sorted(xs), sorted(ys)
    
    def split_image(self, image, xs, ys):
        width, height = image.size

        y_cropped_imgs = []
        for i in range(len(ys)-1):
            top, bottom, left, right = ys[i], ys[i+1], 0, width
            y_cropped_imgs.append(image.crop((left, top, right, bottom)) )

        x_cropped_imgs = []
        for img in y_cropped_imgs:
            width, height = img.size
            for i in range(len(xs)-1):
                top, bottom, left, right = 0, height, xs[i], xs[i+1]
                new_img = img.crop((left, top, right, bottom))
                extrema = new_img.convert("L").getextrema()
                w, h = new_img.size
                if not extrema[0] == extrema[1] and len(list(set(list(new_img.getdata()))))>100 and h>25 and w>20:
                    x_cropped_imgs.append(new_img)
        return x_cropped_imgs
    
    # def split_image(self, image, xs, ys):
    #     width, height = image.size

    #     x_cropped_imgs = []
    #     for i in range(len(xs)-1):
    #         top, bottom, left, right = 0, height, xs[i], xs[i+1]
    #         x_cropped_imgs.append(image.crop((left, top, right, bottom)) )

    #     y_cropped_imgs = []
    #     for img in x_cropped_imgs:
    #         width, height = img.size
    #         for i in range(len(ys)-1):
    #             top, bottom, left, right = ys[i], ys[i+1], 0, width
    #             new_img = img.crop((left, top, right, bottom))
    #             extrema = new_img.convert("L").getextrema()
    #             if not extrema[0] == extrema[1] and len(list(set(list(new_img.getdata()))))>100:
    #                 y_cropped_imgs.append(new_img)
    #     return y_cropped_imgs


    def split_rows_img(self, image):
        open_cv_image = np.array(image) 
        open_cv_image = open_cv_image[:, :, ::-1].copy()

        img_thr = cv2.threshold(
            cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY), 
            128, 255, cv2.THRESH_BINARY_INV)[1]

        thr_y = 200
        y_sum = np.count_nonzero(img_thr, axis=0)
        peaks = np.where(y_sum > thr_y)[0]

        thr_x = 200
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

    def split_cols_img(self, image):
        open_cv_image = np.array(image) 
        open_cv_image = open_cv_image[:, :, ::-1].copy()

        # Inverse binary threshold grayscale version of image
        img_thr = cv2.threshold(cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY), 128, 255, cv2.THRESH_BINARY_INV)[1]

        # Count pixels along the y-axis, find peaks
        thr_y = 350
        y_sum = np.count_nonzero(img_thr, axis=0)
        peaks = np.where(y_sum > thr_y)[0]

        # Clean peaks
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

    def plot_imgs(self, imgs):
        fig=plt.figure(figsize=(7, 15))
        columns = 1
        rows = len(imgs)
        for i in range(0, columns*rows):
            img = imgs[i]
            fig.add_subplot(rows, columns, i+1)
            plt.imshow(img)
            plt.axis('off')
        plt.show()
    

if __name__ == '__main__':
    pdf_path = 'dataset\[Kotak] Karur Vysya Bank, July 25, 2018.pdf'
    # pdf_path = 'dataset\Adani_Power_Q1FY18_results.pdf'
    # pdf_path = 'dataset\[Kotak] Nestle India, October 26, 2018.pdf'
    image = pdf2image.convert_from_path(pdf_path)[0]

    img_tools = ImageTools()
    imgs = img_tools(image)
    # img_tools.plot_imgs(imgs)

    for img in imgs:
        plt.imshow(img)
        plt.axis('off')
        plt.show()