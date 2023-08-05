import plyer
from kivy import platform, Logger

if platform == "android":
    try:
        from jnius import autoclass, cast, PythonJavaClass, java_method
        from android.runnable import run_on_ui_thread

        activity = autoclass("org.kivy.android.PythonActivity")

        AdRequest = autoclass("com.google.android.gms.ads.AdRequest")
        AdRequestBuilder = autoclass(
            "com.google.android.gms.ads.AdRequest$Builder"
        )

        AdSize = autoclass("com.google.android.gms.ads.AdSize")
        AdView = autoclass("com.google.android.gms.ads.AdView")
        MobileAds = autoclass("com.google.android.gms.ads.MobileAds")
        LayoutParams = autoclass("android.view.ViewGroup$LayoutParams")
        LinearLayout = autoclass("android.widget.LinearLayout")
        Gravity = autoclass("android.view.Gravity")
        View = autoclass("android.view.View")

    except Exception as err:
        Logger.error("KivyBannerMob: " + str(err))
else:

    def run_on_ui_thread(x):
        pass


class TestIds:
    """ Test AdMob App ID """
    APP = "ca-app-pub-3940256099942544~3347511713"

    """ Test Banner Ad unit ID """
    BANNER = "ca-app-pub-3940256099942544/6300978111"


class AdMobBridge:
    def __init__(self, appID):
        pass

    def add_test_device(self, test_device):
        pass

    def load_banner_ad(self, bannerID):
        pass

    def show_banner(self):
        pass


class Admob(AdMobBridge):
    @run_on_ui_thread
    def __init__(self, appID, useTestDevice):
        super().__init__(appID)
        if useTestDevice:
            MobileAds.initialize(activity.mActivity, TestIds.APP)
        else:
            Logger.info("KivyBannerMob: Admob App ID initialized with " + str(appID))
            MobileAds.initialize(activity.mActivity, appID)

        self._adview = AdView(activity.mActivity)
        self.useTestDevice = useTestDevice
        self._test_devices = []

    @run_on_ui_thread
    def load_banner_ad(self, bannerID):

        if self.useTestDevice:
            self._adview.setAdUnitId(TestIds.BANNER)
        else:
            Logger.info("KivyBannerMob: BannerAd using unit ID " + str(bannerID))
            self._adview.setAdUnitId(bannerID)

        self._adview.setAdSize(AdSize.SMART_BANNER)

        self._adview.setVisibility(View.GONE)
        adLayoutParams = LayoutParams(
            LayoutParams.MATCH_PARENT, LayoutParams.WRAP_CONTENT
        )
        self._adview.setLayoutParams(adLayoutParams)
        layout = LinearLayout(activity.mActivity)
        layout.setGravity(Gravity.BOTTOM)
        layout.addView(self._adview)
        layoutParams = LayoutParams(
            LayoutParams.MATCH_PARENT, LayoutParams.MATCH_PARENT
        )
        layout.setLayoutParams(layoutParams)
        activity.addContentView(layout, layoutParams)

        self.builder = AdRequestBuilder()

        if self.useTestDevice:
            Logger.info("KivyBannerMob: Adding Test Device: " + str(plyer.uniqueid.id))
            self.add_test_device(str(plyer.uniqueid.id))
        else:
            Logger.info("KivyBannerMob: Showing live ads from Admob")

        Logger.info("KivyBannerMob: AdView loaded.")
        self._adview.loadAd(self.builder.build())

    @run_on_ui_thread
    def add_test_device(self, test_device):
        for test_device in self._test_devices:
            self.builder.addTestDevice(test_device)

    @run_on_ui_thread
    def show_banner(self):
        Logger.info("KivyBannerMob: show_banner called.")
        self._adview.setVisibility(View.VISIBLE)

    @run_on_ui_thread
    def hide_banner(self):
        Logger.info("KivyBannerMob: hide_banner called.")
        self._adview.setVisibility(View.GONE)


class KivyBannerMob:
    def __init__(self, appID, useTestDevice=True):
        Logger.info("KivyBannerMob: __init__ called.")
        if platform == "android":
            # Setting below to True, will override your appID and bannerID to use test ads :)
            self.bridge = Admob(appID, useTestDevice)  # app ID
        else:
            Logger.warning("KivyBannerMob: This only runs on Android devices")

    def load_banner_ad(self, unitID):
        if platform == "android":
            self.bridge.load_banner_ad(unitID)  # ad unit ID

    def show_banner(self):
        if platform == "android":
            self.bridge.show_banner()

    def hide_banner(self):
        if platform == "android":
            self.bridge.show_banner()
