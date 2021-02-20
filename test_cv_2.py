import cv2
import numpy as np
import pdf2image
import matplotlib.pyplot as plt
from PIL import Image




def split_line_regions(image):
    open_cv_image = np.array(image) 
    img = open_cv_image[:, :, ::-1].copy()
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray,50,150,apertureSize = 3)

    minLineLength=int(open_cv_image.shape[0]*0.4)
    # lines = cv2.HoughLines(edges,1,np.pi/180,200)
    lines = cv2.HoughLinesP(image=edges,rho=1,theta=np.pi/180, threshold=100,lines=np.array([]), minLineLength=minLineLength,maxLineGap=10)
    a,b,c = lines.shape
    for i in range(a):
        im = cv2.line(gray, (lines[i][0][0], lines[i][0][1]), (lines[i][0][2], lines[i][0][3]), (0, 0, 255), 3, cv2.LINE_AA)

    return Image.fromarray(cv2.cvtColor(im, cv2.COLOR_BGR2RGB))


pdf_path = 'dataset\[Kotak] Nestle India, October 26, 2018.pdf'
image = pdf2image.convert_from_path(pdf_path)[0]
img = split_line_regions(image)
plt.imshow(img)
plt.show()
