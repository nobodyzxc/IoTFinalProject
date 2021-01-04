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
        embedd = face_recognition.face_encodings(img)[0]
        self.database[name] = embedd
        return True
    def face_com(self,f1):
        '''
            f1 : path to face image
        '''
        if len(self.database.values()) == 0:
            print("Your data not in our database.")
            return False
        unkn = face_recognition.load_image_file(f1)
        embedd_unkn = face_recognition.face_encodings(unkn)[0]
        result = face_recognition.compare_faces(list(self.database.values()),embedd_unkn)
        return True in result


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
