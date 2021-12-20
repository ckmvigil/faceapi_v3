import face_alignment
import cv2
import math
###############################################################################################################
frame = cv2.imread('image-10.jpg')
#frame = cv2.flip(frame,1)
fa = face_alignment.FaceAlignment(face_alignment.LandmarksType._2D, device='cpu', face_detector='sfd')
det = fa.get_landmarks_from_image(frame)
copy = frame.copy()
#################################################################################################################
def slope(x1,y1,x2,y2):
    ###finding slope
    if x2!=x1:
        return((y2-y1)/(x2-x1))
    else:
        return 'NA'
######################################################################################################################
def findAngle(a,b):
    return math.degrees(angle_trunc(math.atan2((det[0][a][1] - det[0][b][1]),(det[0][a][0] - det[0][b][0]))))

def angle_trunc(a):
    while a < 0.0:
        a += math.pi * 2
    return a
#######################################################################################################################
def drawLine(image,x1,y1,x2,y2,color):

    m=slope(x1,y1,x2,y2)
    h,w=image.shape[:2]
    if m!='NA':
        ### here we are essentially extending the line to x=0 and x=width
        ### and calculating the y associated with it
        ##starting point
        px=0
        py=-(x1-0)*m+y1
        ##ending point
        qx=w
        qy=-(x2-w)*m+y2
    else:
    ### if slope is zero, draw a line with x=x1 and y=0 and y=height
        px,py=x1,0
        qx,qy=x1,h
    cv2.line(image, (int(px), int(py)), (int(qx), int(qy)), color , 2)
    #cv2.putText(image,str,(int(px), int(py)), cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,255),1,)


from math import atan
def angle(M1, M2):
    PI = 3.14159265
    angle = abs((M2 - M1) / (1 + M1 * M2))
    ret = atan(angle)
    val = (ret * 180) / PI
    return val

###################################################################################################################
for i in range(len(det[0])):

    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 0.7
    color = (0, 0, 255)
    thickness = 2
    #print((int(det[0][i][0]), int(det[0][i][1])))
    cv2.putText(copy, str(i), (int(det[0][i][0]), int(det[0][i][1])), font, fontScale,
                color, thickness,None, False)
    #cv2.putText()
# def points(h):
#
#
#     font = cv2.FONT_HERSHEY_SIMPLEX
#     fontScale = 0.6
#     color = (0, 0, 255)
#     thickness = 2
#     cv2.putText(copy, str(h), (int(det[0][h][0]), int(det[0][h][1])), font, fontScale,
#                 color, thickness,None, False)
#
# points(1)
# points(9)
# points(21)
# points(22)
# points(27)
# points(30)
# points(33)
# points(40)
# points(41)
# points(50)
# points(58)
#################################################################################################################
def angle_lines(a,b,c,d,m):
    if m==0:
        p1 = slope(det[0][a][0],det[0][a][1],det[0][b][0],det[0][b][1])
        p2 = slope(det[0][c][0],det[0][c][1],det[0][d][0],det[0][d][1])

        if p1 and p2 != 'NA':
            return angle(p1, p2)
        elif p1=='NA':
            return angle(p2,0)
        elif p2=='NA':
            return angle(p1,0)

    else:
        p1 = slope(det[0][a][0],det[0][a][1],(det[0][b][0]+det[0][m][0])//2,(det[0][b][1]+det[0][m][1])//2)
        p2 = slope(det[0][c][0], det[0][c][1], det[0][d][0], det[0][d][1])
        return angle(p1,p2)
#####################################################################################################################
chin_ratio2 = []


def chin_ratio1(a, b, c):
    if (round(abs(a[0] - b[0]) / abs(a[0] - c[0]), 1) == 0.50):
        chin_ratio2.append(
            "Tip of chin is at 1/2 times the distance between pupil perpendicular and head perpendicular line")
    if (round(abs(a[0] - b[0]) / abs(a[0] - c[0]), 1) < 0.50):
        f = "Tip of chin lies at the left of midpoint of pupil perpendicular and head perpendicular line by- " + str(
            round(0.50 - round(abs(a[0] - b[0]) / abs(a[0] - c[0]), 2), 2)) + " times the distance between the lines"

        chin_ratio2.append(f)

    if (round(abs(a[0] - b[0]) / abs(a[0] - c[0]), 1) > 0.50):
        g = "Tip of chin lies at the right of midpoint of pupil perpendicular and head perpendicular line by- " + str(
            round(round(abs(a[0] - b[0]) / abs(a[0] - c[0]), 2) - 0.50, 2)) + " times the distance between the lines"
        chin_ratio2.append(g)


def lip_ratio1(a, b, c):
    if (round(abs(a[0] - b[0]) / abs(a[0] - c[0]), 2) == 0.33):
        chin_ratio2.append(
            "-Lower lip line is at 1/3 times the distance between pupil perpendicular and head perpendicular line")
    if (round(abs(a[0] - b[0]) / abs(a[0] - c[0]), 2) < 0.33):
        h = "Lower lip line lies at the left of 1/3rd of pupil perpendicular and head perpendicular line point by- " + str(
            0.33 - round(abs(a[0] - b[0]) / abs(a[0] - c[0]), 2)) + " times the distance between the lines"
        chin_ratio2.append(h)

    if (round(abs(a[0] - b[0]) / abs(a[0] - c[0]), 2) > 0.33):
        i = "Lower lip line lies at the right of 1/3rd of pupil perpendicular and head perpendicular line point by- " + str(
            round(abs(a[0] - b[0]) / abs(a[0] - c[0]), 2) - 0.33) + " times the distance between the lines"
        chin_ratio2.append(i)

#######################################################################################################################
# slope(int(det[0][27][0]),int(det[0][27][1]),int(det[0][33][0]),int(det[0][33][1])) #N-Sn
# drawLine(copy,int(det[0][27][0]),int(det[0][27][1]),int(det[0][33][0]),int(det[0][33][1]),(128,0,0))
cv2.putText(copy,'N',(int(det[0][27][0]),int(det[0][27][1])),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),3)
cv2.putText(copy,'Sn',(int(det[0][33][0]),int(det[0][33][1])),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),3)
# ##############################################################################################
#
slope(int(det[0][1][0]),int(det[0][1][1]),int(det[0][41][0]),int(det[0][41][1])) #Po-Or
drawLine(copy,int(det[0][1][0]),int(det[0][1][1]),int(det[0][41][0]),int(det[0][41][1]),(0,100,0))
cv2.putText(copy,'Po',(int(det[0][1][0]),int(det[0][1][1])),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),3)
cv2.putText(copy,'Or',(int((det[0][40][0]+det[0][41][0])//2),int((det[0][40][1]+det[0][41][1])//2)),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),3)
# #########################################################################################################
# slope(int(det[0][9][0]),int(det[0][9][1]),int(det[0][33][0]),int(det[0][33][1]))
# drawLine(copy,int(det[0][9][0]),int(det[0][9][1]),int(det[0][33][0]),int(det[0][33][1]),(0,0,128))
cv2.putText(copy,'Pg',(int(det[0][9][0]),int(det[0][9][1])),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),3)
# ########################################################################################################
# slope(int(det[0][9][0]),int(det[0][9][1]),int(det[0][30][0]),int(det[0][30][1]))
# drawLine(copy,int(det[0][9][0]),int(det[0][9][1]),int(det[0][30][0]),int(det[0][30][1]),(128,0,128))
cv2.putText(copy,'Prn',(int(det[0][30][0]),int(det[0][30][1])),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),3)
# ####################################################################################################
# slope(int(det[0][33][0]),int(det[0][33][1]),int((det[0][21][0]+det[0][22][0])/2),int((det[0][21][1]+det[0][22][1])/2))
# drawLine(copy,int(det[0][9][0]),int(det[0][9][1]),int(det[0][30][0]),int(det[0][30][1]),(139,69,19))
cv2.putText(copy,'GI',(int((det[0][21][0]+det[0][22][0])//2),int((det[0][21][1]+det[0][22][1])//2)),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),3)
# ###############################################################################################################
# slope(int(det[0][9][0]),int(det[0][9][1]),int(det[0][58][0]),int(det[0][58][1]))
# drawLine(copy,int(det[0][9][0]),int(det[0][9][1]),int(det[0][30][0]),int(det[0][30][1]),(0,128,128))
#
# ############################################################################################################################
# def acute_obtuse(i):
#     return 180-i
#
# ############################################################################################################################
# #cv2.imshow('result', copy)
# #cv2.waitKey(0)
#
#
# print('The angle between N-Sn line and Frankfort horizontal line is',angle_lines(27,33,1,41,0),'degrees')
#
# print('The angle which connects points Gl (glabella) – Sn (subnasale) – Pg (pogonion) is',acute_obtuse(angle_lines(21,33,33,9,22)),'degrees')
#
# print('The z-angle is ',angle_lines(9,58,1,41,0),'degrees')
#
# chin_ratio1([det[0][41][0],det[0][9][1]],[det[0][9][0],det[0][9][1]],[det[0][27][0],det[0][9][1]])
# lip_ratio1([det[0][41][0],det[0][9][1]],[det[0][9][0],det[0][9][1]],[det[0][27][0],det[0][9][1]])
# print(chin_ratio2)


#cv2.imshow('m',copy)

cv2.imwrite('result-10-fhl.jpg',copy)