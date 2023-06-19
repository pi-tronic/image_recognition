#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

from time import sleep

threshold = 10
background = [0., 0., 0.]
adjacent = [[0,-1], [-1,0], [-1,-1], [-1,1]]    # W, N, NW, NE

src_img = np.array(Image.open('construction_map.pgm'))
M = len(src_img)
N = len(src_img[0])

def two_pass(data):
    linked = []
    labels = np.zeros((M,N))
    print(labels)
    nextLabel = 1
    test = np.zeros((M,N,3))

    # times = 0
    # wrong = 0

    # first pass
    for row in range(len(data)):
        for column in range(len(data[row])):
            # if not background
            if [data[row][column][0], data[row][column][1], data[row][column][2]] != background:
                # get all neighbors (W, N, NW, NE)
                neighbors = []
                neighbors_labels = []
                for direction in adjacent:
                    try:
                        if [data[row][column][0], data[row][column][1], data[row][column][2]] != background:
                            neighbors.append(data[row+direction[0]][column+direction[1]])
                            neighbors_labels.append(labels[row+direction[0]][column+direction[1]])
                            test[row][column] = [1,1,1]
                            print('oh yes')
                    except:
                        print('doesnt exist! out of image!')
                        # times += 1

                        # test if correct out of range
                        # if row+direction[0] >= 0 and row+direction[0] < 79:
                        #     print('wrong')
                        #     wrong += 1
                        
                        # elif column+direction[1] >= 0 and column+direction[0] < 79:
                        #     print('wrong')
                        #     wrong += 1

                if len(neighbors) == 0:
                    print('aeeeffs')
                    linked.append([nextLabel])
                    labels[row][column] = nextLabel
                    nextLabel += 1

                else:
                    # find smallest label of neighbors
                    L = neighbors_labels
                    labels[row][column] = min(L)
                    for label in L:
                        print(len(linked))
                        print(int(label))
                        linked[int(label)-1].append(L)

    # second pass
    # for row in data:
    #     for column in row:
    #         if data[row][column] != background:
    #             labels[row][column] = fin
    
    # print(M, N, times, wrong)
    
    return labels, test

def main():
    gray_img = np.zeros((M,N,3))

    gray_img[src_img>threshold] = [0,0,0]
    gray_img[src_img<threshold] = [1,1,1]

    plt.imshow(src_img, interpolation='None')
    plt.show()

    plt.imshow(gray_img, interpolation='None')
    plt.show()

    label_img, test = two_pass(gray_img)
    plt.imshow(label_img, interpolation='None')
    plt.show()

    plt.imshow(test, interpolation='None')
    plt.show()

main()