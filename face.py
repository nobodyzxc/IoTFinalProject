import face_recognition
import numpy as np

class Face:
    def __init__(self):
        self.database = {}

    def add_data(self,f1,name):
        '''
            f1 : path to face image
            name : string, face name
        '''
        if name in self.database:
            print("person exist")
            return False
        img = face_recognition.load_image_file(f1)
        faces = face_recognition.face_encodings(img)
        if len(faces):
            embedd = faces[0]
            self.database[name] = embedd
            return True
        else: return False

    def face_com(self,f1):
        '''
            f1 : path to face image
        '''
        if len(self.database.values()) == 0:
            print("Your data not in our database.")
            return False
        unkn = face_recognition.load_image_file(f1)
        faces = face_recognition.face_encodings(unkn)
        if len(faces):
            embedd_unkn = faces[0]
            result = face_recognition.compare_faces(
                    list(self.database.values()),
                    embedd_unkn,
                    tolerance=0.3)
            return True in result
        else: return False

if __name__ == "__main__":

    f = Face()
    print(f.face_com("1.png"))
    print(f.face_com("2.png"))
    print(f.face_com("3.png"))

    f.add_data("1.png","biden")

    print(f.face_com("1.png"))
    print(f.face_com("2.png"))
    print(f.face_com("3.png"))

    f.add_data("2.png","biden&trump")

    print(f.face_com("1.png"))
    print(f.face_com("2.png"))
    print(f.face_com("3.png"))

    f.add_data("3.png","trump")
    print(f.face_com("1.png"))
    print(f.face_com("2.png"))
    print(f.face_com("3.png"))
