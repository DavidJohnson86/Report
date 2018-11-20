import kivy

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen  # Imports the Kivy Screen manager and Kivys Screen class
import os

Builder.load_string("""

<Default_Button@Button>:
    #color: .8,.9,0,1

<Default_Label@Label>:
    color: 0,0,0,1

      
    
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
    padding: [10,10]
    border: 10, 10, 10, 10
    
    #Default_Label:
        #id: label_total
        #text: 'Report Manager'
        #font_size: 20
        #pos_hint: {'x': 0, 'top':1}
              
       
    BoxLayout:
        orientation: "horizontal"
        Default_Label:
            text: "Main Report"
        TextInput:
            id: entry
            
                     
        Default_Button
            text: "Browse"
            on_release:  root.manager.current = 'file_chooser'
            
    BoxLayout:
        orientation: "horizontal"
        Default_Label:
            text: "Second Report"
        TextInput:
            on_text: ""
        Default_Button
            text: "Browse"
            on_release: root.manager.current = 'file_chooser'
            
    BoxLayout:
        orientation: "horizontal"
        Default_Button
            text: "OK"
            on_release: main.open(filechooser.path, filechooser.selection)
        Default_Button
            text: "Quit"
            on_release: main.open(filechooser.path, filechooser.selection)
   
        
<FileChooser>:
    id: file_chooser
    FileChooserListView:
        on_selection: root.manager.current = 'main_screen'
        on_selection: root.selected()
      
       
   
""")


class Main(BoxLayout, Screen):
    report_one = ""
    print(report_one)

    def open(self, path, filename):
        with open(os.path.join(path, filename[0])) as f:
            print(f.read())

class FileChooser(BoxLayout, Screen):
    def selected(self):
        self.ids.my_widget.ids.my_label.text = ""


sm = ScreenManager()
sm.add_widget(Main(name='main_screen'))
sm.add_widget(FileChooser(name='file_chooser'))


class MyApp(App):

    def build(self):
        from kivy.core.window import Window
        Window.size = (450, 100)
        self.title = 'Report Manager'
        return sm

if __name__ == '__main__':
    MyApp().run()