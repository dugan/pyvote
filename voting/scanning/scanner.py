from imutils.perspective import four_point_transform
from imutils import contours
import numpy as np
import imutils
import cv2

# Step one: ensure page is square.
# TODO: discover how to use squares in each corner to fix skew.
# For now assume there is no/little skew.

# Step two: find a contest.  Find the square that is the contest and 
# draw a red line around it.
# This could be using contours?

# Step three: 
# Find the rows

# Step four:
# Find the ovals in the rows

# Step five:
# Determine whether an oval is filled

# Step six:
# Output the modified image w/ hash name and add that data point to a dict

# Step seven:
# Output the dict to json.

# Step eight:
# Combine json w/ contest model to associate scores with candidates.

# Step nine:
# Run simple ranked choice voting algorithm to determine winners.


# Find horizontal guiding lines.
# Look for filled / unfilled ovals along those lines


class BallotScanner(object):

  def findTable(self, contours):
    pass
    

  def ScanBallot(self, image):
    box_w = 56
    box_h = 56
    oval_points = self.findOvalsByGrid(image)
    vote_dict = {}
    for (candidate, position) in sorted(oval_points):
      x, y = oval_points[candidate, position]
      exists, filled = self.detectOval(image, (x-box_w/2,y-box_h/2), box_w, box_h)
      if filled:
        vote_dict[position] = candidate
        print "candidate #%d got position #%d" %(candidate+1, position+1)

    votes = [ vote_dict[key] for key in sorted(vote_dict) ]
    return votes

  def detectOval(self, image, upper_left_point, width, height):
    x, y = upper_left_point
    mask_box = np.zeros(image.shape[:2],np.uint8)
    mask_box[y:y+height,x:x+width] = 255

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    filtered_gray = cv2.bitwise_and(gray, gray, mask = mask_box)

    # Canny performs edge detection, removing noise and focusing on clear
    # edges. 
    edged = cv2.Canny(gray, 75, 200)
    filtered_image = cv2.bitwise_and(edged, edged, mask = mask_box)

    # this gets the list of outermost shapes (RETR_EXTERNAL)
    # and gets all points on that 
    cnts = cv2.findContours(filtered_image, cv2.RETR_EXTERNAL,
      cv2.CHAIN_APPROX_SIMPLE)[1]
    if len(cnts) == 0:
      return False, False

    # Box with the shape removed.
    mask_no_shape = mask_box.copy()
    cv2.drawContours(mask_no_shape, cnts, -1, (0,0,0), -1)
    # this should be ~255, but it's 0.
    outside_mean, outside_stddev = cv2.meanStdDev(gray, mask=mask_box)

    mask_only_shape = np.zeros(image.shape[:2],np.uint8)
    cv2.drawContours(mask_only_shape, cnts, -1, (255,255,255), -1)

    inside_mean, inside_stddev = cv2.meanStdDev(gray, mask=mask_only_shape)
    # the last -1 means fill
    # There's something here, try to determine if it's mostly darker #
    # inside the contour than out.
    if inside_mean < 50:
      color = (0, 255, 0)
      filled = True
    else:
      color = (0, 0, 255)
      filled = False

    cv2.drawContours(image, cnts, -1, color, 3)
    return True, filled

  def findOvalsByGrid(self, image):
    # load the image, convert it to grayscale, blur it
    # slightly, then find edges
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 75, 200)
    contours = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
      cv2.CHAIN_APPROX_SIMPLE)
    self.displayImage(image)
    cnts = contours[1]
    guide_length = 12
    guide_thickness = 6
    guide_ratio = float(guide_length) / guide_thickness
    rects = [ cv2.boundingRect(x) for x in cnts ]

    max_x = 0
    max_y = 0
    for (x,y,width,height) in rects:
      if x+width > max_x:
        max_x = x+width
      if y+height > max_y:
        max_y = y+height

    top_x_points = []
    bottom_x_points = []
    left_y_points = []
    right_y_points = []
    for rect in rects:
      x, y, width, height = rect
      if width < height:
        if float(height) / width < 1.5:
          continue
        if y < guide_length:
          top_x_points.append(x + width/2)
        elif (y+height) > (max_y - guide_length):
          bottom_x_points.append(x + width/2)
      else:
        if float(width) / height < 1.5:
          continue
        if x < guide_length:
          left_y_points.append(y + height/2)
        elif (x+width) > (max_x - guide_length):
          right_y_points.append(y + height/2)
    right_y_points.sort()
    left_y_points.sort()
    top_x_points.sort()
    bottom_x_points.sort()

    final_y_points = []
    final_x_points = []
    for (right_y, left_y) in zip(right_y_points, left_y_points):
      if abs(right_y - left_y) < 5:
        final_y_points.append((right_y + left_y) / 2)
    for (top_x, bottom_x) in zip(top_x_points, bottom_x_points):
      if abs(top_x - bottom_x) < 5:
        final_x_points.append((top_x + bottom_x) / 2)

    oval_points = {}
    for x_index, x in enumerate(final_x_points):
      for y_index, y in enumerate(final_y_points):
        oval_points[y_index, x_index] = (x, y)
        #cv2.rectangle(image, (x-28,y-28), (x+28, y+28),  (255, 0, 0), 1)
    return oval_points

  def findOvalsByScanning(self, image):
    # load the image, convert it to grayscale, blur it
    # slightly, then find edges
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 75, 200)
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
      cv2.CHAIN_APPROX_SIMPLE)[1]

    ballot_box = cnts[2]

    # blurred image - blends in some spots that are different color just due to lighting.
    thresh = cv2.threshold(blurred, 30, 255,
      cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    #cv2.drawContours(image, [cnts[2]], -1, color, 3)

    # Filter out everything outside of cnts[2] which is the ballot box.
    x, y, w, h = cv2.boundingRect(ballot_box)
    mask = np.zeros(thresh.shape[:2],np.uint8)
    mask[y:y+h,x:x+w] = 255
    res = cv2.bitwise_and(thresh,thresh,mask = mask)

    # now 
    # there's an extra contour for the whole image at the front for cv3

    color = (0, 255, 0)

    image_width, image_height = res.shape[:2]
    mask = np.zeros((image_width + 2, image_height + 2), np.uint8)
    #mask[y:y+h,x:x+w] = 255
    #cv2.rectangle(res, (x, y), (x+5, y+5), (80, 80, 80), 1)
    cv2.floodFill(res,  mask, (x+2,y+2), (0, 0, 0))

    boxes = cv2.findContours(res.copy(), cv2.RETR_EXTERNAL,
      cv2.CHAIN_APPROX_SIMPLE)[1]
    cv2.drawContours(image, boxes, -1, (255, 0, 0), 3)

    findTable(boxes)

    #cv2.imshow("edged",res)
    self.displayImage(image)

  def displayImage(self, image):
    cv2.imshow("edged",image)
    import sys
    try:
      while True:
        cv2.waitKey(1) 
    except KeyboardInterrupt:
      pass

#
#    # find contours in the edge map, then initialize
#    # the contour that corresponds to the document
#    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
#      cv2.CHAIN_APPROX_SIMPLE)
#    # there's an extra contour at the front if it's not cv2
#    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
#    document_contours = None
#
#    # ensure that at least one contour was found
#    if len(cnts) > 0:
#      # sort the contours according to their size in
#      # descending order
#      cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
#
#      # loop over the sorted contours
#      for c in cnts:
#        # approximate the contour
#        peri = cv2.arcLength(c, True)
#        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
#
#        # if our approximated contour has four points,
#        # then we can assume we have found the paper
#        if len(approx) == 4:
#          docCnt = approx
#          break
#
#    # apply a four point perspective transform to both the
#    # original image and grayscale image to obtain a top-down
#    # birds eye view of the paper
#    paper = four_point_transform(image, docCnt.reshape(4, 2))
#    warped = four_point_transform(gray, docCnt.reshape(4, 2))
#
#    # apply Otsu's thresholding method to binarize the warped
#    # piece of paper - this makes the paper black and white.
#    thresh = cv2.threshold(warped, 0, 255,
#      cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
#
#  ef FindAnswers(self):
#    # find contours in the thresholded image, then initialize
#    # the list of contours that correspond to questions
#    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
#      cv2.CHAIN_APPROX_SIMPLE)
#    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
#    questionCnts = []
#
#    # loop over the contours
#    for c in cnts:
#      # compute the bounding box of the contour, then use the
#      # bounding box to derive the aspect ratio
#      (x, y, w, h) = cv2.boundingRect(c)
#      ar = w / float(h)
#
#      # in order to label the contour as a question, region
#      # should be sufficiently wide, sufficiently tall, and
#      # have an aspect ratio approximately equal to 1
#      if w >= 20 and h >= 20 and ar >= 0.9 and ar <= 1.1:
#        questionCnts.append(c)
#
#    # sort the question contours top-to-bottom, then initialize
#    # the total number of correct answers
#    questionCnts = contours.sort_contours(questionCnts,
#      method="top-to-bottom")[0]
#    correct = 0
#
#    # each question has 5 possible answers, to loop over the
#    # question in batches of 5
#    for (q, i) in enumerate(np.arange(0, len(questionCnts), 5)):
#      # sort the contours for the current question from
#      # left to right, then initialize the index of the
#      # bubbled answer
#      cnts = contours.sort_contours(questionCnts[i:i + 5])[0]
#      bubbled = None
#
#      # loop over the sorted contours
#      for (j, c) in enumerate(cnts):
#        # construct a mask that reveals only the current
#        # "bubble" for the question
#        mask = np.zeros(thresh.shape, dtype="uint8")
#        cv2.drawContours(mask, [c], -1, 255, -1)
#
#        # apply the mask to the thresholded image, then
#        # count the number of non-zero pixels in the
#        # bubble area
#        mask = cv2.bitwise_and(thresh, thresh, mask=mask)
#        total = cv2.countNonZero(mask)
#
#        # if the current total has a larger number of total
#        # non-zero pixels, then we are examining the currently
#        # bubbled-in answer
#        if bubbled is None or total > bubbled[0]:
#          bubbled = (total, j)
#
#      # initialize the contour color and the index of the
#      # *correct* answer
#      color = (0, 0, 255)
#      k = ANSWER_KEY[q]
#
#      # check to see if the bubbled answer is correct
#      if k == bubbled[1]:
#        color = (0, 255, 0)
#        correct += 1
#
#      # draw the outline of the correct answer on the test
#      cv2.drawContours(paper, [cnts[k]], -1, color, 3)
#

