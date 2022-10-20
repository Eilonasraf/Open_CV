import datetime
import imutils
import time
import cv2

def detect_motion(min_area=100):
    vs = cv2.VideoCapture(0)
    time.sleep(5.0)
    first_frame = None
    # For video recording - Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    out = cv2.VideoWriter('output.avi', fourcc, 20.0, (500, 375))

    while True:
        # grab current frame and initialize the occupied/unoccupied text
        success, frame = vs.read()
        text = "Unoccupied"
        # If frame could not be grabbed, then we have reached the end of the
        if frame is None:
            break
        # Resize the frame
        frame = imutils.resize(frame, width=500)
        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # cv2.cvtColor - Converts an image from one color space to another
        # cv2.COLOR_BGR2GRAY - convert between RGB/BGR and grayscale

        # Blur the frame:
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        # cv2.GaussianBlur - Blurs an image using a Gaussian filter
        # if the first frame is None, initialize it

        if first_frame is None:
            first_frame = gray
            continue

    # compute the absolute difference between the current frame and first frame
        frame_delta = cv2.absdiff(first_frame, gray)
        cv2.imshow("Frame Delta", frame_delta)

        cv2.waitKey(1)
        thresh = cv2.threshold(frame_delta, 100, 255, cv2.THRESH_BINARY)[1]

        thresh_dil = cv2.dilate(thresh, None, iterations=2)
        cv2.imshow("Thresh_dil", thresh_dil)

        # find contours (shapes) on thresholded image
        cnts = cv2.findContours(thresh_dil.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        # loop over the contours
        for c in cnts:
            # if the contour is too small, ignore it
            if cv2.contourArea(c) < min_area:
                continue

        # compute the bounding box for the contour, draw it on the frame, and update the text
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            text = "Occupied"

        # draw the text and timestamp on the frame
        cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.putText(frame, datetime.datetime.now().strftime("%A%d%B%Y%I:%M:%S%p"), (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
        # show the frame
        cv2.imshow("Security Feed", frame)
        if text == 'Occupied':
            out.write(frame)

        # if the `q` key is pressed, break from the loop
        key = cv2.waitKey(1)
        if key == ord("q"):
            break
    # cleanup the camera and close any open windows (outside the while loop)
    vs.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    detect_motion()







