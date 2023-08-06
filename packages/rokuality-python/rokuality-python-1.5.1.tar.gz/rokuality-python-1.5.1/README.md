# Rokuality Python - End to End Test Automation for Roku, XBox, Tizen TV, LG webOS, and HDMI devices including Cable SetTop, Playstation, Tivo and more!

The Rokuality platform allows you to distribute Roku, XBox, Tizen TV, LG webOS, and HDMI device end to end tests across multiple devices on your network. Our platform's goal is to provide a low cost solution for various video streaming platforms that otherwise don't offer an easily automatable solution! Download the [Rokuality App](https://www.rokuality.com) and start writing tests!

### Contents
1. [Getting Started with the Rokuality App](#getting-started-get-the-rokuality-app)
2. Automation Platforms
    * [Roku Device Requirements](#device-requirements-roku)
    * [XBox Device Requirements](#device-requirements-xbox)
    * [Samsung Tizen TV Device Requirements](#device-requirements-tizen-tv)
    * [LG webOS TV Device Requirements](#device-requirements-lg-webos)
    * [HDMI Device (Cable SetTop, Tivo, Playstations, and More) Requirements](#Device-requirements-HDMI-Devices-Cable-SetTop-Playstations-Tivo-and-more)
3. Getting Started - [Add Rokuality to Your Python Test Project](#Getting-started-Add-the-bindings-to-your-Project)
4. The Basics - [Starting a Driver and Connecting to Your Device](#the-basics)
5. Finding Elements and Evaluating your Device Screen
    * [Finding Elements on Screen for All Platforms](#finding-elements)
    * [Finding Elements - Roku Webdriver](#Finding-elements-with-Roku-WebDriver)
    * [Finding Elements - Tizen and LG webOS with HTML Capturing](#Finding-elements-with-Tizen-TV-LG-webOS-and-HTML-Capturing)
    * [Element and Polling Timeouts](#Element-Timeouts-and-Polling)
6. Sending Remote Control Commands to your Device
    * [Roku](#Sending-remote-control-commands-to-the-device-Roku-and-XBox)
    * [XBox](#Sending-remote-control-commands-to-the-device-Roku-and-XBox)
    * [Tizen](#Sending-remote-control-commands-to-the-device-tizen-tv)
    * [LG webOS](#Sending-remote-control-commands-to-the-device-lg-webos)
    * [HDMI Devices](#Sending-remote-control-commands-to-an-HDMI-connected-Device-via-Harmony)
7. [Getting Device Screen Artifacts](#Getting-screen-artifacts) - screenshots, video recordings, page source, size, and more
8. Required Device Capabilities for Session Start
    * [Roku](#Roku)
    * [XBox](#XBox)
    * [Tizen TV](#Tizen-TV)
    * [LG WebOS](#LG-webOS)
    * [HDMI Devices](#HDMI-Devices-Cable-SetTop-Playstations-Tivo-and-more)
9. [All Device Capabilities](#all-device-capabilities)
10. Using an OCR Provider for Textual Identification on Screen
    * [Google Vision](#Using-Google-Vision-OCR)
    * [Amazon Rekognition](#Using-Amazon-Rekognition-OCR)
    * [Amazon Textract](#Using-Amazon-Rekognition-OCR)
11. Roku Platform Only
    * [Get Roku Media Player Information](#Getting-information-about-the-media-player-ROKU-ONLY) - bitrate, encoding, media state and more
    * [Get Roku Debug Logs](#Getting-debug-log-info-ROKU-ONLY)
    * [Get Roku Performance Details During Execution](#Getting-performance-data-from-your-application-during-test-ROKU-ONLY)
    * [Testing Roku Deep Links](#Testing-Deep-Links-ROKU-ONLY)
    * [Roku Proxy with SSL Support](#Roku-Proxy-with-ssl-support)
        * [Getting Started](#Roku-Proxy-Getting-Started)
        * [Starting a Proxy](#Roku-Proxy-Starting-a-Proxy)
        * [Monitoring HTTP(s) Requests/Responses During Test](#Roku-Proxy-Monitoring-http-and-https-Calls-During-a-Test)
        * [Rewriting HTTP(s) Traffic During Test](#Roku-Proxy-Applying-Rewrites)

### Getting started: Get the Rokuality App
The [Rokuality App](https://www.rokuality.com/download) operates in 2 modes within a standalone app for Mac and Windows: First as a test debugger/builder which allows you to debug your apps, and Second, as a server which can be used to execute/distribute your tests to your devices.

Once you have installed the Rokuality app, you can start a server which listens for any incoming tests that you've written:

<img src="https://rokuality-public.s3.amazonaws.com/StartServer.png" align="left" height="248" width="288" >

<img src="https://rokuality-public.s3.amazonaws.com/ServerListening.png" align="left" height="248" width="288" > <br /> <br /> <br /> <br /> <br /> <br /> <br /> <br /> <br /> <br />

Note that you can start and run the server headlessly if you download the standalone jar and provide the `serveronly=true` system property during launch. Useful if running on a linux machine or if running from a build/test server environment.

```xml
    java -Dserveronly=true -Dport=7777 -jar /path/to/Rokuality_version.jar
```

Optionally, you can provide a desired set of capabilities and start a manual test session against your device. The test debugger includes a number of UI tools that are geared to help you construct your automated tests:

<img src="https://rokuality-public.s3.amazonaws.com/NewTest.png" align="left" height="248" width="288" >

<img src="https://rokuality-public.s3.amazonaws.com/Test.png" align="left" height="248" width="288" > <br /> <br /> <br /> <br /> <br /> <br /> <br /> <br /> <br /> <br />

### Device requirements: Roku
Automated testing on Roku requires that you have Developer mode enabled on your device. [Enabling developer mode](https://blog.roku.com/developer/developer-setup-guide) on your Roku device is very straight forward. Keep track of your device username and password as created during the basic walkthrough as you'll need them to pass to your DeviceCapabilities at driver startup. Once you've enabled developer mode on your device you should be able to hit the device console page at http://yourrokudeviceip - Once that's done you are all set for automation!

### Device requirements: XBox
Automated testing on XBox requires the following:
1. Google Chrome browser installed on the machine running the Rokuality server. The server uses headless chrome to handle various tasks like installing/launching/uninstalling the XBox appxbundles. You won't physically see chrome launch as it will run in headless mode.
2. Your XBox must be in dev kit mode. [Enabling developer mode](https://docs.microsoft.com/en-us/windows/uwp/xbox-apps/devkit-activation) on your XBox is straight forward but it does require a 19$ Microsoft developer account which will allow you to automate 3 boxes from a single dev account.
3. You must have the [XBox dev console](https://docs.microsoft.com/en-us/windows/uwp/xbox-apps/device-portal-xbox) available for remote access with NO username/password set. If properly setup you should be able to access your dev console remotely at `https://yourxboxip:11443`

### Device requirements: Tizen TV
Automated testing on Tizen TV requires the following:
1. Google Chrome browser installed on the machine running the Rokuality server. The server uses headless chrome to handle various tasks like installing/launching/uninstalling the Tizen TV .wgt app packages. You won't physically see chrome launch as it will run in headless mode.
2. You must have [Tizen Studio](https://developer.tizen.org/development/tizen-studio/download) installed on your machine.
3. Your Tizen TV must be in [developer mode](https://developer.samsung.com/smarttv/develop/getting-started/using-sdk/tv-device.html) and be able to be reached from your machine running the Rokuality app. If setup correctly you should be able to connect to the device from the command line via `sdb connect your_tizen_tv_machine_ip_address:26101`.

### Device requirements: LG webOS
Automated testing on LG webOS TV's requires the following:
1. You must install the [LG webOS Developer SDK](http://webostv.developer.lge.com/sdk/installation/)
2. You must [enable developer mode](http://webostv.developer.lge.com/develop/app-test) on the tv.
3. You must enable/allow "LG Connect Apps" on your TV. Typically found at settings>>all settings>>network>>LG connect apps.

### Device requirements: HDMI Devices (Cable SetTop, Playstations, Tivo, and more)
Automated testing is possible for any device with an HDMI out that accepts IR or bluetooth commands in. It requires the following:
1. You must connect your HDMI device via its HDMI input to an encoder on your network. We recommend the [J-Tech H.264 Encoder](https://jtechdigital.com/product/jtech-ench4-0220/) as it is inexepensive, efficient, and easy to configure/connect your device. Once [configured](http://jtechdi1.nextmp.net/wp-content/uploads/product/jtd-220/JTD-220_Version_1_1_1.pdf) you can access the hdmi output of your device anywhere on your network. This allows the Rokuality app to query your device and perform Image and OCR evaluations against your device's screen.  See the [why encoder?](#whyencoder) section for details.
2. You must have a [Logitech Harmony Hub](https://www.logitech.com/en-us/product/harmony-hub?crid=60) with your device setup as a device and XMPP enabled on the hub. See the sections [why harmony](#whyharmony) and [configuring your harmony](#configuringyourharmony) for details. This is a low cost and extensible solution that allows the Rokuality app to send IR and bluetooth commands to your device without requiring any "magic box" hardware.

### Getting started: Add the bindings to your Project
To use Rokuality in your tests or application, install the `rokuality-python` dependency:
```xml
    pip install rokuality-python
```

### The Basics:
The Rokuality bindings operate via Image Based Object Recognition and OCR techniques to identify 'elements' on the device screen and return them to your test scripts as Objects for verification and interaction. The project is modeled after the Selenium/Appium structure so if you've used those toolsets for browsers/mobile devices previously - this framework will look and feel very comfortable to you. See the [Roku example tests](https://github.com/rokuality/rokuality-python/blob/master/tests/test_roku.py) or [XBox example tests](https://github.com/rokuality/rokuality-python/blob/master/tests/test_xbox.py) or [Tizen TV example tests](https://github.com/rokuality/rokuality-python/blob/master/tests/test_tizentv.py) or [LG webOS example tests](https://github.com/rokuality/rokuality-python/blob/master/tests/test_lg_webos.py) or the [HDMI example tests](https://github.com/rokuality/rokuality-python/blob/master/tests/test_hdmi.py)
for a full list of samples.

#### Declare a driver to connect to the server:
```python
    '''Roku'''
    driver = RokuDriver("http://yourserverurl:yourrunningserverport", self.capabilities)

    '''XBox'''
    driver = XBoxDriver("http://yourserverurl:yourrunningserverport", self.capabilities)

    '''Tizen'''
    driver = TizenTVDriver("http://yourserverurl:yourrunningserverport", self.capabilities)

    '''LG webOS'''
    driver = LGWebOSDriver("http://yourserverurl:yourrunningserverport", self.capabilities)

    '''HDMI'''
    driver = HDMIDriver("http://yourserverurl:yourrunningserverport", self.capabilities)
```
This will take care of installing/launching your device app package, ensure the device is available and ready for test, and start a dedicated session on your device as indicated via your DeviceCapabilities object. See [Device Capabilities](#device-capabilities-explained) for an explanation of what capabilities are available for your driver startup. Note that app installation is not supported when using the HDMIDriver.

#### Finding elements:
There are a variety of ways to locate elements depending on your device type. The 2 primary ways available to all devices are:

1) TEXT
```python
    driver.finder().find_element(By().text("text to find on screen"))
```
In this example, the Rokuality server will capture the image from your device screen, and then perform an evaluation against the found text within that image and match it against your locator. If your locator text is NOT found, then a NoSuchElementException will be thrown. Note that this will use Google Vision, Amazon Rekognition, or Amazon Textract ocr engines as provided by your capability object. See [Using Google Vision](#using-google-vision-ocr), [Using Amazon Rekognition](#using-amazon-rekognition-ocr), or [Using Amazon Textract](#using-amazon-textract-ocr) for those details.

2) IMAGE - local image snippet file
```python
    driver.finder().find_element(By().image("/path/to/your/image/snippet.png"))
```
In this example, you can provide the path to an image snippet that you expect to be contained within your device screen. The server will then ship this image snippet to itself, capture the device screen, and evaluate if it exists on the device.

OR

3) IMAGE - url to to an image snippet file
```python
    driver.finder().find_element(By().image("http://urltoyourimagesnippet.png"))
```
In this example, you can provide a url to your locator image snippet and the server will download that image and evaluate it against the device screen. Useful for those more dynamic testing situations where you may want to query your application feeds to get the dynamic app images for evaluation, or if you want to keep your image based locators in a remote repository.

#### Finding elements with Roku WebDriver:
Optionally when testing on Roku you can provide the following native based locator types:
```python
    element_by_text = roku_driver.finder().find_element(RokuBy().text('text to search for'))
    element_by_tag = roku_driver.finder().find_element(RokuBy().tag('tag'))
    element_by_attribute = roku_driver.finder().find_element(RokuBy().attribute('attribute', 'attribute value'))
```

#### Finding elements with Tizen TV, LG webOS and HTML Capturing:
When testing on Tizen TV or an LG webOS TV, you can provide the following CSS or XPath locators:
```python
    element_by_css = driver.finder().find_element(HTMLBy().css('css locator'))
    element_by_xpath = driver.finder().find_element(HTMLBy().xpath('xpath locator'))
```

#### Finding multi match elements:
You can search for multiple element matches from a singular locator and return the results of match to an Element collection as follows:
```python
    elements = driver.finder().find_elements(By().text("locator that will return multiple matches"))
```
When using `find_elements`, a NoSuchElementException will NOT be thrown to the user in the event that an element is not found. In that event the collection will be empty. So this method can be used to determine if an element is present or not:

```python
    elements = driver.finder().find_elements(By().text("locator"))
    if (len(elements) == 0):
            print("element is not present")
```

#### Elements as objects:
A found element can be stored to an object and additional details about it can be retrieved:
```python
    element = self.roku_driver.finder().find_element(By().text("Hello World!"))
    print("element x: " + str(element.get_x()))
    print("element y: " + str(element.get_y()))
    print("element width: " + str(element.get_width()))
    print("element height: " + str(element.get_height()))
    print("element confidence: " + str(element.get_confidence()))
    print("element text: " + element.get_text())
```
The element details include the elements location and size details as found on the device, the text contained within the match (relevent if an image snippet locator was provided), and the confidence score of the match with higher values indicating the confidence in your find:
```xml
    368
    319
    45
    19
    91.33713
    Hello World!
```

#### Sending remote control commands to the device: Roku and XBox
To send remote button presses to the device you can do the following:
```python
    '''roku'''
    driver.remote().press_button(RokuButton.SELECT)
    
    '''xbox'''
    driver.remote().press_button(XBoxButton.A)
```

#### Sending remote control commands to the device: Tizen TV
For Tizen, you must first authorize the TV and receive an api token which can then be used for all your driver sessions. You'll need to manually accept the alert one time before you can proceed. Note that the api token will be valid for as long as the TV is powered on and awake.
```python
    '''to performan remote control interactions on a tizen tv
    first you need to authorize the tv manually, which returns
    an api token you can pass to your tests'''
    TizenTVRemoteAuthorizer remoteAuthorizer = new TizenTVRemoteAuthorizer("http://localhost:7777", "your_tizen_tv_ip_address");
    tizen_tv_remote_authorizer = TizenTVRemoteAuthorizer('http://localhost:7777', 'your_tizen_tv_ip_address')
		
    '''This will trigger a manual alert on your Tizen TV that you will have 60 seconds to accept once accepted it will return an api token which you can pass to the 'DeviceAPIToken' capability for your automated tests.'''
    api_key = tizen_tv_remote_authorizer.authorize()
```

Additionally, you can use the Rokuality UI test builder to authorize your remote and retrieve your `DeviceAPIToken` during a live test session:

<img src="https://rokuality-public.s3.amazonaws.com/TizenAuthorizeRemote.png" align="left" height="248" width="288" > <br /> <br /> <br /> <br /> <br /> <br /> <br /> <br /> <br /> <br />

#### Sending remote control commands to the device: LG webOS
For LG webOS, there is a one time manual confirmation prompt that must be accepted when you send a remote command. Once you accept this on your tv - the remote key will be saved for your machine and all future requests won't require a prompt.
```python
    driver.remote().press_button(LGWebOSButton.HOME)
```

#### Sending remote control commands to an HDMI connected Device via Harmony:
To send remote button presses to an HDMI device via Harmony you can do the following:
```python
    '''get available remote commands'''
	button_options = self.hdmi_driver.remote().get_button_options()
    print(button_options)

    '''send a remote command'''
    self.hdmi_driver.remote().press_button("DirectionUp")
```

All remote commands are available. See [roku remote command](https://github.com/rokuality/rokuality-python/blob/master/src/enums/roku_button.py) or [xbox remote command](https://github.com/rokuality/rokuality-python/blob/master/src/enums/xbox_button.py) or [tizen remote command](https://github.com/rokuality/rokuality-python/blob/master/src/enums/tizen_tv_button.py) or [lg webos remote command](https://github.com/rokuality/rokuality-python/blob/master/src/enums/lg_webos_button.py) for all available remote buttons. Also you can send literal characters to the device if you need to interact with a Roku/XBox/LG webOS search selector (Note the virtual keyboard must be visible on the screen at the time this call is made):
```python
    driver.remote().send_keys("typing out hello world on a search screen")
```

Note that by default, the time delay between multiple remote control commands is 0 milliseconds, meaning multiple remote control commands will happen as quickly as possible. This can in some cases lead to test flake due to multiple commands happening back to back too quickly. If this is happening, you can add a delay in between remote control button presses as follows:
```python
    """
    sets a delay between remote control button presses to 2 seconds. this will last for the duration of the session or until a new value is set. If not set, defualts to 0
    """
    driver.options().set_remote_interact_delay(2000)
```

#### Getting screen artifacts:
Various methods exist for getting screen artifacts such as the screen image, sub screen image, screen recording during test, and screen text:

```python
    '''get screen size'''
    driver.screen().get_screen_size()

    '''get screen image'''
    driver.screen().get_image()

    '''get the screen sub image from starting x,y with width/height'''
    driver.screen().get_image_sub_screen(1, 1, 300, 300)

    """get the screen recording of the test session from start to now
       note that the screen recordings are created by stitching the collected device screenshots
       together and video quality won't be the best"""
    driver.screen().get_recording()

    '''get the xml page source of the channel. (Roku, TizenTV, and LG webOS)'''
    xml_source = driver.screen().get_page_source()
```

#### Getting screen text:
Screen text of the device is returned as a collection of ScreenText objects as found on the screen. Each ScreenText item will be an object containing details about the found device text such as location, height, and width of the word as found on the device screen:
```python
    screen_texts = roku_driver.screen().get_text()
    for screen_text in screen_texts:
        x = screen_text.get_x()
        y = screen_text.get_y()
        width = screen_text.get_width()
        height = screen_text.get_height()
        confidence = screen_text.get_confidence()
```

Alternatively you can get the entire device screen as a full string via `driver.screen().get_text_as_string()`

#### Getting information about the media player (ROKU ONLY):
For Roku devices, it's possible to get details about your media player in flight through the Roku WebDriver rest api which can be accessed in your test code as follows:
```python
    '''gets information about the media in flight including state, bitrate, encoding information, and much much more!'''
    media_player_info = self.roku_driver.info().get_media_player_info()
    assert media_player_info.is_error() == False
    assert media_player_info.is_live() == False
    assert media_player_info.get_state() == 'none'
```

#### Getting performance data from your application during test (ROKU ONLY):
Roku provides a way to measure your app's cpu and memory utilization through their brightscript profiler. Our platform allows you to access the brightscript performance profile during the course of your test. To utilize this functionality you must provide the 'EnablePerformanceProfiling' capability on test session start and set the value to true. This will take your provided sideloadable .zip package, update the manifest with the necessary values for profile capturing, and then recompile for automation on your device.

```python
    self.capabilities.add_capability('EnablePerformanceProfiling', True)
    self.roku_driver = RokuDriver(self.SERVER_URL, self.capabilities)

    performance_profile = self.roku_driver.info().get_performance_profile()
    performance_profile_mb = os.path.getsize(performance_profile) / 1000000
    print("Performance profile MB size: " + str(performance_profile_mb))
```

Once you've retrieved your .bsprof file during test - this file can be uploaded to [Roku's profiler visualization tool](http://devtools.web.roku.com/profiler/viewer/) to see the performance data in a friendly user format.

#### Getting debug log info (ROKU ONLY):
For Roku devices, it's possible to get the debug logs as follows:
```python
    log_content = self.driver.info().get_debug_logs()
```

#### Testing Deep Links (ROKU ONLY):
It's possible to test your Roku deep links by providing the `ContentID` and `MediaType` capabilities for the deep like you wish to launch. Upon session start the channel should be launched with the deep link content already loaded. If the deep link fails to load a `SessionNotStartedException` will be thrown with details.

```python
    capabilities = DeviceCapabilities()
    capabilities.add_capability('ContentID', 'idofcontent')
    capabilities.add_capability('MediaType', 'mediatypeofcontent')
    driver = RokuDriver(SERVER_URL, capabilities)

    '''the application should be launched with the deep link content loaded'''
```

#### Device Capabilities explained:
Various capabilities and values can be provided and passed to your driver instance at startup. Some of them are required and others are optional. The following are the minimum capabilities **required** to start a driver session.

#### Roku
```python
    '''init a capability object'''
    capabilities = DeviceCapabilities()

    '''indicates you want a Roku test'''
    capabilities.add_capability("Platform", "Roku")

    '''set the path or url to your sideloadable .zip'''
    capabilities.add_capability("AppPackage", "path/or/url/to/your/apppackage")

    '''set your roku ip address'''
    capabilities.add_capability("DeviceIPAddress", "yourdeviceipaddress")

    '''set your device username and password'''
    capabilities.add_capability("DeviceUsername", "yourdeviceusername")
    capabilities.add_capability("DevicePassword", "yourdevicepassword")
    
    '''pass the capabilities and start your driver'''
    driver = RokuDriver("http://yourserverurl:yourrunningserverport", capabilities)
```

#### Xbox
```python
    '''init a capability object'''
    capabilities = DeviceCapabilities()

    '''indicates you want a XBox test'''
    capabilities.add_capability("Platform", "XBox")

    '''set the path or url to your .appxbundle package to install'''
    capabilities.add_capability("AppPackage", "path/or/url/to/your/apppackage")

    '''the app id - will be the friendly app name of your appxbundle'''
    capabilities.add_capability("App", "appid")

    '''set your xbox ip address'''
    capabilities.add_capability("DeviceIPAddress", "yourdeviceipaddress")
    
    '''pass the capabilities and start your driver'''
    driver = XBoxDriver("http://yourserverurl:yourrunningserverport", capabilities)
```

#### Tizen TV
```python
    '''init a capability object'''
    capabilities = DeviceCapabilities()

    '''indicates you want a Tizen TV test'''
    capabilities.add_capability("Platform", "Tizen")

    '''set the path or url to your .wgt package to install'''
    capabilities.add_capability("AppPackage", "/path/or/url/to/your/package.wgt")

    '''the device ip address '''
    capabilities.add_capability("DeviceIPAddress", "your tizen device ip address")

    '''the device id as obtained via sdb devices when your tv is connected'''
    capabilities.add_capability("DeviceID", "your tizen device id")

    '''the ip address of the machine running the rokuality server'''
    capabilities.add_capability("ServerIPAddress", "your host machine ip address")

    '''device api token'''
    capabilities.add_capability("DeviceAPIToken", "your device api token")
    
    '''pass the capabilities and start your driver'''
    driver = TizenTVDriver("http://yourserverurl:yourrunningserverport", capabilities)
```

#### LG webOS
```python
    '''init a capability object'''
    capabilities = DeviceCapabilities()

    '''indicates you want an LG webOS test'''
    capabilities.add_capability("Platform", "LGwebOS")

    '''set the path or url to your zipped up webOS project note that the rokuality app will take care of generating an installable IPK from your provided project'''
    capabilities.add_capability("AppPackage", "/path/or/url/to/your/webOSproject.zip")

    '''the device ip address '''
    capabilities.add_capability("DeviceIPAddress", "your lg webos tv device ip address")

    '''the device id as generated during developer mode setup. can be obtained via 'ares-setup-device --list' when your tv is connected'''
    capabilities.add_capability("DeviceID", "your lg webos tv device id")

    '''the ip address of the machine running the rokuality server'''
    capabilities.add_capability("ServerIPAddress", "your host machine ip address")
    
    '''pass the capabilities and start your driver'''
    driver = LGWebOSDriver("http://yourserverurl:yourrunningserverport", capabilities)
```

#### HDMI Devices (Cable SetTop, Playstations, Tivo, and more)
```python
    '''init a capability object'''
    capabilities = DeviceCapabilities()

    '''The HDMI driver works for any device with HDMI out and IR/Bluetooth in
	includes cable settop boxes, playstations, tivo's, and more'''
    capabilities.add_capability("Platform", "HDMI")

    '''The rtsp url of your encoder with your connected hdmi device'''
    capabilities.add_capability("EncoderUrl", "rtsp://192.168.1.15/0")

    '''The name of your device as saved in your harmony hub'''
    capabilities.add_capability("DeviceName", "device name in harmony")

    '''the ip address of the machine running the rokuality server'''
    capabilities.add_capability("ServerIPAddress", "your host machine ip address")
    
    '''pass the capabilities and start your driver'''
    driver = HDMIDriver("http://yourserverurl:yourrunningserverport", capabilities)
```

#### All Device Capabilities

| Capability  | Description | Required Or Optional | Notes |
| ------------- | ------------- | ------------- | ------------- |
| Platform | Indicates the target platform for the tests.  | Required | String - Options are 'Roku, 'XBox', 'Tizen', 'LGwebOS', and 'HDMI' |
| AppPackage | The sideloadable zip to be installed (Roku), or the .appxbundle (XBox), or the .wgt (Tizen TV), or the zipped up webOS project directory for LG webOS. Must be a valid file path OR a valid url.  | Required for Roku and XBox, Tizen, and LGwebOS - IF the 'App' capability is not provided. Note that for LGwebOS - simply zip up your project directory and the rokuality app will take care of generating and installing a LGwebOS IPK file during the installation process. Ignored for the HDMI driver | String |
| App | The friendly id of your app for Roku and XBox. For Roku this cap is optional. If you provide this cap and ommit the 'AppPackage' cap then the device will attempt to launch an already installed channel - Note that this can be an installed production channel id which you can retrieve from your device via `curl http://yourdeviceip:8060/query/apps`. For XBox this cap is always required and MUST be the app id of your installed .appxbundle - if you ommit the 'AppPackage' cap then the device will attempt to launch an already installed appxbundle matching this id. |Roku = Optional. XBox = Required. Tizen = Ignored. LGwebOS = Ignored. HDMI = Ignored. | String |
| DeviceIPAddress | The ip address of your Roku, XBox, Tizen TV, or LG webOS TV.  | Required for Roku or XBox or Tizen or LG webOS. Ignored for HDMI | String - Your device MUST be reachable from the machine running the Rokuality server. |
| DeviceUsername | Roku Only - The dev console username created when you enabled developer mode on your device.  | Required for Roku | String |
| DevicePassword | Roku Only - The dev console password created when you enabled developer mode on your device.   | Required for Roku | String |
| ImageMatchSimilarity | An optional image match similarity default used during Image locator evaluations. A lower value will allow for greater tolerance of image disimilarities between the image locator and the screen, BUT will also increase the possibility of a false positive.  | Optional | Double. Defaults to .90 |
| ScreenSizeOverride | An optional 'WIDTHxHEIGHT' cap that all screen image captures will be resized to prior to match evaluation. Useful if you want to enforce test consistence across multiple device types and multiple developer machines or ci environments.  | Optional | String - I.e. a value of '1800x1200' will ensure that all image captures are resized to those specs before the locator evaluation happens no matter what the actual device screen size is.  |
| OCRType | The OCR type - Currently supported options are 'GoogleVision', 'AmazonRekognition', or 'AmazonTextract'. If the capability is set to 'GoogleVision' you MUST have a valid Google Vision account setup and provide the 'GoogleCredentials' capability with a valid file path to the oath2 .json file with valid credentials for the Google Vision service. If the capability is set to 'AmazonRekognition' or 'AmazonTextract' then you MUST have a valid AWS account with an IAM role set with Rekognition or Textract priveleges and an AWS api access key id and secret key in file format you can provide, and you MUST provide the 'AWSCredentials' capability with a valid file path to this credentials file.  | Optional | String 
| GoogleCredentials | The path to a valid .json Google Auth key service file. | Optional but Required if the 'OCRType' capability is set to 'GoogleVision' | The .json service key must exist on the machine triggering the tests. See [Using Google Vision](#using-google-vision-ocr) for additional details.  |
| AWSCredentials | The path to a valid AWS credential file with an api key id and secret key. | Optional but Required if the 'OCRType' capability is set to 'AmazonRekognition' or 'AmazonTextract' | The credential file must exist on the machine triggering the tests. See [Using Amazon Rekognition](#using-amazon-rekognition-ocr) or [Using Amazon Textract](#using-amazon-textract-ocr) for additional details.  |
| MirrorScreen | If provided with a widthxheight value, then a window will be launched on the user's desktop showing the test activity in real time for the duration of the test session. Useful for debugging tests on remote devices.  | Optional | String - 'widthxheight' format. i.e. '1200x800' will launch a screen mirror with width 1200, and height 800. |
| EnablePerformanceProfiling | Roku only. If provided your sideloadable .zip package will be updated for performance profiling. Then during the course of the execution you can retrieve the .bsprof file with CPU and memory utilization data from your channel.  | Optional | Boolean - true to allow for performance capturing. Defaults to false. |
| ContentID | Roku only. A content id of a Roku deep link to load on session start.  | Optional - If provided you must also provide the 'MediaType' capability. | String |
| MediaType | Roku only. The media type of a Roku deep link to load on session start.  | Optional - If provided you must also provide the 'ContentID' capability. | String |
| AppPackageType | XBox only. Used if AppPackage is provided and indicates if the package is a 'appx' or 'appxbundle'.  | Optional - Valid values are 'appx' or 'appxbundle'. If this cap is not provided we assume the provided package is an 'appxbundle'. | String |
| ImageCollectorInterval | A value in milliseconds that acts as a delay between image collection during a test session. If you experience 400 http errors during image collection, a small pause here can help alleviate this.  | Optional - A delay in milliseconds i.e. 250. Defaults to 0 | Integer |
| DeviceID | Tizen and LGwebOS Only - The device id of your Tizen TV or LG webOS TV. For Tizen you can discover via 'sdb devices' when your TV is connected. For LGwebOS you can discover via 'ares-setup-device -list'  | Required for Tizen TV and LGwebOS - ignored otherwise | String |
| DeviceAPIToken | Tizen Only - The api token of your authorized Tizen TV remote.  | Required for Tizen TV - ignored otherwise | String |
| ServerIPAddress | Tizen and LG webOS Only - The local ip address of your machine running the Rokuality app. Necessary as this allows us to update your application wgt package (Tizen) or your zipped web package (LG webOS) so that it can communicate with your running Rokuality app and in turn query your app's html5 canvas for elements.  | Required for Tizen TV and LG webOS - ignored otherwise | String |
| TizenStudioHome | Tizen Only - The absolute path to your 'tizen-studio' home directory. Note that if you installed in the default directories you can ignore this capability and we will attempt to find the relevant tools in those locations. But if you changed the installation directories while installing, you can provide this capability pointing to the alternate location  | Optional for Tizen TV - ignored otherwise | String |
| LGWebOSSDKHome | LG webOS Only - The absolute path to your 'web os sdk' home directory as installed during your LG webOS setup. Note that if you installed in the default directories you can ignore this capability and we will attempt to find the relevant tools in those locations. But if you changed the installation directories while installing, you can provide this capability pointing to the alternate location  | Optional for LG webOS - ignored otherwise | String |
| EncoderUrl | HDMI driver Only - The rtsp url of the hdmi encoder your device under test is connected to.  | Required for HDMI - ignored otherwise. See the [why encoder?](#whyencoder) section for details | String |
| DeviceName | HDMI driver Only - The name of your hdmi device as saved in your harmony hub.  | Required for HDMI - ignored otherwise. See the [why harmony?](#whyharmony) section for details | String |
| ProxyHost | Roku Only - The IP address of the machine running the Rokuality server. If this capability is passed in combination with the `ProxyPort` capability, then a Proxy will be started and the underlying Roku application traffic will route through it - allowing your to monitor and modify your Roku http(s) traffic during test execution. See the [proxy section](#Roku-Proxy-with-ssl-support) for details.  | Optional for Roku - ignored otherwise. | String |
| ProxyPort | Roku Only - The port number you wish to start a proxy on. Must be an open port for every proxy instance you wish to start. If this capability is passed in combination with the `ProxyHost` capability, then a Proxy will be started and the underlying Roku application traffic will route through it - allowing your to monitor and modify your Roku http(s) traffic during test execution. See the [proxy section](#Roku-Proxy-with-ssl-support) for details.  | Optional for Roku - ignored otherwise. | Integer |
| ProxyType | Roku Only - The type of Proxy you wish to use. We currently support [Charles Proxy - Windows and Mac](https://www.charlesproxy.com/), and [Fiddler Classic - Windows](https://www.telerik.com/fiddler/fiddler-classic). See the [proxy section](#Roku-Proxy-with-ssl-support) for details.  | Optional for Roku - ignored otherwise. Valid values are `Charles` or `Fiddler`. If this capability is ommitted but the user provides the `ProxyPort` and `ProxyHost` capabilities then we will attempt to determine which proxy is installed and use the appropriate proxy. If you have both Fiddler and Charles installed on your machine you must provide this capability so Rokuality knows which proxy to use. | String |
| ProxyBinary | Roku Only - The absolute path to your Charles or Fiddler binary. See the [proxy section](#Roku-Proxy-with-ssl-support) for details.  | Optional for Roku - ignored otherwise. If this capability is ommitted but the user provides the `ProxyPort` and `ProxyHost` capabilities then we will attempt to find the Charles or Fiddler binary executable in the default installation locations. | String |
| HeadlessProxy | Roku Only - If set to false, then the proxy gui will be visible to the user. See the [proxy section](#Roku-Proxy-with-ssl-support) for details.  | Optional for Roku - ignored otherwise. Defaults to false - i.e. the proxy gui is not visible during execution and runs in the background. | Boolean |

#### Element Timeouts and Polling:
There are two main options when it comes to element timeouts and polling

Timeouts - By default the element timeout is set to 0 milliseconds, meaning if the driver fails to find an element immediately, it will throw a NoSuchElement exception. But a better practice is to set a implicit wait timeout so the driver will poll for a duration, trying to find the element before it fails and throws the NoSuchElementException:

```python
    '''will fail immediately'''
    driver.finder().find_element(By().text("no such text"))
```
vs
```python
    '''will fail after 5 seconds'''
    driver.options().set_element_timeout(5000)
    driver.finder().find_element(By().text("no such text"))
```
It is generally recommended to set respective timeouts to reduce test flake, but setting the values too high can increase test duration.

Additionally you can set the interval of how often the element search polling will happen. In this example, the same timeout is applied but the element polling will happen every second. If the polling interval is ommited the default is 250 milliseconds.
```python
    '''will fail after 5 seconds polling every second'''
    driver.options().set_element_timeout(5000)
    driver.options().set_element_poll_interval(1000)
    driver.finder().find_element(By().text("no such text"))
```

#### Using Google Vision OCR:
You can use Google Vision as your OCR engine during test provided you have a valid [Google Vision](https://cloud.google.com/vision/docs/before-you-begin) account setup. You must also set the path to your .json service file containing your service key in your DeviceCapabilities prior to driver start.

```python
    capabilities = DeviceCapabilities()
    capabilities.add_capability("OCRType", "GoogleVision")
    capabilities.add_capability("GoogleCredentials", "/path/to/your/vision/authkey.json")
```

#### Using Amazon Rekognition OCR:
You can use Amazon Rekognition as your OCR engine during test provided you have a valid [AWS Account](https://aws.amazon.com/rekognition/?blog-cards.sort-by=item.additionalFields.createdDate&blog-cards.sort-order=desc) account setup with an api key with an IAM role set to allow Rekognition use. You must then create the standard [aws credential file](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html) with your api key id and secret key.

```python
    capabilities = DeviceCapabilities()
    capabilities.add_capability("OCRType", "AmazonRekognition")
    capabilities.add_capability("AWSCredentials", "/path/to/your/aws/credential/file")
```

#### Using Amazon Textract OCR:
You can use Amazon Textract as your OCR engine during test provided you have a valid [AWS Account](https://aws.amazon.com/rekognition/?blog-cards.sort-by=item.additionalFields.createdDate&blog-cards.sort-order=desc) account setup with an api key with an IAM role set to allow Textact use. You must then create the standard [aws credential file](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html) with your api key id and secret key.

```python
    capabilities = DeviceCapabilities()
    capabilities.add_capability("OCRType", "AmazonTextract")
    capabilities.add_capability("AWSCredentials", "/path/to/your/aws/credential/file")
```

#### Failing to find elements? :
Image Based Locators `By().image("pathorurltoyoourimagesnippet.png")`
1. Make sure your locator image snippet is in a valid image format. Most tests use .png format so for best results please use locators of this type.
2. Make sure that your image snippets are in good quality and you are doing an apples to apples comparison of the image snippet you wish to find within the screen image. Some image snipping tools are better than others, so if capturing static image snippets for later locator use be wary of the tools you're using. Alternatively, you can get a subscreen section from the device during test and save it as a static locator for later use.
`locator_to_use_later = driver.screen().get_image_sub_screen(40, 80, 160, 220)`
3. You can optionally set the "ImageMatchSimilarity" DeviceCapability at driver startup which will set a tolerance for image comparisons. Lower values will mean a greater likelihood of getting a match, but too low of a value will introduce a false positive.
`capabilities.add_capability("ImageMatchSimilarity", .85)`

Text Based Locators `By().text("text to search for")`
1. Check that your string isn't too complicated, i.e. a locator of `By().text("hello world")` is much more likely to be found than a locator of `By().text("he!!O W@rLd!#!")`. Also, single world locators are better than multiple world locators but we continue to work on the server back end to improve the reliability.
2. You can access the entire decoded device screen text by `driver.screen().get_text_as_string()`. If your locator is present in the string but not found during test, please log a bug on the [issues](https://github.com/rokuality/rokuality-java/issues) page and we'll investigate.
3. By default the OCR evaluations happen against the entire device screen but sometimes it's better to narrow the scope of the find to a smaller region of the screen to get better results. This can be done with `driver.finder().find_element_sub_screen(by, 100, 500, 300, 200)` which will limit the scope of the find to that subset of the screen and likely return better results.

#### Server timeouts and orphaned sessions:
At the end of every driver session, you should close the driver and cleanup all session data by calling the stop method:
```python
    '''stop the driver and clean up all resources'''
    driver.stop()
```
But if you don't a safety exists to eventually clean up those assets. The server session will listen for new commands and will timeout if no commands for the session have been received for a specified duration. The default command timeout is set to 60 seconds - meaning if a session is started and no commands are sent to it for 60 seconds, then the session will automatically be terminated and released. You can increase/decrease this time by setting the 'commandtimeout' option when you launch the server.

<a name="whyencoder"></a>
### Why an Encoder
HDMI device automation requires you to setup an HDMI encoder on your network and connect your HDMI device to it which allows the Rokuality app to query your device's UI during test and perform OCR and image based analysis. Many encoders such as the recommended [J-Tech H.264 Encoder](https://jtechdigital.com/product/jtech-ench4-0220/) are low cost, efficient, and allow you to connect to your devices from anywhere on your network. Other similar solutions on the market ship you a "magic box" device that is proprietary and limits the ability to scale with more devices and across multiple developers/resources. By allowing you to purchase and supply your own encoder, it limits cost and increases your ability to scale and control your own hardware, and not worry about it being provided by only one automation provider.

<a name="whyharmony"></a>
### Why Harmony
HDMI device automation requires a [logitech harmony hub](https://www.logitech.com/en-us/product/harmony-hub?crid=60) to drive the user input. The hub is a low cost (60$) device that provides both IR and Bluetooth capability in an easily available, wireless solution. Since you don't need to use an IR blaster or a cabled base solution you can scale across additional devices easily, and the Rokuality app can drive the harmony and control your devices under test. Other similar solutions on the market ship you a "magic box" device that requires you to plug in your device under test - which is proprietary and limits the ability to scale with more devices and across multiple developers. Using the harmony approach is cheap, effective, and scalable.

<a name="configuringyourharmony"></a>
### Configuring Your Harmony
To setup your Harmony hub and prepare it for automating your devices under test:
1. Download the Harmony mobile app for iOS or Android.
2. During setup it will walk you through adding your device under test. Be sure to keep track of what you name your device when you pair it with your Harmony as that will be used later during your tests as your "DeviceName" capability. This will allow the server to communicate with your device from your test code and drive it like a real user.
3. Enable XMPP on the hub. In the harmony app go to Settings>>Harmony Setup>>Add/Edit Devices & Activities>>Hub>>Enable XMPP

### Roku Proxy with SSL Support
Rokuality is the first platform to provide [proxy support](https://www.rokuality.com/roku-proxy) with ssl decryption for Roku devices! No need to tether your Roku to your  machine via wifi sharing and no need to perform complicated router based modifications!

#### Roku Proxy: Getting Started
To get started monitoring/modifying your Roku http(s) traffic during test, you must install one of our 2 supported proxies. Rokuality current supports [Charles Proxy - Windows and Mac](https://www.charlesproxy.com/) and [Fiddler Classic](https://www.telerik.com/download/fiddler). Both require some simple 1 time setup after you have installed the proxy of your choice.

**Charles Proxy First Time Setup**
1. Install Charles Proxy version 4.5.6 or newer.
2. Launch Charles Proxy for the first time.
3. Optional - If you wish to run multiple instances of Charles Proxy while testing, i.e. test concurrency with each test having their own Charles Proxy instance, please see [these instructions](https://www.charlesproxy.com/documentation/faqs/running-multiple-instances-of-charles/) 

This should be all that is required for Rokuality to be able to create Charles Proxy configurations and launch/stop/query the proxy as needed during automation.

**Fiddler Classic First Time Setup**
1. Install the latest version of Fiddler Classic.
2. Launch Fiddler Classic for the first time.
3. Create a CustomRules.js file for the first time use by choosing the toolbar menu `Rules>>Customize Rules...`. This will create the backend CustomRules.js file that Rokuality needs in order to launch/stop/query the proxy during automation.
4. Allow remote connections from your device to the proxy by choosing the toolbar menu `Tools>>Options>>Connections` and check the `Allow remote computers to connect` checkbox.
5. Disable the system proxy on startup by choosing the toolbar menu `Tools>>Options>>Connections` and un-check the `Act as a system proxy on startup` checkbox.
6. Optional - if you wish to decrypt ssl traffic during test - Enable https connections by choosing the toolbar menu `Tools>>Options>>HTTPS` and check both the `Capture HTTPS CONNECTs` checkbox and the `Decrypt HTTPS traffic from all processes` checkbox. You may also wish to ensure that all protocols are entered for capture including `<client>;ssl2;ssl3;tls1.0;tls1.1;tls1.2`

Note that when using Fiddler - you may only have 1 instance of Fiddler running at one time, i.e. you may only run 1 test per machine at any one time. You can scale this by distributing your tests to multiple Rokuality servers but if you need concurrency, Charles Proxy might be a better solution for you.

#### Roku Proxy: Starting a Proxy

To start a proxy during test execution, you must provide the minimum required capabilities which include the `ProxyHost` and `ProxyPort` capabilities. See the [capabilities section](#all-device-capabilities) for additional capabilities. When the minimum caps for a Proxy connection are provided, a Charles or Fiddler proxy will be started on the backend and all traffic from your Roku device will then route through the proxy. 

```python
    capabilities = DeviceCapabilities()

    '''The ip address of your machine running Rokuality which allows your Roku to communicate with your Rokuality server and proxy server, i.e. 192.168.1.47'''
    capabilities.add_capability('ProxyHost', 'your server ip address')

    '''Any open port on your machine you wish the proxy to run on. Each test session must have a unique port'''
    capabilities.add_capability('ProxyPort', 8876)
```

#### Roku Proxy: Monitoring http and https Calls During a Test

During the course of a test, the proxy api will allow you to retrieve your request/response traffic in standard [har format](https://en.wikipedia.org/wiki/HAR_(file_format)). Several libraries exist that will allow you to parse your har content into objects during test, but at the core a har file is a json file that can be cast/queried as any JSONObject.

```python
    '''gets the har file of every request in the proxy from test start to now'''
    har_log = roku_driver.proxy().get_har_log()
    print("Har file saved to: " + har_log)

    '''clear the har log'''
    roku_driver.proxy().clear_har_log()
```

#### Roku Proxy: Applying Rewrites

Rokuality will use any Charles proxy rewrite configurations you have saved, or any Fiddler Classic CustomRules.js you have saved prior to the start of a test. Rokuality simply reads your existing proxy configurations and then applies the necessary configurations to Charles or Fiddler in order for Roku proxying to work at the test runtime. So if you desire any rewrites to your data during the test execution, simply open up Charles or Fiddler prior to your test suite execution and add any desired rewrite logic prior to test.