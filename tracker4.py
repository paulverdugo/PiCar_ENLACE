import numpy as np
import tensorflow as tf
import cv2

# import class and function from TF object detection API
from object_detector_detection_api import ObjectDetectorDetectionAPI, \
    PATH_TO_LABELS, NUM_CLASSES


class ObjectDetector(ObjectDetectorDetectionAPI):
    def __init__(self, model_path='detect.tflite'):
        """
            Builds Tensorflow graph, load model and labels
        """

        # Load lebel_map
        self._load_label(PATH_TO_LABELS, NUM_CLASSES, use_disp_name=True)

        # Define lite graph and Load Tensorflow Lite model into memory
        self.interpreter = tf.contrib.lite.Interpreter(
            model_path=model_path)
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

    def detect(self, image, threshold=0.1):
        """
            Predicts person in frame with threshold level of confidence
            Returns list with top-left, bottom-right coordinates and list with labels, confidence in %
        """

        # Resize and normalize image for network input
        frame = cv2.resize(image, (300, 300))
        frame = np.expand_dims(frame, axis=0)
        frame = (2.0 / 255.0) * frame - 1.0
        frame = frame.astype('float32')

        # run model
        self.interpreter.set_tensor(self.input_details[0]['index'], frame)
        self.interpreter.invoke()

        # get results
        boxes = self.interpreter.get_tensor(
            self.output_details[0]['index'])
        classes = self.interpreter.get_tensor(
            self.output_details[1]['index'])
        scores = self.interpreter.get_tensor(
            self.output_details[2]['index'])
        num = self.interpreter.get_tensor(
            self.output_details[3]['index'])

        # Find detected boxes coordinates
        return self._boxes_coordinates(image,
                            np.squeeze(boxes[0]),
                            np.squeeze(classes[0]+1).astype(np.int32),
                            np.squeeze(scores[0]),
                            min_score_thresh=threshold)
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

# allow the camera to warm up
time.sleep(0.1)
for frame in camera.capture_continuous(rawCapture, format="bgr",
                                       use_video_port=True):

    # grab the raw NumPy array representing the image, then 
    # initialize the timestamp and occupied/unoccupied text
    image = frame.array

    result = ObjectDetector.detect(image)

    for obj in result:
        logger.info('coordinates: {} {}. class: "{}". confidence: {:.2f}'.
                    format(obj[0], obj[1], obj[3], obj[2]))

        cv2.rectangle(image, obj[0], obj[1], (0, 255, 0), 2)
        cv2.putText(image, '{}: {:.2f}'.format(obj[3], obj[2]),
                    (obj[0][0], obj[0][1] - 5),
                    cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)


    # show the frame
    cv2.imshow("Stream", image)
    key = cv2.waitKey(1) & 0xFF
