from kivy.app import App
from kivy.uix.widget import Widget


class MyWidget(Widget):
    pass


class WidgetApp(App):
    def build(self):
        return MyWidget()


app = WidgetApp()
app.run()