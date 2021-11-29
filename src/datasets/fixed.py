
def get_fixes(pid, bid):
    work_dir = 'data/fixed-lines/'
    target_file = work_dir + pid + '-' + bid + '.fixed.lines'
    fixes = []
    with open(target_file) as f:
        lines = f.readlines()
        for line in lines:
            c_class, c_linenum, code = tuple(line.split('#'))
            c_class = c_class[:-5].replace('/', '.')
            fixes.append(c_class + '#' + c_linenum)
    return fixes