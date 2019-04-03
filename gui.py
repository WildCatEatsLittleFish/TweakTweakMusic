from Tkinter import *
from pythagorean import *
from meantone import Meantone_Scale
from et import ET
from wavesine import WaveSine
import threading,random
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg

from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
import numpy as np
import pyaudio,time
import wckToolTips

f=Figure(figsize=(5,5),dpi=100)
a=f.add_subplot(111)   ##111 means there is only one plot

def animate(i):
    pullData=open("freq.txt","r").readline()
    freq=float(pullData)
    x = np.linspace(0, 44100)
    y=np.sin(2*np.pi*freq*x/4410000)
    a.clear()
    a.plot(x,y)

class User(Frame):
    def __init__(self,master):
        Frame.__init__(self,master)
        self.grid(row=0,column=0)
        ## input the melody
        label_melody=Label(self,text="Melody")
        label_melody.grid(row=0,column=0)
        wckToolTips.register(label_melody, "Enter the notes of melody based on specif format,\n specifing note name and the octave position of the note,\n"
                                           "using ',' to separate each note, using '|' to separate each verse.\nNote: you can only enter 4, 6 or 8 beat notes for each verse.")
        self.melody=StringVar()
        self.melody.set("C1,Db1,C1,Bb1,Ab1,Ab1|C1,Db1,C1,Bb1,Ab1,Ab1|Ab1,Ab1,C1,Db1,Ab1,-|Ab1,Ab1,Db1,C1,Bb1,-|Bb1,Ab1,C1,Ab1,Ab1,-")  ## Ab

        melody_=Entry(self,textvariable=self.melody,width=50)
        melody_.grid(row=0,column=1,columnspan=10,sticky=W)

        label_sample=Label(self,text="Sample")
        label_sample.grid(row=0,column=10)
        wckToolTips.register(label_sample, "Choose the pattern of chord for the melody.")
        self.sample_choice=Spinbox(self, values=("Every breath you take","All I want for Chrismas is You","Twinkle","Stand by me"))
        self.sample_choice.grid(row=0,column=11,columnspan=3)
        wckToolTips.register(self.sample_choice, "Choose the melody sample you want.")


        ## key setting
        label_key=Label(self,text="Key")
        label_key.grid(row=1,column=0)
        wckToolTips.register(label_key, "Choose the correct key for the notes you just entered before playing the notes.")
        Keys=["C","Db/C#","D","Eb/D#","E","F","Gb/F#","G","Ab/G#","A","Bb/A#","B"]
        Keys_value=["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
        self.key=StringVar()
        self.key.set("G#")    ##Initialization
        for i in xrange(len(Keys)):
            b=Radiobutton(self,text=Keys[i],variable=self.key,value=Keys_value[i])
            b.grid(row=1,column=i+1)

        ## system setting
        label_system=Label(self,text="System")
        label_system.grid(row=2,column=0)
        wckToolTips.register(label_system, "Choose different music system to build different freq for the same note.")
        systems=["Ptolemy","Meantone","ET"]
        self.system=StringVar()
        self.system.set("Ptolemy")    ##Initialization
        for i in xrange(len(systems)):
            b=Radiobutton(self,text=systems[i],variable=self.system,value=systems[i])
            b.grid(row=2,column=i+1)

        ## freq setting
        label_freq=Label(self,text="note C1(Hz)")
        label_freq.grid(row=3,column=0)
        wckToolTips.register(label_freq, "Enter a real number for the base frequency of note 'C1', the note 'C' of the 1st octave.")
        self.freq=DoubleVar()
        self.freq.set(264)
        freq_=Entry(self,textvariable=self.freq,width=10)
        freq_.grid(row=3,column=1,columnspan=2,sticky=W)

        ## tempo setting
        label_speed=Label(self,text="tempo")
        label_speed.grid(row=3,column=2)
        wckToolTips.register(label_speed, "Enter a reak number for the speed of the melody, i.e. tempo 60 means 1 second for each note."
                                          "\nThe high the tempo is, the faster the speed goes.")
        self.speed=DoubleVar()
        self.speed.set(100)
        speed_=Entry(self,textvariable=self.speed,width=10)
        speed_.grid(row=3,column=3,columnspan=2,sticky=W)




class Timber(Frame):
    def __init__(self,master):
        Frame.__init__(self,master)
        self.grid(row=1,column=0)

        ## timber setting
        l1=Label(self,text="H1",width=8)
        l1.grid(row=0,column=0,sticky=E)
        wckToolTips.register(l1, "Choose the degree of the 1st overtone to create the timber of each note.")
        self.var1=DoubleVar()
        self.var1.set(1)
        scale1=Scale(self,from_=0,to=1,variable=self.var1,resolution=0.01)
        scale1.grid(row=1,column=0)

        l2=Label(self,text="H2",width=8)
        l2.grid(row=0,column=1)
        wckToolTips.register(l2, "Choose the degree of the 2nd overtone to create the timber of each note.")
        self.var2=DoubleVar()
        self.var2.set(0.38)
        scale2=Scale(self,from_=0,to=1,variable=self.var2,resolution=0.01)
        scale2.grid(row=1,column=1)

        l3=Label(self,text="H3",width=8)
        l3.grid(row=0,column=2)
        wckToolTips.register(l3, "Choose the degree of the 3rd overtone to create the timber of each note.")
        self.var3=DoubleVar()
        self.var3.set(0.06)
        scale3=Scale(self,from_=0,to=1,variable=self.var3,resolution=0.01)
        scale3.grid(row=1,column=2)

        l4=Label(self,text="H4",width=8)
        l4.grid(row=0,column=3)
        wckToolTips.register(l4, "Choose the degree of the 4th overtone to create the timber of each note.")
        self.var4=DoubleVar()
        self.var4.set(0.24)
        scale4=Scale(self,from_=0,to=1,variable=self.var4,resolution=0.01)
        scale4.grid(row=1,column=3)

        l5=Label(self,text="H5",width=8)
        l5.grid(row=0,column=4)
        wckToolTips.register(l5, "Choose the degree of the 5th overtone to create the timber of each note.")
        self.var5=DoubleVar()
        self.var5.set(0.29)
        scale5=Scale(self,from_=0,to=1,variable=self.var5,resolution=0.01)
        scale5.grid(row=1,column=4)

        l6=Label(self,text="H6",width=8)
        l6.grid(row=0,column=5)
        wckToolTips.register(l6, "Choose the degree of the 6th overtone to create the timber of each note.")
        self.var6=DoubleVar()
        scale6=Scale(self,from_=0,to=1,variable=self.var6,resolution=0.01)
        scale6.grid(row=1,column=5)

        l7=Label(self,text="H7",width=8)
        l7.grid(row=0,column=6)
        wckToolTips.register(l7, "Choose the degree of the 7th overtone to create the timber of each note.")
        self.var7=DoubleVar()
        self.var7.set(0.4)
        scale7=Scale(self,from_=0,to=1,variable=self.var7,resolution=0.01)
        scale7.grid(row=1,column=6)

        l8=Label(self,text="H8",width=8)
        l8.grid(row=0,column=7)
        wckToolTips.register(l8, "Choose the degree of the 8th overtone to create the timber of each note.")
        self.var8=DoubleVar()
        scale8=Scale(self,from_=0,to=1,variable=self.var8,resolution=0.01)
        scale8.grid(row=1,column=7)

        l9=Label(self,text="H9",width=8)
        l9.grid(row=0,column=8)
        wckToolTips.register(l9, "Choose the degree of the 9th overtone to create the timber of each note.")
        self.var9=DoubleVar()
        scale9=Scale(self,from_=0,to=1,variable=self.var9,resolution=0.01)
        scale9.grid(row=1,column=8)

        l10=Label(self,text="Volume",width=8)
        l10.grid(row=0,column=9)
        wckToolTips.register(l10, "Choose volume for the created-timber-note.")
        self.var10=DoubleVar()
        self.var10.set(0.5)
        scale10=Scale(self,from_=0,to=1,variable=self.var10,resolution=0.01)
        scale10.grid(row=1,column=9)

        self.var_list=[self.var1,self.var2,self.var3,self.var4,self.var5,self.var6,self.var7,self.var8,self.var9,self.var10]   ## decide the volume

class Setting(Frame):
    def __init__(self,master):
        Frame.__init__(self,master)
        self.grid(row=2,column=0)


        Label(self,text="Setting",width=10).grid(row=1,column=0)
        self.chord_bool=BooleanVar()
        c1=Checkbutton(self,text="Chord",variable=self.chord_bool)
        c1.grid(row=1,column=1)
        wckToolTips.register(c1, "Adding the chord to back up the original melody.")

        self.chorus_bool1=BooleanVar()
        c2=Checkbutton(self,text="Chorus1",variable=self.chorus_bool1)
        c2.grid(row=1,column=2)
        wckToolTips.register(c2, "Adding chorus 1 to rich the sound.")

        self.chorus_bool2=BooleanVar()
        c3=Checkbutton(self,text="Chorus2",variable=self.chorus_bool2)
        c3.grid(row=1,column=3)
        wckToolTips.register(c3, "Adding chorus 2 to rich the sound.")

        self.duel_bool=BooleanVar()
        c4=Checkbutton(self,text="Duel",variable=self.duel_bool)
        c4.grid(row=1,column=4)
        wckToolTips.register(c4, "Adding duel to rich the sound.")


class Graph(Frame):
    def __init__(self,master):
        Frame.__init__(self,master)
        self.grid(row=4,column=0)



        canvas=FigureCanvasTkAgg(f,self)
        canvas.show()
        canvas.get_tk_widget().pack(side=TOP,fill=BOTH,expand=True)

        toolbar=NavigationToolbar2TkAgg(canvas,self)
        toolbar.update()
        canvas._tkcanvas.pack(side=TOP,fill=BOTH,expand=True)


class Note(Frame):
    def __init__(self,master):
        Frame.__init__(self,master)
        self.grid(row=3,column=0)

        l1=Label(self,text="Note")
        l1.grid(row=0,column=0)
        wckToolTips.register(l1, "Show the current played note.")
        notes=["C","Db/C#","D","Eb/D#","E","F","Gb/F#","G","Ab/G#","A","Bb/A#","B"]
        notes_value=["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
        self.note=StringVar()
        self.note.set("C")    ##Initialization
        for i in xrange(len(notes)):
            Radiobutton(self,text=notes[i],variable=self.note,value=notes_value[i]).grid(row=0,column=i+1)


        l2=Label(self,text="Interval")
        l2.grid(row=1,column=0)
        wckToolTips.register(l2, "Show the current played interval.")
        intervals=['1','m2','M2','m3','M3','4','b5','5','m6','M6','m7','M7']
        self.interval=StringVar()
        self.interval.set("1")    ##Initialization
        for i in xrange(len(intervals)):
            Radiobutton(self,text=intervals[i],variable=self.interval,value=intervals[i]).grid(row=1,column=i+1)


        l3=Label(self,text="Frequency")
        l3.grid(row=2,column=0)
        wckToolTips.register(l3, "Show the current played frequency.")
        self.freq_str=StringVar()
        Entry(self,textvariable=self.freq_str).grid(row=2,column=1,columnspan=2)

class GUI(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title("Tweak Tweak Melody!")
        self.minsize(500,500)
        self.user=User(self)
        self.timber=Timber(self)
        self.graph=Graph(self)
        self.setting=Setting(self)
        self.note=Note(self)



        b1=Button(self.setting,text="Play",command=self.play,width=6)
        b1.grid(row=0,column=0,sticky=W)
        wckToolTips.register(b1, "Play the melody.")

        self.key_choice=Spinbox(self.setting, values=("C","C#","D","D#","E","F","F#","G","G#","A","A#","B"))
        self.key_choice.grid(row=0,column=1)
        wckToolTips.register(self.key_choice, "Choose the key you want to switch to.")
        b2=Button(self.setting,text="Change Key",command=self.change_key,width=10)
        b2.grid(row=0,column=2,sticky=E)
        wckToolTips.register(b2, "Switch the key, and the meantime convert the original melody notes to corresponding noted based on the current chosen key.")

        l=Label(self.setting,text="Chord pattern",width=10)
        l.grid(row=0,column=4,sticky=E)
        wckToolTips.register(l, "Choose the pattern of chord for the melody.")
        self.pattern_choice=Spinbox(self.setting, values=("1010","1000","101010","100100","010101","10101010","10001000","10010010","01001001"))
        self.pattern_choice.grid(row=0,column=5)
        wckToolTips.register(self.pattern_choice, "Choose the key you want to switch to.")

        b3=Button(self.user,text="Confirm",command=self.change_sample)
        b3.grid(row=0,column=14,sticky=E)
        wckToolTips.register(b1, "Confirm the melody sample choice.")


        b1=Button(self.setting,text="QUIT",command=self.quit,width=6)
        b1.grid(row=0,column=6,sticky=W)
        wckToolTips.register(b1, "Quit the App.")

        b4=Button(self.timber,text="Reset Timber",command=self.reset_timber)
        b4.grid(row=1,column=10)
        wckToolTips.register(b4, "Back to the default timber.")

        self.reload()

    def reload(self):
        ## choice from User frame
        self.melody=self.user.melody.get().split('|')  ## partition into verses
        self.verse_num=len(self.melody)
        self.beat_num=len(self.melody[0].split(','))
        systems_dic={"Ptolemy":Ptolemy_Scale,"Meantone":Meantone_Scale,"ET":ET}
        self.system=systems_dic[self.user.system.get()]   ##should be a scale class
        self.base_freq=float(self.user.freq.get())    ## always should be the freq of the 1C

        file=open("freq.txt","w")
        file.write(str(self.base_freq))
        file.close()

        self.scale=self.system(self.base_freq)
        self.scale_dic=self.scale.scale_dic   ## the relationship of interval and ratio   interval-ratio
        self.key=self.user.key.get()   ## should be "C" or ...
        self.pattern=self.change_pattern()
        keyindex_dic={"C":1,"Db":2,"C#":2,"D":3,"Eb":4,"D#":4,"E":5,"F":6,"Gb":7,"F#":7,"G":8,"Ab":9,"G#":9,"A":10,"Bb":11,"A#":11,"B":12}
        self.root_freq=self.scale.freq_list[keyindex_dic[self.key]-1]
        self.speed=float(self.user.speed.get())

        ## create three tables
        # 1. interval-ratio  -- already created by self.scale_dic
        # 2. interval-note
        notes=["C",{"Db","C#"},"D",{"Eb","D#"},"E","F",{"Gb","F#"},"G",{"Ab","G#"},"A",{"Bb","A#"},"B"]
        key_order_notes=notes[keyindex_dic[self.key]-1:]+notes[:keyindex_dic[self.key]-1]
        intervals=['1','m2','M2','m3','M3','4','b5','5','m6','M6','m7','M7']
        self.interval_note_dic={}
        for i in xrange(12):
            self.interval_note_dic[intervals[i]]=key_order_notes[i]  ## PA: the value could be a set
        # 3. note-interval
        self.note_interval_dic={}
        for key,value in self.interval_note_dic.items():
            if isinstance(value,set):
                for each in value:
                    self.note_interval_dic[each]=key
            else:
                self.note_interval_dic[value]=key

        ## choice from Timber Frame
        overtone_list=[]
        volume_list=[]
        for i in xrange(9):
            overtone_list.append(float(self.timber.var_list[i].get()))
        whole=sum(overtone_list)
        self.volume=float(self.timber.var_list[9].get())/2  ## the biggest volume should be 0.5
        for i in xrange(9):
            volume_list.append(overtone_list[i]/whole*self.volume)
        self.volume_list=volume_list   ### for timber of each note, remember the volume list for one note for the get_wavedata method

        ## based on the choice to calculate
        self.r_interval,self.r_ratio,self.r_freq=self.converting()

        # self.chord_data_list=self.chord_analize()
        # self.get_melody_data()
        self.melody_data=self.get_melody_data()
        self.chord_data=self.chord_analize()
        self.chorus_data1=self.get_chorus1()
        self.chorus_data2=self.get_chorus2()

    def reset_timber(self):
        self.timber.var1.set(1)
        self.timber.var2.set(0.38)
        self.timber.var3.set(0.06)
        self.timber.var4.set(0.24)
        self.timber.var5.set(0.29)
        self.timber.var6.set(0)
        self.timber.var7.set(0.4)
        self.timber.var8.set(0)
        self.timber.var9.set(0)
        self.timber.var10.set(0.5)
        # return self.timber.var1,




    def converting(self):
        ## get the duration verted from self.speed
        duration=60/self.speed  ##self.speed is based on tempo, while duration is based on seconds
        self.beat,=(duration,)   ## can note change this, we have to change the key based on the original duration
        verses=[]
        for i in self.melody:
            verse=i.split(",")
            verses.append(verse)
        r_interval=[]
        r_ratio=[]
        r_freq=[]
        for i in xrange(self.verse_num):  ## for each verse
            verse_interval=[]
            verse_ratio=[]
            verse_freq=[]
            for j in xrange(len(verses[i])):  ## the length of verses[i] should be even number
                per_beat=verses[i][j]   ## could be note_name or "-" or " "
                if per_beat!="-" and per_beat!=" ":   # should be a note  and the format should be like C1
                    temp=len(per_beat)
                    note=per_beat[:temp-1]
                    octave_index=int(per_beat[temp-1:])
                    interval_position=self.note_interval_dic[note]
                    ratio=self.scale_dic[interval_position]
                    verse_interval.append([interval_position,octave_index,duration])
                    verse_ratio.append([ratio*octave_index,duration])
                    verse_freq.append([self.root_freq*ratio*octave_index,duration])
                else:
                    if per_beat=="-":
                        temp=len(verse_interval)
                        verse_interval.append(verse_interval[temp-1])
                        verse_ratio.append(verse_ratio[temp-1])
                        verse_freq.append(verse_freq[temp-1])


                        # verse_interval[temp-1][2]+=duration
                        # verse_ratio[temp-1][1]+=duration
                        # verse_freq[temp-1][1]+=duration
                    if per_beat==" ":
                        verse_interval.append(["Rest",0,duration])
                        verse_ratio.append([Fraction(0,1),duration])
                        verse_freq.append([0,duration])
            r_interval.append(verse_interval)
            r_ratio.append(verse_ratio)
            r_freq.append(verse_freq)
        return r_interval,r_ratio,r_freq

    def change_key(self):
        self.user.key.set(self.key_choice.get())  ## reset the key
        self.note.note.set(self.key_choice.get())
        ## reverse from intervals to note
        pre_r_interval=self.r_interval
        self.reload()   ## get the previous self.r_interval( pre_r_interval) and different self.interval_note_dic and self.note_interval_dic
        # print(self.interval_note_dic)
        # print(self.note_interval_dic)
        d=self.beat   ## the original duration=60/self.speed
        verse_list=[]
        for i in xrange(self.verse_num):
            verse_interval=pre_r_interval[i]
            beat_list=[]
            for each in verse_interval:#xrange(len(verse_interval)):   [interval_position,octave_index,duration]
                interval_position=each[0]
                octave_index=each[1]
                duration=each[2]
                if interval_position=="Rest":
                    note_str=" ,"
                else:
                    note=self.interval_note_dic[interval_position]
                    if isinstance(note, set):
                        note=random.sample(note,1)[0]
                    note_str=note+str(octave_index)+","
                    n=int(duration/d-1)   ## n number of "-"
                    for j in xrange(n):
                        note_str=note_str+"-,"
                beat_list.append(note_str)
            verse="".join(beat_list).strip(",")+"|"   ## remove the last "," , adding the bar to separate each verse
            verse_list.append(verse)
        melody="".join(verse_list).strip("|")    ## remove the last "|"
        self.user.melody.set(melody)
        # self.user.melody.insert(0,melody)
        # self.user.melodyVar.set(melody)

        self.reload()    # recorrect the self.r_interval

    def change_pattern(self):
        str=self.pattern_choice.get()
        pattern_list=[]
        for each in str:
            pattern_list.append(int(each))
        if len(pattern_list)!=self.beat_num:
            if self.beat_num==4:
                self.pattern_choice.delete(0,END)
                self.pattern_choice.insert(0,"1010")
                return [1,0,1,0]
            elif self.beat_num==6:
                self.pattern_choice.delete(0,END)
                self.pattern_choice.insert(0,"101010")
                return [1,0,1,0,1,0]
            elif self.beat_num==8:
                self.pattern_choice.delete(0,END)
                self.pattern_choice.insert(0,"10101010")
                return [1,0,0,0,1,0,0,0]
        else:
            return pattern_list

    twinkle="C1,C1,G1,G1,A1,A1,G1,-|F1,F1,E1,E1,D1,D1,C1,-"
    stand_by_me="E1,G1,A1,-|E1,G1,-,-|C1,D1,E1,-|D1,E1,-,-|E1,D1,C1,-|C1,E1,D1,D1|D1,C1,E1,G1|E1,G1,A1,-|E1,G1,G1,-|C1,D1,E1,-|E1,D1,C1,-|C1,D1,E1,D1|C1,E1,D1,-|D1,C1,C1,-"
    every_breath_you_take="C1,Db1,C1,Bb1,Ab1,Ab1|C1,Db1,C1,Bb1,Ab1,Ab1|Ab1,Ab1,C1,Db1,Ab1,-|Ab1,Ab1,Db1,C1,Bb1,-|Bb1,Ab1,C1,Ab1,Ab1,-"
    all_I_want_for_chrismas_is_you="G1,B1,D1,F#1,G1,E1,D1,-|A1,G1,G1,F#1,G1,F#1,E1,D1|B1,D1,G1,A1,B1,A1,G1,E1|" \
                                   "B1,D1,G1,G1,A1,G1,E1,D1|G1,A1,F#1,G1,E1,F#1,D#1,-|G1,A1,A1,G1,E1,F#1,D#1,-|D1,E1,G1,D1,C1,D1,-,-|B1,B1,G1,E1,D1,-,A1,-|B1,-,D1,-,A1,-,-,-"
    # all_of_me="C1,Eb1,-,C1,F1,-|C1,Bb1,-,Ab1,C1,-|C1,C1,Bb1,Bb1,Bb1,Ab1|Bb1,Ab1,-,C1,C1,Bb1|Bb1,Bb1,Ab1,Bb1,Ab1,-|C1,C1,Eb1,-,C1,F1|F1,C1,F1,C1,Bb1,-|" \
    #           "Ab1,C1,-,C1,C1,Bb1|Bb1,Bb1,Ab1,Bb1,Ab1,-|C1,C1,Bb1,Bb1,Bb1,Ab1|Bb1,Ab1,-,C1,C1,Db1|Eb1,Ab1,G1,F1,Eb1,-|C1,C1,-,C1,C1,Db1|Eb1,Ab1,G1,F1,Eb1,-|C1,C1,-,C1,Bb1,-"

    def change_sample(self):
        str=self.user.sample_choice.get()
        melody=None
        if str=="Twinkle":
            melody=self.twinkle
            self.user.key.set("C")
        if str=="Stand by me":
            melody=self.stand_by_me
            self.user.key.set("C")
        if str=="Every breath you take":   #"C1,Db1,C1,Bb1,Ab1,Ab1|C1,Db1,C1,Bb1,Ab1,Ab1|Ab1,Ab1,C1,Db1,Ab1,-|Ab1,Ab1,Db1,C1,Bb1,-|Bb1,Ab1,C1,Ab1,Ab1,-":
            melody=self.every_breath_you_take
            self.user.key.set("G#")
        if str=="All I want for Chrismas is You":
            melody=self.all_I_want_for_chrismas_is_you
            self.user.key.set("C")
        self.user.melody.set(melody)


    def chord_analize(self):
        # pattern=[1,0,1,0,1,0]
        l=len(self.pattern)
        ## analyze the self.r_interval
        d=self.beat
        new_r_interval=[]
        for i in xrange(self.verse_num):
            new_verse=[]
            verse=self.r_interval[i]   ## current verse
            for j in xrange(len(verse)):
                interval_position=verse[j][0]
                octave_index=verse[j][1]
                duration=verse[j][2]
                num=int(duration/d)
                for k in xrange(num):
                    new_verse.append([interval_position,octave_index])
            new_r_interval.append(new_verse)
        ## after separating each verse into each beat

        chord_data_list=[]    ##only contain self.verse_num num of chord data for each verse
        for i in xrange(self.verse_num):
            chord_data=[]
            verse=new_r_interval[i]

            m=0
            n=0
            while m<l-1:
                if self.pattern[m]==0:
                    n+=1
                if self.pattern[m]==1:
                    interval_position,octave_index=verse[m]
                    volume=0.3      #self.volume*0.6
                    temp=self.get_chord(interval_position,octave_index,volume)
                    temp_shape=temp.shape
                    pause=np.int16(np.zeros(temp_shape*n))
                    if n!=0:
                        chord_data.append(pause)
                        n-=1
                    chord_data.append(temp)
                    m+=1
                    while m<l:
                        if self.pattern[m]==0:
                            volume=volume*0.5
                            data=self.get_chord(interval_position,octave_index,volume)
                            chord_data.append(data)
                            m+=1
                        else:
                            break
                    while m<l:
                        interval,octave=verse[m]
                        if interval=="Rest":
                            volume=volume*0.5
                            data=self.get_chord(interval_position,octave_index,volume)
                            chord_data.append(data)
                            m+=1
                        else:
                            break

            chord_data_list.append(chord_data)
        return chord_data_list



    def get_chord(self,interval_position,octave_index,volume):
        chord_dic={'1':(["4","M6","1"],["M3","5","1"]),
                        'm2':["4","M6","m2"],
                        'M2':["5","M7","M2"],
                        'm3':["5","M7","m3"],
                        'M3':["5","1","M3"],
                        '4':["M6","1","4"],
                        'b5':["m7","m2","b5"],
                        '5':(["M7","M2","5"],["1","M3","5"]),
                        'm6':["1","m3","m6"],
                        'M6':["1","4","M6"],
                        'm7':["M2","4","m7"],
                        'M7':["M2","5","M7"]}
        chord_list=chord_dic[interval_position]
        if isinstance(chord_list,tuple):
            chord_list=chord_list[1]
        interval0,interval1,interval2=chord_list
        ratio2=self.scale_dic[interval2]*octave_index
        ratio1=self.scale_dic[interval1]*octave_index
        ratio0=self.scale_dic[interval0]*octave_index
        if ratio2<ratio1:
            ratio1=ratio1/2
        if ratio2<ratio0:
            ratio0=ratio0/2
        note0=WaveSine.get_wavedata(ratio0*self.root_freq,volume,self.beat)
        note1=WaveSine.get_wavedata(ratio1*self.root_freq,volume,self.beat)
        note2=WaveSine.get_wavedata(ratio2*self.root_freq,volume,self.beat)

        note0_shape,=note0.shape
        note1_shape,=note1.shape
        note2_shape,=note2.shape
        note1_add=np.concatenate([np.int16(np.zeros(note0_shape-note1_shape)),note1])
        note2_add=np.concatenate([np.int16(np.zeros(note0_shape-note2_shape)),note2])
        data=WaveSine.pack(note0,note1_add,note2_add)
        return data

    def get_chorus1(self):
        chorus_data1=[]
        for i in xrange(self.verse_num):
            verse_wavedata=[]
            for j in xrange(len(self.r_freq[i])):
                freq,duration=self.r_freq[i][j]
                wavedata=WaveSine.get_timberdata(freq=freq+1,volume_list=self.volume_list,duration=duration)
                verse_wavedata.append(wavedata)
            chorus_data1.append(verse_wavedata)
        return chorus_data1

    def get_chorus2(self):
        chorus_data2=[]
        for i in xrange(self.verse_num):
            verse_wavedata=[]
            for j in xrange(len(self.r_freq[i])):
                freq,duration=self.r_freq[i][j]
                wavedata=WaveSine.get_timberdata(freq=freq+2,volume_list=self.volume_list,duration=duration)
                verse_wavedata.append(wavedata)
            chorus_data2.append(verse_wavedata)
        return chorus_data2


    def get_melody_data(self):
        melody_data=[]
        for i in xrange(self.verse_num):
            verse_wavedata=[]
            for j in xrange(len(self.r_freq[i])):
                freq,duration=self.r_freq[i][j]
                # print(freq)
                # WaveSine.play(WaveSine.get_wavedata(freq))
                wavedata=WaveSine.get_timberdata(freq=freq,volume_list=self.volume_list,duration=duration)
                verse_wavedata.append(wavedata)
            melody_data.append(verse_wavedata)
        # WaveSine.play(melody_data)
        return melody_data


    def duet(self,i,j):
        def callback(i,j):
            if i==0 and j==0:
                sleep=self.beat*0.1
                time.sleep(sleep)

            p=pyaudio.PyAudio()
            stream=p.open(format=pyaudio.paInt16,
                          channels=1,
                          rate=44100,
                          output=True,)

            # for i in xrange(self.verse_num):
            #     for j in xrange(self.beat_num):
            #         per_beat=np.int16(self.melody_data[i][j]*0.2)
            #         stream.write(per_beat)
            per_beat=np.int16(self.melody_data[i][j]*0.3)
            stream.write(per_beat)

            stream.close()
            p.terminate()

        threading.Thread(target=callback,args=(i,j,)).start()

    myLock=threading.Lock()

    def play(self):
        def callback():
            self.reload()
            song=[]
            duel_bool=False
            for i in xrange(self.verse_num):
                verse=[]
                for j in xrange(self.beat_num):
                    data=self.melody_data[i][j]
                    if self.setting.chord_bool.get():
                        data=data+self.chord_data[i][j]
                    if self.setting.chorus_bool1.get():
                        data=data+self.chorus_data1[i][j]/2
                    if self.setting.chorus_bool2.get():
                        data=data+self.chorus_data2[i][j]/2
                    verse.append(data)
                song.append(verse)
            if self.setting.duel_bool.get():
                duel_bool=True


            def update(i,j):
                per_freq=self.r_freq[i][j][0]
                per_interval=self.r_interval[i][j][0]
                if per_interval!="Rest":
                    per_note=self.interval_note_dic[per_interval]
                    self.note.interval.set(per_interval)
                    if isinstance(per_note,set):
                        for each in per_note:
                            if each in ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]:
                                self.note.note.set(each)
                    else:
                        self.note.note.set(per_note)

                    self.note.freq_str.set(str(per_freq)+"Hz")
                    file=open("freq.txt","w")
                    file.write(str(per_freq))
                    file.close()




            GUI.myLock.acquire(True)

            p=pyaudio.PyAudio()
            stream=p.open(format=pyaudio.paInt16,
                          channels=1,
                          rate=44100,
                          output=True,)

            for i in xrange(self.verse_num):
                for j in xrange(self.beat_num):
                    per_beat=song[i][j]
                    threading.Thread(target=update,args=(i,j,)).start()
                    stream.write(per_beat)
                    if duel_bool:
                        threading.Thread(target=self.duet,args=(i,j,)).start()


            stream.close()
            p.terminate()

            GUI.myLock.release()

        self.t=threading.Thread(target=callback)
        self.t.daemon=True
        self.t.start()

file=open("freq.txt","w")
file.write(str(264))
file.close()

app=GUI()

ani=animation.FuncAnimation(fig=f,func=animate,interval=1000)
app.mainloop()




