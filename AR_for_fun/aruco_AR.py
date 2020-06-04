# Script for add image on video stream by aruco markers (see ar_example)
# Image with markers is image_frame.jpg
# Image with new image is image_new.jpg
# Marakulin Andrey @annndruha
# 2020
import cv2 as cv
import argparse
import sys
import os.path
import numpy as np

parser = argparse.ArgumentParser(description='Augmented Reality using Aruco markers')
parser.add_argument('--image', help='Path to image file.')
parser.add_argument('--video', help='Path to video file.')
args = parser.parse_args()

im_src = cv.imread("AR_for_fun/image_new.jpg")

outputFile = "AR_for_fun/ar_out_py.avi"
if (args.image):
    # Open the image file
    if not os.path.isfile(args.image):
        print("Input image file ", args.image, " doesn't exist")
        sys.exit(1)
    cap = cv.VideoCapture(args.image)
    outputFile = args.image[:-4]+'_ar_out_py.jpg'
elif (args.video):
    # Open the video file
    if not os.path.isfile(args.video):
        print("Input video file ", args.video, " doesn't exist")
        sys.exit(1)
    cap = cv.VideoCapture(args.video)
    outputFile = args.video[:-4]+'_ar_out_py.avi'
    print("Storing it as :", outputFile)
else:
    # Webcam input
    cap = cv.VideoCapture(0)

# Get the video writer initialized to save the output video
if (not args.image):
    vid_writer = cv.VideoWriter(outputFile, cv.VideoWriter_fourcc('M','J','P','G'), 12, (round(2*cap.get(cv.CAP_PROP_FRAME_WIDTH)),round(cap.get(cv.CAP_PROP_FRAME_HEIGHT))))

winName = "Augmented Reality using Aruco markers in OpenCV"
#Load the dictionary that was used to generate the markers.

dictionary = cv.aruco.Dictionary_get(cv.aruco.DICT_6X6_250)
# Initialize the detector parameters using default values
parameters =  cv.aruco.DetectorParameters_create()

while cv.waitKey(1) < 0:
    #try:
    # get frame from the video
    hasFrame, frame = cap.read()
        
    # Stop the program if reached end of video
    if not hasFrame:
        print("Done processing!")
        print("Output file is stored as ", outputFile)
        cv.waitKey(3000)
        break
        
    # Detect the markers in the image
    markerCorners5, markerIds5, rejectedCandidates5 = cv.aruco.detectMarkers(frame, cv.aruco.Dictionary_get(cv.aruco.DICT_5X5_250), parameters=parameters)
    markerCorners6, markerIds6, rejectedCandidates6 = cv.aruco.detectMarkers(frame, cv.aruco.Dictionary_get(cv.aruco.DICT_6X6_250), parameters=parameters)
    if len(markerCorners5)==2 and len(markerCorners6)==2:
        index = np.squeeze(np.where(markerIds6==0))
        refPt1 = np.squeeze(markerCorners6[index[0]])[0] #np.squeeze(markerCorners6[index[0]])[0] 
        
        index = np.squeeze(np.where(markerIds6==1))
        refPt2 = np.squeeze(markerCorners6[index[0]])[1] #np.squeeze(markerCorners6[index[0]])[1]

        distance = np.linalg.norm(refPt1-refPt2)
        
        scalingFac = 0.02
        pts_dst = [[refPt1[0] - round(scalingFac*distance), refPt1[1] - round(scalingFac*distance)]]
        pts_dst = pts_dst + [[refPt2[0] + round(scalingFac*distance), refPt2[1] - round(scalingFac*distance)]]
        
        index = np.squeeze(np.where(markerIds5==0))
        refPt3 = np.squeeze(markerCorners5[index[0]])[2] #np.squeeze(markerCorners5[index[0]])[2]
        pts_dst = pts_dst + [[refPt3[0] + round(scalingFac*distance), refPt3[1] + round(scalingFac*distance)]]

        index = np.squeeze(np.where(markerIds5==1))
        refPt4 = np.squeeze(markerCorners5[index[0]])[3] #np.squeeze(markerCorners5[index[0]])[3]
        pts_dst = pts_dst + [[refPt4[0] - round(scalingFac*distance), refPt4[1] + round(scalingFac*distance)]]

        pts_src = [[0,0], [im_src.shape[1], 0], [im_src.shape[1], im_src.shape[0]], [0, im_src.shape[0]]]
        
        pts_src_m = np.asarray(pts_src)
        pts_dst_m = np.asarray(pts_dst)

        # Calculate Homography
        h, status = cv.findHomography(pts_src_m, pts_dst_m)
        
        # Warp source image to destination based on homography
        warped_image = cv.warpPerspective(im_src, h, (frame.shape[1],frame.shape[0]))
        
        # Prepare a mask representing region to copy from the warped image into the original frame.
        mask = np.zeros([frame.shape[0], frame.shape[1]], dtype=np.uint8)
        cv.fillConvexPoly(mask, np.int32([pts_dst_m]), (255, 255, 255), cv.LINE_AA)

        # Erode the mask to not copy the boundary effects from the warping
        element = cv.getStructuringElement(cv.MORPH_RECT, (3,3))
        mask = cv.erode(mask, element, iterations=3)

        # Copy the mask into 3 channels.
        warped_image = warped_image.astype(float)
        mask3 = np.zeros_like(warped_image)
        for i in range(0, 3):
            mask3[:,:,i] = mask/255

        # Copy the warped image into the original frame in the mask region.
        warped_image_masked = cv.multiply(warped_image, mask3)
        frame_masked = cv.multiply(frame.astype(float), 1-mask3)
        im_out = cv.add(warped_image_masked, frame_masked)

        
        # Showing the original image and the new output image side by side
        concatenatedOutput = cv.hconcat([frame.astype(float), im_out])
        cv.imshow("AR using Aruco markers", concatenatedOutput.astype(np.uint8))
    else:
        concatenatedOutput = cv.hconcat([frame.astype(float), frame.astype(float)])
        cv.imshow("AR using Aruco markers", concatenatedOutput.astype(np.uint8))
        
    #Write the frame with the detection boxes
    if (args.image):
        cv.imwrite(outputFile, concatenatedOutput.astype(np.uint8))
    else:
        vid_writer.write(concatenatedOutput.astype(np.uint8))


    #except Exception as inst:
    #    print(inst)

cv.destroyAllWindows()
if 'vid_writer' in locals():
    vid_writer.release()
    print('Video writer released..')