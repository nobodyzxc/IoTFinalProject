from resemblyzer import VoiceEncoder, preprocess_wav
from pathlib import Path
import numpy as np
from pathlib import Path
class Voice:
    def __init__(self):
        self.encoder = VoiceEncoder()
        self.database = {}
    def add_data(self,v,name):
        '''
        v: wav file path
        name : str
        '''
        if name in self.database:
            print("person exist")
            return False
        wav = preprocess_wav(Path(v))
        self.database[name] = self.encoder.embed_utterance(wav)

        return True


    def voice_com(self,v1):
        '''
        v1: wav file path

        return True if speaker in database
        '''
        if len(self.database.values()) == 0:
            print("Your data not in our database.")
            return False
        wav = preprocess_wav(Path(v1))

        # ## method 1
        # embed1 = self.encoder.embed_speaker(wav1)
        # embed2 = self.encoder.embed_speaker(wav2)
        # sims1 = np.inner(embed1,embed2) # bigger 0.85

        ## method 2
        embed = self.encoder.embed_utterance(wav)

        for dk in self.database.keys():
            sims = embed @ self.database[dk] # bigger 0.75
            if sims > 0.75:
                print("welcome {}!".format(dk))
                return True
        print("Your data not in our database.")
        return False

ifsymotion-prefix) __name__ == "__main__":
    vo = Voice()
    a1 = "a1.flac"
    a2 = "a2.flac"
    b1 = "b1.flac"
    b2 = "b2.flac"
    print(vo.voice_com(a2))#f
    print(vo.voice_com(b1))#f
    print(vo.voice_com(b2))#f
    vo.add_data(a1,"a1")
    print(vo.voice_com(a2))#t
    print(vo.voice_com(b1))#f
    print(vo.voice_com(b2))#f
    vo.add_data(b2,"b2")
    print(vo.voice_com(a2))#t
    print(vo.voice_com(b1))#t
