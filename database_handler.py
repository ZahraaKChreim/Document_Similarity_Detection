import mysql.connector

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
            select_query = """  SELECT *
                                FROM data
                                WHERE data.query = '""" + query + """ '"""
            cursor.execute(select_query)

            select_result = cursor.fetchall()

            results = []
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

                result = {'id': id, 'lang': lang, 'domain': domain, 'query': query, 'url': url, 'website_title': website_title, 'page_title': page_title, 'subtitles': subtitles, 'urls': urls, 'body': body}
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

                result = {'id': id, 'lang': lang, 'domain': domain, 'query': query, 'url': url, 'website_title': website_title, 'page_title': page_title, 'subtitles': subtitles, 'urls': urls, 'body': body}
            
            return result

        except mysql.connector.Error as error:
            print("Failed to select url " + url + " from MySQL: {}".format(error))


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