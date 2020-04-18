import json
import copy
import string
import random
from pp_utils import Monitor

"""
31/12/2016 - fixed crash if mediashow id shffled and there is one track - taks Drew Keller
"""


# *************************************
# MEDIALIST CLASS
# ************************************

class MediaList(object):
    """
    manages a media list of tracks and the track selected from the medialist
    """
    

    def __init__(self,sequence):
        self.clear()
        self.mon=Monitor()
        self.sequence=sequence
        
 # Functions for the editor dealing with complete list

    def clear(self):
        self._tracks = []  #MediaList, stored as a list of dicts
        self._num_tracks=0
        self._selected_track_index=-1 # index of currently selected track

    def print_list(self):
        print('\n')
        print(self._tracks)

    def first(self):
        self._selected_track_index=-1
        self.next(self.sequence) #let this do the work of randomaising or  advancing to 0

    def length(self):
        return self._num_tracks

    def append(self, track_dict):
        # print '\ntrack dict',track_dict
        """appends a track dictionary to the end of the medialist store"""
        self._tracks.append(copy.deepcopy(track_dict))
        self._num_tracks+=1

    def update(self,index,values):
        self._tracks[index].update(values)


    def remove(self,index):
        self._tracks.pop(index)
        self._num_tracks-=1
        # deselect any track, saves worrying about whether index needs changing
        self._selected_track_index=-1

    def move_up(self):
        if self._selected_track_index != 0:
            self._tracks.insert(self._selected_track_index-1, self._tracks.pop(self._selected_track_index))
            self.select(self._selected_track_index-1)

    def move_down(self):
        if self._selected_track_index != self._num_tracks-1:
            self._tracks.insert(self._selected_track_index+1, self._tracks.pop(self._selected_track_index))
            self.select(self._selected_track_index+1)

    def copy(self):
        self._tracks.insert(self._selected_track_index+1, copy.deepcopy(self._tracks[self._selected_track_index]))
        self._num_tracks+=1
        self.select(self._selected_track_index+1)


    def replace(self,index,replacement):
        self._tracks[index]= replacement     
        
        
# Common functions work for anything
           

    def track_is_selected(self):
        if self._selected_track_index>=0:
            return True
        else:
            return False
            
    def selected_track_index(self):
        return self._selected_track_index

    def track(self,index):
        return self._tracks[index]

    def selected_track(self):
        """returns a dictionary containing all fields in the selected track """
        return self._selected_track

    def select(self,index):
        """does housekeeping necessary when a track is selected"""
        if self._num_tracks>0 and index>=0 and index< self._num_tracks:
            self._selected_track_index=index
            self._selected_track = self._tracks[index]
            return True
        else:
            return False

# Dealing with anonymous tracks for use and display

  
     
    def at_end(self):
        # true is selected track is last anon
        index=self._num_tracks-1
        while index>=0:
            if self._tracks[index] ['track-ref'] =="":
                end=index
                if self._selected_track_index==end:
                    return True
                else:
                    return False
            index -=1
        return False
        
        
    def index_of_end(self):
        if self.anon_length()==0:
            return False
        index=self._num_tracks-1
        while index >= 0:
            if self._tracks[index] ['track-ref'] =="":
                return index
            index -=1
        return -1
   
   
    def at_start(self):
        if self.anon_length()==0:
            return False
        index=0
        while index<self._num_tracks:
            if self._tracks[index] ['track-ref'] =="":
                start =  index
                if self._selected_track_index==start:
                    return True
                else:
                    return False
            index +=1
        return False
   
            
    def index_of_start(self):
        if self.anon_length()==0:
            return False
        index=0
        while index<self._num_tracks:
            if self._tracks[index] ['track-ref'] =="":
                return index
            index +=1
        return False


    def anon_length(self):
        # number of anonymous tracks
        count=0
        index=0
        while index<self._num_tracks:
            if self._tracks[index] ['track-ref'] =="":
                count+=1
            index +=1
        return count

    def start(self):
        if self.anon_length()==0:
            return False
        # select first anonymous track in the list
        if self.sequence == 'ordered':
            index=0
            while index<self._num_tracks:
                if self._tracks[index] ['track-ref'] =="":
                    self.select(index)
                    return True
                index +=1
            return False
        else:
            match=random.randint(0,self.anon_length()-1)
            # print 'match',match
            index=0
            while index<self._num_tracks:
                if self._tracks[index] ['track-ref'] =="" and index==match:
                    self.select(index)
                    # print index
                    return index
                index +=1

    def finish(self):
        if self.anon_length()==0:
            return False
        if self.sequence == 'ordered':
            # select last anymous track in the list
            index=self._num_tracks-1
            while index>=0:
                if self._tracks[index] ['track-ref'] =="":
                    self.select(index)
                    return True
                index -=1
            return False
        else:
            match=random.randint(0,self.anon_length()-1)
            # print 'match',match
            index=0
            while index<self._num_tracks:
                if self._tracks[index] ['track-ref'] =="" and index==match:
                    self.select(index)
                    # print index
                    return index
                index +=1
        

    def select_anon_by_index(self,wanted):
        if self.anon_length()==0:
            return False
        index=0
        anon_index=0
        while index != self._num_tracks:
            # print index,self._tracks[index] ['track-ref'],wanted
            if self._tracks[index] ['track-ref'] =="":
                if anon_index==wanted:
                    # print 'match\n'
                    self.select(index)
                    return True
                anon_index+=1
            index= index+1
        return False


    def next(self,sequence):
        if self.anon_length()==0:
            return False
        if sequence=='ordered':
            if self._selected_track_index== self._num_tracks-1:
                index=0
            else:
                index= self._selected_track_index+1
                
            end=self._selected_track_index
        else:
            index=random.randint(0,self.anon_length()-1)
            if index==0:
                end=self._num_tracks-1
            else:
                end=index-1
        # search for next anonymous track
        # print 'index', index, 'end',end
        while index != end:
            if self._tracks[index] ['track-ref'] =="":
                self.select(index)
                return True
            if index== self._num_tracks-1:
                index=0
            else:
                index= index+1
        return False

    def previous(self,sequence):
        if self.anon_length()==0:
            return False
        if sequence=='ordered':
            if self._selected_track_index == 0:
                index=self._num_tracks-1
            else:
                index= self._selected_track_index-1
            end = self._selected_track_index
        else:
            index=random.randint(0,self.anon_length()-1)
            if index==self._num_tracks-1:
                end=0
            else:
                end=index+1
        # print 'index', index, 'end',end                
        # search for previous anonymous track            
        while index != end :
            if self._tracks[index] ['track-ref'] =="":
                self.select(index)
                return True                
            if index == 0:
                index=self._num_tracks-1
            else:
                index= index-1
        return False
    
    
# Lookup for labelled tracks
    
    
    def index_of_track(self,wanted_track):
        index = 0
        for track in self._tracks:
            if track['track-ref']==wanted_track:
                return index
            index +=1
        return -1




# open and save

    def add_track_for_file(self, filename, filetype):
        """
        Simulates adding an image or video as if it was coming from a media list.
        :param filename: The image to add
        :return:
        """

        track = {}
        track["type"] = filetype
        track["location"] = filename
        track["track-ref"] = ""
        track["background-image"] = ""
        track["background-colour"] = ""
        track["animate-begin"] = ""
        track["animate-end"] = ""
        track["duration"] = ""
        track["image-window"] = "fit"
        track["image-rotation"] = ""
        track["image-rotate"] = "0"
        track["pause-timeout"] = ""
        track["plugin"] = ""
        track["track-html-background-colour"] = "white"
        track["track-html-height"] = "300"
        track["track-html-width"] = "300"
        track["track-text-x"] = ""
        track["track-text-y"] = ""
        track["track-text-justify"] = ""
        track["track-text-font"] = ""
        track["track-text-colour"] = ""
        track["track-text-location"] = ""
        track["track-text-type"] = "plain"
        track["track-text"] = ""
        track["display-show-background"] = ""
        track["show-control-begin"] = ""
        track["show-control-end"] = ""
        track["thumbnail"] = ""
        track["transition"] = "cut"
        track["pause-text"] = ""
        track["animate-clear"] = ""

        track["omx-audio"] = ""
        track["cmx-audio"] = ""
        track["omx-volume"] = ""
        track["omx-window"] = ""
        track["omx-other-options"] = ""
        track["freeze-at-start"] = ""
        track["freeze-at-end"] = ""
        track["seamless-loop"] = ""
        track["pause-timeout"] = ""

        self._tracks.append(track)
        self._num_tracks = len(self._tracks)
        self.mon.log(self, "Added file " + filename)

    def open_directory(self,directory, match_glob, exclude_regex):
        """
        Opens a directory as if it was a tracklist of all the files in the directory.
        Right now, we're hard-coding the files to look for to .jpg files ... but
        extending it would be fairly straightforward ...
        :param directory: Directory to scan for files and load everything with a matching extension.  Lame
                          error-checking -- be sure no trailing slash
        :param match_glob: A set of file-specs to scan for and match.  The list itself is separated by |.  Then
                           each item in the list consists of a glob-type match, separated by # from the type
                           (image or video) that we're matching.
                           i.e., glob#type|glob#type|glob#type
                           e.g., /**/*.jpg#image|/**/*.mpg#video
        :param exclude_regex: A regular expression indicating files to skip
        :return:
        """

        self.clear()

        self.mon.log(self, "Adding files matching " + match_glob + " from " + directory)
        self.mon.log(self, "Excluding files: " + exclude_regex)

        import glob
        import re
        if len(exclude_regex) > 0:
            matcher = re.compile(exclude_regex)
        else:
            matcher = None

        pats = match_glob.split("|")
        for each_pat in pats:
            thisglob, type = each_pat.split("#")
            self.mon.log(self, "Matching glob " + thisglob)
            for filename in glob.iglob(directory + thisglob):
                if matcher is None or not matcher.match(filename):
                    self.add_track_for_file(filename, type)

        self.mon.log(self, "Loaded " + str(self._num_tracks) + " files.")

        self.last_num_tracks = self._num_tracks

        return True


    def open_list(self,filename,profile_version):
        """
        opens a saved medialist
        medialists are stored as json arrays.
        """
        ifile  = open(filename, 'r')
        mdict = json.load(ifile)
        ifile.close()
        if 'issue' in mdict:
            self.medialist_version_string= mdict['issue']
        else:
            self.medialist_version_string="1.0"

        # If the media file contains a loaddir key, then treat this as a directory to load, instead of a single file.
        #   loaddir:  the directory to (recursively) load
        #   exclude-regex:  optional - a regular expression to use to exclude files from the load (I use to exclude
        #                   directories)
        #   match-glob: a list of glob specs and types separated by |, where the glob spec and type are separated by #
        # e.g.:
        #   "loaddir":"/media/some-pictures"
        #   "exclude-regex":".*\\/(skip-this-dir|skip-this-dir-also)\\/.*"
        #   "match-glob":"//**/*.jpg#image|/**/*.JPG#image|/**/*.gif#image|/**/*.GIF#image|/***/*.mpg#video"
        if 'loaddir' in mdict:
            if 'match-glob' in mdict:
                match_glob = mdict['match-glob']
            else:
                match_glob = "/**/*.jpg"
            if 'exclude-regex' in mdict:
                exclude_regex = mdict['exclude-regex']
            else:
                exclude_regex = ''
            return self.open_directory(mdict['loaddir'], match_glob, exclude_regex)
        else:
            self._tracks = mdict['tracks']

            if self.medialist_version()==profile_version:
                self._num_tracks=len(self._tracks)
                self.last_num_tracks=self._num_tracks
                self._selected_track_index=-1
                return True
            else:
                return False

    def medialist_version(self):
        vitems=self.medialist_version_string.split('.')
        if len(vitems)==2:
            # cope with 2 digit version numbers before 1.3.2
            return 1000*int(vitems[0])+100*int(vitems[1])
        else:
            return 1000*int(vitems[0])+100*int(vitems[1])+int(vitems[2])



    # dummy for mediliast, in livelist the list is created from the live_track directories
    def use_new_livelist(self):
        pass

    def create_new_livelist(self):
        pass

    def new_length(self):
        return self.length()

    # for medialist the content of the list never changes so return False
    def livelist_changed(self):
            return False

    def save_list(self,filename):
        """ save a medialist """
        if filename=="":
            return False
        dic={'issue':self.medialist_version_string,'tracks':self._tracks}
        filename=str(filename)
        filename = str.replace(filename,'\\','/')
        tries = 1
        while tries<=10:
            # print "save  medialist  ",filename
            try:
                ofile  = open(filename, "w")
                json.dump(dic,ofile,sort_keys=True,indent=1)
                ofile.close()
                self.mon.log(self,"Saved medialist "+ filename)
                break
            except IOError:
                self.mon.err(self,"failed to save medialist, trying again " + str(tries))
                tries+=1
        return




