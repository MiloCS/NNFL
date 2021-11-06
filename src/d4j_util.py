import subprocess
import os


# clones the project to the wd (working dir)
def checkout_project_vid(project_vid, wd):
    project, vid = project_vid.split('_')
    wd += project_vid + '/'
    checkout_command = ['defects4j', 'checkout', '-p', project, '-v', vid, '-w', wd]
    subprocess.Popen(checkout_command, env=dict(os.environ)).wait()


# returns a list of strings of the modified classes for the project, bid
def get_modified_classes_info(project, bid):
    command = ['defects4j', 'query', '-p', project, '-q', 'classes.modified']
    output = subprocess.check_output(command).decode('utf-8')
    for line in output.splitlines():
        curr_bid, classes = line.split(',')
        classes = classes[1:-1]
        classes = list(classes.split(';'))
        if int(curr_bid) == int(bid):
            return classes
