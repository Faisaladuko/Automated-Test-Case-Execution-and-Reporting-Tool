By Faisal Aduko Wahabu {faisaladuko@gmail.com}
##Automated Test Case Execution and Reporting Tool

A Python script that automates the execution of test cases and generates a
comprehensive report for software quality validation. The script provide the following
functionalities:

● Read test cases from a specified location or file.
● Execute the test cases against the target software or application. (ping a IP address 127.0.0.1)
● Capture test results and generate a detailed report highlighting the pass/fail status of each test case.

##Run Script
Include Test_Execution_Script.py into your project root directory and provide the following parameters at the functions call below;

● test_location = 'test_cases'  #Indicate testcases directory here
● host = '127.0.0.1'           #Indicate host IP/Domain to ping here
● HTML_Report = 'ReportOut.html'  #Indicate HTML report file name for your perusal here
Example:
#Running necessary functions
if __name__ == '__main__':
    test_location = 'test_cases'  #Indicate testcases directory here
    host = '127.0.0.1'           #Indicate host IP/Domain here
    HTML_Report = 'ReportOut.html'  #Indicate HTML report file name here

    if executing(host, test_location):   #Executing Pytest
        Reportage(HTML_Report)           #Executing the report out
        Serve_Report(HTML_Report)        #Serving the application in the browser

## Requirement
Run  pip install -r requirements. txt   to install requirements
