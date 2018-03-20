import images.loader as images;
import methods.gap_valley as gap_valley;
import methods.perpendicular_lines as perpendicular_lines;
import methods.contour as contour;
import numpy as np;
import matplotlib.pyplot as plt;
from scipy.interpolate import UnivariateSpline;

# define dev env
plot = True;
outline = True;

# get image
image_path = "images/teeth_sample.png";
image, size = images.load(image_path);

if(outline):
    # get spline of gap valley
    centers, y_i_list = gap_valley.nonlinear_find(image, 197);
    valley_spline = UnivariateSpline(centers, y_i_list);

    # plot image -vs- predictions -vs- spline
    if(plot):
        splined_x_list = np.arange(0, image.shape[1]+1, 1);
        y_i_splined = [valley_spline(x) for x in splined_x_list];

        plt.imshow(image,  cmap='gray');
        plt.plot(centers, y_i_list, 'ro');
        plt.plot(splined_x_list, y_i_splined);


    # find verticle gap valleys to "box" teeth
    lines_top = gap_valley.verticle_find_several(image, valley_spline, 6, "above");
    lines_bottom = gap_valley.verticle_find_several(image, valley_spline, 5, "below");
    lines = [];
    lines.extend(lines_top);
    lines.extend(lines_bottom);

    # plot the verticle gap valleys
    if(plot):
        for index, line in enumerate(lines):
            x, y = line;
            plt.plot(x, y, 'blue');

    # find center for each tooth
    start_line_start_point = [lines_bottom[-2][0][0], lines_bottom[-2][1][0]];
    end_line_start_point = [lines_bottom[-1][0][0], lines_bottom[-1][1][0]];
    tooth_center_1 = contour.find_center(start_line_start_point, end_line_start_point, image.shape, "below");
    print(tooth_center_1);

    plt.plot(tooth_center_1[0],tooth_center_1[1], 'go')

# compute gradient image
def compute_gradient(image):
    gradient_image = np.array(image);
    for x_i in range(image.shape[1]):
        for y_i in range(image.shape[0]):
            if(x_i == 0 or y_i == 0):
                gradient = 0;
            else :
                gradient = np.sqrt((image[y_i, x_i] - image[y_i, x_i - 1])**2 + (image[y_i, x_i] - image[y_i - 1, x_i])**2 )
            gradient_image[y_i, x_i] = gradient;
    return gradient_image;

if(False):
    gradient_image = compute_gradient(image);
    plt.imshow(gradient_image,  cmap='gray');

if(plot):
    plt.show()
