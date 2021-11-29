# NNFL
Neural-Network-Ensemble based fault localization project

## DB setup

#### Dataset we collected

[D4J FL Dataset (~3GB)](https://drive.google.com/file/d/1Axv_ycpNJkztaFROB9-LrYL-J-b60TuM/view?usp=sharing) -
a set of ~4000 test runs & associated coverages from all projects matching Mockito_1*b

setup:
1. install [postgreSQL](https://www.postgresql.org/download/)
   (if you already have a db server setup, skip to 4.)
2. initialize a database cluster - 'initdb -w database/'
3. start a server on the cluster - 'pg_ctl -D database/ -l psql.logfile start'
4. try connecting to the db server (enter psql shell)- 'psql -h localhost postgres'
5. create the database we'll dump the dataset into - 'createdb -T template0 d4j_fl'
6. exit - '\q'
7. dump the coverage data into the database - 'psql d4j_fl < path/to/d4j_fl_backup'

#### Collected by D4J publishers (Wash):
1. wget --recursive --no-parent --accept gzoltar-files.tar.gz http://fault-localization.cs.washington.edu/data
2. move fault-localization.cs.washington.edu into NNFL/data/ (~5GB)
3. move fixed-lines from https://bitbucket.org/rjust/fault-localization-data/src/master/analysis/pipeline-scripts/ into NNFL/data/, you'll need to clone the repo





## Dev Setup:
1. install [defects4j](https://github.com/rjust/defects4j)
2. modify config.py with psql db info and d4j install info
3. cd NNFL/
4. pip install virtualenv
5. virtualenv venv (or conda on M1 due to scikit incompatability)
6. source venv/bin/activate
7. pip install -r requirements.txt
8. pip install -r src/SBFL/requirements.txt
9. python main.py Or python EXAMplot.py