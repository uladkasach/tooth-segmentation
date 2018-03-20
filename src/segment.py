import images.loader as images;
import methods.gap_valley as gap_valley;
import methods.perpendicular_lines as perpendicular_lines;
import numpy as np;
import matplotlib.pyplot as plt;
from scipy.interpolate import UnivariateSpline;

# get image
image_path = "images/teeth_sample.png";
image, size = images.load(image_path);

# get spline of gap valley
centers, y_i_list = gap_valley.nonlinear_find(image, 197);
valley_spline = UnivariateSpline(centers, y_i_list);

# plot image -vs- predictions -vs- spline
if(True):
    splined_x_list = np.arange(0, image.shape[1]+1, 1);
    y_i_splined = [valley_spline(x) for x in splined_x_list];

    plt.imshow(image,  cmap='gray');
    plt.plot(centers, y_i_list, 'ro');
    plt.plot(splined_x_list, y_i_splined);


lines_top = gap_valley.verticle_find_several(image, valley_spline, 6, "above");
lines_bottom = gap_valley.verticle_find_several(image, valley_spline, 5, "below");
lines = [];
lines.extend(lines_top);
lines.extend(lines_bottom);
#lines = [lines[7*25]]
for index, line in enumerate(lines):
    #if(index % 25 != 0): continue;
    x, y = line;
    plt.plot(x, y, 'blue');

plt.show()


# get 4 gap valleys for the bottom teeth
