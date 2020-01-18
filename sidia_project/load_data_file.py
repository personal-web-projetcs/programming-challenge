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
    
    def commit_changes(self):      
        self.conn.commit()
        
            

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
        dataset = csv.reader(f, delimiter=  '\t', quoting=csv.QUOTE_NONE)

        i = 0
        next(dataset)
        for str_item in dataset:
            i = i + 1

            #if (i == 51):
            #    break
            
            self.tconst = str_item[0]
            self.title_type = str_item[1]
            self.primary_title = str_item[2]
            self.original_title = str_item[3]
            if str_item[4].isdigit() and (str_item[4] in ['0', '1', 0, 1]):
                self.is_adult = True if (str_item[4] == '1') else False
            else:
                self.is_adult = None
            
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
            
            sql_code = 'INSERT INTO tbl_title VALUES (default, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            fields = (self.tconst, self.title_type, self.primary_title, self.original_title, self.is_adult, self.start_year, self.end_year, self.runtime_minutes, self.genres)            

            try:
                formatted_query = db_cursor.mogrify(sql_code, fields)
                db_cursor.execute(formatted_query)
                if (i % 100 == 0):
                    db.commit_changes()
            except Exception as e:
                print(e)
                print(str_item)
                exit()
            print("title - i = " + str(i))
        db_cursor.close()
        db.conn.close()
    
    def update_titles(self, pathfile, db):
        db_cursor = db.connect()

        f = open(pathfile, 'r', encoding='utf-8')
        dataset = csv.reader(f, delimiter=  '\t', quoting=csv.QUOTE_NONE)

        i = 0
        next(dataset)
        for str_item in dataset:
            i = i + 1

            #if (i == 51):
            #    break
            
            self.tconst = str_item[0]
            self.title_type = str_item[1]
            self.primary_title = str_item[2]
            self.original_title = str_item[3]
            if str_item[4].isdigit() and (str_item[4] in ['0', '1', 0, 1]):
                self.is_adult = True if (str_item[4] == '1') else False
            else:
                self.is_adult = None
            if not self.is_adult: continue
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
            
            sql_code = 'INSERT INTO tbl_title_temp VALUES (default, %s, %s)'
            fields = (self.tconst, self.is_adult)     

            try:
                formatted_query = db_cursor.mogrify(sql_code, fields)
                db_cursor.execute(formatted_query)
                if (i % 100 == 0):
                    db.commit_changes()
            except Exception as e:
                print(e)
                print(str_item)
                exit()
            print("ratings - i = " + str(i))
        db_cursor.close()
        db.conn.close()

    


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
        dataset = csv.reader(f, delimiter=  '\t', quoting=csv.QUOTE_NONE)

        i = 0
        next(dataset)
        for str_item in dataset:
            i = i + 1

            #if (i == 51):
            #    break
            
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
            
            sql_code = 'INSERT INTO tbl_actor VALUES (default, %s, %s, %s, %s, %s)'
            fields = (self.nconst, self.primary_name, self.birth_year, self.death_year, self.primary_profession)
            
            try:
                formatted_query = db_cursor.mogrify(sql_code, fields)
                db_cursor.execute(formatted_query)
                if (i % 100 == 0):
                    db.commit_changes()
            except Exception as e:
                print(e)
                print(str_item)
                exit()
                #continue

            print("actors - i = " + str(i))
        
        try:
            db.commit_changes()
            db_cursor.close()
            db.conn.close()
        except:
            pass



class TitleActor(object):
    def __init__(self):
        self.title_id = 0
        self.actor_id = 0
    
    def load_data_title_actor(self, pathfile, db):
        db_cursor = db.connect()

        f = open(pathfile, 'r', encoding='utf-8')
        dataset = csv.reader(f, delimiter=  '\t', quoting=csv.QUOTE_NONE)

        i = 0
        next(dataset)
        for str_item in dataset:
            i = i + 1

            nconst = str_item[0]
            sql_code = 'SELECT * FROM tbl_actor WHERE nconst = %s'
            fields = (nconst,)
                
            try:
                formatted_query = db_cursor.mogrify(sql_code, fields)
                db_cursor.execute(formatted_query)
                result = db_cursor.fetchone()
            except Exception as e:
                print(e)
                print(formatted_query)
                exit()

            if len(result) > 0: 
                actor_id = result[0]
                self.save_known_titles(actor_id, str_item[5], db_cursor)
            else:
                print("Actor not found " + nconst)

            print("title_actor - i = " + str(i))


    def save_known_titles(self, actor_id, titles, db_cursor):
    
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
                
                try:
                    formatted_query = db_cursor.mogrify(sql_code, fields)
                    db_cursor.execute(formatted_query)
                    result = db_cursor.fetchone()
                except Exception as e:
                    print(e)
                    print(formatted_query)
                    exit()
                    # db_cursor = db.connect()
                    # continue

                if (result): self.known_for_titles.append(result[0])

            if (len(self.known_for_titles) > 0):
                for k in self.known_for_titles:
                    sql_code = 'INSERT INTO tbl_title_actor VALUES (default, %s, %s)'
                    fields = (actor_id, k)
                    try:
                        formatted_query = db_cursor.mogrify(sql_code, fields)
                        db_cursor.execute(formatted_query)
                        db.commit_changes()
                    except Exception as e:
                        print(e)
                        print(formatted_query)
                        exit()
                        # db_cursor = db.connect()
                        # continue
            else:
                print(">> Not found titles in db ")
                print(">> Actor : " + str(actor_id))
                print(">> Titles : " + str(known_for_titles))

    def load_data_title_actor_temp(self, pathfile, db):
        db_cursor = db.connect()

        f = open(pathfile, 'r', encoding='utf-8')
        dataset = csv.reader(f, delimiter=  '\t', quoting=csv.QUOTE_NONE)

        i = 0
        l = 0
        next(dataset)
        for str_item in dataset:
            i = i + 1
            l = l + 1
            nconst = str_item[0]
            
            p = str_item[5].replace(' ', '')
            p = p.replace('\n', '')
            p = p.replace('\\', '')
            p = p.split(",")
            known_for_titles = []
            for kft in p:
                if (kft != "N"):   known_for_titles.append(kft)
            
            j = 0
            for k in known_for_titles:
                sql_code = 'INSERT INTO tbl_title_actor_temp VALUES (%s, %s, %s)'
                fields = ((i + j), k, nconst)
                try:
                    formatted_query = db_cursor.mogrify(sql_code, fields)
                    db_cursor.execute(formatted_query)
                    j = j + 1
                    if (i % 100 == 0):
                        db.commit_changes()
                except Exception as e:
                    print(e)
                    print(formatted_query)
                    exit()

            i = i + j
            print("title_actor - l = " + str(l))
        self._execute_query(db_cursor)
        db_cursor.close()
        db.conn.close()

    def _execute_query(self, db_cursor):
        
        sql_code = """INSERT INTO tbl_title_actor 
                        SELECT tbl_title_actor_temp.uid, tbl_actor.actor_id, tbl_title.title_id 
                        FROM  tbl_title INNER JOIN tbl_title_actor_temp ON tbl_title.tconst=tbl_title_actor_temp.tconst 
                        INNER JOIN tbl_actor ON tbl_actor.nconst=tbl_title_actor_temp.nconst 
                        WHERE tbl_title.title_id IS NOT NULL AND tbl_actor.actor_id IS NOT NULL"""
        try:
            #formatted_query = db_cursor.mogrify(sql_code)
            #db_cursor.execute(formatted_query)
            db_cursor.execute(sql_code)
            db.commit_changes()
        except Exception as e:
            print(e)
            print(sql_code)
            exit()


class Rating(object):
    def __init__(self):
        self.title_id = 0
        self.average_rating = 0
        self.num_votes = 0
        
    def load_and_save_ratings(self, pathfile, db):
        db_cursor = db.connect()

        f = open(pathfile, 'r', encoding='utf-8')
        dataset = csv.reader(f, delimiter=  '\t', quoting=csv.QUOTE_NONE)

        i = 0
        next(dataset)
        for str_item in dataset:   
            i = i + 1

            if (i == 1001):
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
                #if (i % 100 == 0):
                   #db.commit_changes()
                db.commit_changes()
            except Exception as e:
                print(e)
                print(formatted_query)
                exit()
            
            
            print("ratings - i = " + str(i))

        db_cursor.close()
        db.conn.close()
    
    def load_and_save_ratings_temp(self, pathfile, db):

        db_cursor = db.connect()

        f = open(pathfile, 'r', encoding='utf-8')
        dataset = csv.reader(f, delimiter=  '\t', quoting=csv.QUOTE_NONE)

        i = 0
        next(dataset)
        for str_item in dataset:   
            i = i + 1
            
            tconst = str_item[0]
            
            try:
                self.average_rating = float(str_item[1])
            except:
                self.average_rating = None

            self.num_votes = int(str_item[2]) if (str_item[2].isdigit()) else None

            sql_code = 'INSERT INTO tbl_rating_temp VALUES (%s, %s, %s, %s)'
            fields = (i, tconst, self.average_rating, self.num_votes)
            formatted_query = db_cursor.mogrify(sql_code, fields)
            #print(formatted_query)
            try:
                db_cursor.execute(formatted_query)
                if (i % 100 == 0):
                    db.commit_changes()
            except Exception as e:
                print(e)
                print(formatted_query)
                exit()
            
            print("ratings_temp - i = " + str(i))

        try:
            db.commit_changes()
        except Exception as e:
            print(e)
            exit()
        self._execute_query(db_cursor)    
        db_cursor.close()
        db.conn.close()
        
    
    def _execute_query(self, db_cursor):
        
        sql_code = """INSERT INTO tbl_rating
                      SELECT title_id, average_rating, num_votes
                      FROM  tbl_title INNER JOIN tbl_rating_temp ON tbl_title.tconst=tbl_rating_temp.tconst
                      WHERE tbl_title.tconst <> ''"""
        try:
            db_cursor.execute(sql_code)
            db.commit_changes()
        except Exception as e:
            print(e)
            exit()


def max_size_field(pathfile, column):
    max = 0
    value = ""

    f = open(pathfile, 'r', encoding='utf-8')
    dataset = csv.reader(f, delimiter=  '\t',  quoting=csv.QUOTE_NONE)

    next(dataset)
    for str_item in dataset:
        if len(str_item[column]) > max: 
            max = len(str_item[column])
            value = str_item
    return (value, max)

def count_fields(pathfile, lim):
    f = open(pathfile, 'r', encoding='utf-8')
    dataset = csv.reader(f, delimiter='\t', quoting=csv.QUOTE_NONE)

    next(dataset)
    for str_item in dataset:
        if len(str_item) != lim: 

            print(str(str_item))

# max = max_size_field('data_title.tsv', 2)
# print(max)
# count_fields('data_rating.tsv', 3)


db = DataBaseInterface()

t = Title()
#t.load_and_save_titles('data_title.tsv', db)
t.update_titles('data_title.tsv', db)
print("Success - Titles data saved")

# t = Actor()
# t.load_and_save_actors('data_name.tsv', db)
# print("Success - Actors data saved")

# t = TitleActor()
# t.load_data_title_actor('data_name.tsv', db)
# print("Success - TitleActor data saved")

# t = TitleActor()
# t.load_data_title_actor_temp('data_name.tsv', db)
# print("Success - TitleActor data saved")

# t = Rating()
# t.load_and_save_ratings('data_rating.tsv', db)
# print("Success - Ratings data saved")

# t = Rating()
# t.load_and_save_ratings_temp('data_rating.tsv', db)
# print("Success - Ratings data saved")






