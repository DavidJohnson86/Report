import kivy

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen  # Imports the Kivy Screen manager and Kivys Screen class
import os
from kivy.properties import StringProperty
from kivy.core.window import Window

Builder.load_string("""

<Default_Button@Button>:
    #color: .8,.9,0,1

<Default_Label@Label>:
    color: 0,0,0,1

<AppScreenManager>:
    Main:
        id: main_screen
    FileChooser1:
        id: file_chooser1
    FileChooser1:
        id: file_chooser2
    
<Main>:
    id: main_screen
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            pos: self.pos
            size: self.size
    
    orientation : "vertical"
    spacing: 10
    padding: [5,5]
    border: 10, 10, 10, 10
    #Default_Label:
        #id: label_total
        #text: 'Report Manager'
        #font_size: 20
        #pos_hint: {'x': 0, 'top':1}
  
        
    GridLayout:
        cols: 3
        spacing: 10
        orientation: "horizontal"
        Default_Label:
            text: "Main Report"
        TextInput:
            id: entry1
            text: root.report_one
        Default_Button
            text: "Browse"
            on_release: root.manager.current = "file_chooser1"
          

        Default_Label:
            text: "Second Report"
        TextInput:
            id: entry2
            text: root.report_two
        Default_Button
            text: "Browse"
            on_release: root.manager.current = "file_chooser2"
    
        Default_Button
            text: "OK"
            on_release: main.open(filechooser.path, filechooser.selection)
        Label:
            text:""
        Default_Button
            text: "Quit"
            on_release: main.open(filechooser.path, filechooser.selection)


<FileChooser1>:
    id: file_chooser1
    FileChooserListView:
        on_selection: root.manager.current = 'main_screen'
        on_selection: root.ChangeScreen(self.selection[0])
        
<FileChooser2>:
    id: file_chooser2
    FileChooserListView:
        on_selection: root.manager.current = 'main_screen'
        on_selection: root.ChangeScreen(self.selection[0])



""")


class AppScreenManager(ScreenManager):
    pass


class Main(Screen):
    report_one = StringProperty()
    report_two = StringProperty()

    def open(self, path, filename):
        with open(os.path.join(path, filename[0])) as f:
            print(f.read())


class FileChooser1(Screen):

     def ChangeScreen(self, text):
        sm.get_screen('main_screen').ids.entry1.text = text


class FileChooser2(Screen):

    def ChangeScreen(self, text):
        sm.get_screen('main_screen').ids.entry2.text = text


sm = ScreenManager()
sm.add_widget(Main(name='main_screen'))
sm.add_widget(FileChooser1(name='file_chooser1'))
sm.add_widget(FileChooser2(name='file_chooser2'))


class MyApp(App):

    def build(self):
        Window.size = (450, 150)
        self.title = 'Report Manager'
        return sm


if __name__ == '__main__':
    MyApp().run()