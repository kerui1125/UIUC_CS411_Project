from neo4j import GraphDatabase

DB_ADDRESS = "bolt://localhost: 7687"
DB_AUTH = ("neo4j", "cs411")


def get_keywords():
    try:
        driver = GraphDatabase.driver(DB_ADDRESS, auth=DB_AUTH)
        with driver.session(database='academicworld') as session:
            keywords = []
            result = session.run('MATCH (keyword:KEYWORD) RETURN keyword.name')
            for data in result.data():
                keywords.append(data['keyword.name'])
        driver.close()

    except Exception as e:
        print(f"Error occurred: {e}")
        exit(0)
    return keywords


def get_institutes():
    try:
        driver = GraphDatabase.driver(DB_ADDRESS, auth=DB_AUTH)
        with driver.session(database='academicworld') as session:
            institutes = []
            result = session.run('MATCH (i:INSTITUTE) RETURN i.name')
            for data in result.data():
                institutes.append(data['i.name'])
        driver.close()
    except Exception as e:
        print(f"Error occurred: {e}")
        exit(0)
    return institutes


def get_faculties(institute):
    try:
        driver = GraphDatabase.driver(DB_ADDRESS, auth=DB_AUTH)
        with driver.session(database='academicworld') as session:
            faculties = []
            institute_str = "','".join(institute)
            result = session.run("MATCH (f:FACULTY)-[r:AFFILIATION_WITH]->(i:INSTITUTE) "
                                 f"where i.name = '{institute_str}' "
                                 "RETURN f.name")
            for data in result.data():
                faculties.append(data['f.name'])
        driver.close()
    except Exception as e:
        print(f"Error occurred: {e}")
        exit(0)
    return faculties


def get_selection_items(keywords, institutes):
    try:
        driver = GraphDatabase.driver(DB_ADDRESS, auth=DB_AUTH)
        with driver.session(database='academicworld') as session:
            results = []
            keywords_str = "','".join(keywords)
            institutes_str = "','".join(institutes)
            result_2 = session.run("match (faculty:FACULTY)-[r:INTERESTED_IN]->(keyword:KEYWORD), "
                                   "(faculty:FACULTY)-[af:AFFILIATION_WITH]->(i:INSTITUTE) "
                                   "with keyword as keyword,count(faculty.name) as faculty_count, i.name as institute "
                                   f"where institute in ['{institutes_str}'] and keyword.name in ['{keywords_str}']  "
                                   "return keyword, institute, faculty_count order by faculty_count desc")
            for data in result_2.data():
                results.append([data["keyword"]["name"], data["institute"], data["faculty_count"]])
        driver.close()
    except Exception as e:
        print(f"Error occurred: {e}")
        exit(0)
    return results
