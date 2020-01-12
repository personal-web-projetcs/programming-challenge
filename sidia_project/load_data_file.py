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
        self.title_type = ""
        self.primary_title = ""
        self.original_title = ""
        self.is_adult = False
        self.start_year = 0
        self.end_year = None
        self.runtime_minutes = 0
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
            self.title_type = str_item[1]
            self.primary_title = str_item[2]
            self.original_title = str_item[3]
            self.is_adult = True if (str_item[4] == 1) else False
            self.start_year = int(str_item[5]) if (str_item[5].isdigit() and len(str_item[5]) == 4) else None
            self.end_year = int(str_item[6]) if (str_item[6].isdigit() and len(str_item[6]) == 4) else None
            self.runtime_minutes = int(str_item[7]) if (str_item[7].isdigit()) else None

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
            fields = (self.tconst, self.title_type, self.primary_title, self.original_title, self.is_adult, self.start_year, self.end_year, self.runtime_minutes, self.genres)

            formatted_query = db_cursor.mogrify(sql_code, fields)

            print(formatted_query)

            db_cursor.execute(formatted_query)
        
        db.commit_changes()


class Actor(object):
    def __init__(self):
        self.nconst = ""
        self.primary_name = ""
        self.birth_year = 0
        self.death_year = 0
        self.primary_profession = []
        self.known_for_titles = []

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
            self.primary_name = str_item[1]
            self.birth_year = int(str_item[2]) if (str_item[2].isdigit() and len(str_item[2]) == 4) else None
            self.death_year = int(str_item[3]) if (str_item[3].isdigit() and len(str_item[3]) == 4) else None

            p = str_item[4].replace(' ', '')
            p = p.replace('\n', '')
            p = p.replace('\\', '')
            p = p.split(",")

            self.primary_profession = []
            for prof in p:
                if (prof != "N"): self.primary_profession.append(prof)

            if (len(self.primary_profession) == 0): self.primary_profession = None
            
            sql_code = 'INSERT INTO tbl_actor VALUES (default, %s, %s, %s, %s, %s) RETURNING *'
            fields = (self.nconst, self.primary_name, self.birth_year, self.death_year, self.primary_profession)
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
                actor_id = result[0]
                self.load_and_save_known_titles(actor_id, str_item[5], db_cursor)

        db.commit_changes()
    
    def load_and_save_known_titles(self, actor_id, titles, db_cursor):

            p = titles.replace(' ', '')
            p = p.replace('\n', '')
            p = p.replace('\\', '')
            p = p.split(",")
            known_for_titles = []
            for kft in p:
                if (kft != "N"):   known_for_titles.append(kft)

            if (len(known_for_titles) == 0): known_for_titles = None

            self.known_for_titles = []

            for k in known_for_titles:
                sql_code = 'SELECT * FROM tbl_title WHERE tconst = %s'
                fields = (k,)
                formatted_query = db_cursor.mogrify(sql_code, fields)
                try:
                    db_cursor.execute(formatted_query)
                except Exception as e:
                    print(e)
                    print(formatted_query)
                result = db_cursor.fetchone()

                if (result): self.known_for_titles.append(result[0])

            if (len(self.known_for_titles) > 0):
                for k in self.known_for_titles:
                    sql_code = 'INSERT INTO tbl_title_actor VALUES (default, %s, %s)'
                    fields = (k, actor_id)
                    formatted_query = db_cursor.mogrify(sql_code, fields)
                    try:
                        db_cursor.execute(formatted_query)
                        print(formatted_query)
                    except Exception as e:
                        print(e)
                        print(formatted_query)
            else:
                print("Have no known titles from " + str(actor_id))
    

class Rating(object):
    def __init__(self):
        self.title_id = 0
        self.average_rating = 0
        self.num_votes = 0
        
    def load_and_save_ratings(self, pathfile, db):
        db_cursor = db.connect()

        f = open(pathfile, 'r', encoding='utf-8')
        dataset = csv.reader(f, delimiter=  '\t')

        i = 0
        next(dataset)
        for str_item in dataset:   
            i = i + 1

            if (i == 51):
                break
            
            tconst = str_item[0]
            sql_code = 'SELECT * FROM tbl_title WHERE tconst = %s'
            fields = (tconst,)
            formatted_query = db_cursor.mogrify(sql_code, fields)
            try:
                db_cursor.execute(formatted_query)
            except Exception as e:
                print(e)
                print(formatted_query)
            result = db_cursor.fetchone()

            if (result): self.title_id = result[0]

            try:
                self.average_rating = float(str_item[1])
            except:
                self.average_rating = None

            self.num_votes = int(str_item[2]) if (str_item[2].isdigit()) else None

            sql_code = 'INSERT INTO tbl_rating VALUES (%s, %s, %s)'
            fields = (self.title_id, self.average_rating, self.num_votes)
            formatted_query = db_cursor.mogrify(sql_code, fields)
            #print(formatted_query)
            try:
                db_cursor.execute(formatted_query)
            except Exception as e:
                print(e)
                print(formatted_query)
        db.commit_changes()


db = DataBaseInterface()

t = Title()
t.load_and_save_titles('data_title.tsv', db)
print("Success - Titles data saved")

t = Actor()
t.load_and_save_actors('data_name.tsv', db)
print("Success - Actors data saved")

t = Rating()
t.load_and_save_ratings('data_rating.tsv', db)
print("Success - Ratings data saved")


