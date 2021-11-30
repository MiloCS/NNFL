import subprocess
import os
import src.config as cf
from collections import defaultdict

# clones the project to the wd (working dir)
def checkout_project_vid(project_vid):
    wd = cf.TMP_DIR
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


def get_program_statements_dict(p_vid):
    program_statements_dict = defaultdict(lambda: '') # to avoid key errors, default is empty string
    project_path = cf.TMP_DIR + p_vid + '/'
    d4j_project_src_path = subprocess.check_output(['defects4j', 'export', '-p', 'dir.src.classes'],
                                                cwd=project_path).decode('utf-8')
    full_path = project_path + d4j_project_src_path + '/'
    l = len(full_path.split('/')) - 1
    d4j_project_files = [os.path.join(dp, f) for dp, dn, fn in os.walk(os.path.expanduser(full_path)) for f in fn]
    for file in d4j_project_files:
        if file[-5:] == '.java':
            with open(file) as f:
                file = file[:-5]
                lines = f.readlines()
                for i, line in enumerate(lines):
                    program_statements_dict['.'.join(file.split('/')[l:]) + '#' + str(i)] = line
    return program_statements_dict



