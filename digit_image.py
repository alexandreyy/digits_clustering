'''
Created on 20/04/2015

@author: Alexandre Yukio Yamashita
'''
import matplotlib.pyplot as plt


def convert_to_image(data, size=8):
    '''
    Convert data to image matrix.
    '''
    
    # Check if size is valid.
    if size ** 2 != len(data):
        # Size is not valid.
        print "Data size is not valid."
        return None
    else:
        print "Converting data to image matrix."
        return data.reshape(size, size)

def plot_image(image, index=None, farthest_index = None, size = 96):
    '''
    Plot image.
    '''
    plt.grid(True, which="both", ls="-")
    plt.xticks([i - 0.5 for i in range(1, len(image[0]))]) 
    plt.yticks([i - 0.5 for i in range(1, len(image[0]))])
   
    frame = plt.gca()
    frame.axes.get_xaxis().set_ticklabels([])
    frame.axes.get_yaxis().set_ticklabels([])    
    plt.imshow(image, interpolation="nearest", cmap='gray')
    
    dpi = (10*size)/48
   
    if farthest_index != None:
        farthest_index += 1
        print "Saving " + str(farthest_index) + "farthest image from centroid_" + str(index) + '.png'
        plt.savefig("result/centroid_" + str(index) + '_farthest_' + str(farthest_index) + '.png', bbox_inches='tight', pad_inches = 0, dpi=dpi)
        
    elif index != None:
        print "Saving centroid in centroid_" + str(index) + '.png'
        plt.savefig("result/centroid_" + str(index) + '.png', bbox_inches='tight', pad_inches = 0, dpi=dpi)
    else:
        plt.show()
