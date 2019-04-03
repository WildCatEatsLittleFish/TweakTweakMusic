"""
Generate the wavedata,
and create the music
"""
import pyaudio
import numpy as np

class WaveSine():
    @staticmethod
    def get_timberdata(freq=528,volume_list=None,duration=1.0,sampleRate=44100):   ##volume start from 1 to below
        frames=np.arange(2*duration*sampleRate)
        # wavedata=np.int16(np.sin(2*np.pi*frames*freq/sampleRate)*32767*volume)    ## change this to 0.1, then we can play four-note chord
        w_list=[]
        for i in xrange(len(volume_list)):
            data=np.sin(2*np.pi*frames*freq*(i+1)/sampleRate)*32767*volume_list[i]
            w_list.append(data)
        wavedata=np.int16(sum(w_list))
        return wavedata

    @staticmethod
    def get_wavedata(freq=528,volume=0.5,duration=1.0,sampleRate=44100):   ##volume start from 1 to below
        frames=np.arange(2*duration*sampleRate)
        wavedata=np.int16(np.sin(2*np.pi*frames*freq/sampleRate)*32767*volume)    ## change this to 0.1, then we can play four-note chord
        return wavedata


    @staticmethod
    def fpack(freq_list,volume=0.5,duration=1.0,sampleRate=44100):
        wavedata_list=[]
        num=len(freq_list)
        for i in freq_list:
            wavedata_list.append(WaveSine.get_wavedata(i,volume/num,duration,sampleRate))
        wavedata=sum(wavedata_list)
        return wavedata

    @staticmethod
    def pack(*wavedata_list):
        wavedata=sum(wavedata_list)/len(wavedata_list)   ## maybe this is much safer
        return wavedata

    @staticmethod
    def play(wavedata):
        p=pyaudio.PyAudio()

        stream=p.open(format=pyaudio.paInt16,
                      channels=1,
                      rate=44100,
                      output=True,
                      )
        file=open("wavedata.txt","wb")
        if isinstance(wavedata,list):
            for data in wavedata:
                # size=len(data)
                # pause=np.zeros(size/2)
                # print(pause)
                # stream.write(pause)
                stream.write(data)

                # str_data=np.str(data)
                # print(str_data)
                # # file.writelines(str_data)
                # file.write(str_data+"\n")
        else:
            stream.write(wavedata)
          
            # for data in wavedata:
            #
            #     print(data)
            #     str=np.str(data)
            # # str_data=np.str(wavedata)
            # # file.writelines(str_data)
            #     file.write(str+"\n")

        file.close()


        stream.stop_stream()
        stream.close()
        p.terminate()


