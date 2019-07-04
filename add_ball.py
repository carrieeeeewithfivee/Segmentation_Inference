import numpy as np
from PIL import Image, ImageDraw
class Add_Ball():
    def __init__(self, seg_image):
        #cut bottem half of picture into 108 (3*6*6) squares
        #calculate points
        height = seg_image.shape[0]
        width = seg_image.shape[1]
        gap_y = height/2/6
        gap_x = width/18

        left_points = np.zeros((36,4,2), dtype=int)
        middle_points = np.zeros((36,4,2), dtype=int)
        right_points = np.zeros((36,4,2), dtype=int)

        for y in range(0,6):
            for x in range(0,6):
                left_points[y*6+x,0,:] = [x*gap_x, y*gap_y+(height/2-1)]
                left_points[y*6+x,1,:] = [(x+1)*gap_x, y*gap_y+(height/2-1)]
                left_points[y*6+x,2,:] = [x*gap_x, (y+1)*gap_y+(height/2-1)]
                left_points[y*6+x,3,:] = [(x+1)*gap_x, (y+1)*gap_y+(height/2-1)]

                middle_points[y*6+x,0,:] = [x*gap_x+(width/3), y*gap_y+(height/2-1)]
                middle_points[y*6+x,1,:] = [(x+1)*gap_x+(width/3), y*gap_y+(height/2-1)]
                middle_points[y*6+x,2,:] = [x*gap_x+(width/3), (y+1)*gap_y+(height/2-1)]
                middle_points[y*6+x,3,:] = [(x+1)*gap_x+(width/3), (y+1)*gap_y+(height/2-1)]

                right_points[y*6+x,0,:] = [x*gap_x+(width*2/3), y*gap_y+(height/2-1)]
                right_points[y*6+x,1,:] = [(x+1)*gap_x+(width*2/3), y*gap_y+(height/2-1)]
                right_points[y*6+x,2,:] = [x*gap_x+(width*2/3), (y+1)*gap_y+(height/2-1)]
                right_points[y*6+x,3,:] = [(x+1)*gap_x+(width*2/3), (y+1)*gap_y+(height/2-1)]
        self.left_points = left_points
        self.middle_points = middle_points
        self.right_points = right_points

        #priority map           left                   middle                 right               
        #00 01 02 03 04 05      28 27 18 17 25 31      05 03 01 02 04 06      31 25 17 18 27 28     
        #06 07 08 09 10 11      16 15 14 13 26 32      11 09 07 08 10 12      32 26 13 14 15 16
        #12 13 14 15 16 17      07 05 01 03 19 33      17 15 13 14 16 18      33 19 03 01 05 07
        #18 19 20 21 22 23      08 06 02 04 20 34      23 21 19 20 22 24      34 20 04 02 06 08
        #24 25 26 27 28 29      12 11 10 09 29 35      29 27 25 26 28 30      35 29 09 10 11 12
        #30 31 32 33 34 35      24 23 22 21 30 36      35 33 31 32 34 36      36 30 21 22 23 24    
        self.p_left = [14,20,15,21,13,19,12,18,27,26,25,24,9,8,7,6,3,2,16,22,33,32,31,30,4,10,1,0,28,34,5,11,17,23,29,35]
        self.p_middle = [2,3,1,4,0,5,8,9,7,10,6,11,14,15,13,16,12,17,20,21,19,22,18,23,26,27,25,28,24,29,32,33,31,34,30,35]
        self.p_right = [19,13,21,15,20,14,24,25,26,27,18,12,2,3,6,7,8,9,30,31,32,33,22,16,34,28,0,1,10,4,32,29,23,17,11,5]

    #change numpy array seems faster
    def add_test(self, seg_image):
        """self.seg_image = Image.fromarray(self.seg_image, 'RGB') #change to image
        draw = ImageDraw.Draw(self.seg_image)
        draw.rectangle([(40, 80), (100, 140)], fill=(0, 220, 220))
        self.seg_image = np.array(self.seg_image) #change to array"""

        seg_image[100:140,40:80,:] = [0, 220, 220] 
        return seg_image

    def add_check(self, vector, seg_image):
        #check and add square
        if vector==1: #left
            for num in range(0,35):
                #print(self.p_left[num])
                if ((np.array_equal(seg_image[self.left_points[self.p_left[num],0,1],self.left_points[self.p_left[num],0,0],:],[128,64,128]) or np.array_equal(seg_image[self.left_points[self.p_left[num],0,1],self.left_points[self.p_left[num],0,0],:],[244,35,232])) and 
                    (np.array_equal(seg_image[self.left_points[self.p_left[num],1,1],self.left_points[self.p_left[num],1,0],:],[128,64,128]) or np.array_equal(seg_image[self.left_points[self.p_left[num],1,1],self.left_points[self.p_left[num],1,0],:],[244,35,232])) and 
                    (np.array_equal(seg_image[self.left_points[self.p_left[num],2,1],self.left_points[self.p_left[num],2,0],:],[128,64,128]) or np.array_equal(seg_image[self.left_points[self.p_left[num],2,1],self.left_points[self.p_left[num],2,0],:],[244,35,232])) and
                    (np.array_equal(seg_image[self.left_points[self.p_left[num],3,1],self.left_points[self.p_left[num],3,0],:],[128,64,128]) or np.array_equal(seg_image[self.left_points[self.p_left[num],3,1],self.left_points[self.p_left[num],3,0],:],[244,35,232]))):
                    seg_image[self.left_points[self.p_left[num],0,1]:self.left_points[self.p_left[num],2,1],self.left_points[self.p_left[num],0,0]:self.left_points[self.p_left[num],1,0],:] = [220, 220, 0] 
                    break

        elif vector==2: #middle
            for num in range(0,35):
                #print(self.p_middle[num])
                if ((np.array_equal(seg_image[self.middle_points[self.p_middle[num],0,1],self.middle_points[self.p_middle[num],0,0],:],[128,64,128]) or np.array_equal(seg_image[self.middle_points[self.p_middle[num],0,1],self.middle_points[self.p_middle[num],0,0],:],[244,35,232])) and 
                    (np.array_equal(seg_image[self.middle_points[self.p_middle[num],1,1],self.middle_points[self.p_middle[num],1,0],:],[128,64,128]) or np.array_equal(seg_image[self.middle_points[self.p_middle[num],1,1],self.middle_points[self.p_middle[num],1,0],:],[244,35,232])) and 
                    (np.array_equal(seg_image[self.middle_points[self.p_middle[num],2,1],self.middle_points[self.p_middle[num],2,0],:],[128,64,128]) or np.array_equal(seg_image[self.middle_points[self.p_middle[num],2,1],self.middle_points[self.p_middle[num],2,0],:],[244,35,232])) and
                    (np.array_equal(seg_image[self.middle_points[self.p_middle[num],3,1],self.middle_points[self.p_middle[num],3,0],:],[128,64,128]) or np.array_equal(seg_image[self.middle_points[self.p_middle[num],3,1],self.middle_points[self.p_middle[num],3,0],:],[244,35,232]))):
                    seg_image[self.middle_points[self.p_middle[num],0,1]:self.middle_points[self.p_middle[num],2,1],self.middle_points[self.p_middle[num],0,0]:self.middle_points[self.p_middle[num],1,0],:] = [220, 220, 0] 
                    break

        elif vector==3: #right
            for num in range(0,35):
                #print(self.p_right[num])
                if ((np.array_equal(seg_image[self.right_points[self.p_right[num],0,1],self.right_points[self.p_right[num],0,0],:],[128,64,128]) or np.array_equal(seg_image[self.right_points[self.p_right[num],0,1],self.right_points[self.p_right[num],0,0],:],[244,35,232])) and 
                    (np.array_equal(seg_image[self.right_points[self.p_right[num],1,1],self.right_points[self.p_right[num],1,0],:],[128,64,128]) or np.array_equal(seg_image[self.right_points[self.p_right[num],1,1],self.right_points[self.p_right[num],1,0],:],[244,35,232])) and 
                    (np.array_equal(seg_image[self.right_points[self.p_right[num],2,1],self.right_points[self.p_right[num],2,0],:],[128,64,128]) or np.array_equal(seg_image[self.right_points[self.p_right[num],2,1],self.right_points[self.p_right[num],2,0],:],[244,35,232])) and
                    (np.array_equal(seg_image[self.right_points[self.p_right[num],3,1],self.right_points[self.p_right[num],3,0],:],[128,64,128]) or np.array_equal(seg_image[self.right_points[self.p_right[num],3,1],self.right_points[self.p_right[num],3,0],:],[244,35,232]))):
                    seg_image[self.right_points[self.p_right[num],0,1]:self.right_points[self.p_right[num],2,1],self.right_points[self.p_right[num],0,0]:self.right_points[self.p_right[num],1,0],:] = [220, 220, 0] 
                    break

        else:
            print("no vector provided")
    
        seg_image = np.array(seg_image) #change to array
        return seg_image
