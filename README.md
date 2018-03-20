# tooth-segmentation
This program does the following:
1. conduct gap valley detection to find the gap valley between top and bottom teeth
    - calculate probability of depth and location as outlined in paper [1]
    - choose max probability as gap valley
    - setting sigma to be 20% for the position probability parameter
    - ![predictions_vs_spline](https://user-images.githubusercontent.com/10381896/37637560-d1b405ee-2bde-11e8-9d63-f04147291601.png)
    
2. conduct gap valley detection to find the gaps between each tooth (for top teeth and for bottom teeth);
    - define how many gap valleys to look for manually (similar to defining approximately where the gap valleys should be found)
    - calculate parameters of perpendicular lines and then generate a dense list of points for the line in the appropriate sector which will be used to calculate depth
    - utilize only the depth probability component to calculate probability of it being a gap valley
    - iteratively find N most probably valleys between teeth
        - find max probability vector,
        - remove all that start within vectors within X%-pixels horizontally of the max probability line
        - repeat above until N lines found
    - ![tooth_boxing](https://user-images.githubusercontent.com/10381896/37637558-d19ee40c-2bde-11e8-841b-d90767aa18f4.png)

3. find contours of teeth
    - in progress
