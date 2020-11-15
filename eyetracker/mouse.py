from pynput.mouse import Listener
class Mouse:
    def __init__(self,mouseClick):
        self.mouseClick = mouseClick
        with Listener(on_click=self.on_click) as listener:
            listener.join()
    def on_click(self,x,y,button,pressed):
        if pressed  and button is  button.left:
            self.mouseClick(x , y)
