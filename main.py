import src.d4jUtil as d4j
import src.config as cf
import src.datasets.d4j_fl as d4j_fl

if __name__ == '__main__':
    # We're going to build a FL NN for a specific bug.
    project = "Mockito"
    bug_id = "10"

    res = d4j.get_modified_classes_info("Mockito", "10")
    print("Classes Modified in Fix", res)

    # ideally, we want to fault localize at a line level, but we need to extract the modified line information from the git log in the 'b' and 'f' versions of the bug and diff'ing the logs

    # get all test_id's for a specific bug, the fl dataset only has test runs for the 'b' versions
    full_project_name = project + '_' + bug_id + 'b'
    tests = d4j_fl.get_all_test_ids(cf.c_str, full_project_name)
    print("Num Tests", len(tests))

    # get the test info for the first test_id
    test_id = tests[0]
    info = d4j_fl.get_test_tuple(cf.c_str, test_id)
    print(info)
    _, _, test_class, test_method = info

    # TODO - method to request coverage & result for specific test_id

    # TODO - coerce each coverage str to binary list of length N corresponding to the N program lines

    # we then train a NN to learn execution result from the coverage binary list, then extract the suspicion scores from the NN weights
    # also need to implement SB-FL Ochai, should be trivial

    # lastly, we need to compute the EXAM score which tells us the accuracy of a particular FL technique (we'll have to use class level localization for now...)







