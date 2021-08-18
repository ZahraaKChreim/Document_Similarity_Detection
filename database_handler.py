import preprocess
import time
import mysql.connector
from textblob import TextBlob
from googletrans import Translator
from langdetect import detect

class databaseHandler:

    def __init__(self):
        self.con = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="m2_internship"
        )

    def insert_into_db(self, lang, domain, query, url, website_title, page_title, subtitles, urls, body):  

        try:
            cursor = self.con.cursor()

            insert_query =  """ INSERT INTO data (lang, domain, query, url, website_title, page_title, subtitles, urls, body) 
                                VALUES 
                                (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            record = (lang, domain, query, url, website_title, page_title, subtitles, urls, body)
            
            cursor.execute(insert_query, record)
            self.con.commit()
            print("New Record inserted successfully\n")
            return True
        
        except mysql.connector.Error as error:
            print("Failed to insert into MySQL table {}".format(error))
            return False

    def select_from_db_by_query(self, query):

        try:
            cursor = self.con.cursor()
            select_query = 'SELECT * FROM data WHERE data.query = "'+ query + '"'
            cursor.execute(select_query)

            select_result = cursor.fetchall()

            results = []
            if len(results) == 0:
                print("no results for query:", query, "!")
            for record in select_result:
                id = record[0]
                lang = record[1]
                domain = record[2]
                query = record[3]
                url = record[4]
                website_title = record[5]
                page_title = record[6]
                subtitles = record[7]
                urls = record[8]
                body = record[9]
                synt_proc_body = record[10]
                sem_proc_body = record[11]

                result = {'id': id, 'lang': lang, 'domain': domain, 'query': query, 'url': url, 'website_title': website_title, 'page_title': page_title, 'subtitles': subtitles, 'urls': urls, 'body': body, 'synt_proc_body': synt_proc_body, 'sem_proc_body': sem_proc_body}
                results.append(result)
                
            return results

        except mysql.connector.Error as error:
            print("Failed to select query " + query + " from MySQL: {}".format(error))
            
    def select_from_db_by_url(self, url):

        try:
            cursor = self.con.cursor()
            select_query = """  SELECT *
                                FROM data
                                WHERE data.url = '""" + url + """ ' """
            cursor.execute(select_query)

            select_result = cursor.fetchall()

            # This should be one row result
            for record in select_result:
                id = record[0]
                lang = record[1]
                domain = record[2]
                query = record[3]
                url = record[4]
                website_title = record[5]
                page_title = record[6]
                subtitles = record[7]
                urls = record[8]
                body = record[9]
                synt_proc_body = record[10]
                sem_proc_body = record[11]

                result = {'id': id, 'lang': lang, 'domain': domain, 'query': query, 'url': url, 'website_title': website_title, 'page_title': page_title, 'subtitles': subtitles, 'urls': urls, 'body': body, 'synt_proc_body': synt_proc_body, 'sem_proc_body': sem_proc_body}
                
            return result

        except mysql.connector.Error as error:
            print("Failed to select url " + url + " from MySQL: {}".format(error))

    def select_from_db_by_id(self, id):

        try:
            cursor = self.con.cursor()
            select_query = """  SELECT *
                                FROM data
                                WHERE data.id = '""" + str(id) + """ ' """
            cursor.execute(select_query)

            select_result = cursor.fetchall()

            # This should be one row result
            for record in select_result:
                id = record[0]
                lang = record[1]
                domain = record[2]
                query = record[3]
                url = record[4]
                website_title = record[5]
                page_title = record[6]
                subtitles = record[7]
                urls = record[8]
                body = record[9]
                synt_proc_body = record[10]
                sem_proc_body = record[11]

                result = {'id': id, 'lang': lang, 'domain': domain, 'query': query, 'url': url, 'website_title': website_title, 'page_title': page_title, 'subtitles': subtitles, 'urls': urls, 'body': body, 'synt_proc_body': synt_proc_body, 'sem_proc_body': sem_proc_body}
                
            return result

        except mysql.connector.Error as error:
            print("Failed to select id " + id + " from MySQL: {}".format(error))

    def select_all_queries_from_db(self):

        try:
            cursor = self.con.cursor()
            select_query = """  SELECT DISTINCT query
                                FROM data """
            cursor.execute(select_query)
            select_result = cursor.fetchall()

            queries = []
            for query in select_result:
                queries.append(query[0])

            return queries

        except mysql.connector.Error as error:
            print("Failed to select list of queries from MySQL: {}".format(error))

    def select_all_ids_from_db(self):

        try:
            cursor = self.con.cursor()
            select_query = """  SELECT id
                                FROM data WHERE lang='ar' and body != "" and id > 11606 """
            cursor.execute(select_query)
            select_result = cursor.fetchall()

            ids = []
            for query in select_result:
                ids.append(query[0])

            return ids

        except mysql.connector.Error as error:
            print("Failed to select list of ids from MySQL: {}".format(error))

    def preprocess_record_by_id(self, id):

        lang = "ar"
        try:
            cursor = self.con.cursor()
            select_query = """ SELECT body
                               FROM data
                               WHERE id = '""" + str(id) + """'"""
            cursor.execute(select_query)
            select_result = cursor.fetchall()

            # This should be one row result
            for record in select_result:
                body = record[0]

            if lang == "en":
                synt_proc_body = preprocess.get_syntactically_preprocessed_paragraph(body)
                sem_proc_body_list = preprocess.get_semantically_preprocessed_paragraph(body)
                sem_proc_body = "___".join(sentence for sentence in sem_proc_body_list)

            elif lang == "fr":
                synt_proc_body = preprocess.get_syntactically_preprocessed_french_paragraph(body)
                sem_proc_body_list = preprocess.get_semantically_preprocessed_french_paragraph(body)
                sem_proc_body = "___".join(sentence for sentence in sem_proc_body_list)

            elif lang == "ar":
                synt_proc_body = preprocess.get_syntactically_preprocessed_arabic_paragraph(body)
                sem_proc_body_list = preprocess.get_semantically_preprocessed_arabic_paragraph(body)
                sem_proc_body = "___".join(sentence for sentence in sem_proc_body_list)

            cursor = self.con.cursor()
            update_query = """ UPDATE data
                            SET synt_proc_body = '""" + synt_proc_body + """' , sem_proc_body = '""" + sem_proc_body + """'
                            WHERE id = '""" + str(id) + """'"""
            cursor.execute(update_query)
            self.con.commit()
            print(cursor.rowcount, "record(s) affected")

        except mysql.connector.Error as error:
            print("Failed to update record: {}".format(error))

    def correct_language_by_id(self, id):
        
        try:
            cursor = self.con.cursor()
            select_query = """ SELECT body
                               FROM data
                               WHERE id = '""" + str(id) + """'"""
            cursor.execute(select_query)
            select_result = cursor.fetchall()

            # This should be one row result
            for record in select_result:
                body = record[0]

            if body != "":
                # tb = TextBlob(body)
                # lang = tb.detect_language()
                
                # translator = Translator()
                # lang = translator.detect(body).lang

                lang = detect(body)

                if lang != 'en':
                    print(lang, "not en\n\n")
                    cursor = self.con.cursor()
                    update_query = """ UPDATE data
                                    SET lang = '""" + lang + """'
                                    WHERE id = '""" + str(id) + """'"""
                    cursor.execute(update_query)
                    self.con.commit()
                    print(cursor.rowcount, "record(s) affected:", id)

        except mysql.connector.Error as error:
            print("Failed to update record lang: {}".format(error))

def correct_languages():

    db = databaseHandler()
    print("MySQL connection is opened")

    ids = db.select_all_ids_from_db()
    i = 1
    total = len(ids)
    for id in ids:
        print(id, ", nb", i, "of", total)
        i += 1
        db.correct_language_by_id(id)

    if db.con.is_connected():
        db.con.close()
        print("MySQL connection is closed")

def preprocessing():

    db = databaseHandler()
    print("MySQL connection is opened")

    ids = db.select_all_ids_from_db()
    total = len(ids)

    i = 1
    t = time.time()

    for id in ids:
        print("preprocessing ", id, "(", i, "of", total, ")")
        i += 1
        db.preprocess_record_by_id(id)

    x = time.time() - t
    x = x/60
    print("Preprocessing time:", x, "min")

    if db.con.is_connected():
        db.con.close()
        print("MySQL connection is closed")

if __name__ ==  '__main__':
    
    #correct_languages()
    preprocessing()

    # from nltk.tokenize import word_tokenize
    # from snowballstemmer import stemmer
    # ar_stemmer = stemmer("arabic")
    # from qalsadi import lemmatizer
    # ar_lemmer = lemmatizer.Lemmatizer()
    # db = databaseHandler()
    # r = db.select_from_db_by_id(10014)
    # sentence = r.get('body')
    # # synt = preprocess.get_syntactically_preprocessed_arabic_paragraph(body) 
    # # sem = preprocess.get_semantically_preprocessed_arabic_paragraph(body)
    # sentence = sentence.replace("/","").replace("|", "").replace("\\","").replace('"',"").replace("''","").replace("`","").replace("-", " ").replace("–", " ").replace("؟", ".").replace(".....", ".").replace("....", ".").replace("...", ".").replace("..", ".")
    
    # sentence = ''.join([i for i in sentence if not i.isdigit()])
    # import string
    # stopset = list(string.punctuation)
    # sentence = " ".join([i for i in word_tokenize(sentence) if i not in stopset])

    # eng_letters = list(string.ascii_letters) + ['é', 'è', 'ê', 'à', 'ù', 'î' , 'ô', 'û', 'ç']
    # for letter in eng_letters:
    #     if sentence.__contains__(letter):
    #         sentence = sentence.replace(letter, "")


    # for word in word_tokenize(sentence):
    #     lemma = ar_lemmer.lemmatize(word, preprocess.get_wordnet_pos(word))
    #     print(lemma)
    #     print(lemma[1])
    # #print(body)
    # db.con.close()
