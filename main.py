from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.uix.image import Image

# خلفية عامة داكنة
Window.clearcolor = (0.1, 0.1, 0.12, 1)


# -------- Splash Screen --------
class SplashScreen(Screen):
    def on_enter(self):
        # Fade-in لكل العناصر
        for child in self.children[0].children:
            child.opacity = 0
            anim = Animation(opacity=1, duration=1.5)
            anim.start(child)

        # بعد 3 ثواني نروح للآلة الحاسبة
        Clock.schedule_once(self.switch_to_main, 3)

    def switch_to_main(self, dt):
        self.manager.current = "main"


# -------- Calculator Screen --------
class CalculatorScreen(Screen):
    def build_ui(self):
        self.expression = ""

        main_layout = GridLayout(cols=1, padding=10, spacing=10)

        # شاشة العرض
        self.display = TextInput(
            multiline=False,
            readonly=True,
            halign="right",
            font_size=45,
            background_color=(0.15, 0.15, 0.18, 1),
            foreground_color=(1, 1, 1, 1)
        )

        main_layout.add_widget(self.display)

        # أزرار الآلة الحاسبة
        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '%', '0', 'C', '+'
        ]

        grid = GridLayout(cols=4, spacing=10)

        for button in buttons:
            color = (0.2, 0.2, 0.25, 1)
            if button in ['+', '-', '*', '/', '%']:
                color = (0.9, 0.5, 0.1, 1)
            if button == 'C':
                color = (0.8, 0.2, 0.2, 1)

            btn = Button(
                text=button,
                font_size=30,
                background_color=color,
                color=(1, 1, 1, 1),
                on_press=self.on_button_press
            )

            grid.add_widget(btn)

        # زر "="
        equal_button = Button(
            text='=',
            font_size=35,
            size_hint=(1, 0.4),
            background_color=(0.2, 0.6, 1, 1),
            color=(1, 1, 1, 1),
            on_press=self.on_equal
        )

        main_layout.add_widget(grid)
        main_layout.add_widget(equal_button)

        self.add_widget(main_layout)

    # وظائف الأزرار
    def on_button_press(self, instance):
        if instance.text == "C":
            self.expression = ""
        elif instance.text == "%":
            try:
                self.expression = str(float(self.expression) / 100)
            except:
                self.expression = ""
        else:
            self.expression += instance.text

        self.display.text = self.expression

    def on_equal(self, instance):
        try:
            self.expression = str(eval(self.expression))
            self.display.text = self.expression
        except:
            self.display.text = "Error"
            self.expression = ""


# -------- Main App --------
class CalculatorApp(App):
    def build(self):
        sm = ScreenManager()

        # Splash Screen
        splash = SplashScreen(name="splash")
        splash_layout = GridLayout(cols=1, spacing=10, padding=50)

        # Logo (ضع أي صورة صغيرة اسمها "logo.png" في نفس مجلد المشروع)
        try:
            splash_layout.add_widget(
                Image(source="logo.png", size_hint=(1, 0.3))
            )
        except:
            pass  # إذا ماكانش الصورة، يتجاهل

        # نصوص Splash Screen
        splash_layout.add_widget(
            Label(
                text="Dr.",
                font_size=30,
                bold=True,
                color=(0.9, 0.9, 0.9, 1),
                opacity=0
            )
        )
        splash_layout.add_widget(
            Label(
                text="Kossay Makhlouf",
                font_size=45,
                bold=True,
                color=(0.2, 0.6, 1, 1),
                opacity=0
            )
        )
        splash_layout.add_widget(
            Label(
                text="Calculator",
                font_size=25,
                italic=True,
                color=(0.9, 0.9, 0.9, 1),
                opacity=0
            )
        )

        splash.add_widget(splash_layout)

        # شاشة الآلة الحاسبة
        main_screen = CalculatorScreen(name="main")
        main_screen.build_ui()

        sm.add_widget(splash)
        sm.add_widget(main_screen)

        sm.current = "splash"

        return sm


# تشغيل التطبيق
CalculatorApp().run()