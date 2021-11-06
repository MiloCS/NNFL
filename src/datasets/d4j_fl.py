import psycopg2
import psycopg2.extras
from collections import defaultdict
import xml.etree.ElementTree as ET
import numpy as np

def get_test_tuple(cur, test_id):
    cur.execute("SELECT * FROM tests WHERE testid=%s", [test_id])
    return cur.fetchone()


def get_all_tests(cur, project_vid): # that have an existing coverage
    cur.execute("SELECT DISTINCT t.testid, t.class, t.method FROM tests AS t, coverages AS c, invocations AS i WHERE c.coverageid=i.coverageid AND t.testid=i.testid AND t.project=%s", [project_vid])
    return cur.fetchall()


def get_coverage_invocation_tuple(cur, test_id):
    cur.execute("SELECT i.passed, c.xml FROM coverages AS c, invocations AS i WHERE i.coverageid=c.coverageid AND i.testid=%s", [test_id])
    return cur.fetchone()


# and this is why post processing a datasets sucks *sigh*
def data_formatted(cur, project_vid):
    tests = get_all_tests(cur, project_vid)

    # STEP 1: load all coverage data for the bug
    tests_counts = dict({}) # test_id -> defaultdict(default 0) ; class+line -> count
    # and
    line_set = set({})  # {class+line,..} observed for all tests
    tests_passed = []
    for test_id, _, _ in tests:
        c = dict({})
        c = defaultdict(lambda: 0, c)
        passed, xml_memview = get_coverage_invocation_tuple(cur, test_id)
        xml_str = xml_memview.tobytes().decode()  # this a coverage.xml but as a string
        for packages in ET.fromstring(xml_str).iter('package'):
            for classes in packages.find('classes').findall('class'):
                for method in classes.find('methods').findall('method'):
                    for line in method.find('lines').findall('line'):
                        cnt = line.get('number')
                        line_id = packages.get('name') + '$' + classes.get('name').split('.')[-1] + '#' + method.get('name') + '():' + str(cnt)
                        c[line_id] = int(cnt)
                        line_set.add(line_id)
        tests_counts[str(test_id)] = c
        tests_passed.append(int(not passed))

    D = len(line_set)
    N = len(tests)
    # STEP 2: construct the np arrays for NN training
    X = np.zeros((N,D), dtype=np.single)
    Y = np.array(tests_passed, dtype=np.single, ndmin=2).T
    n_lab = []
    d_lab = []

    for _, test_class, test_method in tests:
        n_lab.append(test_class + '::' + test_method)

    d = 0
    for line_id in line_set:
        d_lab.append(line_id)
        n = 0
        for test_id, test_class, test_method in tests:
            X[n, d] = tests_counts[test_id][line_id]
            n += 1
        d += 1

    return X, Y, n_lab, d_lab
