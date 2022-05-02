from neo4j import GraphDatabase

DB_ADDRESS = "bolt://localhost: 7687"
DB_AUTH = ("neo4j", "cs411")


def get_keywords() -> list:
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


def get_institutes() -> list:
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


def get_selection_items(keywords: list, institutes: list) -> list:
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


def get_faculties(institute: str) -> list:
    try:
        driver = GraphDatabase.driver(DB_ADDRESS, auth=DB_AUTH)
        with driver.session(database='academicworld') as session:
            faculties = []
            result = session.run("MATCH (f:FACULTY)-[r:AFFILIATION_WITH]->(i:INSTITUTE) "
                                 f"where i.name = '{institute}' "
                                 "RETURN f.name")
            for data in result.data():
                faculties.append(data['f.name'])
        driver.close()
    except Exception as e:
        print(f"Error occurred: {e}")
        exit(0)
    return faculties


def get_faculty_data(faculty_name: str) -> dict:
    try:
        driver = GraphDatabase.driver(DB_ADDRESS, auth=DB_AUTH)
        with driver.session(database='academicworld') as session:
            faculty_all_info = {}
            result = session.run("match (f:FACULTY)-[af:AFFILIATION_WITH]->(i:INSTITUTE) "
                                 f"where f.name in ['{faculty_name}'] "
                                 "return f.photoUrl, f.phone, f.position, f.email, i.name")
            for data in result.data():
                faculty_all_info["photoUrl"] = data.get("f.photoUrl", "")
                faculty_all_info["phone"] = data.get("f.phone", "").split(" ")[1]
                faculty_all_info["position"] = data.get("f.position", "")
                faculty_all_info["email"] = data.get("f.email", "")
                faculty_all_info["institute_name"] = data.get("i.name", "")
        driver.close()
    except Exception as e:
        print(f"Error occurred: {e}")
        exit(0)
    return faculty_all_info


def add_a_faculty_member(name, phone, position, email, institute_name) -> None:
    driver = GraphDatabase.driver(DB_ADDRESS, auth=DB_AUTH)
    with driver.session(database='academicworld') as session:
        session.run(
            "CREATE (f:FACULTY {{name: '{name}', phone: '{phone}', position: '{position}', email: '{email}'}})"
            .format(name=name, phone=phone, position=position, email=email)
        )
        session.run(
            "CREATE (i:INSTITUTE {{name: '{institute_name}'}})".format(institute_name=institute_name)
        )
        session.run(
            "MATCH (f:FACULTY), (i:INSTITUTE) WHERE f.name = '{name}' AND i.name = '{institute_name}' "
            "CREATE (f)-[r:AFFILIATION_WITH]->(i)".format(name=name, institute_name=institute_name)
        )
