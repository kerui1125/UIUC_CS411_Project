import pandas as pd
import sqlalchemy as sa

from src.uiuc_411_project.db.load_db_secrets import secretloader


class MYSQL:
    def __init__(self):
        secret = secretloader('mysql')
        host = secret.host
        user = secret.user
        password = secret.password
        database = secret.db
        port = secret.port
        charset = secret.charset
        self.connection = sa.create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}?charset={charset}")

    def query1Panda(self, paperThreshold):
        query = f"SELECT count_table.name FROM (SELECT faculty.name FROM faculty, publication, faculty_publication WHERE faculty.id = faculty_publication.faculty_id and faculty_publication.publication_id = publication.id and publication.num_citations > 10 and publication.year = 2012) as count_table GROUP BY count_table.name HAVING count(count_table.name) > {paperThreshold} ORDER BY trim(count_table.name)"
        pandaQuery = pd.read_sql_query(query, self.connection)
        df = pd.DataFrame(pandaQuery, columns=['name'])
        print(df)


db = MYSQL()
db.query1Panda(20)
