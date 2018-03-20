import numpy as np;
import perpendicular_lines;

def find_horizontal_depth_probabilities(image):
    lines = [];
    for y_i in range(image.shape[0]):
        line = [];
        for x_i in range(image.shape[1]):
            line.append((x_i, y_i));
        lines.append(line);
    return find_depth_probabilities(lines, image);

def find_depth_probabilities(lines, image):
    # convert each line into a depth_rating
    max_intensity = image.max();
    bounds = image.shape;
    depth_ratings = [];
    for index, line in enumerate(lines):
        intensities = [];
        for point in line:
            x_i, y_i = point[0], point[1];
            if(y_i < 0 or y_i > bounds[0]): continue;
            if(x_i < 0 or x_i > bounds[1]): continue;
            intensity = image[y_i, x_i];
            intensities.append(intensity);
        intensities = np.array(intensities);
        average_intensity = intensities.mean();
        depth = (1-average_intensity/float(max_intensity));
        depth_ratings.append(depth);
    depth_ratings = np.array(depth_ratings);

    # normalize depth ratings s.t. sum equals to 1
    sum = depth_ratings.sum();
    depth_ratings = depth_ratings/sum;
    sum_string = str(depth_ratings.sum());
    assert sum_string == "1.0"; # cast to string since we have a float->int conversion error occasionally
    return np.array(depth_ratings);

def find_position_probabilities(image, prediction):
    # calculate probabilities
    sigma = image.shape[0]*0.2; # assume standard error in users prediction is 20%
    prediction_probabilities = [];
    for y_i in range(image.shape[0]):
        this_probability = (np.pi * 2 * sigma**2)**(-0.5) * np.exp(-1*(y_i - prediction)**2 * sigma**(-2))
        prediction_probabilities.append(this_probability);
    return np.array(prediction_probabilities);

def find_gap_valley(image, prediction):
    # find probability vectors for each vertical position
    depth_probability_vector = find_horizontal_depth_probabilities(image);
    position_probability_vector = find_position_probabilities(image, prediction);

    # find total probaiblities for each vertical position
    probabilities = [];
    for y_i in range(image.shape[0]):
        this_probability = depth_probability_vector[y_i] * position_probability_vector[y_i];
        probabilities.append(this_probability);
    probabilities = np.array(probabilities);

    ## get max probability
    y_i = probabilities.argmax();
    return y_i;

def find(image, prediction): return find_gap_valley(image, prediction); # convinience method


def find_nonlinear_gap_valley(image, prediction, width_count = 5):
    # split image into half overlapping segments with a set width
    segment_width = image.shape[1] / width_count;
    bounds, centers = [], [];
    end, start = 0, 0;
    while(start + segment_width < image.shape[1]):
        start = end - segment_width / 2; # increase by half segment width
        if(start < 0): start = 0;
        center = start + segment_width/2;
        end = start + segment_width; # be a segment width in front of start
        bounds.append((start, end));
        centers.append(center);

    # get gap_valley position for each segment
    y_i_list = [];
    for bound_tuple in bounds:
        this_image = image[:, bound_tuple[0]:bound_tuple[1]]; # get the verticle slice
        this_y_i = find_gap_valley(this_image, prediction);
        y_i_list.append(this_y_i);

    # return centers and predictions
    return [centers, y_i_list];
def nonlinear_find(image, prediction): return find_nonlinear_gap_valley(image, prediction);


def find_several_verticle_gap_valleys(image, spline, valley_count, direction):
    # for each pixel on the spline, find the perpendicular line in the direction `valley_section`(above/below) the spline
    lines = []; # list of (start, slope)
    for x_i in range(image.shape[1]):
        # skip first and last since we cant average the slope around them
        if(x_i == 0): continue; # skip first one
        if(x_i == image.shape[1] - 1): continue; # skip the last one
        if(x_i < 15): continue; # skip first 15
        if(x_i > image.shape[1] - 20): continue; # skip last 35

        # calculate perpendicular line
        line = perpendicular_lines.find_line(x_i, spline, direction, image.shape)

        # validate line
        if(len(line) < 10): continue; #skip line if it consists of less than 10 points

        # store
        lines.append(line)

    # calculate valley_gap probability for each line
    tupled_lines = [];
    probabilities = find_depth_probabilities(lines, image);


    # find max
    max_lines = [];
    while(len(max_lines) < valley_count):
        # get max index from probabilities array
        max_index = probabilities.argmax();

        # save the max line
        max_lines.append(lines[max_index]);

        # set probability to -1 - effectivly removing the max element from array
        probabilities[max_index] = -1;

        # remove all lines (set prob to -1) which are within 5% in x direction of the max probability line
        buffer = 0.15;
        buffer_pixels = image.shape[1] * buffer;
        target_x_i = lines[max_index][0][0];
        for index, line in enumerate(lines):
            x_i, y_i = line[0];
            if(np.abs(x_i - target_x_i) < buffer_pixels):
                probabilities[index] = -1; # efectivly remove it

    # convert tuples to x_list and y_list for each line
    dual_list_lines = [];
    for line in max_lines:
        x_list = [];
        y_list = [];
        for tupe in line:
            x_list.append(tupe[0]);
            y_list.append(tupe[1]);
        dual_list_lines.append((x_list, y_list));
    max_lines = dual_list_lines;

    return max_lines;
def verticle_find_several(image, spline, valley_count, direction): return find_several_verticle_gap_valleys(image, spline, valley_count, direction);
