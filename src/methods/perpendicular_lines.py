import numpy as np;

def point_is_in_sector(y_i, x_i, magnitude_direction, spline):
    valley_y_i = spline(x_i);
    if(y_i > valley_y_i and magnitude_direction == "smaller"): return False;
    if(y_i < valley_y_i and magnitude_direction == "larger"): return False;
    return True;

# get 6 gap valleys for the top teeth
def calculate_points_for_line(line, spline, direction, bounds, bound_buffer = 15): # bound buffer prevents errors due to image margin effects
    slope, intercept = line;

    # flip since x,y direction is flipped in matrix representation
    if(direction == "above"): magnitude_direction = "smaller";
    if(direction == "below"): magnitude_direction = "larger";

    # calculate all points within bounds
    points = dict();
    for x_i in range(bounds[1]):
        y_i = x_i * slope + intercept;
        y_i = int((y_i));
        if(y_i < 0): continue;
        if(y_i > bounds[0]): continue;
        if(not point_is_in_sector(y_i, x_i, magnitude_direction, spline)): continue;
        points[y_i] = x_i;

    # fill in gaps for verticle slopes - ensure that every y_i has a point
    x_list = [];
    y_list = [];
    waiting_y_list = [];
    latest_x_i = None;
    for y_i in range(bounds[0]):
        if(latest_x_i is not None): # if latest_x_i is defined, check that y_i is reasonable
            if(not point_is_in_sector(y_i, latest_x_i, magnitude_direction, spline)): continue;
        if(y_i in points):
            latest_x_i = points[y_i]; # if y is defined, we can update latest x_i
            for waiting_y_i in waiting_y_list: # and now that its defined, we can use it for the ones we couldnt find a value for
                if(not point_is_in_sector(waiting_y_i, latest_x_i, magnitude_direction, spline)): continue;
                if(latest_x_i < bound_buffer): continue;
                if(latest_x_i > bounds[1]-bound_buffer): continue;
                x_list.append(latest_x_i);
                y_list.append(waiting_y_i);
            waiting_y_list = []; # clear queue
        if(latest_x_i is None): # if latest_x_i not defined, queue it to be defined
            waiting_y_list.append(y_i)
        else:  # if latest_x_i is defined, we can put down a point
            x_list.append(latest_x_i);
            y_list.append(y_i);

    # convert to list of tuples
    lines = [];
    for index in range(len(x_list)):
        lines.append((x_list[index], y_list[index]));

    return lines; #[x_list, y_list];

def calculate_perpendicular_line_to_spline(x_i, spline):

        # get current point
        y_i = float(spline(x_i));

        # get before and after points
        x_before = x_i - 1;
        y_before = spline(x_before);
        x_after = x_i + 1;
        y_after = spline(x_after);

        # derive perpendicular line
        slope = (y_after - y_before) / float(x_after - x_before); # m = (y2 - y1)/(x2 - x1)
        perpendicular_slope = -1 * slope ** -1;
        perpendicular_intercept = intercept = y_i - perpendicular_slope * x_i; # y = mx + b -> b = y - mx

        # return
        line_tuple = (perpendicular_slope, perpendicular_intercept);
        return line_tuple;


def find_line(x_i, spline, direction, bounds):
    line_parameters = calculate_perpendicular_line_to_spline(x_i, spline);
    line_points = calculate_points_for_line(line_parameters, spline, direction, bounds);
    return line_points;
