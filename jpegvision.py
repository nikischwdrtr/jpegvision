import os, glob, cv2, shutil, ffmpeg
import numpy as np
from PIL import Image

# create new folders / delete if already exists
dir = './'
directoryog = 'og'
filesog = os.listdir(dir)
newpathog = os.path.join(dir, directoryog)
if os.path.exists(newpathog):
    shutil.rmtree(newpathog)
os.mkdir(newpathog)
directoryf = 'first'
filesf = os.listdir(dir)
newpathf = os.path.join(dir, directoryf)
if os.path.exists(newpathf):
    shutil.rmtree(newpathf)
os.mkdir(newpathf)
directorys = 'second'
filess = os.listdir(dir)
newpaths = os.path.join(dir, directorys)
if os.path.exists(newpaths):
    shutil.rmtree(newpaths)
os.mkdir(newpaths)
directoryo = 'output'
fileso = os.listdir(dir)
newpatho = os.path.join(dir, directoryo)
if os.path.exists(newpatho):
    shutil.rmtree(newpatho)
os.mkdir(newpatho)

# motion blur functions
def mb_vert(img):
    kernel_size = ksize 
    kernel_v = np.zeros((kernel_size, kernel_size))
    kernel_v[:, int((kernel_size - 1)/2)] = np.ones(kernel_size)
    kernel_v /= kernel_size
    vertical_mb = cv2.filter2D(img, -1, kernel_v)
    return  vertical_mb
def mb_hori(img):
    kernel_size = ksize 
    kernel_h = np.zeros((kernel_size, kernel_size))
    kernel_h[int((kernel_size - 1)/2), :] = np.ones(kernel_size)
    kernel_h /= kernel_size
    horizontal_mb = cv2.filter2D(img, -1, kernel_h)
    return horizontal_mb

# noise function
def noise(img):
    row,col,ch= img.shape
    mean = 10
    var = 200
    sigma = var**0.5
    gauss = np.random.normal(mean,sigma,(row,col,ch))
    gauss = gauss.reshape(row,col,ch)
    noisy = img + gauss
    return noisy

# image resize function
def img_resize(img, width = None, height = None, inter = cv2.INTER_AREA):
    dim = None
    (h, w) = img.shape[:2]
    if width is None and height is None:
        return img
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))
    resized = cv2.resize(img, dim, interpolation = inter)
    return resized

# get movie
getVideo = []
for filename in os.listdir(dir):
    if filename.endswith('.avi') or filename.endswith('.AVI') or filename.endswith('.mp4') or filename.endswith('.MP4') or filename.endswith('.mov') or filename.endswith('.MOV'):
        getVideo.append(filename)

# get all frames
(
    ffmpeg
    .input(getVideo[0])
    .filter('fps', fps='25')
    .output('og/%03d.jpg', start_number=0)
    .overwrite_output()
    .run(quiet=True)
)

# get list of jpges
pathog = newpathog+'/'
jpg_list = glob.glob(pathog + "*.jpg")

# change reso / add motion blur / add noise
pathf = newpathf+'/'
ext = '.jpg'
ksize = 100
for x in range(len(jpg_list)):
    img = cv2.imread(jpg_list[x])
    img = img_resize(img, width = 1280)
    img = mb_vert(img)
    img = noise(img)
    cv2.imwrite(pathf+str(x)+ext, img, [int(cv2.IMWRITE_JPEG_QUALITY), 20])

# change reso / render again
paths = newpaths+'/'
ext = '.jpg'
ksize = 20
jpg_list_s = glob.glob(pathf + "*.jpg")
for x in range(len(jpg_list_s)):
    img = cv2.imread(jpg_list_s[x])
    img = img_resize(img, width = 860)
    img = mb_vert(img)
    cv2.imwrite(paths+str(x)+ext, img, [int(cv2.IMWRITE_JPEG_QUALITY), 60])

# scale up / render again
patho = newpatho+'/'
ext = '.jpg'
ksize = 20
jpg_list_o = glob.glob(paths + "*.jpg")
for x in range(len(jpg_list_o)):
    img = cv2.imread(jpg_list_o[x])
    img = img_resize(img, width = 2000, height = 2000)
    cv2.imwrite(patho+str(x)+ext, img, [int(cv2.IMWRITE_JPEG_QUALITY), 100])

# create new video
(
    ffmpeg
    .input(patho+'*.jpg', pattern_type='glob', framerate=25)
    .output('jpegvision.mp4')
    .run(quiet=True)
)