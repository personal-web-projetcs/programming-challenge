import psycopg2
import csv

class DataBaseInterface(object):
       
    def connect(self):

        try:
            self.conn = psycopg2.connect(database = "titles",
                                         user = "djangoapp",
                                         password = "@01123581321",
                                         host = "localhost",
                                         port = "5432")
            self.cursor = self.conn.cursor()
        except Exception as e:
            print(e)
            self.cursor = None
            self.conn = None
            
        return self.conn.cursor()
    
    #Execute query prepared using mogrify lib
    def execute_prepared_query(self, query):
        try:
            self.cursor.execute(query)
            print(query)
        except Exception as e:
            print(e)
            print(query)

    
    def commit_changes(self):
        try:
            self.conn.commit()
            self.cursor.close()
            self.conn.close()
        except Exception as e:
            print(e)
            self.cursor = None
            self.conn = None
            

class Title(object):
    def __init__(self):
        self.tconst = ""
        self.titleType = ""
        self.primaryTitle = ""
        self.originalTitle = ""
        self.isAdult = False
        self.startYear = 0
        self.endYear = None
        self.runtimeMinutes = 0
        self.genres = []
            
    def load_and_save_titles(self, pathfile, db):
        db_cursor = db.connect()

        f = open(pathfile, 'r', encoding='utf-8')
        dataset = csv.reader(f, delimiter=  '\t')

        i = 0
        next(dataset)
        for str_item in dataset:
            i = i + 1

            if (i == 51):
                break
            
            self.tconst = str_item[0]
            self.titleType = str_item[1]
            self.primaryTitle = str_item[2]
            self.originalTitle = str_item[3]
            self.isAdult = True if (str_item[4] == 1) else False
            self.startYear = int(str_item[5]) if (str_item[5].isdigit() and len(str_item[5]) == 4) else None
            self.endYear = int(str_item[6]) if (str_item[6].isdigit() and len(str_item[6]) == 4) else None
            self.runtimeMinutes = int(str_item[7]) if (str_item[7].isdigit()) else None

            g = str_item[8].replace(' ', '')
            g = g.replace('\n', '')
            g = g.replace('\\', '')
            g = g.split(",")
            
            self.genres = []
            for genre in g:
                if (genre != "N"):
                    self.genres.append(genre)

            if (len(self.genres) == 0): self.genres = None
            
            sql_code = 'INSERT INTO tbl_title VALUES (default, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING *'
            fields = (self.tconst, self.titleType, self.primaryTitle, self.originalTitle, self.isAdult, self.startYear, self.endYear, self.runtimeMinutes, self.genres)

            formatted_query = db_cursor.mogrify(sql_code, fields)

            print(formatted_query)

            db_cursor.execute(formatted_query)
        
        db.commit_changes()


class Actor(object):
    def __init__(self):
        self.nconst = ""
        self.primaryName = ""
        self.birthYear = 0
        self.deathYear = 0
        self.primaryProfession = []
        self.knownForTitles = []

    def load_and_save_actors(self, pathfile, db):
        db_cursor = db.connect()

        f = open(pathfile, 'r', encoding='utf-8')
        dataset = csv.reader(f, delimiter=  '\t')

        i = 0
        next(dataset)
        for str_item in dataset:
            i = i + 1

            if (i == 51):
                break
            
            self.nconst = str_item[0]
            self.primaryName = str_item[1]
            self.birthYear = int(str_item[2]) if (str_item[2].isdigit() and len(str_item[2]) == 4) else None
            self.deathYear = int(str_item[3]) if (str_item[3].isdigit() and len(str_item[3]) == 4) else None

            p = str_item[4].replace(' ', '')
            p = p.replace('\n', '')
            p = p.replace('\\', '')
            p = p.split(",")

            self.primaryProfession = []
            for prof in p:
                if (prof != "N"): self.primaryProfession.append(prof)

            if (len(self.primaryProfession) == 0): self.primaryProfession = None
            
            sql_code = 'INSERT INTO tbl_actor VALUES (default, %s, %s, %s, %s, %s) RETURNING *'
            fields = (self.nconst, self.primaryName, self.birthYear, self.deathYear, self.primaryProfession)
            formatted_query = db_cursor.mogrify(sql_code, fields)
            #print(formatted_query)
            try:
                db_cursor.execute(formatted_query)
            except Exception as e:
                print(e)
                print(formatted_query)

            result = db_cursor.fetchone()
            print(result)
            if (result):
                actorId = result[0]
                self.load_and_save_known_titles(actorId, str_item[5], db_cursor)

        db.commit_changes()
    
    def load_and_save_known_titles(self, actorId, titles, db_cursor):

            p = titles.replace(' ', '')
            p = p.replace('\n', '')
            p = p.replace('\\', '')
            p = p.split(",")
            knownForTitles = []
            for kft in p:
                if (kft != "N"):   knownForTitles.append(kft)

            if (len(knownForTitles) == 0): knownForTitles = None

            self.knownForTitles = []

            for k in knownForTitles:
                sql_code = 'SELECT * FROM tbl_title WHERE tconst = %s'
                fields = (k,)
                formatted_query = db_cursor.mogrify(sql_code, fields)
                try:
                    db_cursor.execute(formatted_query)
                except Exception as e:
                    print(e)
                    print(formatted_query)
                result = db_cursor.fetchone()

                if (result): self.knownForTitles.append(result[0])

            if (len(self.knownForTitles) > 0):
                for k in self.knownForTitles:
                    sql_code = 'INSERT INTO tbl_title_actor VALUES (default, %s, %s)'
                    fields = (k, actorId)
                    formatted_query = db_cursor.mogrify(sql_code, fields)
                    try:
                        db_cursor.execute(formatted_query)
                        print(formatted_query)
                    except Exception as e:
                        print(e)
                        print(formatted_query)
            else:
                print("Have no known titles from " + str(actorId))
        

db = DataBaseInterface()

# t = Title()
# t.load_and_save_titles('data_title.tsv', db)
# print("Success - Titles data saved")

t = Actor()
t.load_and_save_actors('data_name.tsv', db)
print("Success - Actors data saved")



