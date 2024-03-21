# Automated Test Case Execution and Reporting Tool

***By Faisal Aduko Wahabu {faisaladuko@gmail.com}***

## About Script
A Python script that automates the execution of test cases and generates a comprehensive report for software quality validation. 
> The script provides the following functionalities:

+ Read test cases from a specified location or file.
+ Execute the test cases against the target software or application. (ping an IP address 127.0.0.1)
+ Capture test results and generate a detailed report highlighting each test case's pass/fail status.

## Output
https://share.zight.com/X6uXXG09
![image](https://github.com/Faisaladuko/Automated-Test-Case-Execution-and-Reporting-Tool/assets/39354209/37d62734-dfb6-46bf-89d2-204a74b8783f)
![image](https://github.com/Faisaladuko/Automated-Test-Case-Execution-and-Reporting-Tool/assets/39354209/a5b60256-8b0b-4783-bfcd-7a2ec00583b1)
![image](https://github.com/Faisaladuko/Automated-Test-Case-Execution-and-Reporting-Tool/assets/39354209/f0f32d39-eb02-4f82-92c2-a55c36250366)
![image](https://github.com/Faisaladuko/Automated-Test-Case-Execution-and-Reporting-Tool/assets/39354209/a9b76f5d-34ab-4d01-9281-f6847576b6c6)
![image](https://github.com/Faisaladuko/Automated-Test-Case-Execution-and-Reporting-Tool/assets/39354209/6b68e869-3dea-4262-a5bc-45e6be00de18)









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
