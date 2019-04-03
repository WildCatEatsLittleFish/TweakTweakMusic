"""
Here, use the 3/2 to create the scale.
Pythagorean Scale series
"""

from fractions import Fraction


class Pythagorean_Scale():
    def __init__(self,base_freq):
        self.scale_name="Pythagorean Scale"
        self.base_freq=base_freq

        self.ratio_list=Pythagorean_Scale.get_ratio_list(-1,6)   # supposed to be a list of Fraction type
        self.length=len(self.ratio_list)  #should be 7
        self.freq_list=self.get_freq_list()

        self.interval_names=['1','M2','M3','4','5','M6','M7']

        self.scale_dic=self.get_dic()

    @staticmethod
    def cal_ratio(interval_num):   #interval_num has to be an integer
        base_ratio=Fraction(3,2)
        ratio=Fraction(base_ratio**interval_num)
        while ratio>2:
            ratio/=2
        while ratio<1:
            ratio*=2
        return ratio    # return the Fraction type

    @staticmethod
    def get_ratio_list(from_interval, to_interval):
        ratio_list=[]
        for i in range(from_interval, to_interval):        # interval_number from -1 to 5
            ratio_list.append(Pythagorean_Scale.cal_ratio(i))
        ratio_list.sort()
        return ratio_list

    def get_freq_list(self):
        freq_list=[]
        for i in range(self.length):
            freq_list.append(float(self.ratio_list[i])*self.base_freq)
        return freq_list

    def get_dic(self):
        scale_dic={'1':None,'M2':None,'M3':None,'4':None,'5':None,'M6':None,'M7':None}
        for i in xrange(self.length):
            scale_dic[self.interval_names[i]]=self.ratio_list[i]  ## ratio
        return scale_dic

class Dodecaphonic_Scale(Pythagorean_Scale):
    def __init__(self,base_freq):
        self.scale_name="Dodecaphonic Scale"
        self.base_freq=base_freq
        self.ratio_list=Pythagorean_Scale.get_ratio_list(-5,7)   # supposed to be a list of Fraction type
        self.length=len(self.ratio_list)  #should be 12
        self.freq_list=self.get_freq_list()
        self.interval_names=['1','m2','M2','m3','M3','4','b5','5','m6','M6','m7','M7']

        self.scale_dic=self.get_dic()

    def get_dic(self):
        scale_dic={'1':None,'m2':None,'M2':None,'m3':None,'M3':None,'4':None,'b5':None,'5':None,'m6':None,'M6':None,'m7':None,'M7':None}
        for i in xrange(self.length):
            scale_dic[self.interval_names[i]]=self.ratio_list[i]
        return scale_dic

class Ptolemy_Scale(Pythagorean_Scale):
    def __init__(self,base_freq):
        self.scale_name="Ptolemy Scale"
        self.base_freq=base_freq
        self.ratio_list=self.get_ratio_list()  # supposesd to be a list of Fraction type
        self.length=len(self.ratio_list)  #should be 12
        self.freq_list=self.get_freq_list()

        self.interval_names=['1','m2','M2','m3','M3','4','b5','5','m6','M6','m7','M7']

        self.scale_dic=self.get_dic()

    def get_ratio_list(self):
        ratio_list=[]
        adjustment=Fraction(81,80)
        for i in range(-5,7):  # interval_number from -5 to 6
            ratio=Pythagorean_Scale.cal_ratio(i)
            if i in [-3,-4,-5]:
                ratio*=adjustment
            if i in [3,4,5]:
                ratio/=adjustment
            if i==6:
                ratio=Fraction(64,45)
            ratio_list.append(ratio)
        ratio_list.sort()
        return ratio_list

    def get_dic(self):
        scale_dic={'1':None,'m2':None,'M2':None,'m3':None,'M3':None,'4':None,'b5':None,'5':None,'m6':None,'M6':None,'m7':None,'M7':None}
        for i in xrange(self.length):
            scale_dic[self.interval_names[i]]=self.ratio_list[i]   ## ratio
        return scale_dic

