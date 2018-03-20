import numpy as np;

def find_center(start_line, end_line, bounds, direction):
    if(start_line[0] > end_line[0]): start_line, end_line = end_line, start_line; # swap
    center_x = (end_line[0] - start_line[0])/2 + start_line[0]; # calculate center in x
    center_y_of_starts = (end_line[1] - start_line[1])/2 + start_line[1];

    if(direction == "above"):
        y_bound = 0;
        start_y = y_bound;
        end_y = center_y_of_starts;
        center_y = (end_y - start_y)/2 + start_y; # calculate center in x
    if(direction == "below"):
        y_bound = bounds[0];
        start_y = center_y_of_starts;
        end_y = y_bound;
        center_y = (end_y - start_y)/2 + start_y; # calculate center in x
    return [center_x, center_y]
