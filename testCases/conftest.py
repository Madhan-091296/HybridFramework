# import os
# import pytest
# from pytest_metadata.plugin import metadata_key
# from selenium import webdriver
# from datetime import datetime
# @pytest.fixture()
# def setup(browser):
#    if browser == 'edge':
#       options = webdriver.EdgeOptions()
#       options.add_experimental_option("detach", True)
#       driver = webdriver.Edge(options=options)
#       print("Launching Edge browser.........")
#    elif browser == 'firefox':
#       options = webdriver.FirefoxOptions()
#       driver = webdriver.Firefox(options=options)
#       print("Launching firefox browser.........")
#    else:
#       options = webdriver.ChromeOptions()
#       options.add_experimental_option("detach", True)
#       driver = webdriver.Chrome(options=options)
#       print("Launching chrome browser.........")
#    yield driver
#    driver.quit()
#
# def pytest_addoption(parser):    # This will get the value from CLI /hooks
#    parser.addoption("--browser")
# @pytest.fixture()
# def browser(request):  # This will return the Browser value to setup method
#    return request.config.getoption("--browser")
#
# # It is hook for Adding Environment info to HTML Report
# def pytest_configure(config):
#    config.stash[metadata_key]['Project Name'] = 'Tutorial Ninja'
#    config.stash[metadata_key]['Module Name'] = 'CustRegistration'
#    config.stash[metadata_key]['Tester Name'] = 'KMR'
# # It is hook for delete/Modify Environment info to HTML Report
# @pytest.hookimpl(optionalhook=True)
# # @pytest.mark.optionalhook   # Deprecated
# def pytest_metadata(metadata):
#   metadata.pop("Python", None)
#   metadata.pop("Plugins", None)
# # Specifying report folder location and save report with timestamp
# @pytest.hookimpl(tryfirst=True)
# def pytest_configure(config):
#    config.option.htmlpath = (os.path.dirname(os.getcwd()) + "\\HybridFramework\\reports\\"+datetime.now().strftime("%d-%m-%Y %H-%M-%S")+".html")
import os
import pytest
from datetime import datetime
from pytest_metadata.plugin import metadata_key
from selenium import webdriver
from utilities.readProperties import ReadConfig


@pytest.fixture()
def setup(browser_platform):
   baseenv = ReadConfig.getEnvironment()
   browser,platform = browser_platform
   if baseenv == "remote":
       options = {
           "chrome": webdriver.ChromeOptions,
           "edge": webdriver.EdgeOptions,
           "firefox": webdriver.FirefoxOptions
       }
       if browser not in options:
           raise ValueError(f"Unsupported browser: {browser}")
       platform_mapping = {"windows": "WIN10", "mac": "MAC", "linux": "LINUX"}
       platform_name = platform_mapping.get(platform)
       if not platform_name:
           raise ValueError(f"Unsupported platform: {platform}")
       opt = options[browser]()
       opt.add_experimental_option("detach", True) if browser in ["chrome", "edge"] else None
       opt.platform_name = platform_name
       driver = webdriver.Remote(command_executor="http://localhost:4444/wd/hub", options=opt)
   elif baseenv == "local":
       if browser == 'edge':
           options = webdriver.EdgeOptions()
           options.add_experimental_option("detach", True)
           driver = webdriver.Edge(options=options)
           print("Launching Edge browser.........")
       elif browser == 'firefox':
           options = webdriver.FirefoxOptions()
           driver = webdriver.Firefox(options=options)
           print("Launching firefox browser.........")
       else:
           options = webdriver.ChromeOptions()
           options.add_experimental_option("detach", True)
           driver = webdriver.Chrome(options=options)
           print("Launching chrome browser.........")
   yield driver
   driver.quit()
# Hook to add command-line options for browser and OS
def pytest_addoption(parser):
   parser.addoption("--browser", default="chrome", choices=["chrome", "edge", "firefox"], help = "Browser to test")
   parser.addoption("--os", default="linux", choices=["windows", "mac", "linux"], help = "Operating system to test")
# Get value from command Line
@pytest.fixture()
def browser_platform(request):
   browser = request.config.getoption("--browser")
   platform = request.config.getoption("--os")
   return browser,platform

# It is hook for Adding Environment info to HTML Report
def pytest_configure(config):
   config.stash[metadata_key]['Project Name'] = 'Tutorial Ninja'
   config.stash[metadata_key]['Module Name'] = 'CustRegistration'
   config.stash[metadata_key]['Tester Name'] = 'KMR'
# It is hook for delete/Modify Environment info to HTML Report
@pytest.hookimpl(optionalhook=True)
# @pytest.mark.optionalhook   # Deprecated
def pytest_metadata(metadata):
  metadata.pop("Python", None)
  metadata.pop("Plugins", None)
# Specifying report folder location and save report with timestamp
@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
   config.option.htmlpath = (os.path.dirname(os.getcwd()) + "\\HybridFramework\\reports\\"+datetime.now().strftime("%d-%m-%Y %H-%M-%S")+".html")
