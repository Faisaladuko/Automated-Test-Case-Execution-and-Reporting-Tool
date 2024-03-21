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
            f"--cov={project_root}",  #Test Code Coverage,
            "--junitxml=xmlReport.xml"
            #"--html=report.html",
            #'--log-file=command_line_output.log'

        ]
        #Extend pytest arguments with test case file exluding directory and __init__ files
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
            #print(captured_report)


            #Write stdout into a text file: fileout.txt
            # with open('fileout.txt', 'w') as file:
            #     file.write(captured_report)
            mylog.info("Pytest executed successfully")
            return True

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
    # with open('ReportOut.html', 'r', encoding="utf-8") as file:
    #     html_ = file.read()
    # print(html_)

    import xml.etree.ElementTree as et
    from jinja2 import Template
    tree = et.parse('xmlReport.xml')
    root = tree.getroot()

    first_summary = root[0].attrib
    Num_error = first_summary['errors']
    Num_failures = first_summary['failures']
    Num_skipped = first_summary['skipped']
    Num_tests = first_summary['tests']


    failed_modules = {}
    past_modules = []

    testcases = root[0]
    #print(testcases[0][0].text)
    for i in range(len(testcases)):

        if len(testcases[i])>0:
            # failed_modules[testcases[i].attrib['name']] = {'test_file_loc':testcases[i].attrib['classname'], 'func_error':testcases[i][0].attrib['message']}
            if testcases[i].attrib['classname'] in failed_modules:
                failed_modules[testcases[i].attrib['classname']].update({testcases[i].attrib['name']:testcases[i][0].text})
            else:
                failed_modules[testcases[i].attrib['classname']] = {testcases[i].attrib['name']:testcases[i][0].text}
                #print(failed_modules[testcases[i].attrib['classname']])

        else:
            past_modules.append([testcases[i].attrib['name'],testcases[i].attrib['classname']])
    len_past_modules = len(past_modules)
    #print(failed_modules)
    print(past_modules)
    # for k, v in failed_modules.items():
    #     print(k)
    #     for k1, v1 in v.items():
    #         print(v1.strip())

    # Create HTML template from stdout output
    html_file= '''
   <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>QA Report</title>
    <style>
        html, body {
            height:100%;
            width:100%;
            margin:0;
            padding:0;
        }
        pre {
           margin: 0;
           padding: 0;
           box-sizing: content-box;
           white-space: pre-wrap;
        }
    
        h1 {
            background-color: blue;
            color: white;
            padding: 10px;
            text-align: center;
            margin:0;
         
        }

       
        ul {
            list-style-type: none;
            padding: 0;
        }

        li {
            text-align: left;
        }

        hr {
            border: 1px solid lightblue;
        }
        .collapsible:hover {
              background-color: #555;
        }
        .collapsible:after {
              content: '\+';
              color: white;
              font-weight: bold;
              float: right;
              margin-left: auto;
              
        }
      
        .collapsible {
              background-color: #7f8585;
              color: white;
              cursor: pointer;
              padding: 18px;
              width: 90%;
              border: none;
              text-align: left;
              outline: none;
              font-size: 1.5vw;
              margin-left: 10px;
              box-sizing: border-box;
              
              
             
       }

        .collapsible-content {
              padding-top: 0 18px;
              max-height: 0;
              overflow: hidden;
              transition: max-height 0.2s ease-out;
              background-color: #f1f1f1;
              width: 85%;
              margin-left: 5%;
              overflow-y: scroll
              
        }
        
        
        .active + .collapsible2:hover {
              background-color: #565;
        }
        .collapsible2:after {
              content: '\+';
              color: white;
              font-weight: bold;
              float: right;
              margin-left: auto;
              
        }
        
        
        .active:after {
              content: "\-";
              
        }
        .collapsible2 {
              background-color: red;
              color: white;
              cursor: pointer;
              padding: 18px;
              width: 85%;
              border: none;
              text-align: left;
              outline: none;
              font-size: 1.4vw;
              margin-left: 10%;
              box-sizing: border-box;     
             
       }
        .collapsible-content2 {
              padding: 0 18px;
              max-height: 0;
              overflow: hidden;
              transition: max-height 0.2s ease-out;
              background-color: #c9c5c5;
              width: 75%;
              margin-left: 10%;        
              
        }
        
           .passList{
              background-color: green;
              color: white;
              cursor: pointer;
              padding: 18px;
              width: 85%;
              border: none;
              text-align: left;
              outline: none;
              font-size: 1.4vw;
              margin-left: 10%;
              box-sizing: border-box;     
       }
       .funcsnames{
       background-color: #9e9b9b;
       text-align: left;
       font-size: 1vw;
       color: white;
       font-weight: bold;
      
       
       }
       .funcsmessage{
       text-align: left;
       font-size: 1vw;
       }
      .sum{
        list-style: none;
        display: flex;
        justify-content: space-between; 
       
      }
      .sum li{
       text-align: center;
      }
      
    .sum .item {
            text-align: center;
            background-color: #e0e0e0; 
            border-radius: 10px; 
            padding: 10px; 
            margin: 5px; 
    }
      .value {
            font-weight: bold;
            font-size: 2vw; 
        }
        
      .label {
            margin-top: 5px; 
        }
      
       
    </style>
</head>
<body>
    <header>
        <h1>QA Report</h1>
    </header>
    <pre>
        <br>
        <button type ='button', class="collapsible">Test Summary</button>
        <div class="collapsible-content">
            <ul class=sum>
                <li class="item">
                    <div class="value"> {{ Num_tests }} </div>
                    <div class="label">Tested Functions</div>
                </li>
                <li class="item">
                    <div class="value"> {{ Num_error }} </div>
                    <div class="label">Syntax Errors</div>
                </li>
                <li class="item">
                    <div class="value"> {{ len_past_modules }} </div>
                    <div class="label">Passed Functions</div>
                </li>
                <li class="item">
                    <div class="value"> {{ Num_failures }} </div>
                    <div class="label">Failed Functions</div>
                </li>
                <li class="item">
                    <div class="value"> {{ Num_skipped }} </div>
                    <div class="label">Skipped Functions</div>
                </li>
            </ul>
        </div>
        <hr>
        <button type='button', class="collapsible", id='failed'>Failed Tests</button>
        <div class="collapsible-content">
            {% for k, v in failed_modules.items() %}
                <button type='button', class="collapsible2">
                module:  ./{{ k }}.py
                 </button>
                <div class="collapsible-content2">
                    <ul>
                        {% for k1, v1 in v.items() %}
                            <li class='funcsnames'>
                            _ _ _ _ _ _ _ _ _ _{{ k1 }}()_ _ _ _ _ _ _ _ _ _ 
                            </li> 
                            <code class=funcsmessage>
                            {{ v1.strip()|e }}
                            </code>
                        {% endfor %}
                    </ul>
                </div>
            {% endfor %}
        </div>
        <hr>
        <button type='button', class="collapsible", id='passed'>Passed Tests</button>
        <div class="collapsible-content">
            <ul>
                {% for p in past_modules %}
                <div class ='passList'>
                    <li>module: ./{{p[1]}}.py ----------->> func: def {{ p[0] }}()</li>
                </div>
                {% endfor %}
            </ul>
        </div>
    </pre>

    <script>
        var coll = document.getElementsByClassName("collapsible");
        var coll2 = document.getElementsByClassName("collapsible2");
        var i;
        
        for (i = 0; i < coll.length; i++) {
          coll[i].addEventListener("click", function() {
            this.classList.toggle("active");
            var content = this.nextElementSibling;
            console.log(content)
            if (content.style.maxHeight){
              content.style.maxHeight = null;
            } else {
              content.style.maxHeight = content.scrollHeight + "px";
            } 
          });
        }
        
        
        
        for (i = 0; i < coll2.length; i++) {
          coll2[i].addEventListener("click", function() {
            this.classList.toggle("active");
            var content = this.nextElementSibling;
            
            if (content.style.maxHeight){
              content.style.maxHeight = null;
            } else {
              content.style.maxHeight = content.scrollHeight + "px";
            } 
          });
        }
    </script>
</body>
</html>
'''

    temp = Template(html_file)
    rend = temp.render(
        Num_tests=Num_tests,
        Num_error=Num_error,
        past_modules=past_modules,
        Num_failures=Num_failures,
        Num_skipped=Num_skipped,
        failed_modules=failed_modules,
        len_past_modules=len_past_modules
    )

    #Save HTML template into a fileout.html file
    with open(HTML_Report, 'w', encoding="utf-8") as f:
        f.write(rend)

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





