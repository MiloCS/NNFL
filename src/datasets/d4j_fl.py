import psycopg2
import psycopg2.extras


def get_test_tuple(c_str, test_id):
    with psycopg2.connect(c_str) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM tests WHERE testid=%s", [test_id])
            return cur.fetchone()

def get_all_test_ids(c_str, project_vid):
    with psycopg2.connect(c_str) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT testid FROM tests WHERE project=%s", [project_vid])
            return cur.fetchall()

