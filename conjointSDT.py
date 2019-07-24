# Conjoint Survey Design Tool Version 2.0: A Python Graphical User Interface For Creating Conjoint Experimental Designs Usable With Web Survey Platforms
# Copyright (c) 2019 Anton Strezhnev, Jens Hainmueller, Daniel J. Hopkins, and Teppei Yamamoto

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# This software program was designed as a companion to 
# "Causal Inference in Conjoint Analysis: Understanding Multi-Dimensional Choices via Stated Preference Experiments" 
# by Hainmueller, J., D. J. Hopkins and T. Yamamoto

# Imports
import sys, os, re
import csv
import pickle
import copy
from fractions import Fraction
# Import TK
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog


### Map function replacement for Python 3.0 - Thanks to Katarina Jensen
from itertools import starmap, zip_longest
def map(func, *iterables):
   zipped = zip_longest(*iterables)
   if func is None:
       return zipped
   return list(starmap(func, zipped))


# Default Options Dictionary
default_options = {}
default_options["listbox_width"] = 30
default_options["listbox_height"] = 30

# License Environmental Variables
version = "2.0"
progname = "Conjoint Survey Design Tool Version " + version + ": A Python Graphical User Interface For Creating Conjoint Experimental Designs Usable With Web Survey Platforms"
copyright = "Copyright (c) 2019 Anton Strezhnev, Jens Hainmueller, Daniel J. Hopkins, and Teppei Yamamoto"
GPL = "This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.\n\nThis program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License along with this program. If not, see <http://www.gnu.org/licenses/>."
companion = "This software program was designed as a companion to"
citation = '"Causal Inference in Conjoint Analysis: Understanding Multi-Dimensional Choices via Stated Preference Experiments" By Hainmueller, J., D. J. Hopkins and T. Yamamoto'
        
# conjointGUI is the main GUI control class
# arguments: parent - TK window parent class
class conjointGUI:
    
    # Initialize class features
    def __init__(self, parent):
        
        # -- Layout control constants --
        listbox_width = default_options["listbox_width"]
        listbox_height = default_options["listbox_height"]
        
        # Define parent window (root)
        self.myParent = parent
        
        # Define the default file name
        self.file_name = "Untitled"
        

        # File Interaction Options
        self.file_opt = {}
        self.file_opt['defaultextension'] = '.sdt'
        self.file_opt['initialfile'] = "untitled.sdt" 
        self.file_opt['filetypes'] = [('Survey Design Tool Files','.sdt'),('All Files', '.*')]
        self.file_opt['title'] = "Select a file..."
        self.file_opt['parent'] = self.myParent

        self.file_php = {}
        self.file_php['defaultextension'] = '.php'
        self.file_php['initialfile'] = "untitled.php" 
        self.file_php['filetypes'] = [('PHP files','.php'),('All Files', '.*')]
        self.file_php['title'] = "Select a file..."
        self.file_php['parent'] = self.myParent
        
        self.file_html = {}
        self.file_html['defaultextension'] = '.html'
        self.file_html['initialfile'] = "untitled.html" 
        self.file_html['filetypes'] = [('HTML files','.html'),('All Files', '.*')]
        self.file_html['title'] = "Select a file..."
        self.file_html['parent'] = self.myParent
        
        self.file_dat = {}
        self.file_dat['defaultextension'] = '.dat'
        self.file_dat['initialfile'] = "untitled.dat" 
        self.file_dat['filetypes'] = [('DAT files','.dat'),('All Files', '.*')]
        self.file_dat['title'] = "Select a file..."
        self.file_dat['parent'] = self.myParent

        self.csv_opt = {}
        self.csv_opt['defaultextension'] = '.csv'
        self.csv_opt['initialfile'] = "untitled.csv" 
        self.csv_opt['filetypes'] = [('Comma Separated Value Files','.csv'),('All Files', '.*')]
        self.csv_opt['title'] = "Select a file..."
        self.csv_opt['parent'] = self.myParent

        # Re-title the parent window
        self.myParent.title(self.file_name.split("/")[-1]+ " -- "+"Conjoint Survey Design Tool (SDT)")
        
        # Initialize the Menu
        self.menu = Menu(parent)
        parent.config(menu=self.menu)
        
        # File Menu
        self.filemenu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", menu=self.filemenu)
        self.filemenu.add_command(label="New", command=self.new_survey)
        self.filemenu.add_command(label="Open...", command=self.open_survey)
        self.filemenu.add_command(label="Save...", command=self.save_survey)
        self.filemenu.add_command(label="Save As...", command=self.saveas_survey)
        self.filemenu.add_command(label="Import from .csv...", command=self.import_csv)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.exit_survey)

        # Edit Menu
        self.editmenu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Edit", menu=self.editmenu)
        self.editmenu.add_command(label="Settings", command=self.open_settings)
        self.editmenu.add_command(label="Restrictions", command=self.edit_restrictions)
        self.editmenu.add_command(label="Randomization Weights", command=self.probability_menu)
        self.editmenu.add_command(label="Attribute Order Constraints", command=self.edit_orderconstraints)
        self.editmenu.add_separator()
        self.editmenu.add_command(label="Export to PHP", command=self.export_qualtrics)
        self.editmenu.add_command(label="Create Qualtrics Question Templates", command=self.export_question)
        self.editmenu.add_command(label="Export design to R", command=self.export_R)        
        
        self.aboutmenu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="About", menu=self.aboutmenu)
        self.aboutmenu.add_command(label="License", command=self.show_license)
        
        # Initialize main frame - Two halves (left_frame/right_frame)
        self.left_frame = Frame(self.myParent)
        self.left_frame.pack(side=LEFT, padx=10)
        self.right_frame = Frame(self.myParent)
        self.right_frame.pack(side=RIGHT, padx=10)
        
        # -- Initialize Main Variables (Attribute Lists, Levels, etc..)
        self.attribute_list = []
        self.level_dict = {}
        self.restrictions = []
        self.constraints = []
        self.probabilities = {}
        self.activeAttribute = None
        self.randomize_resp_attr = IntVar()
        self.randomize_resp_attr.set(1)
        self.weighted_randomize_attr = IntVar()
        self.weighted_randomize_attr.set(0)
        self.task_num = StringVar()
        self.task_num.set("5")
        self.profile_num = StringVar()
        self.profile_num.set("2")
        
        self.options = default_options
        
        # Boxes for Attributes and Levels
        
        # Box Titles
        self.attr_label = Label(self.left_frame, text="Attributes")
        self.levels_label = Label(self.right_frame, text="Levels")
        self.attr_label.pack(side=TOP, pady=5, padx=5)
        self.levels_label.pack(side=TOP, pady=5, padx=5)
        if self.activeAttribute != None:
            self.levels_label.config(text="Levels - " + self.activeAttribute)
        # Boxes
        
        # Box Frames
        self.left_box_frame = Frame(self.left_frame)
        self.right_box_frame = Frame(self.right_frame)
        self.left_box_frame.pack()
        self.right_box_frame.pack()
        
        # List boxes and scroll bars (vertical/horizontal)
        self.box_attributes_vscroll = Scrollbar(self.left_box_frame)
        self.box_attributes = Listbox(self.left_box_frame, height=listbox_height, width=listbox_width)
        self.box_levels_vscroll = Scrollbar(self.right_box_frame)
        self.box_levels = Listbox(self.right_box_frame, height=listbox_height, width=listbox_width)
        
        # Pack Boxes/Scroll Bars
        self.box_attributes.pack(side=LEFT)
        self.box_attributes_vscroll.pack(side=LEFT,fill=Y)
        self.box_levels.pack(side=LEFT)
        self.box_levels_vscroll.pack(side=LEFT,fill=Y)
        
        # Configure Scroll Bars
        self.box_attributes_vscroll.config(command=self.box_attributes.yview)
        self.box_attributes.config(yscrollcommand=self.box_attributes_vscroll.set)
        self.box_levels_vscroll.config(command=self.box_levels.yview)
        self.box_levels.config(yscrollcommand=self.box_levels_vscroll.set)
                
        self.box_attributes.bind('<<ListboxSelect>>',self.update_levels)
        
        # Buttons 
        # Left Panel (Attributes)
        self.left_button_frame = Frame(self.left_frame)
        self.left_button_frame.pack(side=BOTTOM)
        self.attr_add = Button(self.left_button_frame, text="Add", command=self.add_attribute)
        self.attr_del = Button(self.left_button_frame, text="Remove", command=self.remove_attribute)
        self.attr_edit = Button(self.left_button_frame, text="Edit", command=self.edit_attribute)
        self.attr_add.pack(side=LEFT)
        self.attr_del.pack(side=LEFT)
        self.attr_edit.pack(side=LEFT)
        
        
        # Right Panel (Levels)
        self.right_button_frame = Frame(self.right_frame)
        self.right_button_frame.pack(side=BOTTOM)
        self.level_add = Button(self.right_button_frame, text="Add", command=self.add_level)
        self.level_del = Button(self.right_button_frame, text="Remove", command=self.remove_level)
        self.level_edit = Button(self.right_button_frame, text="Edit", command=self.edit_level)
        self.level_add.pack(side=LEFT)
        self.level_del.pack(side=LEFT)
        self.level_edit.pack(side=LEFT)
         
    
    def update_file_name(self, name):
        self.file_name = name
        self.myParent.title(self.file_name.split("/")[-1] + " -- "+"Conjoint Survey Design Tool (SDT)")
    
    # Displays the GPL License Information
    def show_license(self):
        license_string = progname + "\n" + copyright + "\n\n" + GPL + "\n\n" + companion + "\n" + citation
        messagebox.showinfo("License Information", license_string)
     
    # -- Menu Functions --
    # - File Menu -
    # Create a new survey - re-set the attribute_list, level_dict, restrictions and options
    def new_survey(self):
        okcancel = messagebox.askokcancel("Clear current workspace?","Creating a new survey will delete all unsaved data in the current survey. Are you sure you wish to continue?")
        if okcancel == 1:
            self.activeAttribute = None
            self.clear_all_data()
            
            self.update_file_name("Untitled")
        else:
            pass
    
    # Open a saved attribute_list, level_dict, restrictions and options from a python pickle file
    def open_survey(self):
        in_file_name = filedialog.askopenfilename(**self.file_opt)
        if in_file_name != None:
            if re.search("\.sdt",in_file_name[-4:]) != None:
                try:
                    open_file = open(in_file_name,"rb")
                    pick_in = pickle.Unpickler(open_file)
                    self.attribute_list = pick_in.load()
                    self.level_dict = pick_in.load()
                    self.restrictions = pick_in.load()
                    self.constraints = pick_in.load()
                    self.probabilities = pick_in.load()                    
                    
                    task = pick_in.load()
                   
                    self.task_num.set(str(task))
                    profile = pick_in.load()
                    
                    self.profile_num.set(str(profile))
                    self.activeAttribute = self.attribute_list[0]
                    open_file.close()
                    
                    self.file_name = in_file_name
                    self.update_file_name(in_file_name)
                
                    self.update_listbox_attributes()
                    self.update_listbox_levels()
                    
                except:
                   messagebox.showerror(title="Error",message="Error: Could not open file")
            else:
                messagebox.showerror(title="Invalid File Name",message="Invalid file extension. File must have the .sdt extension")
        
    # Save survey data to python pickle instance
    def saveas_survey(self):
        out_file_name = filedialog.asksaveasfilename(**self.file_opt)
        if out_file_name != () and out_file_name != "":
            if re.search("\.sdt",out_file_name[-4:]) != None:
                try:
                    save_file = open(out_file_name,"wb")
                    pick_out = pickle.Pickler(save_file)
                    pick_out.dump(self.attribute_list)
                    pick_out.dump(self.level_dict)
                    pick_out.dump(self.restrictions)
                    pick_out.dump(self.constraints)
                    pick_out.dump(self.probabilities)
                    pick_out.dump(self.task_num.get())
                    pick_out.dump(self.profile_num.get())
                    save_file.close()
                    self.file_name = out_file_name
                    self.update_file_name(out_file_name)
                except:
                    messagebox.showerror(title="Error",message="Error: Could not save to file")
            else:
                messagebox.showerror(title="Invalid File Name",message="Invalid file extension. Save file must have the .sdt file extension")
            
    def save_survey(self):
        if re.search("\.sdt",self.file_name[-4:]) == None:
            self.saveas_survey()
        else:
            try:
                save_file = open(self.file_name,"wb")
                pick_out = pickle.Pickler(save_file)
                pick_out.dump(self.attribute_list)
                pick_out.dump(self.level_dict)
                pick_out.dump(self.restrictions)
                pick_out.dump(self.constraints)
                pick_out.dump(self.probabilities)
                pick_out.dump(self.task_num.get())
                pick_out.dump(self.profile_num.get())
                save_file.close()
            except:
                self.saveas_survey()
                
    # Imports attribute and level data from a csv file
    # Each row is an attribute + levels. First value is the attribute name, all others are levels
    def import_csv(self):
        response = messagebox.askyesnocancel(title="Save survey?", message="Would you like to save your current survey?")
        if response == None:
            pass
        elif response == 1:
            self.save_survey()

        if response != None:
            in_file_name = filedialog.askopenfilename(**self.csv_opt)
            if re.search("\.csv",in_file_name[-4:]) != None:
                try:
                    open_file = open(in_file_name,"rb")
                    csv_open = csv.reader(open_file)
                    self.attribute_list = []
                    self.level_dict = {}
                    self.probabilities = {}
                    self.options = default_options
                    self.restrictions = []
                    self.constraints = []
                    self.update_listbox_attributes()
                    self.update_listbox_levels()
                    self.randomize_resp_attr = IntVar()
                    self.randomize_resp_attr.set(1)
                    self.weighted_randomize_attr = IntVar()
                    self.weighted_randomize_attr.set(0)
                    self.task_num = StringVar()
                    self.task_num.set("5")
                    self.profile_num = StringVar()
                    self.profile_num.set("2")
                    
                    for line in csv_open:
                        attr = line.pop(0)
                        self.attribute_list.append(attr)
                        self.level_dict[attr] = []
                        for entr in line:
                            if entr != "":
                                self.level_dict[attr].append(entr)
                                
                         
                    open_file.close()
                    self.clear_probabilities()
                    self.file_name = "Untitled"
                    self.update_file_name("Untitled")
                    
                    self.update_listbox_attributes()
                    self.update_listbox_levels()
                except:
                    messagebox.showerror(title="Error",message="Error: Could not open file")
            else:
                messagebox.showerror(title="Invalid File Name",message="Invalid file extension. File must have the .csv extension")
                
    # Quits the gui
    def exit_survey(self):
        response = messagebox.askyesnocancel(title="Quit",message="Would you like to save your current survey?")

        if response == None:
            pass
        elif response == 1:
            self.save_survey()
            self.myParent.destroy()
            quit()
        elif response == False:
            self.myParent.destroy()
            quit()
                        
    # - Edit Menu -
    
    # Open and edit the settings menu
    def open_settings(self):
        self.settings = Toplevel()
        self.settings.title("Settings")
        
        self.randomization_label = Label(self.settings, text="Randomization Settings")
        self.randomization_label.pack()
        
        self.randomize_each_respondent = Checkbutton(self.settings, text="Randomize order of attributes for each respondent", variable = self.randomize_resp_attr)
        self.randomize_each_respondent.pack()
        
        self.randomization_rule = Frame(self.settings,height=1,width=200,bg="black")
        self.randomization_rule.pack(pady=10)
        
        self.weighted_randomize_button = Checkbutton(self.settings, text="Use weighted randomization", variable = self.weighted_randomize_attr)
        self.weighted_randomize_button.pack()
        
        self.weighted_randomize_rule = Frame(self.settings,height=1,width=200,bg="black")
        self.weighted_randomize_rule.pack(pady=10)
        
        self.numbers_label = Label(self.settings, text="Survey Settings")
        self.numbers_label.pack()

        self.tasks_box = Frame(self.settings)
        self.tasks_box.pack()
        
        self.entry_tasks_label = Label(self.tasks_box, text="Number of Tasks per Respondent")
        self.entry_tasks_label.pack(side=LEFT)
        self.entry_tasks = Entry(self.tasks_box, width=5, textvariable=self.task_num)
        self.entry_tasks.pack(side=LEFT)
        
        self.profiles_box = Frame(self.settings)
        self.profiles_box.pack()
        
        self.entry_profiles_label = Label(self.profiles_box, text="Number of Profiles per Task")
        self.entry_profiles_label.pack(side=LEFT)
        self.entry_profiles = Entry(self.profiles_box, width=5, textvariable=self.profile_num)
        self.entry_profiles.pack(side=LEFT)
        
        self.settings_save = Button(self.settings, text="Save Settings", command=self.settings.destroy)
        self.settings_save.pack()
        
    # Edit the Restrictions
    def edit_restrictions(self):
        listbox_width = 80
        listbox_height = 10
        
        
        # Main New Window Frame
        self.restrict_window = Toplevel()
        self.restrict_window.title("Manage Restrictions")
        
        
        
        self.restrict_header = Frame(self.restrict_window)
        self.restrict_text_header = Label(self.restrict_header, text="Specified Restrictions")
        self.restrict_header.pack()
        self.restrict_text_header.pack()
        
        
        # Frame to fit to
        self.restrict_main = Frame(self.restrict_window)
        self.restrict_main.pack()
        
        self.restrict_main_box = Frame(self.restrict_main)
        self.restrict_main_box.pack(side=LEFT)
        
        # List boxes and scroll bars (vertical/horizontal)
        self.box_restrictions_vscroll = Scrollbar(self.restrict_main)
        self.box_restrictions_xscroll = Scrollbar(self.restrict_main_box, orient=HORIZONTAL)
        self.box_restrictions = Listbox(self.restrict_main_box, height=listbox_height, width=listbox_width)
        
        # Pack Boxes/Scroll Bars
        self.box_restrictions.pack()
        self.box_restrictions_xscroll.pack(fill=X)
        self.box_restrictions_vscroll.pack(side=LEFT,fill=Y)
        
        # Config Boxes/Scroll
        self.box_restrictions_vscroll.config(command=self.box_restrictions.yview)
        self.box_restrictions.config(yscrollcommand=self.box_restrictions_vscroll.set)
        self.box_restrictions_xscroll.config(command=self.box_restrictions.xview)
        self.box_restrictions.config(xscrollcommand=self.box_restrictions_xscroll.set)
        
        self.restrict_footer = Frame(self.restrict_window)
        self.restrict_footer.pack()
        
        self.restrictions_add = Button(self.restrict_footer, text="New Restriction", command=self.new_restriction)
        self.restrictions_remove = Button(self.restrict_footer, text="Delete Restriction", command=self.delete_restriction)
        self.restrictions_add.pack()
        self.restrictions_remove.pack()
        
        self.rule = Frame(self.restrict_window,height=1,width=200,bg="black")
        self.rule.pack(pady=10)
        
        self.restrict_footer2 = Frame(self.restrict_window)
        self.restrict_footer2.pack(pady=10)
        
        self.restrict_select_left = Frame(self.restrict_footer2)
        self.restrict_select_right = Frame(self.restrict_footer2)
        self.restrict_select_left.pack(side=LEFT,padx=5)
        self.restrict_select_right.pack(side=LEFT)
        
        self.attr_rest_label = Label(self.restrict_select_left, text="Attribute")
        self.level_rest_label = Label(self.restrict_select_right, text="Level")
        self.attr_rest_label.pack()
        self.level_rest_label.pack()
        
        attr_list = self.attribute_list
        if len(self.attribute_list) > 0:
            self.attr_var = StringVar(self.myParent)
            self.attr_var.set(attr_list[0])
            self.restrictions_attribute_select = OptionMenu(self.restrict_select_left, self.attr_var, command=self.update_restriction_levels, *tuple(attr_list))
            
            level_list = self.level_dict[self.attr_var.get()]
            
            if level_list == []:
                self.level_var = StringVar(self.myParent)
                self.level_var.set("No Levels")
                self.restrictions_level_select = OptionMenu(self.restrict_select_right, self.level_var, tuple([]))
            else:
                self.level_var = StringVar(self.myParent)
                self.level_var.set(level_list[0])
                self.restrictions_level_select = OptionMenu(self.restrict_select_right, self.level_var, *tuple(level_list))
        else:
            self.attr_var = StringVar(self.myParent)
            self.attr_var.set("No Attributes")
            self.restrictions_attribute_select = OptionMenu(self.restrict_select_left, self.attr_var, tuple([]))
            self.level_var = StringVar(self.myParent)
            self.level_var.set("No Levels")  
            self.restrictions_level_select = OptionMenu(self.restrict_select_right, self.level_var, tuple([]))
        self.update_restriction_list()

        self.restrictions_attribute_select.pack()
        self.restrictions_level_select.pack()
            
        self.restrict_footer3 = Label(self.restrict_window)
        self.restrict_footer3.pack()
        
        self.restrictions_edit = Button(self.restrict_footer3, text="Add Selected Level to Restriction",command=self.edit_restriction)
        self.restrictions_edit.pack()
        
    def new_restriction(self):
        self.restrictions.append([])
        self.update_restriction_list()
    
    def delete_restriction(self):
        select = map(int, self.box_restrictions.curselection())
        if len(select) > 0:
            self.restrictions.pop(select[0])
            self.update_restriction_list()
            
    def edit_restriction(self):
        select = map(int, self.box_restrictions.curselection())
        if len(select) > 0:
            attribute = self.attr_var.get()
            level = self.level_var.get()
            if attribute in self.attribute_list and level in self.level_dict[attribute]:
                exist = 0
                id = None
                for m in range(len(self.restrictions[int(select[0])])):
                    key = self.restrictions[int(select[0])][m]
                    if key[0] == attribute:
                        exist = 1
                        id = m
                
                if exist == 0:
                    self.restrictions[int(select[0])].append((attribute, level))
                else:
                    self.restrictions[int(select[0])][id] = (attribute, level)
                    
                self.update_restriction_list()
            else:
                messagebox.showerror(title="Cannot Add Restriction",message="Attribute or level does not exist")
        
    def update_restriction_list(self):
        self.box_restrictions.delete(0,END)
        if len(self.restrictions) > 0:
            for i in range(len(self.restrictions)):
                txt = str(i+1) + " - " + str(self.restrictions[i])
                self.box_restrictions.insert(END,txt)
        
    def update_restriction_levels(self, misc):
        new_level_list = self.level_dict[self.attr_var.get()]
        if new_level_list != []:
            self.restrictions_level_select['menu'].delete(0, END)
            for level in new_level_list:
                self.restrictions_level_select['menu'].add_command(label=level, command=lambda temp = level: self.restrictions_level_select.setvar(self.restrictions_level_select.cget("textvariable"), value = temp))
            self.level_var.set(new_level_list[0])
        else:
            self.restrictions_level_select['menu'].delete(0, END)
            self.level_var.set("No Levels")
    
    ### Update Attribute Order randomization constraints
    # Edit the Restrictions
    def edit_orderconstraints(self):
        constrbox_width = 80
        constrbox_height = 10

        # Main New Window Frame
        self.constraint_window = Toplevel()
        self.constraint_window.title("Manage Attribute Order Randomization")
        
        self.constraint_header = Frame(self.constraint_window)
        self.constraint_text_header = Label(self.constraint_header, text="Defined Orderings")
        self.constraint_header.pack()
        self.constraint_text_header.pack()
        
        # Frame to fit to
        self.constraint_main = Frame(self.constraint_window)
        self.constraint_main.pack()
        
        self.constraint_main_box = Frame(self.constraint_main)
        self.constraint_main_box.pack(side=LEFT)
        
        # List boxes and scroll bars (vertical/horizontal)
        self.box_constraint_vscroll = Scrollbar(self.constraint_main)
        self.box_constraint_xscroll = Scrollbar(self.constraint_main_box, orient=HORIZONTAL)
        self.box_constraint = Listbox(self.constraint_main_box, height=constrbox_height, width=constrbox_width)
        
        # Pack Boxes/Scroll Bars
        self.box_constraint.pack()
        self.box_constraint_xscroll.pack(fill=X)
        self.box_constraint_vscroll.pack(side=LEFT,fill=Y)
        
        # Config Boxes/Scroll
        self.box_constraint_vscroll.config(command=self.box_constraint.yview)
        self.box_constraint.config(yscrollcommand=self.box_constraint_vscroll.set)
        self.box_constraint_xscroll.config(command=self.box_constraint.xview)
        self.box_constraint.config(xscrollcommand=self.box_constraint_xscroll.set)
        
        self.constraint_footer = Frame(self.constraint_window)
        self.constraint_footer.pack()
        
        self.constraint_add = Button(self.constraint_footer, text="New Constraint", command=self.new_constraint)
        self.constraint_remove = Button(self.constraint_footer, text="Delete Constraint", command=self.delete_constraint)
        self.constraint_add.pack()
        self.constraint_remove.pack()
        
        self.constrrule = Frame(self.constraint_window,height=1,width=200,bg="black")
        self.constrrule.pack(pady=10)
        
        self.constraint_footer2 = Frame(self.constraint_window)
        self.constraint_footer2.pack(pady=10)
        
        self.constraint_select_left = Frame(self.constraint_footer2)
        self.constraint_select_right = Frame(self.constraint_footer2)
        self.constraint_select_left.pack(side=LEFT,padx=5)
        self.constraint_select_right.pack(side=LEFT)
        
        self.attr_constraint_label = Label(self.constraint_select_left, text="Attribute")
        self.attr_constraint_label.pack()

        attr_list_constr = self.attribute_list
        if len(self.attribute_list) > 0:
            self.constr_attr_var = StringVar(self.myParent)
            self.constr_attr_var.set(attr_list_constr[0])
            self.constraint_attribute_select = OptionMenu(self.constraint_select_left, self.constr_attr_var, *tuple(attr_list_constr))
        else:
            self.constr_attr_var = StringVar(self.myParent)
            self.constr_attr_var.set("No Attributes")
            self.constraint_attribute_select = OptionMenu(self.constraint_select_left, self.constr_attr_var, tuple([]))

        self.update_constraint_list()

        self.constraint_attribute_select.pack()
            
        self.constraint_footer3 = Label(self.constraint_window)
        self.constraint_footer3.pack()
        
        self.constraint_edit = Button(self.constraint_footer3, text="Add Selected Attribute to Constraint",command=self.edit_constraint)
        self.constraint_edit.pack()
        
    def new_constraint(self):
        self.constraints.append([])
        self.update_constraint_list()
    
    def delete_constraint(self):
        select = map(int, self.box_constraint.curselection())
        if len(select) > 0:
            self.constraints.pop(select[0])
            self.update_constraint_list()
            
    def edit_constraint(self):
        select = map(int, self.box_constraint.curselection())
        if len(select) > 0:
            attribute = self.constr_attr_var.get()
            
            if attribute in self.attribute_list:
                exist = 0
                for m in self.constraints:
                    if attribute in m:
                        exist = 1
                
                if exist == 1:
                     messagebox.showerror(title="Cannot Add Attribute",message="An Attribute can only be a part of one order randomization constraint")
                elif exist == 0:
                    self.constraints[int(select[0])].append(attribute)
                
                    
                self.update_constraint_list()
            else:
                messagebox.showerror(title="Cannot Add Constraint",message="Attribute does not exist")
        
    def update_constraint_list(self):
        self.box_constraint.delete(0,END)
        if len(self.constraints) > 0:
            for i in range(len(self.constraints)):
                txt = str(i+1) + " - " + str(self.constraints[i])
                self.box_constraint.insert(END,txt)
        
    ## Specify weighted randomization
    
    # Reset all probabilities to even
    def clear_probabilities(self):
        self.probabilities = {}
        
        for k in self.level_dict:
            self.probabilities[k] = []
            length = float(len(self.level_dict[k]))
            if (length > 0):
                for p in range(len(self.level_dict[k])):
                    self.probabilities[k].append(1/length)
    
    # Update the probabilities with a new set
    def update_probabilities(self, update_dictionary):
        self.probabilities = update_dictionary
        
    # Create a menu that allows user to edit randomization weights
    def probability_menu(self):
        if len(self.attribute_list) > 0:
            listbox_width = 30
            listbox_height = 30
            
            self.tempProbabilities = copy.deepcopy(self.probabilities)       
            
            # Main New Window Frame
            self.prob_window = Toplevel()
            self.prob_window.title("Edit Randomization Weights")
    
            self.prob_window.grab_set()    
            self.probactiveAttribute = self.attribute_list[0]
            
            self.left_prob_frame = Frame(self.prob_window)
            self.left_prob_frame.pack(side=LEFT, padx=10)
            self.right_prob_frame = Frame(self.prob_window)
            self.right_prob_frame.pack(side=RIGHT, padx=10)
            
            # Set up attribute and level selection boxes
            # Box Titles
            self.attr_prob_label = Label(self.left_prob_frame, text="Attributes")
            self.levels_prob_label = Label(self.right_prob_frame, text="Levels")
            self.attr_prob_label.pack(side=TOP, pady=5, padx=5)
            self.levels_prob_label.pack(side=TOP, pady=5, padx=5)
            if self.probactiveAttribute != None:
                self.levels_prob_label.config(text="Levels - " + self.probactiveAttribute)
                
             # Box Frames
            self.left_prob_box_frame = Frame(self.left_prob_frame)
            self.right_prob_box_frame = Frame(self.right_prob_frame)
            self.left_prob_box_frame.pack()
            self.right_prob_box_frame.pack()
            
            # List boxes and scroll bars (vertical/horizontal)
            self.prob_box_attributes_vscroll = Scrollbar(self.left_prob_box_frame)
            self.prob_box_attributes = Listbox(self.left_prob_box_frame, height=listbox_height, width=listbox_width)
            self.prob_box_levels_vscroll = Scrollbar(self.right_prob_box_frame)
            self.prob_box_levels = Listbox(self.right_prob_box_frame, height=listbox_height, width=listbox_width)
            
            # Pack Boxes/Scroll Bars
            self.prob_box_attributes.pack(side=LEFT)
            self.prob_box_attributes_vscroll.pack(side=LEFT,fill=Y)
            self.prob_box_levels.pack(side=LEFT)
            self.prob_box_levels_vscroll.pack(side=LEFT,fill=Y)
            
            # Configure Scroll Bars
            self.prob_box_attributes_vscroll.config(command=self.prob_box_attributes.yview)
            self.prob_box_attributes.config(yscrollcommand=self.prob_box_attributes_vscroll.set)
            self.prob_box_levels_vscroll.config(command=self.prob_box_levels.yview)
            self.prob_box_levels.config(yscrollcommand=self.prob_box_levels_vscroll.set)
            
            self.prob_box_attributes.bind('<<ListboxSelect>>',self.update_prob_levels)
    
            # Buttons 
            # Left Panel (Save/Reset)
            self.right_prob_button_frame = Frame(self.right_prob_frame)
            self.right_prob_button_frame.pack(side=BOTTOM)
            self.prob_edit = Button(self.right_prob_button_frame, text="Edit Weight", command=self.edit_level_prob)
            self.prob_edit.pack(side=RIGHT)
    
            # Right Panel (Edit)
            self.left_prob_button_frame = Frame(self.left_prob_frame)
            self.left_prob_button_frame.pack(side=BOTTOM)
            self.prob_save = Button(self.left_prob_button_frame, text="Save Weights", command=self.save_probs)
            self.prob_clear = Button(self.left_prob_button_frame, text="Reset Weights to Default", command=self.reset_weights)        
            self.prob_save.pack(side=LEFT)
            self.prob_clear.pack(side=LEFT)
            
            #Load output?
            self.update_prob_levels(1)
            self.update_prob_attributes()
        else:
            messagebox.showerror(title="Error",message="Error: No Attributes to Load")
        
    def reset_weights(self):
        
        self.tempProbabilities = {}
        
        for k in self.level_dict:
            self.tempProbabilities[k] = []
            length = float(len(self.level_dict[k]))
            if (length > 0):
                for p in range(len(self.level_dict[k])):
                    self.tempProbabilities[k].append(1/length)
                    
        self.update_prob_levels(1)
        
    def edit_level_prob(self):
        levelSel = map(int, self.prob_box_levels.curselection())
        selAct = self.probactiveAttribute
        if len(levelSel) > 0 and selAct != None:
            self.msg_box(cmd=self.change_level_prob, msg='Enter a weight between 0 and 1', title="Edit Level Weight", btname="OK")
 
 
    def change_level_prob(self, event=None):
        data= self.entry0.get()
        if data:
            if data.strip(" ") != "":
                levelSel = map(int, self.prob_box_levels.curselection())
                selAct = self.probactiveAttribute
                res = Fraction(data)
                true_result = float(res)
                if len(levelSel) > 0 and true_result >= 0 and true_result <= 1 and selAct != None:
                    self.tempProbabilities[selAct][int(levelSel[0])] = true_result
                    self.update_prob_levels(1)
                    self.top.destroy()
                else:
                    self.top.destroy()
            else:
                self.top.destroy()
        else:
            self.top.destroy()

    def update_prob_attributes(self):
        self.prob_box_attributes.delete(0,END)
        for k in self.attribute_list:
            self.prob_box_attributes.insert(END, k)
        
    # Update levels in the probability box
    def update_prob_levels(self, index):

        item = map(int, self.prob_box_attributes.curselection())
        sums = self.compute_prob_sums()
        #print(self.probabilities)
        #print(self.level_dict)
        #print(sums)
        if len(item) > 0:
            self.probactiveAttribute = self.attribute_list[item[0]]
            if self.probactiveAttribute != None:
                val = sums[self.probactiveAttribute]
                if val.denominator >= 1000:
                    self.levels_prob_label.config(text="Levels - " + self.probactiveAttribute + " - " + "Sum = " + str(float(val.numerator/val.denominator)))
                elif val == 1:
                    self.levels_prob_label.config(text="Levels - " + self.probactiveAttribute + " - " + "Sum = " + str(val))
                else:
                    self.levels_prob_label.config(text="Levels - " + self.probactiveAttribute+ " - " + "Sum = " + str(val.numerator) + "/" + str(val.denominator))
            self.prob_box_levels.delete(0,END)
            for k in range(len(self.level_dict[self.attribute_list[item[0]]])):
                level_name = self.level_dict[self.attribute_list[item[0]]][k]
                Frac = Fraction(self.tempProbabilities[self.attribute_list[item[0]]][k]).limit_denominator()
                if Frac.denominator >= 1000:
                    level_prob_str = level_name + ": " + str(self.tempProbabilities[self.attribute_list[item[0]]][k])
                else:
                    level_prob_str = level_name + ": " + str(Frac.numerator)+ "/" + str(Frac.denominator)
                self.prob_box_levels.insert(END,level_prob_str)
        else:
            self.prob_box_levels.delete(0,END)
            if self.probactiveAttribute != None:
                val = sums[self.probactiveAttribute]
                if val.denominator >= 1000:
                    self.levels_prob_label.config(text="Levels - " + self.probactiveAttribute + " - " + "Sum = " + str(float(val.numerator/val.denominator)))
                elif val == 1:
                    self.levels_prob_label.config(text="Levels - " + self.probactiveAttribute + " - " + "Sum = " + str(val))
                else:
                    self.levels_prob_label.config(text="Levels - " + self.probactiveAttribute+ " - " + "Sum = " + str(val.numerator) + "/" + str(val.denominator))
            
            if self.probactiveAttribute != None:
                for k in range(len(self.level_dict[self.probactiveAttribute])):
                    level_name = self.level_dict[self.probactiveAttribute][k]
                    Frac = Fraction(self.tempProbabilities[self.probactiveAttribute][k]).limit_denominator()
                    if Frac.denominator >= 1000:
                        level_prob_str = level_name + ": " +  str(self.tempProbabilities[self.probactiveAttribute][k])
                    else:
                        level_prob_str = level_name + ": " +  str(Frac.numerator)+ "/" + str(Frac.denominator)
                    self.prob_box_levels.insert(END,level_prob_str)

    # Save probabilities    
    def save_probs(self):
        # Check over the data
        validation = self.validate_probabilities()
        
        if validation[0]:
            self.probabilities = copy.deepcopy(self.tempProbabilities)
            self.prob_window.destroy()
        else:
            errmsg = "Error: The following attribute weights do not sum to 1\n"
            
            for err in validation[1]:
                errmsg = errmsg + str(err) + ", "
                
            errmsg = errmsg.rstrip(", ")
            messagebox.showerror(title="Error",message=errmsg)
        
    
    # Check to make sure the probabilities are legitimate    
    def validate_probabilities(self):
        sums = self.compute_prob_sums()
       
        all_sum_to_one = True
        fails = []
        for k in sums:
            if float(sums[k]) != 1:
                all_sum_to_one = False
                fails.append(k)
        return all_sum_to_one, fails
        
    # Sum the probabilities for each section
    def compute_prob_sums(self):
        sums = {}
        for attr in self.tempProbabilities:
            sum_out = Fraction()
            for k in self.tempProbabilities[attr]:
                sum_out = sum_out + Fraction(k)
            sums[attr] = sum_out.limit_denominator()
        
        return(sums)
        
    # Export the design information to .php
    def export_qualtrics(self):
        out_php_name = filedialog.asksaveasfilename(**self.file_php)
        if out_php_name != None:
            if re.search("\.php",out_php_name[-4:]) != None:
                qualtrics_out(out_php_name, self.attribute_list, self.level_dict, self.restrictions, self.constraints, self.probabilities, self.weighted_randomize_attr.get(), int(self.profile_num.get()), int(self.task_num.get()),int(self.randomize_resp_attr.get()))
            else:
                messagebox.showerror(title="Invalid File Name",message="Invalid file extension. File must have the .php extension")

    # Export the design information to R
    def export_R(self):
        out_R_name = filedialog.asksaveasfilename(**self.file_dat)
        if out_R_name != None:
            R_out(out_R_name, self.attribute_list, self.level_dict, self.restrictions, self.constraints, self.probabilities, self.weighted_randomize_attr.get(), int(self.profile_num.get()), int(self.task_num.get()),int(self.randomize_resp_attr.get()))
            
    # Create a default template to pass into Qualtrics
    def export_question(self):
        out_html_name = filedialog.asksaveasfilename(**self.file_html)
        if out_html_name != None:
            if re.search("\.html",out_html_name[-5:]) != None:
                html_out(out_html_name, len(self.attribute_list), int(self.profile_num.get()), int(self.task_num.get()))
            else:
                messagebox.showerror(title="Invalid File Name",message="Invalid file extension. File must have the .html extension")

    # -- Message Box Prompt
    def msg_box(self, msg='Name of new attribute?', btname="Add", cmd = None, title = "",extra=True):
        top = self.top = Toplevel()
        self.top.title(title)
        label0 = Label(top, text=msg)
        label0.pack()
        self.top.grab_set()
        if extra:
            self.entry0 = Entry(top)
            self.entry0.pack()
            self.entry0.focus_set()
            button2 = Button(top, text=btname, command=cmd)
            top.bind('<Return>', cmd)
            button2.pack()

        button3 = Button(top, text='Cancel', command=lambda: self.top.destroy())
        button3.pack()

    def append_attribute(self, event=None):
        data = self.entry0.get()
        if data:
            if data.strip(" ") != "":
                self.attribute_list.append(data)
                self.level_dict[data] = []
                if len(self.attribute_list) == 1:
                    self.activeAttribute = data
                self.clear_probabilities()
                self.update_listbox_attributes()
                self.update_listbox_levels()
                self.top.destroy()
            else:
                self.top.destroy()
        else:
            self.top.destroy()
                
    def append_level(self, event=None):
        data= self.entry0.get()
        if data:
            if data.strip(" ") != "":
                attrit = map(int, self.box_attributes.curselection())
                if len(attrit) > 0:
                    self.level_dict[self.attribute_list[attrit[0]]].append(data)
                    self.clear_probabilities()
                    self.update_listbox_levels()
                    self.update_listbox_attributes()
                    self.top.destroy()
                elif self.activeAttribute != None:
                    self.level_dict[self.activeAttribute].append(data)
                    self.clear_probabilities()
                    self.update_listbox_levels()
                    self.update_listbox_attributes()
                    self.top.destroy()
            else:
                self.top.destroy()
        else:
            self.top.destroy()
    
    def change_attribute(self, event=None):
        data= self.entry0.get()
        if data:
            if data.strip(" ") != "":
                selAct = map(int, self.box_attributes.curselection())
                if len(selAct) > 0:
                    oldAtt = self.attribute_list[int(selAct[0])]
                    self.attribute_list[int(selAct[0])] = data
                    self.level_dict[data] = self.level_dict[oldAtt]
                    if oldAtt in self.level_dict: del self.level_dict[oldAtt]
                    self.activeAttribute = data
                    self.clear_probabilities()
                    self.update_listbox_attributes()                    
                    self.update_listbox_levels()
                    
                    self.top.destroy()
                else:
                    self.top.destroy()
            else:
                self.top.destroy()
        else:
            self.top.destroy()
        
    def change_level(self, event=None):
        data= self.entry0.get()
        if data:
            if data.strip(" ") != "":
                levelSel = map(int, self.box_levels.curselection())
                selAct = self.activeAttribute
                if len(levelSel) > 0 and selAct != None:
                    self.level_dict[selAct][int(levelSel[0])] = data
                    self.clear_probabilities()
                    self.update_listbox_levels()
                    self.update_listbox_attributes()
                    self.clear_probabilities()
                    self.top.destroy()
                else:
                    self.top.destroy()
            else:
                self.top.destroy()
        else:
            self.top.destroy()

    # -- Button Functions
    

    # Adds an attribute to the existing list
    def add_attribute(self):
        self.msg_box(cmd=self.append_attribute, msg='Name of new attribute?', title="Add Attribute")
        
    def add_level(self):

        if len(self.attribute_list) > 0:
            self.msg_box(cmd=self.append_level, msg='Name of new level?', title="Add Level")

    def edit_level(self):
        levelSel = map(int, self.box_levels.curselection())
        selAct = self.activeAttribute
        if len(levelSel) > 0 and selAct != None:
            self.msg_box(cmd=self.change_level, msg='New name of level?', title="Edit Level", btname="Edit")
            
    def edit_attribute(self):
        attrit = map(int, self.box_attributes.curselection())
        if len(attrit) > 0:
            self.msg_box(cmd=self.change_attribute, msg='New name of attribute?', title="Edit Attribute", btname="Edit")
        
    def remove_attribute(self):
        attrit = map(int, self.box_attributes.curselection())
        if len(attrit) > 0:
            
            self.attribute_list.remove(self.attribute_list[attrit[0]])
            self.level_dict[attrit[0]] = []
            if len(self.attribute_list) > 0:
                self.activeAttribute = self.attribute_list[0]
            else:
                self.activeAttribute = None    
            self.clear_probabilities()
            self.update_listbox_attributes()
            self.update_listbox_levels()
        

    def remove_level(self):
        attrit = self.activeAttribute
        level = map(int, self.box_levels.curselection())
        if len(level) > 0 and attrit != None:
            self.level_dict[attrit].pop(level[0])
            self.clear_probabilities()
            self.update_listbox_levels()
            self.update_listbox_attributes()
        
    # -- List Box Functions
    
    def update_levels(self, index):
        
        item = map(int, self.box_attributes.curselection())

        
        if len(item) > 0:
            self.activeAttribute = self.attribute_list[item[0]]
            if self.activeAttribute != None:
                    self.levels_label.config(text="Levels - " + self.activeAttribute)
            self.box_levels.delete(0,END)
            for i in self.level_dict[self.attribute_list[item[0]]]:
                self.box_levels.insert(END,i)
        else:
            self.box_levels.delete(0,END)
            if self.activeAttribute != None:
                    self.levels_label.config(text="Levels - " + self.activeAttribute)
            if self.activeAttribute != None:
                for i in self.level_dict[self.activeAttribute]:
                    self.box_levels.insert(END,i)

    # Clears all stored data (attributes, levels, etc...)
    def clear_all_data(self):
        self.attribute_list = []
        self.level_dict = {}
        self.options = default_options
        self.restrictions = []
        self.constraints = []
        self.probabilities = {}
        self.update_listbox_attributes()
        self.update_listbox_levels()
        self.randomize_resp_attr = IntVar()
        self.randomize_resp_attr.set(1)
        self.weighted_randomize_attr = IntVar()
        self.weighted_randomize_attr.set(0)
        self.task_num = StringVar()
        self.task_num.set("5")
        self.profile_num = StringVar()
        self.profile_num.set("2")
        
    # -- Listbox --
    # Update the displayed attributes listbox using the attribute_list
    def update_listbox_attributes(self):
        self.box_attributes.delete(0,END)
        for i in self.attribute_list:
            self.box_attributes.insert(END, i)
        
    # Update the displayed levels listbox using the active_attribute
    def update_listbox_levels(self):
        self.update_levels("")

# General Utility Functions
# Output design to the R package
def R_out(filename, attributes, level_dict, restrictions, constraints, probabilities, random, profiles, tasks, randomize):
    
     out_file = open(filename, "w")
     # Write attribute names and levels
     out_file.write("Attributes\n")
     for attr in attributes:
         string_attr = attr + ":"
         for level in level_dict[attr]:
             string_attr = string_attr + level + ","
         string_attr = string_attr.rstrip(",")
         out_file.write(string_attr + "\n")
     # Write Weights    
     out_file.write("Weights\n")
     for attr in attributes:
         weight_attr = attr + ":"
         for prob in probabilities[attr]:
             weight_attr = weight_attr + str(prob) + ","
         weight_attr = weight_attr.rstrip(",")
         out_file.write(weight_attr + "\n")
     # Write Restrictions
     out_file.write("Restrictions\n")
     for restrict in restrictions:
         restrict_string = ""
         for elem in restrict:
             attr = elem[0]
             levels = elem[1:]
             restrict_string = restrict_string + attr + ":"
             for lev in levels:
                 restrict_string = restrict_string + lev + ","
             restrict_string = restrict_string.rstrip(",") + ";"
         restrict_string = restrict_string.rstrip(";")
         out_file.write(restrict_string + "\n")    
     out_file.close()
    
# Output results to a qualtrics-compatible php file
def qualtrics_out(filename, attributes, level_dict, restrictions, constraints, probabilities, random, profiles, tasks, randomize):
    
    temp_1 = """<?php
// Code to randomly generate conjoint profiles to send to a Qualtrics instance

// Terminology clarification: 
// Task = Set of choices presented to respondent in a single screen (i.e. pair of candidates)
// Profile = Single list of attributes in a given task (i.e. candidate)
// Attribute = Category characterized by a set of levels (i.e. education level)
// Level = Value that an attribute can take in a particular choice task (i.e. "no formal education")

// Attributes and Levels stored in a 2-dimensional Array 

// Function to generate weighted random numbers
function weighted_randomize($prob_array, $at_key)
{
	$prob_list = $prob_array[$at_key];
	
	// Create an array containing cutpoints for randomization
	$cumul_prob = array();
	$cumulative = 0.0;
	for ($i=0; $i<count($prob_list); $i++){
		$cumul_prob[$i] = $cumulative;
		$cumulative = $cumulative + floatval($prob_list[$i]);
	}

	// Generate a uniform random floating point value between 0.0 and 1.0
	$unif_rand = mt_rand() / mt_getrandmax();

	// Figure out which integer should be returned
	$outInt = 0;
	for ($k = 0; $k < count($cumul_prob); $k++){
		if ($cumul_prob[$k] <= $unif_rand){
			$outInt = $k + 1;
		}
	}

	return($outInt);

}
                    """
    temp_2 = """// Re-randomize the $featurearray

// Place the $featurearray keys into a new array
$featureArrayKeys = array();
$incr = 0;

foreach($featurearray as $attribute => $levels){	
	$featureArrayKeys[$incr] = $attribute;
	$incr = $incr + 1;
}

// Backup $featureArrayKeys
$featureArrayKeysBackup = $featureArrayKeys;

// If order randomization constraints exist, drop all of the non-free attributes
if (count($attrconstraintarray) != 0){
	foreach ($attrconstraintarray as $constraints){
		if (count($constraints) > 1){
			for ($p = 1; $p < count($constraints); $p++){
				if (in_array($constraints[$p], $featureArrayKeys)){
					$remkey = array_search($constraints[$p],$featureArrayKeys);
					unset($featureArrayKeys[$remkey]);
				}
			}
		}
	}
} 
// Re-set the array key indices
$featureArrayKeys = array_values($featureArrayKeys);
// Re-randomize the $featurearray keys
shuffle($featureArrayKeys);

// Re-insert the non-free attributes constrained by $attrconstraintarray
if (count($attrconstraintarray) != 0){
	foreach ($attrconstraintarray as $constraints){
		if (count($constraints) > 1){
			$insertloc = $constraints[0];
			if (in_array($insertloc, $featureArrayKeys)){
				$insert_block = array($insertloc);
				for ($p = 1; $p < count($constraints); $p++){
					if (in_array($constraints[$p], $featureArrayKeysBackup)){
						array_push($insert_block, $constraints[$p]);
					}
				}
				
				$begin_index = array_search($insertloc, $featureArrayKeys);
				array_splice($featureArrayKeys, $begin_index, 1, $insert_block);
			}
		}
	}
}


// Re-generate the new $featurearray - label it $featureArrayNew

$featureArrayNew = array();
foreach($featureArrayKeys as $key){
	$featureArrayNew[$key] = $featurearray[$key];
}"""
    temp_3 = """
// Initialize the array returned to the user
// Naming Convention
// Level Name: F-[task number]-[profile number]-[attribute number]
// Attribute Name: F-[task number]-[attribute number]
// Example: F-1-3-2, Returns the level corresponding to Task 1, Profile 3, Attribute 2 
// F-3-3, Returns the attribute name corresponding to Task 3, Attribute 3

$returnarray = array();

// For each task $p
for($p = 1; $p <= $K; $p++){

	// For each profile $i
	for($i = 1; $i <= $N; $i++){

		// Repeat until non-restricted profile generated
		$complete = False;

		while ($complete == False){

			// Create a count for $attributes to be incremented in the next loop
			$attr = 0;
			
			// Create a dictionary to hold profile's attributes
			$profile_dict = array();

			// For each attribute $attribute and level array $levels in task $p
			foreach($featureArrayNew as $attribute => $levels){	
				
				// Increment attribute count
				$attr = $attr + 1;

				// Create key for attribute name
				$attr_key = "F-" . (string)$p . "-" . (string)$attr;

				// Store attribute name in $returnarray
				$returnarray[$attr_key] = $attribute;

				// Get length of $levels array
				$num_levels = count($levels);

				// Randomly select one of the level indices
				if ($weighted == 1){
					$level_index = weighted_randomize($probabilityarray, $attribute) - 1;

				}else{
					$level_index = mt_rand(1,$num_levels) - 1;	
				}	

				// Pull out the selected level
				$chosen_level = $levels[$level_index];
			
				// Store selected level in $profileDict
				$profile_dict[$attribute] = $chosen_level;

				// Create key for level in $returnarray
				$level_key = "F-" . (string)$p . "-" . (string)$i . "-" . (string)$attr;

				// Store selected level in $returnarray
				$returnarray[$level_key] = $chosen_level;

			}

			$clear = True;
			// Cycle through restrictions to confirm/reject profile
			if(count($restrictionarray) != 0){

				foreach($restrictionarray as $restriction){
					$false = 1;
					foreach($restriction as $pair){
						if ($profile_dict[$pair[0]] == $pair[1]){
							$false = $false*1;
						}else{
							$false = $false*0;
						}
						
					}
					if ($false == 1){
						$clear = False;
					}
				}
			}
			$complete = $clear;
		}
	}


}

// Return the array back to Qualtrics
print  json_encode($returnarray);
?>
"""
    # Drop attributes that don't have any levels
    attrout = []
    contin = True
    for i in range(len(attributes)):
        if len(level_dict[attributes[i]]) > 0:
            attrout.append(attributes[i])
        else:
            contin = False
            print("Error: Attribute " + attributes[i] + " has no associated levels")
    if contin == False:
        messagebox.showerror(title="Error",message="Error: Cannot export to PHP. Some attributes have no levels.")
        return 
    
    # Drop any Null constraints
    constrai = []
    for c in constraints:
        if c != []:
            constrai.append(c)
    
    constraints = constrai
    
    out_file = open(filename,"w", encoding="utf-8")
    out_file.write(temp_1)
    out_file.write("\n\n")
    arrayString = "$featurearray = array("
    for i in range(len(attrout)):
        attr = attrout[i]
        
        arrayString = arrayString + '"'+attr+'" => array('
        
        for k in range(len(level_dict[attr])):
            level = level_dict[attr][k]
            arrayString = arrayString + '"' + level + '"'
            if k != len(level_dict[attr]) - 1:
                arrayString = arrayString + ","
                
        if i != len(attributes) - 1:
            arrayString = arrayString + "),"     
        else:
            arrayString = arrayString + ")"
    
    arrayString = arrayString + ");\n\n"
    
    out_file.write(arrayString)
    if len(restrictions) > 0:
        restrictionString = "$restrictionarray = array("
        for m in range(len(restrictions)):
            restrict = restrictions[m]
            restrictionString = restrictionString + "array("
            for i in range(len(restrict)):
                entry = restrict[i]
                restrictionString = restrictionString + "array("
                restrictionString = restrictionString + '"' + entry[0] + '"'
                restrictionString = restrictionString + ","
                restrictionString = restrictionString + '"' + entry[1] + '"'
                if i != len(restrict)-1:
                    restrictionString = restrictionString + "),"
                else:
                    restrictionString = restrictionString + ")"
            if m != len(restrictions)-1:
                restrictionString = restrictionString + "),"
            else:
                restrictionString = restrictionString + ")"

        restrictionString = restrictionString + ");\n\n"
    else:
        restrictionString = '$restrictionarray = array();\n\n'
    
    out_file.write(restrictionString)    
    
    if random == 1:
        probString = "$probabilityarray = array("
        for i in range(len(attrout)):
            attr = attrout[i]
        
            probString = probString + '"'+attr+'" => array('
            for k in range(len(probabilities[attr])):
                prob = probabilities[attr][k]
                probString = probString + str(prob) 
                if k != len(probabilities[attr]) - 1:
                    probString = probString + ","
            

            if i != len(attributes) - 1:
                probString = probString + "),"
            else:
                probString = probString + ")"
                
        probString = probString + ");\n\n"
        
        out_file.write(probString)

     
    
    out_file.write("// Indicator for whether weighted randomization should be enabled or not\n")
    out_file.write("$weighted = " + str(random) + ";\n\n")
    out_file.write("// K = Number of tasks displayed to the respondent\n")
    out_file.write("$K = " + str(tasks) + ";\n\n")
    out_file.write("// N = Number of profiles displayed in each task\n")
    out_file.write("$N = " + str(profiles) + ";\n\n")
    out_file.write("// num_attributes = Number of Attributes in the Array\n")
    out_file.write("$num_attributes = count($featurearray);\n\n")

    if randomize == 1:
        out_file.write("\n")
        
        if len(constraints) > 0:
            constString = "$attrconstraintarray = array("
            for m in range(len(constraints)):
                const = constraints[m]
                constString = constString + "array("
                for i in range(len(const)):
                    entry = const[i]
                    constString = constString + '"' + entry + '"'
                    if i != len(const)-1:
                        constString = constString + ","
                if m != len(constraints)-1:
                    constString = constString + "),"
                else:
                    constString = constString + ")"
            constString = constString + ");\n\n"
        else:
            constString = "$attrconstraintarray = array();\n\n"
        
        out_file.write(constString)        
        out_file.write("\n")
        out_file.write(temp_2)
    else:
        out_file.write("\n")
        out_file.write("$featureArrayNew = $featurearray;\n\n")
    
    out_file.write(temp_3)
    
    out_file.close()

# Output sample HTML template 
def html_out(filename, num_attr, profiles, tasks):
    filename = filename.rstrip("html")
    filename = filename.rstrip(".")
    
    for i in range(tasks):
        # Top Row
        top = '<span>Question '+ str(i+1) + '</span>\n<br /><br />\n<span>Please carefully review the options detailed below, then please answer the questions.</span>\n<br/>\n<br/>\n<span>Which of these choices do you prefer?</span>\n<br />\n<div>\n<br />\n<table class="UserTable">\n<tbody>\n'    
        
        # Create a header row
        header = "<tr>\n<td>&nbsp;</td>\n"
        for k in range(profiles):
            header = header + '<td style="text-align: center;">\n<strong>Choice ' + str(k+1) + '</strong></td>\n'
        header = header + '</tr>\n'
        
        # Row Array
        rows = ["A"]*num_attr
        for m in range(num_attr):
            rows[m] = "<tr>\n<td style='text-align: center;'><strong>${e://Field/F-" + str(i+1) + "-" + str(m+1) + "}</strong></td>\n"
            for n in range(profiles):
                rows[m] = rows[m] + "<td style='text-align: center;'>${e://Field/F-"+str(i+1) +"-" + str(n+1)+"-"+str(m+1)+"}</td>\n"
            rows[m] = rows[m] + "</tr>"
            
        # Ending

        
        footer = "</tbody>\n</table>\n</div>"
        
        text_out = top + header
        for j in rows:
            text_out = text_out + j
            
        text_out = text_out + footer
        
        out_file = open(filename + "_task"+str(i+1) + ".html", "w")
        out_file.write(text_out)
        out_file.close()
    messagebox.showinfo(title="Files Created", message=str(tasks) + " files created\n\n" + filename + "_task#.html")
    
# Main Loop
if __name__=="__main__":
    
    # Create the root window
    root = Tk()
    root.title('Conjoint Survey Design Tool')
    conjointMain = conjointGUI(root)

    # Execute root window main loop
    root.mainloop()
    
