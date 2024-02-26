"""
By Faisal Aduko Wahabu {faisaladuko@gmail.com}

    Automated Test Case Execution and Reporting Tool
A Python script that automates the execution of test cases and generates a
comprehensive report for software quality validation. The script provide the following
functionalities:

● Read test cases from a specified location or file.
● Execute the test cases against the target software or application. (ping a IP address 127.0.0.1)
● Capture test results and generate a detailed report highlighting the pass/fail status of each test case.

Include Test_Execution_Script.py into you project root directory and provide the following parameters at the functions call below;
● test_location = 'test_cases'  #Indicate testcases directory here
● host = '127.0.0.1'           #Indicate host IP/Domain to ping here
● HTML_Report = 'ReportOut.html'  #Indicate HTML report file name for your perusal here

"""
import pytest
import pathlib
import sys
import subprocess
import webbrowser
import http.server
import socketserver
import platform
import os
import logging


logging.basicConfig(level=logging.DEBUG)
mylog = logging.getLogger()


#Ping IP address
def ping_ip(host):
    try:
        system = platform.system().lower()   #Get the current operating system
        if system == 'windows':
            sub =subprocess.run(['ping', '-n', '4', host], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        else:
            sub =subprocess.run(['ping', '-c', '4', host], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

        if sub.returncode ==0:   #Check if ping was successfull
            print("Ping was successful...")
            mylog.info(sub.stdout.decode('utf-8'))
            return True
        else:
            mylog.error(f'{host} cannot be reached')
            return False

    except subprocess.CalledProcessError as e:
        mylog.exception(f"Cannot reach {host}")
        return False


#Read test case file(s)
def read_test_case_file(test_location):
    #Get the file(s) that contains the test cases
    test_case_scripts = pathlib.Path(__file__, '..', test_location).resolve().glob('*.py')
    return test_case_scripts  # Return is a generator

#Executing test cases
def executing(host, test_location):

    flg = ping_ip(host)  #Test ping

    #Get the root directory of the project
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, '..'))


    #Execute pytest command only if pinging the host was successful
    if flg:
        scripts = read_test_case_file(test_location) #retrieve testcase files
        #Set command line arguments as a list for pytest execution
        sys.argv = [
            "pytest",
            "-rA", #outputs text out for both pass and fail tests
            "--capture=tee-sys",  #Allow output capture
            "--showlocals",      # show local variables in tracebacks
            f"--cov={project_root}"  #Test Code Coverage
            #"--html=report.html",
            #'--log-file=command_line_output.log'
            #"-junitxml = report.xml"
        ]
        #Extend pytest arguments with test case file exluding directory and __inti__ files
        sys.argv.extend([str(script) for script in scripts if not os.path.isdir(str(script)) and not str(script).endswith("__init__.py")])

        try:
            # Run pytest command
            pytest_command = subprocess.run(
                sys.argv,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,

            )
            # Capture stdout
            captured_report= pytest_command.stdout
            #stderr = pytest_command.stderr

            #Write stdout into a text file: fileout.txt
            with open('fileout.txt', 'w') as file:
                file.write(captured_report)
            mylog.info("Pytest executed successfully")
            return  True

        #catch errors
        except subprocess.CalledProcessError as e:
            mylog.exception(f"Pytest Execution Error: {e}")
            return False
    else:
        mylog.warning("Cannot execute pytest. Ensure your host is correct")
        return False


#Reporting pytest output in an HTML file
def Reportage(HTML_Report):
    mylog.info("Reporting test status...")
    #Read text from the fileout.txt file
    with open('fileout.txt', 'r') as file:
        text_content = file.read()

   #Create HTML template from stdout output
    html_file = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>File Content</title>
        <style>
            body {{
                text-align: center;
            }}
            pre {{
                display: inline-block;
                text-align: left;
            }}
            h1 {{
               background-color: blue;
            }}
        </style>
    </head>
    <body>
        <header>
            <h1>QA Report</h1>
        </header>
        <pre>
            {text_content}
        </pre>
    </body>
    </html>
    """
    #Save HTML template into a fileout.html file
    with open(HTML_Report, 'w') as f:
        f.write(html_file)

#Making pytest report available in the brower
def Serve_Report(HTML_Report):
    # Serve the HTML report on 127.0.0.1 and open in browser
    with socketserver.TCPServer((host, 0), http.server.SimpleHTTPRequestHandler) as httpd:
        port = httpd.server_address[1]
        mylog.info(f"Serving HTML report at http://{host}:{port}/{HTML_Report}")
        webbrowser.open(f"http://{host}:{port}/{HTML_Report}")
        mylog.debug("Communicating Requests....")
        httpd.serve_forever()

#Running necessary functions
if __name__ == '__main__':
    test_location = 'test_cases'  #Indicate testcases directory here
    host = '127.0.0.1'           #Indicate host IP/Domain here
    HTML_Report = 'ReportOut.html'  #Indicate HTML report file name here

    if executing(host, test_location):   #Executing Pytest
        Reportage(HTML_Report)           #Executing the report out
        Serve_Report(HTML_Report)        #Serving the application in the browser





