# KivyBannerMob

Put Admob banner ads in your Kivy application

## Example usage

```
class MyApp(App):
    def __init__(self):
        super().__init__()
        
        admob = KivyBannerMob('ca-app-pub-7420457689342922~9251120518', True) # if True, will disregard your APP ID and Banner Ad Unit ID and display the Test Admob Banner Ad
        admob.load_banner_ad('ca-app-pub-7420457689342922/1311445966')
        admob.show_banner()
            
    def build(self):
        return Label(text='Hello world')


if __name__ == '__main__':
    MyApp().run()
```