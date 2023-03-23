import cv2
import os
from keras_facenet import FaceNet
from mtcnn.mtcnn import MTCNN
import pickle
class Embeddings:
    def encodings(self,img):
        face_detector = MTCNN()
        face_encoders = FaceNet()
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        face_coordinates = face_detector.detect_faces(img)
        bbox = face_coordinates[0]["box"]
        x,y,w,h = bbox
        x1,y1,x2,y2 = x,y,x+w,y+h
        face = img[y1:y2,x1:x2]
        face = face.reshape(1,face.shape[0],face.shape[1],face.shape[2])
        face_encodings = face_encoders.embeddings(face)
        return face_encodings
    def embeddings_from_path(self,path):
        face_embeddings = dict()
        for filename in os.listdir(path):
            Face_Encodings = self.encodings(cv2.imread(os.path.join(path,filename)))
            face_embeddings[filename.removesuffix(".jpg")] = Face_Encodings
        return face_embeddings
    def adding_new_face(self,path,roll):
        file = open("encoded_data.p","rb")
        encoding_faces = pickle.load(file)
        Face_Encodings = self.encodings(cv2.imread(path))
        encoding_faces[roll] = Face_Encodings
        file = open("encoded_data.p","wb")
        pickle.dump(encoding_faces,file)
        file.close()
    


