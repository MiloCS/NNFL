
# DB Config
psql = {
    'user': 'guest', # the dumps file will set the own of d4j_fl to dgraymullen, ask me if you need to the admin psswd
    'password': 'None',
    'port': 14566,  # psql default is 5432
    'host': 'localhost',
    'dbname': 'd4j_fl'
}

# D4J Config
d4j_project_clone_dir = 'tmp/'  # where d4j will clone projects
d4j_dir = '/Users/dgraymullen/Documents/GitHub/defects4j/' # where you installed d4j



# adjust anything above here
# ----------------------------------------------------------------------------------------------------------------------

# pass c_str to psycopg2 to connect
c_str = 'host=' + psql['host']
c_str += ' dbname=' + psql['dbname']
c_str += ' user=' + psql['user']
c_str += ' password=' + psql['password']
c_str += ' port=' + str(psql['port'])

d4j_pdd = d4j_dir + 'framework/projects/'  # d4j project data dir, needed to retrieving d4j query data manually

