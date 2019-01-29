'''
Created on 20/04/2015

@author: Alexandre Yukio Yamashita
'''
import cv2
import math
import scipy

from data_file import read_file
from digit_image import convert_to_image, plot_image
import numpy as np


def cluster(data, k, random):
    '''
    Cluster data points in k clusters.
    '''
    term_crit = (cv2.TERM_CRITERIA_EPS, 30, 0.1)
      
    if not random:
        kmeans_flags = cv2.KMEANS_PP_CENTERS
    else:
        kmeans_flags = cv2.KMEANS_RANDOM_CENTERS
    
    #term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_MAX_ITER, 1, 10000)
    term_crit = (cv2.TERM_CRITERIA_EPS, 100, 0.1)
      
    compactness, classified_points, centers = cv2.kmeans(data=data, K=k, bestLabels=None,
        criteria=term_crit, attempts=100, flags=kmeans_flags) 

    centers = [np.asarray(center).reshape(8, 8) for center in centers]    
    return compactness, classified_points, centers

def save_classified_points(data):
    '''
    Save classified points.
    '''
    print "Saving classified points."
    
    file_data = ""
    
    index = 0
    for result in data:
        #file_data += str(index) + ": " + str(result[0]) + "\n"
        file_data += str(result[0]) + "\n"
        index += 1
    
    new_file = open("result/classified_points.txt", "w")
    new_file.write(file_data)
    new_file.close() 

def save_cov(data, group_index):
    '''
    Save covariance matrix.
    '''
    print "Saving covariance matrix for group " + str(group_index) + "."
    
    file_data = ""
    
    for line in data:
        size = len(line)
        index = 0
        for column in line:
            if index == size -1:
                file_data += str(column) + "\n"
            else:
                file_data += str(column) + ","
                
            index += 1
    
    new_file = open("result/cov_" + str(group_index) +".txt", "w")
    new_file.write(file_data)
    new_file.close() 

def save_dists(data, group_index):
    '''
    Save distances.
    '''
    print "Saving distances for group " + str(group_index) + "."
    
    file_data = ""
        
    index = 0
    for result in data:
        file_data += str(index) + ": " + str(result) + "\n"
        index += 1
        
    new_file = open("result/mahalanobis_distances_" + str(group_index) +".txt", "w")
    new_file.write(file_data)
    new_file.close() 

def create_groups(images, k, classified_points):
    '''
    Create groups using classified points.
    '''
    groups = [[] for k_index in range(k)]
    
    size = len(images[0])
    index = 0
    for point in classified_points:
        groups[point[0]].append(images[index].reshape(size**2))
        index += 1
        
    return groups

def mahalanobis_dists(group, centroid, cov_matrix):
    
    inv_cov_matrix = np.linalg.pinv(cov_matrix)
    centroid_reshape = centroid.reshape(len(centroid)**2)
    
    dists = []
    
    for item in group:
        sub = item -centroid_reshape
        prod = np.dot(sub, inv_cov_matrix)
        result = np.dot(prod, sub)
        
        dists.append(math.sqrt(result))
    
    return dists

def main():  
    # Read data file.
    data = read_file("resources/digits.raw")
    
    # Convert data to image matrix.
    images = np.asarray(map(convert_to_image, data))
    
    # Cluster images.
    compactness, classified_points, centroids = cluster(images, 10, True)
    
    # Save centroid images.
    index = 0
    for centroid in centroids:
        # Save image.
        plot_image(centroid, index)
        index += 1
    
    # for centroid in centroids:
    #    # Plot result.
    #    plot_image(centroid)

    # Save classified points.
    #save_classified_points(classified_points)
    
    # Create the clusters.
    groups = create_groups(images, 10, classified_points)
    
    # Calculate the matrices of covariances.
    cov_matrices = []
    
    for index_group in range(len(groups)):
        cov_matrix = np.cov(np.transpose(groups[index_group]))
        save_cov(cov_matrix, index_group)
        cov_matrices.append(cov_matrix)    
    
    # Calculate the mahalanobis distances.
    for index_group in range(len(groups)):
        dists = mahalanobis_dists(groups[index_group], centroids[index_group], cov_matrices[index_group]);
        dists, groups[index_group] = (list(t) for t in zip(*sorted(zip(dists, groups[index_group]))))
        dists = dists[::-1]
        groups = groups[::-1]
        
        save_dists(dists, index_group)
        
        for index in range(3):
            plot_image(convert_to_image(groups[index_group][index]), index_group, index)
        
if __name__ == '__main__':
    main()
