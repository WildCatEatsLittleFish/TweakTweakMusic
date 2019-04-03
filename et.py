import math
from fractions import Fraction

class ET():
    def __init__(self,base_freq=528):
        self.scale_name="Even-Tempered Scale"
        self.base_freq=base_freq
        self.ratio_list=self.get_ratio_list()  # supposed to be a list of Fraction type
        self.length=len(self.ratio_list)  #should be 12
        self.freq_list=self.get_freq_list()
        self.interval_names=['1','m2','M2','m3','M3','4','b5','5','m6','M6','m7','M7']

        self.scale_dic=self.get_dic()

    @staticmethod
    def get_ratio_list():
        ratio_list=[]
        semitone_factor=math.pow(2,(1/float(12)))
        for i in xrange(12):
            ratio=Fraction(math.pow(semitone_factor,i))
            ratio_list.append(ratio)
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





# e=ET(base_freq=528)
# for each in e.freq_list:
#     print(float(each))

