#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

from random import randint

threshold = 10
background = [0., 0., 0.]
center = [1., 1., 1.]
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
    
    # get amount of remaining labels
    used_labels = []
    label_amount = 1
    for row in labels:
        for column in row:
            if column not in used_labels and column != 0:
                used_labels.append(column)
                label_amount += 1
    
    # clean up the labels to be 1 to label_amount
    for row in range(len(labels)):
        for column in range(len(labels[row])):
            if labels[row][column] in used_labels:
                labels[row][column] = used_labels.index(labels[row][column]) + 1

    # get amount of remaining labels
    # used_labels = []
    # for row in labels:
    #     for column in row:
    #         if column not in used_labels and column != 0:
    #             used_labels.append(column)
    # print(used_labels)

    
    return labels, label_amount-1

# find the center coordinate of each label
def find_coords(data, labels):
    coords = []
    for i in range(labels):
        coords.append([])

    # get all the same labels coords together
    for row in range(len(data)):
        for column in range(len(data[row])):

            item = data[row][column]
            if item > 0:
                coords[int(item)-1].append([row, column])

    # get center per label
    for label in range(len(coords)):
        x, y = 0, 0
        for coord in coords[label]:
            x += coord[0]
            y += coord[1]
        
        coords[label] = [int(x / len(coords[label])), int(y / len(coords[label]))]

    return coords

def find_coords2(data, labels):
    coords = []
    for i in range(labels):
        coords.append([])

    # get all the same labels coords together
    for row in range(len(data)):
        for column in range(len(data[row])):

            item = data[row][column]
            if item > 0:
                coords[int(item)-1].append([row, column])

    # get center per label
    for label in range(len(coords)):
        min_x, min_y = N, M
        max_x, max_y = 0, 0
        for coord in coords[label]:
            if coord[0] < min_x:
                min_x = coord[0]
            if coord[0] > max_x:
                max_x = coord[0]
            
            if coord[1] < min_y:
                min_y = coord[1]
            if coord[1] > max_y:
                max_y = coord[1]
        
        print(min_x, max_x, min_y, max_y)

        coords[label] = [int((max_x+min_x) / 2), int((max_y+min_y) / 2)]

    return coords

def find_coords3(data, labels, x1, y1, x2, y2):
    coords = []
    for i in range(labels):
        coords.append([])

    # get all the same labels coords together
    for row in range(len(data)):
        for column in range(len(data[row])):

            item = data[row][column]
            if item > 0:
                coords[int(item)-1].append([row, column])

    # get center per label
    for label in range(len(coords)):
        min_x, min_y = N, M
        max_x, max_y = 0, 0
        for coord in coords[label]:
            if coord[0] < min_x:
                min_x = coord[0]
            if coord[0] > max_x:
                max_x = coord[0]
            
            if coord[1] < min_y:
                min_y = coord[1]
            if coord[1] > max_y:
                max_y = coord[1]
        
        coords[label] = [int((max_x+min_x) / 2), int((max_y+min_y) / 2)]

    # check for all center points within x1, y1, x2, y2
    valid_coords = []
    for coord in coords:
        if coord[0]>y1 and coord[0]<y2 and coord[1]>x1 and coord[1]<x2:
            valid_coords.append(coord)


    return valid_coords

def main():
    # make image black and white
    gray_img = np.zeros((M,N,3))
    gray_img[src_img>threshold] = [0,0,0]
    gray_img[src_img<threshold] = [1,1,1]

    # apply two-pass algorithm (label connected areas)
    label_img, label_amount = two_pass(gray_img)

    # colorize labels to be distinguishable
    col_img = np.zeros((M,N,3))
    for label in range(1, label_amount):
        col_img[label_img==label] = colors[randint(0, len(colors)-1)]

    # paint center coords on top (white)
    coords = find_coords3(label_img, label_amount, 0, 0, 40, 40)
    for coord in coords:
        print(coord)
        col_img[coord[0]][coord[1]] = center

    # show image
    plt.imshow(col_img, interpolation='None')
    plt.show()

main()