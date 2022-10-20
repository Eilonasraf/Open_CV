import cv2

def cam_test (port=0):
    cap = cv2.VideoCapture(port)
    if not cap.isOpened():  # Check if the web cam is opened correctly
        print("failed to open cam")
    else:
        print('cam opened on port {}'.format(port))

        for i in range(10 ** 10):
            success, cv_frame = cap.read()
            if not success:
                print('failed to capture frame on iter {}'.format(i))
                break
            cv2.imshow('Input', cv_frame)
            k = cv2.waitKey(1)  # Wait for a pressed key
            if k == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()
    return

if __name__ == '__main__':
    cam_test()
