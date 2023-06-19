#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

from random import randint

threshold = 10
background = [0., 0., 0.]
colors = [[.69, .15, .4], [1., .2, .43], [1., .74, .4], [1., .42, .3], [.0, .53, .6], [.24, .51, .38], [1., .9, .41], [.88, .67, .35], [.72, .58, .82], [1., .0, .0], [.0, 1., .0], [.0, .0, 1.], [1., 1., .0], [1., .0, 1.], [.0, 1., 1.]]
adjacent1 = [[0,-1], [-1,0], [-1,-1], [-1,1]]    # W, N, NW, NE
adjacent2 = [[0,1], [1,0], [1,-1], [1,1]]    # O, S, SW, SE

src_img = np.array(Image.open('construction_map.pgm'))
M = len(src_img)
N = len(src_img[0])

def two_pass(data):
    linked = []
    labels = np.zeros((M,N))
    nextLabel = 1

    # first pass
    for row in range(len(data)):
        for column in range(len(data[row])):
            # if not background
            if data[row][column].tolist() != background:
                # get all neighbors (W, N, NW, NE)
                neighbors = []
                neighbors_labels = []
                for direction in adjacent1:
                    try:
                        if data[row+direction[0]][column+direction[1]].tolist() != background:
                            neighbors.append(data[row+direction[0]][column+direction[1]])
                            neighbors_labels.append(labels[row+direction[0]][column+direction[1]])
                    except:
                        print('doesnt exist! out of image!')

                # create new label if no neighbors found
                if len(neighbors) == 0:
                    linked.append([nextLabel])
                    labels[row][column] = nextLabel
                    nextLabel += 1

                else:
                    # find smallest label of neighbors
                    L = neighbors_labels
                    labels[row][column] = min(L)
                    for label in L:
                        linked[int(label)-1].append(L)

    # second pass
    for row in range(len(data)):
        for column in range(len(data[row])):
            if data[row][column].tolist() != background:
                # get all neighbors (O, S, SW, SE)
                neighbors_labels = []
                for direction in adjacent2:
                    try:
                        if data[row+direction[0]][column+direction[1]].tolist() != background:
                            neighbors_labels.append(labels[row+direction[0]][column+direction[1]])
                    except:
                        # print('doesnt exist! out of image!')
                        pass

                if len(neighbors_labels) > 0:
                    # find smallest label of neighbors
                    L = neighbors_labels
                    labels[row][column] = min(L)

    
    return labels, nextLabel-1

def main():
    # original image
    plt.imshow(src_img, interpolation='None')
    plt.show()
    
    # make image black and white
    gray_img = np.zeros((M,N,3))
    gray_img[src_img>threshold] = [0,0,0]
    gray_img[src_img<threshold] = [1,1,1]

    plt.imshow(gray_img, interpolation='None')
    plt.show()

    # apply two-pass algorithm (label connected areas)
    label_img, max_label = two_pass(gray_img)

    plt.imshow(label_img, interpolation='None')
    plt.show()

    # colorize labels to be distinguishable
    col_img = np.zeros((M,N,3))
    for label in range(1, max_label):
        col_img[label_img==label] = colors[randint(0, len(colors)-1)]

    plt.imshow(col_img, interpolation='None')
    plt.show()

main()