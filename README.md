# README #


## Installation ##

1. Install Python on your machine, add scripts fonder into "path" environmental variable
2. In the project command line run: > pip install -r requirements.txt


## How to write tests ##

For the simple tests with one test data and one verification you can create a simple test function.
So you have to: 
    1.1 Under the 'tests/{feature_name}' folder create a new file
    1.2 create a method starts with the name 'test_...'
    1.3 pass the fixture name 'browser_driver' as a function parameter to get web driver instance and write your test there. 
    WebDriver instance is available calling ``` browser_driver ``` object in the test.
    1.4 You can use pytest assert there.

Example ([test_login_with_gmail.py](tests%2Flogin%2Ftest_login_with_gmail.py)):
``` 
    def test_login_with_gmail(browser_driver):
    login_page = LoginPage(browser_driver)
    login_page.open()
    ...
    assert ... #put any condition here
    
``` 
### DDT approach ###

If you want to use ddt approach with several testdata for your test, it's important to create a test class, inherited from unittest.TestCase,
for such test because it's a requirements of ddt library.

As an example see **test_login_page_fields.py**

1.1 You have to annotate your class with '@ddt' annotation
1.2 You have to annotate your class with '@pytest.mark.usefixtures("browser_driver")' annotation to be able to use WedDriver instance through ```  self.browser ``` call
1.3 Use '@file_data("../../testdata/...")' annotation under your test method to set the name of the file. You have to write the path from the current test folder, so that why you see "../.." there.
1.4 Test method name should start with the name 'test_...'

Check the different ways to set test data on official ddt library page: https://ddt.readthedocs.io/en/latest/example.html

### Soft asserts ###
If you need to use soft asserts (verifications, that don't fail the test as soon as the first one fails, 
but continue to perform the other verifications) you still have to create a test class, but inherited from softtest.TestCase.

Example - **test_login_page_fields.py**
To make a soft assert you can write 

``` 
    self.soft_assert(self.assertEqual, {expected value}, {actual value})
    self.soft_assert(self.assertTrue, {actual boolean value})
    soft.assert_all()
``` 

It is important to use 'soft.assert_all()' in the end to make the final check if test passed or failed


## Webdriver management ##

WebDriver instance is created in conftest.py using test fixtures, see
```  
  @pytest.fixture(scope='function', autouse=False)
  def browser_driver(request):
  ...
```

You don't need to create a driver instance in the test or destroy it in test post conditions. It all is already managed by test fixture.

## Page Objects ##

Use Page object approach here and describe page locators and all possible actions with elements inside page class.
Tests should only contain steps and assertions.

Page classes should be stored in "pages" folder and inherit BasePage

``` 
class LoginPage(BasePage):
    def __init__(self, browser):
        super().__init__(browser)
``` 
BasePage contains some basic methods to interact with elements

## Configuration and run against different browsers ##

File .test.env contains some configurable parameters, for example you can change parameter ``` browser_name=chrome ```  to run tests with another browser.

**Currently, tests can be run only from IDE,** I'm working to make it available from CI and command line.
You can type ``` pytest ``` in the ID terminal to run all the tests, or you can simply right click on test file or test folder to run something specific.
