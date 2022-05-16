# 411 Final Project Report: CS Academic World

*Group member: Kerui Liu, Juntao Yu*

**Purpose: What is the application scenario? Who are the target users?**

This application is designed for users who are interested in computer science department professors of US universities.

**Purpose: What are the objectives?**

Users are able to:

a. Visualize and locate the Academic world related universities by US map

b. Find the count of professors in certain universities who are interested in selected areas, I.e. Internet, data mining, machine learning. Then students can prioritize what universities they would like to go to by the amount of interested professors.

c. View existing faculty member data table by selecting the university name and faculty name

d. Add new faculty member data (including name, email, phone number, position, institute) to Academic World database by entering these fields in input forms.

e. Query the publication based on keyword. The publication id, name, year and author gets returned

f. Give reviews to publications by inputting scores. Once a score is submitted, all the previous ratings of the publication will be returned.

**Demo:**

https://mediaspace.illinois.edu/media/t/1_q4dgg4w7

**Installation: How to install the application?**

We’re using pipenv as the main project environment. Pipenv uses pipfile to manage the dependency packages so users just need to run “pipenv install” to install all packages needed. As for credentials to access database, users need to change the default path of each DB creds to make the application run successfully.

**Usage: How to use it?**

a. In the “US University Map”, the universities with the count of professors in CS department are classified into 0-10, 10-20 xxx . Users can show certain class by click the map legend.

b. In the “Keywords Institutes Faculty Number Pie Chart”, the pie chart will show the percentage of faculty total number who are interested in certain keywords. Users can visualize the pie chart by add or delete the keywords and institutes names in the two dropdowns.

c. In the “Show Faculty” widget, users will see a multi-tabs editable datatable. In the “Show/Modify” tab, faculty info and photos can be modified. In the “Add New” tab, new faculty info and photo url can be added in. This widget will interact with the backend database.

d. In the “Modify Faculty” widget, users will be able to input five basic properties for a faculty member. So that a new faculty member information can be added. Or an existing faculty can be modified.

e. In the “publication by keyword” widget, users are prompted to input the keyword for research area. A table which contains publication information and a unioned list of authors will be returned.

f. In the “publications review” widget, users input publication id which could be fetched from widget #5, a reviewer id and a score. A new created table publication_review will be updated. The full list of previous reviews for this paper will be returned as a result.

**Design: What is the design of the application? Overall architecture and components?**

Used Dash dashboard application to build 6 independent widgets, including 4 querying (US map, pie chart, show faculty, publication_keyword) and 2 updating backend MySQL, MongoDB, and Neo4j database (add faculty, review a publication).

a. In the US Map widget, we used MongoDB database, we called external api to generate the geography latitude and longitude for each university, since the data is large, we used cache to save all information.

b. For the Pie Chart widget, we used Neo4j database, wrote functions to get all keywords and institutes. Then used callback function to interactively generate the pie chart which shows the percentage of faculties in certain keyword area.

c. For the Show/Add Faculty widget, we used Neo4j database to query and add new faculty node and university node, and create a relationship edge between these new nodes.

e. For the publication by keyword widget, we used mysql database to query the publications based on keyword in the input. The query joined multiple tables, and was able to provide abundant information including all the authors of this publication, which was processed based on the dataframe returned from mysql query.

f. For the publication review widget, we used mysql database. First, a new table publication_review was created to capture the activity of a user giving scores to publications. The table was created with foreign key constraint added to ensure the data integrity. Then we created a stored procedure to work on the update/insert operation. After a write query completes, a read query was fired to get all reviews for the given publication.

**Implementation: How did you implement it?**

a. Frontend: Dash has all frontend components (html/css/js) integrated in the application, including map, dropdowns, pie charts, data tables.

b. Backend: Dash app, which is based on flask app, serves as the main application server on localhost. “db” module contains all python files related with databases queries and updates. “widgets” contains all python files that related to our 6 widgets built.

c.Database: “neo4j.py” to connect neo4j database, “mongodb.py” to connect mongodb database, “MySQL.py” to connect MySQL database.

Database Techniques: What database techniques have you implemented?

a. Indexing

b. Constraint

c. Stored procedure

**Database Techniques: How?**

a. Indexing: Created clustered index which consists of a self incremental score id, publication_id and reviewer_id in new table publication_review to ensure a performant query experience.

b. Constraint: Created a foreign key constraint for the new table publication_review to keep the data integrity.

```
Create table publication_review
(
    score_id int NOT NULL auto_increment,
    publication_id int NOT NULL,
    score int NOT NULL,
    reviewer_id varchar(30) NOT NULL,
    constraint pk
    primary key (`score_id`, `publication_id`, `reviewer_id`),
    INDEX pub_id (`publication_id`),
    FOREIGN KEY (`publication_id`)
        REFERENCES publication(id)
        ON DELETE CASCADE
);
```

c. Stored procedure: Created a stored procedure to perform the update/insert task with transaction included to keep the data consistency.

```
DELIMITER $$
CREATE PROCEDURE UpsertPublicationReview(
	p_id INT, 
	s INT,
	r_id VarChar(30))
	BEGIN
	    DECLARE review_count INT DEFAULT 0;
		
	    SELECT 
		COUNT(*)
		INTO review_count 
		FROM publication_review
		WHERE publication_id = p_id AND reviewer_id = r_id;

	    START transaction;
		IF review_count = 0 THEN
			INSERT INTO publication_review (publication_id, score, reviewer_id) values (p_id, s, r_id);
		ELSE 
			UPDATE publication_review SET score = s WHERE publication_id = p_id AND reviewer_id = r_id;
		END IF;
	    COMMIT;
		
	END $$
 ```
**Extra-Credit Capabilities: What extra-credit capabilities have you developed, if any?**

We have implemented RESTful API based on self-structured flask app to replace the default one in Dash. We have registered a few routes to support restful API calls. For example, one can grab institute name, latitude and longitude as well as its faculty number in raw json format.
