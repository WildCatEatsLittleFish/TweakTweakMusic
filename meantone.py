from pythagorean import *
import math


class Meantone_Scale(Pythagorean_Scale):
    notes=["C","Db/C#","D","Eb/D#","E","F","Gb/F#","G","Ab/G#","A","Bb/A#","B","C"]
    def __init__(self,base_freq):
        self.scale_name="Meantone Scale"
        self.base_freq=base_freq
        self.ratio_list=self.get_ratio_list()  # supposed to be a list of Fraction type
        self.length=len(self.ratio_list)  #should be 12
        self.freq_list=self.get_freq_list()
        self.interval_names=['1','m2','M2','m3','M3','4','b5','5','m6','M6','m7','M7']

        self.scale_dic=self.get_dic()

    @staticmethod
    def get_ratio_list():
        ratio_list=[]
        adjustment=Fraction(81,80)
        step=math.pow(float(Fraction(5,4)),0.5)
        semitone=math.pow(2,0.5)/math.pow(float(Fraction(5,4)),float(Fraction(5,4)))
        for i in xrange(-5,7):  # interval_number from -5 to 6
            ratio=Pythagorean_Scale.cal_ratio(i)
            ## from dedocaphonic to ptolemy
            if i in [-3,-4,-5]:
                ratio*=adjustment
            if i in [3,4,5]:
                ratio/=adjustment
            if i==6:
                ratio=Fraction(64,45)
            ratio_list.append(ratio)
        ratio_list.sort()
        for i in xrange(13):
            ## from ptolemy to meantone
            if i in [2,47,9,11]:
                ratio_list[i]=ratio_list[i-2]*step
            if i in [5]:
                ratio_list[i]=ratio_list[i-1]*semitone
        return ratio_list

    def get_freq_list(self):
        freq_list=[]
        ratio_list=self.ratio_list
        for i in xrange(self.length):
            freq_list.append(float(self.ratio_list[i])*self.base_freq)
        return freq_list

    def get_dic(self):
        scale_dic={'1':None,'m2':None,'M2':None,'m3':None,'M3':None,'4':None,'b5':None,'5':None,'m6':None,'M6':None,'m7':None,'M7':None}
        for i in xrange(self.length):
            scale_dic[self.interval_names[i]]=self.ratio_list[i]   ## ratio
        return scale_dic

# m=Meantone_Scale(base_freq=528)
# print(m.scale_dic)
