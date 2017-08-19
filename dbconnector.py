import mysql.connector


class DBConnector(object):
    def __init__(self, configurator):
        self._configurator = configurator
        self._add_row = "INSERT INTO review (idreview, raiting, comment, title, updated, author) VALUES (%(id)s, %(rait)s, %(comm)s, %(tit)s, %(upd)s, %(auth)s)"
        self._cnx = mysql.connector.connect(user='root', password='1234', host='127.0.0.1', database='applecomments')

    def insertReview(self, id, raiting, comment, title, updated, author):
        result = True
        try:
            cursor = self._cnx.cursor()
            review = {
                'id': id,
                'rait': raiting,
                'comm': comment,
                'tit': title,
                'upd': updated,
                'auth': author
            }
            cursor.execute(self._add_row, review)
            self._cnx.commit()

        except Exception, e:
            print str(e)
            #print "Baza vec ima najnovije podatke"
            #if e.errno == 1062:
                #result = False

        return result
