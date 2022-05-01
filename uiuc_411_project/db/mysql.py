import pandas as pd
import sqlalchemy as sa

from uiuc_411_project.db.load_db_secrets import secretloader


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

    def get_publication_by_keyword(self, keyword, last_id) -> pd.DataFrame:
        query = f"select distinct pub.id as publication_id, pub.title as publication_name, pub.year as year, faculty.name as professor from keyword k inner join publication_keyword pub_k on k.id = pub_k.keyword_id inner join publication pub on pub_k.publication_id = pub.id inner join faculty_publication fp on pub.id = fp.publication_id inner join faculty on fp.faculty_id = faculty.id WHERE k.name = '{keyword}' AND pub.id > {last_id} ORDER BY pub.id LIMIT 10"
        pandaQuery = pd.read_sql_query(query, self.connection)
        df = pd.DataFrame(pandaQuery, columns=['publication_id', 'publication_name', 'year', 'professor'])

        unique_paper_ids = dict()
        duplicate_index_ids = list()
        index = 0
        while index < len(df):
            paper_id = df['publication_id'].values[index]
            if paper_id not in unique_paper_ids:
                unique_paper_ids[paper_id] = index
            else:
                duplicate_index_ids.append(index)
                df.at[unique_paper_ids[paper_id], 'professor'] += " | " + df['professor'].values[index]
            index += 1
        df = df.drop(labels=duplicate_index_ids)
        return df

    def test_merge_prof(self) -> pd.DataFrame:
        df = self.get_publication_by_keyword('data mining', 0)
        unique_paper_ids = dict()
        duplicate_index_ids = list()
        index = 0
        while index < len(df):
            paper_id = df['publication_id'].values[index]
            if paper_id not in unique_paper_ids:
                unique_paper_ids[paper_id] = index
            else:
                duplicate_index_ids.append(index)
                df.at[unique_paper_ids[paper_id], 'professor'] += " | " + df['professor'].values[index]
            index += 1
        df = df.drop(labels=duplicate_index_ids)
        return df




