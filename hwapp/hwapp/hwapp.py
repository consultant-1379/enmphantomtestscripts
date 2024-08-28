# import mysql.connector
import os,subprocess
from math import sqrt
# # Get the current directory
# current_dir = os.path.dirname(os.path.abspath(__file__))
#
# # Specify the path to the templates directory, relative to the current directory
# template_dir = os.path.join(current_dir, 'templates')
# import os.path
# __path__ = [os.path.join(os.path.dirname(__file__), subdir) for subdir in ['logger','data' ]]
from jinja2 import Environment, FileSystemLoader
import logger
import saninfo
from flask import Flask, render_template, Response, stream_with_context, stream_template
from pygments.formatters import HtmlFormatter
from pygments import highlight
from pygments.lexers import BashLexer

import logging
import time

hwapp = Flask(__name__)
# Starts logger for file
# log = Logger().get_logger(__name__)
# This sets the root logger level to be info.

# def activate_logging():
#     logname = "log_saninfo.log"
#     logging.basicConfig(filename=logname,
#                         filemode='a',
#                         format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
#                         datefmt='%H:%M:%S',
#                         level=logging.DEBUG)
#     logger = logging.getLogger("log_saninfo.log")
#     logging.debug("any info log?")
#     logger.debug("any debug logs?")
#     logger.debug(f"eris file : {get_eris_file()}")
#     return logger
#
#
# logger = activate_logging()
# logging.root.setLevel(logging.INFO)
# logname="log21.log" # PS C:\Users\EEIDLE\OneDrive - Ericsson\ENM Test\ENM20_projects\src> Get-Content .\log21.log -Wait -Tail 10
# logging.basicConfig(filename=logname,
#                     filemode='w',
#                     format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
#                     datefmt='%H:%M:%S',
#                     level=logging.DEBUG)


max_score = 100
test_name = "ENM Racks with NO FC Switches"
ENMS = [
    {"name": "51077", "score": 100},
    {"name": "51078", "score": 87},
    {"name": "51119", "score": 92},
    {"name": "51122", "score": 75},
    {"name": "-", "score": 40},
]

import inspect

logger = logger.activate_logging(logname="logging_saninfo.log")
def execute(command):
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, errors = p.communicate()
    return output, errors


@hwapp.route('/')
def home():
    return render_template("base.html", title="Hardware Management")


@hwapp.route("/results")
def results():
    context = {
        "title": "Results",
        "ENMS": ENMS,
        "test_name": test_name,
        "max_score": max_score,
    }
    return render_template("results.html", **context)


@hwapp.route('/unity')
def unity():
    hw_model = "EMC UNITY 450F"
    hwapp.logger.debug(f" in func {inspect.currentframe().f_code.co_name}({hw_model})")
    return Response(stream_with_context(
        stream_template('my_stream_template.html', rows=saninfo.getUnitylist(hw_model), title=hw_model)))

@hwapp.route('/VNX 5400')
def vnx():
    hw_model = "EMC VNX5400 DPE"
    hwapp.logger.debug(f" in func {inspect.currentframe().f_code.co_name}({hw_model})")
    return Response(stream_with_context(
        stream_template('my_stream_template.html', rows=saninfo.getVNXlist(hw_model), title=hw_model)))

    # output = SAN.main("-s", "EMC VNX5400 DPE")
    # context = {
    #     "title": "VNX 5400",
    #     "model": "testdec",
    #     "output": output,
    # }
    # return render_template("output.html", **context)

@hwapp.route('/stest')
def stest():
    command = ["python", "-u", "saninfo.py","-s","EMC UNITY 450F"]  # -u: don't buffer output
    output, errors = execute(command)
    return render_template('output.html', console_gave=[output, errors])
    # return Response(stream_with_context(stream_template('my_stream_template.html' ,rows=generate(),title='content')))


@hwapp.route('/content')
def content():
    def generate():
        for i in range(10):
            time.sleep(0.1)
            yield "{}\n".format(sqrt(i))
            hwapp.logger.debug(
                f"in func {inspect.currentframe().f_code.co_name}() line: {inspect.getframeinfo(inspect.currentframe()).lineno}")

    return Response(stream_with_context(stream_template('my_stream_template.html', rows=generate(), title='content')))


@hwapp.route('/Unity 450F')
def unity2():  # def execute(script):
    def inner():
        hwapp.logger.debug(
            f"in func {inspect.currentframe().f_code.co_name}() line: {inspect.getframeinfo(inspect.currentframe()).lineno}")
        script = saninfo
        # assert re.match(r'^[a-zA-Z._-]+$', script)
        # exec_path = "." + script + ".py" +"," +"-s" +"," + "EMC UNITY 450F"
        # exec_path =  script + ".py"  +"-s EMC UNITY 450F"
        exec_path = "EMC UNITY 450F"

        command = ["python", "-u", "saninfo.py", "-s", exec_path]  # -u: don't buffer output
        print("debug unity2", command)
        logging.info(f"2subrocess.run command is :{command}")
        hwapp.logger.debug(f"3subrocess.run command is :{command}")

        with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as proc:
            hwapp.logger.debug(f"in with {command}")
            #sanapp.logger.debug(proc.stdout.read())

        proc = subprocess.Popen(
            command,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )

        # for line in iter(proc.stdout.readline, ''):
        for line in proc.stdout:
            hwapp.logger.debug(f"proc.stdout is :{line}")
            yield highlight(line, BashLexer(), HtmlFormatter())
            # If process is done, break loop

    #         if proc.poll() == 0:
    #             break
    exec_path = "saninfo.py -s EMC UNITY 450F"
    exec_path = '-s "EMC UNITY 450F"'

    command = ["python", "-u", "saninfo.py"]  # -u: don't buffer output
    hwapp.logger.debug(
        f"in func {inspect.currentframe().f_code.co_name}() line: {inspect.getframeinfo(inspect.currentframe()).lineno} & {command}")
    logging.info(f"2subrocess.run command is :{command}")
    hwapp.logger.debug(f"3subrocess.run command is :{command}")

    with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as proc:
        hwapp.logger.debug(f"in with {command}")
        hwapp.logger.debug(proc.stdout.read())
    hwapp.logger.debug(f"in func {__name__}")

    env = Environment(loader=FileSystemLoader('templates'))
    tmpl = env.get_template('output.html')
    hwapp.logger.debug(f"in func {inspect.currentframe().f_code.co_name}() & {tmpl}")
    output = inner()
    hwapp.logger.debug(
        f"in func {inspect.currentframe().f_code.co_name}() line: {inspect.getframeinfo(inspect.currentframe()).lineno} & {output}")
    # return Response(tmpl.generate(output=inner()))
    return Response(tmpl.generate(output))


# def unity2():
#     output = SAN.main("-s", "EMC UNITY 450F")
#     context = {
#         "title": "EMC UNITY 450F",
#         "model": "testdec",
#         "output": output,
#     }



@hwapp.route('/ENM')
def toolshome():
    return render_template("ENMQueryForm.html", title="ENM Tools")


from flask import request, make_response
import shelve

# TODO fix up to return ENM info
@hwapp.route('/fetch', methods=['POST'])
def fetch():
    #(this form action should have been callign /cgi-bin/c2.py)
    enm = request.form['ENM']
    print(enm)
    enmversion = request.form['ENM Version']
    rhelversion = request.form['Redhat Version']
    # Get data from fields
    if request.form['enmversioncheckbox']:
        enmversioncheckbox_flag = "ON"
    else:
        enmversioncheckbox_flag = "OFF"
    if request.form['rhelcheckbox']:
        rhelcheckbox_flag = "ON"
    else:
        rhelcheckbox_flag = "OFF"
    if request.form['javaversioncheckbox']:
        javaversioncheckbox_flag = "ON"
    else:
        javaversioncheckbox_flag = "OFF"

    def getenms_in_db():
        db = shelve.open( 'class-shelve')
        enms = ""
        for key in db:  # key = ENM ID
            enms += key + ","
        db.close()
        return enms

    print("Content-Type: text/html")  # HTML is following
    print()  # blank line, end of headers
    print("<html>")
    print("<title>ENM Audit</title>")
    # print(os.getcwd())
    enms = getenms_in_db()
    num_enms = enms.count((","))
    num_enms_text = f"<h2>Number of ENMs in Audit: {num_enms}</h2>"
    enm_table = "ENM {enm} :ENM Version {enmversion} \n: RHEL {rhelversion}".format(enm=enm, enmversion=enmversion,
                                                                                    rhelversion=rhelversion)
    choices = " enmversioncheckbox is : {0}\n rhelcheckbox_flag is {1}".format(enmversioncheckbox_flag,
                                                                               rhelcheckbox_flag)
    replyhtml = f"""
    <body>
    <h1>ENM environments </h1>
    <h2>ENMS</h2>
    {num_enms_text}
    <p>{enms} </p>
    <hr>
    <p>{enm_table}</p>
    <p>{choices}</p>
    </body>
    """
    # print(html)
    # enm_table = string."ENM %s :ENM Version %s \n: RHEL %s" % (enm, enmversion, rhelversion)
    # "My name is {fname}, I'm {age}".format(fname = "John", age = 36)
    print(replyhtml)
    print("</html>")

    # print(" ENM %s :ENM Version %s \n: RHEL %s" % (enm, enmversion, rhelversion))
    # print(" enmversioncheckbox is : %s" % (enmversioncheckbox_flag))
    resp = make_response(render_template('base.html'))
    resp.mimetype = 'text/plain'
    return (replyhtml)
    #return redirect(url_for('content'))

if __name__ == "__main__":
    # app.run(host ='0.0.0.0')
    hwapp.run(debug=True)
