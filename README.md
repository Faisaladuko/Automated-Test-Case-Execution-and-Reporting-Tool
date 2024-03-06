# Automated Test Case Execution and Reporting Tool

***By Faisal Aduko Wahabu {faisaladuko@gmail.com}***

## About Script
A Python script that automates the execution of test cases and generates a comprehensive report for software quality validation. 
> The script provides the following functionalities:

+ Read test cases from a specified location or file.
+ Execute the test cases against the target software or application. (ping an IP address 127.0.0.1)
+ Capture test results and generate a detailed report highlighting each test case's pass/fail status.

## Output
![image](https://github.com/Faisaladuko/Automated-Test-Case-Execution-and-Reporting-Tool/assets/39354209/40cb9753-eaff-4289-9431-e4e4cdb55b1b)
![image](https://github.com/Faisaladuko/Automated-Test-Case-Execution-and-Reporting-Tool/assets/39354209/17001434-882b-4f32-9344-153da0a3faaf)
![image](https://github.com/Faisaladuko/Automated-Test-Case-Execution-and-Reporting-Tool/assets/39354209/f83b0841-dbbe-4f21-9a36-01cad6e41642)




## Run Script
> Include **Test_Execution_Script.py** into your project root directory and provide the following parameters at the functions call below;

- test_location = 'test_cases'  [Indicate test cases directory here]
- host = '127.0.0.1'           [Indicate host IP/Domain to ping here]
- HTML_Report = 'ReportOut.html'  [Indicate HTML report file name for your perusal here]
### Example:
```
if __name__ == '__main__':
    test_location = 'test_cases'  
    host = '127.0.0.1'           
    HTML_Report = 'ReportOut.html'  

    if executing(host, test_location):   #[Executing Pytes]
        Reportage(HTML_Report)           #[Executing the report out]
        Serve_Report(HTML_Report)        #[Serving the application in the browser]
```

## Requirement
> Install requirements
> >pip install -r requirements.txt
