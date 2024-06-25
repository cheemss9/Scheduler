#Imports the modules needed
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager, NoTransition, CardTransition
from kivy.uix.dropdown import DropDown
from kivy.properties import BooleanProperty
from kivy.graphics import Color, RoundedRectangle
import kivy.utils
from kivy.utils import platform
from kivy.uix.image import Image
from kivy.clock import Clock
from functools import partial
from kivy.uix.button import ButtonBehavior
from kivy.config import Config
import random
import sys
import os
import shutil
from datetime import datetime
from datetime import date
import time
Config.set('graphics', 'width', '16')
Config.set('graphics', 'height', '9')
Config.set('graphics', 'resizable', True)
sys.path.append("/".join(x for x in __file__.split("/")[:-1]))

#Includes the home window the buttons, the processes where you can add schedules and alarms or delete it or edit
class ImageButton(ButtonBehavior, Image):
    pass

class MainScreen( Screen ):
    pass


class ShowScheduleScreen( Screen ):
    pass

class ShowAlarmScreen( Screen ):
    pass

class AddScheduleScreen( Screen ):
    pass

class AddAlarmScreen( Screen ):
    pass

#The main class that includes all of the processes
class MainApp( App ):
    def build( self ):
        self.root_directory = os.getcwd()
        self.init_global_vars()

        return Builder.load_file("main.kv")
    #Updates all the widgets
    def on_start ( self ):
        self.update_all_widgets()
        self.check_notifications = Clock.schedule_interval( self.delay, 20)

    
    def delay ( self, dt ):
        self.weekdays = [ "monday" , "tuesday" , "wednesday" , "thursday" , "friday" , "saturday" , "sunday" ]
        self.t = time.localtime()
        self.current_time = time.strftime( "%H:%M", self.t )
        print ( self.current_time )
        self.weekday = self.weekdays[ date.today().weekday() ]
        print ( self.weekday )
        self.day_to_check = [line.strip() for line in open( os.path.join( self.alarm_list_directory , self.weekday + ".txt" ))]
        print( self.day_to_check )
        for i in range ( len ( self.day_to_check ) ):
            self.temp_alarm_info = self.get_alarm_info ( self.day_to_check[i] )
            if self.temp_alarm_info[1][0] == self.current_time:
                print ( self.temp_alarm_info[1][0] )
                self.alarm_title = self.temp_alarm_info[0][0]
                self.alarm_day = self.temp_alarm_info[0][1]
                self.show_alarm( alarm_title = self.alarm_title )
                return
                
    #Updates the date and the schedules indicated
    def update_all_widgets( self ):
        self.update_widgets( "monday" )
        self.update_widgets( "tuesday" )
        self.update_widgets( "wednesday" )
        self.update_widgets( "thursday" )
        self.update_widgets( "friday" )
        self.update_widgets( "saturday" )
        self.update_widgets( "sunday" )
        
     #The data inputted by the user will go into the text file within the folder
    def init_global_vars ( self ):
        self.root_directory = os.getcwd()
        self.sched_list_directory = os.path.join( self.root_directory, "sched_list" )
        self.schedules_directory = os.path.join( self.root_directory, "schedules" )
        self.sched_list_monday = [line.strip() for line in open( os.path.join( self.sched_list_directory , "monday.txt" ))]
        self.sched_list_tuesday = [line.strip() for line in open( os.path.join( self.sched_list_directory , "tuesday.txt" ))]
        self.sched_list_wednesday = [line.strip() for line in open( os.path.join( self.sched_list_directory , "wednesday.txt" ))]
        self.sched_list_thursday = [line.strip() for line in open( os.path.join( self.sched_list_directory , "thursday.txt" ))]
        self.sched_list_friday = [line.strip() for line in open( os.path.join( self.sched_list_directory , "friday.txt" ))]
        print ( self.sched_list_monday )
        self.alarm_list_directory = os.path.join( self.root_directory, "alarm_list" )
        self.alarm_directory = os.path.join( self.root_directory, "alarms" )
        self.alarm_list_monday = [line.strip() for line in open( os.path.join( self.alarm_list_directory , "monday.txt" ))]
        self.alarm_list_tuesday = [line.strip() for line in open( os.path.join( self.alarm_list_directory , "tuesday.txt" ))]
        self.alarm_list_wednesday = [line.strip() for line in open( os.path.join( self.alarm_list_directory , "wednesday.txt" ))]
        self.alarm_list_thursday = [line.strip() for line in open( os.path.join( self.alarm_list_directory , "thursday.txt" ))]
        self.alarm_list_friday = [line.strip() for line in open( os.path.join( self.alarm_list_directory , "friday.txt" ))]
    #The data inputted will be a logo or  picture inside the indicated date (alarm)
    def show_schedule ( self, *args, sched_title ):
        app = App.get_running_app()
        self.sched_title = sched_title
        self.schedule_info = self.get_sched_info ( self.sched_title )
        self.sched_day = self.schedule_info[0][1]
        app.root.ids['ShowScheduleScreen'].ids['error_message'].text = ""
        app.root.ids['ShowScheduleScreen'].ids['schedTitle_TextInput'].text = self.schedule_info[0][0]
        app.root.ids['ShowScheduleScreen'].ids['schedDay_TextInput'].text = self.sched_day
        print ( self.schedule_info )
        self.sched_note = ""
        for i in range ( len(self.schedule_info[1]) ):
            self.sched_note += self.schedule_info[1][i]
        app.root.ids['ShowScheduleScreen'].ids['schedNote_TextInput'].text = self.sched_note
        
        print ( " clicked " , self.sched_title)
        app.root.current = "ShowScheduleScreen"

    #The data inputted will be a logo or  picture inside the indicated date (schedule)
    def show_alarm ( self, *args, alarm_title ):
        app = App.get_running_app()
        self.alarm_title = alarm_title
        self.alarm_info = self.get_alarm_info ( self.alarm_title )
        self.alarm_day = self.alarm_info[0][1]
        app.root.ids['ShowAlarmScreen'].ids['error_message'].text = ""
        app.root.ids['ShowAlarmScreen'].ids['alarmTitle_TextInput'].text = self.alarm_info[0][0]
        app.root.ids['ShowAlarmScreen'].ids['alarmDay_TextInput'].text = self.alarm_info[0][1]
        app.root.ids['ShowAlarmScreen'].ids['alarmTime_TextInput'].text = self.alarm_info[1][0]
        
        app.root.current = "ShowAlarmScreen"

    def update_widgets ( self, day ):
        self.day = day.lower()
        self.schedules_widgets_to_update = [line.strip() for line in open( os.path.join( self.sched_list_directory , self.day + ".txt" ))]
        self.alarm_widgets_to_update = [line.strip() for line in open( os.path.join( self.alarm_list_directory , self.day + ".txt" ))]
        print ( self.schedules_widgets_to_update )
        self.root.ids['MainScreen'].ids[ self.day + "_scrollview"].clear_widgets()
        for i in range ( len( self.schedules_widgets_to_update )):
            print ( self.schedules_widgets_to_update[i] )
            self.sched_Title = self.schedules_widgets_to_update[i]
            self.imgButton = ImageButton(source="resources/buttons/schedule_button.jpg", on_release=partial(self.show_schedule, sched_title = self.schedules_widgets_to_update[i]))
            self.root.ids['MainScreen'].ids[ self.day + "_scrollview"].add_widget(self.imgButton)
        for i in range ( len( self.alarm_widgets_to_update )):
            print ( self.alarm_widgets_to_update[i] )
            self.sched_Title = self.alarm_widgets_to_update[i]
            self.imgButton = ImageButton(source="resources/buttons/alarm_roundbutton.jpg", on_release=partial(self.show_alarm, alarm_title = self.alarm_widgets_to_update[i]))
            self.root.ids['MainScreen'].ids[ self.day + "_scrollview"].add_widget(self.imgButton)
        
    #This function processes the addition of schedule inside the program   
    def add_schedule( self, sched_title, sched_day, sched_note ):
        app = App.get_running_app()
        self.sched_title = sched_title
        self.sched_day = sched_day.lower()
        self.sched_note = sched_note

        self.days_list = [ "monday", "tuesday", "wednesday", "thursday", "friday",
                           "saturday", "sunday" ]

        if self.sched_title != "" and self.sched_day != "" and self.sched_note != "" and self.sched_day in self.days_list :
            if self.sched_title in self.sched_list_monday:
                app.root.ids['AddScheduleScreen'].ids['error_message'].text = "INVALID INPUT: Schedule Title Already Exists"
                app.root.ids['AddScheduleScreen'].ids['schedTitle_TextInput'].text = ""
                app.root.ids['AddScheduleScreen'].ids['schedDay_TextInput'].text = ""
                app.root.ids['AddScheduleScreen'].ids['schedNote_TextInput'].text = ""
                print ( "error" )
            elif self.sched_title in self.sched_list_tuesday:
                app.root.ids['AddScheduleScreen'].ids['error_message'].text = "INVALID INPUT: Schedule Title Already Exists"
                app.root.ids['AddScheduleScreen'].ids['schedTitle_TextInput'].text = ""
                app.root.ids['AddScheduleScreen'].ids['schedDay_TextInput'].text = ""
                app.root.ids['AddScheduleScreen'].ids['schedNote_TextInput'].text = ""
                print ( "error" )
            elif self.sched_title in self.sched_list_wednesday:
                app.root.ids['AddScheduleScreen'].ids['error_message'].text = "INVALID INPUT: Schedule Title Already Exists"
                app.root.ids['AddScheduleScreen'].ids['schedTitle_TextInput'].text = ""
                app.root.ids['AddScheduleScreen'].ids['schedDay_TextInput'].text = ""
                app.root.ids['AddScheduleScreen'].ids['schedNote_TextInput'].text = ""
                print ( "error" )
            elif self.sched_title in self.sched_list_thursday:
                app.root.ids['AddScheduleScreen'].ids['error_message'].text = "INVALID INPUT: Schedule Title Already Exists"
                app.root.ids['AddScheduleScreen'].ids['schedTitle_TextInput'].text = ""
                app.root.ids['AddScheduleScreen'].ids['schedDay_TextInput'].text = ""
                app.root.ids['AddScheduleScreen'].ids['schedNote_TextInput'].text = ""
                print ( "error" )
            elif self.sched_title in self.sched_list_friday:
                app.root.ids['AddScheduleScreen'].ids['error_message'].text = "INVALID INPUT: Schedule Title Already Exists"
                app.root.ids['AddScheduleScreen'].ids['schedTitle_TextInput'].text = ""
                app.root.ids['AddScheduleScreen'].ids['schedDay_TextInput'].text = ""
                app.root.ids['AddScheduleScreen'].ids['schedNote_TextInput'].text = ""
                print ( "error" )
            else:
                self.add_sched_directory = os.path.join( self.schedules_directory, self.sched_title )
                if not os.path.exists( self.add_sched_directory ):
                    os.makedirs( self.add_sched_directory )
                self.schedInfo_Txt = open( os.path.join( self.add_sched_directory
                                                  , "sched_Info.txt" ) , "w" )
                self.schedInfo_Txt.write( self.sched_title + "\n" )
                self.schedInfo_Txt.write( self.sched_day + "\n" )
                self.schedInfo_Txt.close()
                
                self.schedNote_Txt = open( os.path.join( self.add_sched_directory
                                                  , "sched_note.txt" ) , "w" )
                self.schedNote_Txt.write( self.sched_note + "\n" )
                self.schedNote_Txt.close()

                self.schedDay_list = [ line.strip() for line in
                                 open ( os.path.join( self.sched_list_directory
                                                      , self.sched_day + ".txt" )) ]
                self.schedDay_list.append ( self.sched_title )
                print( self.schedDay_list )
                
                self.schedDay_Txt = open ( os.path.join( self.sched_list_directory , self.sched_day + ".txt" ), "w") 
                for i in range ( len ( self.schedDay_list ) ):
                    self.schedDay_Txt.write( self.schedDay_list[i] + "\n" )
                    print( self.schedDay_list[i] )
                self.schedDay_Txt.close()

                self.root.current = "MainScreen"
                app.root.ids['AddScheduleScreen'].ids['schedTitle_TextInput'].text = ""
                app.root.ids['AddScheduleScreen'].ids['schedDay_TextInput'].text = ""
                app.root.ids['AddScheduleScreen'].ids['schedNote_TextInput'].text = ""
        else:
            app.root.ids['AddScheduleScreen'].ids['error_message'].text = "INVALID INPUT"
            app.root.ids['AddScheduleScreen'].ids['schedTitle_TextInput'].text = ""
            app.root.ids['AddScheduleScreen'].ids['schedDay_TextInput'].text = ""
            app.root.ids['AddScheduleScreen'].ids['schedNote_TextInput'].text = ""

    #This function processes the addition of alarm inside the program
    def add_alarm( self, alarm_title, alarm_day, alarm_time ):
        app = App.get_running_app()
        self.alarm_title = alarm_title
        self.alarm_day = alarm_day.lower()
        self.alarm_time = alarm_time

        self.days_list = [ "monday", "tuesday", "wednesday", "thursday", "friday",
                           "saturday", "sunday" ]
        self.isTime = self.isTimeFormat( self.alarm_time )
        print( self.isTime )
        if self.alarm_title != "" and self.alarm_day != "" and self.alarm_time != "" and self.alarm_day in self.days_list and self.isTime :
            if self.alarm_title in self.alarm_list_monday:
                app.root.ids['AddAlarmScreen'].ids['error_message'].text = "INVALID INPUT: Alarm Title Already Exists"
                app.root.ids['AddAlarmScreen'].ids['alarmTitle_TextInput'].text = ""
                app.root.ids['AddAlarmScreen'].ids['alarmDay_TextInput'].text = ""
                app.root.ids['AddAlarmScreen'].ids['alarmTime_TextInput'].text = ""
                print ( "error" )
            elif self.alarm_title in self.alarm_list_tuesday:
                app.root.ids['AddAlarmScreen'].ids['error_message'].text = "INVALID INPUT: Alarm Title Already Exists"
                app.root.ids['AddAlarmScreen'].ids['alarmTitle_TextInput'].text = ""
                app.root.ids['AddAlarmScreen'].ids['alarmDay_TextInput'].text = ""
                app.root.ids['AddAlarmScreen'].ids['alarmTime_TextInput'].text = ""
                print ( "error" )
            elif self.alarm_title in self.alarm_list_wednesday:
                app.root.ids['AddAlarmScreen'].ids['error_message'].text = "INVALID INPUT: Alarm Title Already Exists"
                app.root.ids['AddAlarmScreen'].ids['alarmTitle_TextInput'].text = ""
                app.root.ids['AddAlarmScreen'].ids['alarmDay_TextInput'].text = ""
                app.root.ids['AddAlarmScreen'].ids['alarmTime_TextInput'].text = ""
                print ( "error" )
            elif self.alarm_title in self.alarm_list_thursday:
                app.root.ids['AddAlarmScreen'].ids['error_message'].text = "INVALID INPUT: Alarm Title Already Exists"
                app.root.ids['AddAlarmScreen'].ids['alarmTitle_TextInput'].text = ""
                app.root.ids['AddAlarmScreen'].ids['alarmDay_TextInput'].text = ""
                app.root.ids['AddAlarmScreen'].ids['alarmTime_TextInput'].text = ""
                print ( "error" )
            elif self.alarm_title in self.alarm_list_friday:
                app.root.ids['AddAlarmScreen'].ids['error_message'].text = "INVALID INPUT: Alarm Title Already Exists"
                app.root.ids['AddAlarmScreen'].ids['alarmTitle_TextInput'].text = ""
                app.root.ids['AddAlarmScreen'].ids['alarmDay_TextInput'].text = ""
                app.root.ids['AddAlarmScreen'].ids['alarmTime_TextInput'].text = ""
                print ( "error" )
            else:
                self.add_alarm_directory = os.path.join( self.alarm_directory, self.alarm_title )
                if not os.path.exists( self.add_alarm_directory ):
                    os.makedirs( self.add_alarm_directory )
                self.alarmInfo_Txt = open( os.path.join( self.add_alarm_directory
                                                  , "alarm_Info.txt" ) , "w" )
                self.alarmInfo_Txt.write( self.alarm_title + "\n" )
                self.alarmInfo_Txt.write( self.alarm_day + "\n" )
                self.alarmInfo_Txt.close()
                
                self.alarmTime_Txt = open( os.path.join( self.add_alarm_directory
                                                  , "alarm_time.txt" ) , "w" )
                self.alarmTime_Txt.write( self.alarm_time + "\n" )
                self.alarmTime_Txt.close()

                self.alarmDay_list = [ line.strip() for line in
                                 open ( os.path.join( self.alarm_list_directory
                                                      , self.alarm_day + ".txt" )) ]
                self.alarmDay_list.append ( self.alarm_title )
                print( self.alarmDay_list )
                
                self.alarmDay_Txt = open ( os.path.join( self.alarm_list_directory , self.alarm_day + ".txt" ), "w") 
                for i in range ( len ( self.alarmDay_list ) ):
                    self.alarmDay_Txt.write( self.alarmDay_list[i] + "\n" )
                    print( self.alarmDay_list[i] )
                self.alarmDay_Txt.close()

                self.root.current = "MainScreen"
                app.root.ids['AddAlarmScreen'].ids['alarmTitle_TextInput'].text = ""
                app.root.ids['AddAlarmScreen'].ids['alarmDay_TextInput'].text = ""
                app.root.ids['AddAlarmScreen'].ids['alarmTime_TextInput'].text = ""
        else:
            app.root.ids['AddAlarmScreen'].ids['error_message'].text = "INVALID INPUT"
            app.root.ids['AddAlarmScreen'].ids['alarmTitle_TextInput'].text = ""
            app.root.ids['AddAlarmScreen'].ids['alarmDay_TextInput'].text = ""
            app.root.ids['AddAlarmScreen'].ids['alarmTime_TextInput'].text = ""

    #This function do the alarm inside the program
    def isTimeFormat( self, alarm_time ):
        try:
            time.strptime( alarm_time, "%H:%M" )
            return True
        except ValueError:
            return False
        
    #This function do the updates when the user wants to change the note inside the schedule
    def update_schedule( self, sched_title, sched_day, sched_note ):
        app = App.get_running_app()
        self.update_sched_title = sched_title
        self.update_sched_day = sched_day
        self.sched_note = sched_note
        
        self.update_sched_directory = os.path.join( self.schedules_directory, self.sched_title )

        self.schedNote_Txt = open( os.path.join( self.update_sched_directory
                                                 , "sched_note.txt" ) , "w" )
        self.schedNote_Txt.write( self.sched_note + "\n" )
        self.schedNote_Txt.close()
        self.root.current = "MainScreen"
        app.root.ids['AddScheduleScreen'].ids['schedTitle_TextInput'].text = ""
        app.root.ids['AddScheduleScreen'].ids['schedDay_TextInput'].text = ""
        app.root.ids['AddScheduleScreen'].ids['schedNote_TextInput'].text = ""

    #This function do the updates when the user wants to change the note inside the alarm
    def update_alarm( self, alarm_title, alarm_day, alarm_time ):
        app = App.get_running_app()
        self.update_alarm_title = alarm_title
        self.update_alarm_day = alarm_day
        self.alarm_time = alarm_time

        self.isTime = self.isTimeFormat( self.alarm_time )
        print ( self.isTime )
        if self.isTime:
            self.update_alarm_directory = os.path.join( self.alarm_directory, self.alarm_title )

            self.alarmTime_Txt = open( os.path.join( self.update_alarm_directory
                                                 , "alarm_time.txt" ) , "w" )
            self.alarmTime_Txt.write( self.alarm_time + "\n" )
            self.alarmTime_Txt.close()
            self.root.current = "MainScreen"
            app.root.ids['ShowAlarmScreen'].ids['alarmTitle_TextInput'].text = ""
            app.root.ids['ShowAlarmScreen'].ids['alarmDay_TextInput'].text = ""
            app.root.ids['ShowAlarmScreen'].ids['alarmTime_TextInput'].text = ""
        else:
            app.root.ids['ShowAlarmScreen'].ids['error_message'].text = "INVALID INPUT: Alarm Time not recognized."
    #This function do the removes the schedule data picked by the user
    def remove_schedule( self, sched_title, day ):
        print ( "delete" + day )
        print ( "delete" + sched_title )
        app = App.get_running_app()
        self.remove_sched_title = sched_title
        self.remove_sched_day = day
        self.remove_sched_directory = os.path.join( self.schedules_directory, sched_title )
        try:
            shutil.rmtree( self.remove_sched_directory )
        except:
            print ( "Error" )
        self.schedDay_list = [ line.strip() for line in
                                 open ( os.path.join( self.sched_list_directory
                                                      , self.sched_day + ".txt" )) ]
        self.schedDay_list.remove( self.remove_sched_title )
        self.schedDay_Txt = open ( os.path.join( self.sched_list_directory , self.sched_day + ".txt" ), "w") 
        for i in range ( len ( self.schedDay_list ) ):
            self.schedDay_Txt.write( self.schedDay_list[i] + "\n" )
        self.schedDay_Txt.close()

        self.update_all_widgets()
        self.root.current = "MainScreen"
        app.root.ids['ShowScheduleScreen'].ids['schedTitle_TextInput'].text = ""
        app.root.ids['ShowScheduleScreen'].ids['schedDay_TextInput'].text = ""
        app.root.ids['ShowScheduleScreen'].ids['schedNote_TextInput'].text = ""
        
    #This function do the removes the alarm data picked by the user
    def remove_alarm( self, alarm_title, day ):
        print ( "delete" + day )
        print ( "delete" + alarm_title )
        app = App.get_running_app()
        self.remove_alarm_title = alarm_title
        self.remove_alarm_day = day
        self.remove_alarm_directory = os.path.join( self.alarm_directory, alarm_title )
        try:
            shutil.rmtree( self.remove_alarm_directory )
        except:
            print ( "Error" )
        self.alarmDay_list = [ line.strip() for line in
                                 open ( os.path.join( self.alarm_list_directory
                                                      , self.alarm_day + ".txt" )) ]
        self.alarmDay_list.remove( self.remove_alarm_title )
        self.alarmDay_Txt = open ( os.path.join( self.alarm_list_directory , self.alarm_day + ".txt" ), "w") 
        for i in range ( len ( self.alarmDay_list ) ):
            self.alarmDay_Txt.write( self.alarmDay_list[i] + "\n" )
        self.alarmDay_Txt.close()

        self.update_all_widgets()
        self.root.current = "MainScreen"
        app.root.ids['ShowAlarmScreen'].ids['alarmTitle_TextInput'].text = ""
        app.root.ids['ShowAlarmScreen'].ids['alarmDay_TextInput'].text = ""
        app.root.ids['ShowAlarmScreen'].ids['alarmTime_TextInput'].text = ""

    #This function will output the schedule inside the program    
    def get_sched_info( self, sched_title ):
        self.sched_title = sched_title
        self.get_sched_directory = os.path.join( self.schedules_directory, self.sched_title )
        self.schedInfo = [ line.strip() for line in
                                 open ( os.path.join( self.get_sched_directory
                                                      , "sched_Info.txt" )) ]
        self.schedNote = [ line.strip() for line in
                                 open ( os.path.join( self.get_sched_directory
                                                      , "sched_note.txt" )) ]
        return [ self.schedInfo, self.schedNote ]

    #This function will output the schedule inside the program
    def get_alarm_info( self, alarm_title ):
        self.alarm_title = alarm_title
        self.get_alarm_directory = os.path.join( self.alarm_directory, self.alarm_title )
        self.alarmInfo = [ line.strip() for line in
                                 open ( os.path.join( self.get_alarm_directory
                                                      , "alarm_Info.txt" )) ]
        self.alarmTime = [ line.strip() for line in
                                 open ( os.path.join( self.get_alarm_directory
                                                      , "alarm_time.txt" )) ]
        return [ self.alarmInfo, self.alarmTime ]
        
        
# THE KIVY APP WILL START/RUN.        
MainApp().run()
