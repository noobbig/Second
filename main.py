import os
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.utils import platform

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.utils.set_bars_colors import set_bars_colors
from kivymd.uix.fitimage import FitImage

# Android storage permissions
if platform == 'android':
    from android.permissions import request_permissions, Permission
    request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])

class SampleApp(MDApp):

    def __init__(self, **kwargs) -> None:
        super(SampleApp, self).__init__(**kwargs)
        self.theme_cls.primary_palette = "Darkblue"

    def build(self) -> MDScreen:
        self.appKv="""
MDScreen:
    MDBoxLayout:
        orientation: 'vertical'
        MDTopAppBar:
            title: "Gallery App"
            elevation: 4
        
        ScrollView:
            MDGridLayout:
                id: imageGrid
                cols: 3
                adaptive_height: True
                padding: dp(10)
                spacing: dp(10)

    MDButton:
        style: 'tonal'
        pos_hint: {'center_x': 0.5, 'center_y': 0.1}
        on_press:
            app.apply_styles("Light") if (not app.theme_cls.theme_style == "Light") else app.apply_styles("Dark")

        MDButtonText:
            text: 'Switch Theme'
"""
        AppScreen = Builder.load_string(self.appKv)
        self.apply_styles("Light")
        return AppScreen

    def on_start(self):
        self.load_gallery()

    def load_gallery(self):
        if platform == 'android':
            from android.storage import primary_external_storage_path
            path = primary_external_storage_path()
        else:
            path = os.path.expanduser("~")

        exts = ('.jpg', '.png', '.jpeg')
        image_list = []
        
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.lower().endswith(exts):
                    image_list.append(os.path.join(root, file))
                    if len(image_list) > 30: 
                        break
            if len(image_list) > 30:
                break

        for img_path in image_list:
            image_widget = FitImage(
                source=img_path,
                size_hint_y=None,
                height="120dp",
                radius="12dp"
            )
            self.root.ids.imageGrid.add_widget(image_widget)

    def apply_styles(self, style: str = "Light") -> None:
        self.theme_cls.theme_style = style
        if style == "Light":
            Window.clearcolor = status_color = nav_color = self.theme_cls.surfaceColor
            style = "Dark"
        else:
            Window.clearcolor = status_color = nav_color = self.theme_cls.surfaceColor
            style = "Light"
        self.set_bars_colors(status_color, nav_color, style)

    def set_bars_colors(self, status_color: list[float] = [1.0, 1.0, 1.0, 1.0], nav_color: list[float] = [1.0, 1.0, 1.0, 1.0], style: str = "Dark") -> None:
        set_bars_colors(
            status_color,  # status bar color
            nav_color,  # navigation bar color
            style,  # icons style of status and navigation bar
        )

if __name__ == "__main__":
    app = SampleApp()
    app.run()
