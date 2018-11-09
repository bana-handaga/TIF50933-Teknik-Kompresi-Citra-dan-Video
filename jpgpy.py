import io
import os
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from scipy import fftpack
# import urllib2
import urllib3
import IPython



# fungsi untuk membaca file image dari link web
image_url='http://i.imgur.com/8vuLtqi.png'
def get_image_from_url(image_url='http://i.imgur.com/8vuLtqi.png', size=(128, 128)):
    file_descriptor = urllib2.urlopen(image_url)
    image_file = io.BytesIO(file_descriptor.read())
    image = Image.open(image_file)
    img_color = image.resize(size, 1)
    img_grey = img_color.convert('L')
    img = np.array(img_grey, dtype=np.float)
    return img

def get_image_from_url3(image_url='http://i.imgur.com/8vuLtqi.png', size=(128, 128)):
    # modifikasi menggunakan urllib3
    http = urllib3.PoolManager()
    r = http.request('GET',image_url)
    image_file = io.BytesIO(r.data)
    ###
    image = Image.open(image_file)
    img_color = image.resize(size, 1)
    img_grey = img_color.convert('L')
    img = np.array(img_grey, dtype=np.float)
    return img


def get_2D_dct(img):
    """ Get 2D Cosine Transform of Image
    """
    return fftpack.dct(fftpack.dct(img.T, norm='ortho').T, norm='ortho')

def get_2d_idct(coefficients):
    """ Get 2D Inverse Cosine Transform of Image
    """
    return fftpack.idct(fftpack.idct(coefficients.T, norm='ortho').T, norm='ortho')

def get_reconstructed_image(raw):
    img = raw.clip(0, 255)
    img = img.astype('uint8')
    img = Image.fromarray(img)
    return img


pixels = get_image_from_url3(image_url=image_url, size=(256, 256))
dct_size = pixels.shape[0]
dct = get_2D_dct(pixels)  # langkah-3 eksekusi DCT
reconstructed_images = []

for ii in range(dct_size):
    dct_copy = dct.copy()
    dct_copy[ii:,:] = 0
    dct_copy[:,ii:] = 0
    
    # Reconstructed image
    r_img = get_2d_idct(dct_copy);
    reconstructed_image = get_reconstructed_image(r_img);

    # Create a list of images
    reconstructed_images.append(reconstructed_image);

plt.figure(figsize=(16, 12));
plt.scatter(range(dct.ravel().size), np.log10(np.abs(dct.ravel())), c='#348ABD', alpha=.3);
plt.title('DCT Coefficient Amplitude vs. Order of Coefficient');
plt.xlabel('Order of DCT Coefficients');
plt.ylabel('DCT Coefficients Amplitude in log scale');
plt.show()

plt.figure(figsize=(16, 12))
plt.hist(np.log10(np.abs(dct.ravel())), bins=100, color='#348ABD', alpha=.3, histtype='stepfilled');
plt.xlabel('Amplitude of DCT Coefficients (log-scaled)');
plt.ylabel('Number of DCT Coefficients');
plt.title('Amplitude distribution of DCT Coefficients');
plt.show()

plt.matshow(np.abs(dct[:50, :50]), cmap=plt.cm.Paired);
plt.title('First 2500 coefficients in Grid');
plt.show()

fig = plt.figure(figsize=(16, 16))
for ii in range(64):
    plt.subplot(8, 8, ii + 1)
    plt.imshow(reconstructed_images[ii], cmap=plt.cm.gray)
    plt.grid(False);
    plt.xticks([]);
    plt.yticks([]);

plt.show()
