#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

from random import randint

robot_position = [0.77, 0.25]
map_r = 1.9

threshold = 10
background = [0., 0., 0.]
center = [1., .0, .0]
bot = [.0, 1., .0]
waypoint = [.0, .0, 1.]
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

    
    return labels, label_amount-1

# find the center coordinate of each label
def find_coords(data, labels, x1, y1, x2, y2):
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
        
        coords[label] = [int((max_x+min_x) / 2), int((max_y+min_y) / 2)+1]

    # check for all center points within x1, y1, x2, y2
    valid_coords = []
    for coord in coords:
        if coord[0]>y1 and coord[0]<y2 and coord[1]>x1 and coord[1]<x2:
            valid_coords.append(coord)


    return valid_coords

# create waypoints
def create_waypoints(obstacles, robot_x, robot_y):
    waypoints = []
    obstacles = np.asarray(obstacles)
    
    # waypoint 1
    x1 = obstacles[obstacles[:,0].tolist().index(max(obstacles[:,0])), 1]
    y1 = robot_y
    waypoints.append([y1, x1])

    # waypoint 2
    x2 = obstacles[obstacles[:,0].tolist().index(sorted(obstacles[:,0])[1]), 1]
    y2 = obstacles[obstacles[:,0].tolist().index(max(obstacles[:,0])), 0]
    waypoints.append([y2, x2])

    # waypoint 3
    x3 = x1
    y3 = obstacles[obstacles[:,0].tolist().index(sorted(obstacles[:,0])[1]), 0]
    waypoints.append([y3, x3])

    # waypoint 4
    x4 = x2
    y4 = obstacles[obstacles[:,0].tolist().index(min(obstacles[:,0])), 0]
    waypoints.append([y4, x4])

    # waypoint 5
    x5 = x1
    y5 = y3 - (y1 - y3)
    waypoints.append([y5, x5])

    return waypoints

def main():
    # make image black and white
    gray_img = np.zeros((M,N,3))
    gray_img[src_img>threshold] = [0,0,0]
    gray_img[src_img<threshold] = [1,1,1]

    # apply two-pass algorithm (label connected areas)
    label_img, label_amount = two_pass(gray_img)

    # calculate coords of the robot for matplotlib coordinate system, also visualize them
    robot_x = (robot_position[0] + map_r) / (2 * map_r) * N
    robot_y = (-robot_position[1] + map_r) / (2 * map_r) * M
    gray_img[int(robot_y)][int(robot_x)] = bot

    # paint center coords on top (white)
    coords = find_coords(label_img, label_amount, robot_x, 0, N, robot_y)   # check in construction site
    for coord in coords:
        print(coord)
        gray_img[coord[0]][coord[1]] = center

    # set and visualize waypoints
    waypoints = create_waypoints(coords, robot_x, robot_y)
    for wp in waypoints:
        gray_img[int(wp[0])][int(wp[1])] = waypoint

    # show image
    plt.imshow(gray_img, interpolation='None')
    plt.show()

main()