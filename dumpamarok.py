import sys
import MySQLdb
from songparser import BaseSong, BaseLibraryParser


def main(argv):
	server =argv[1]
	database = argv[2]
	username = argv[3]
	pwd = argv[4]
	
	print "Reading database from " + username + "@" + server + "/" + database
	parser = AmarokLibraryParser( server,  database,  username,  pwd );
        allSongs = parser.getSongs()
        for song in allSongs:
                print song.artist + " - " + song.album + " - " + song.title + " - " + str(song.size)


class AmarokSong(BaseSong):
	def __init__(self, row):
		self.id = row[0]
		self.artist =row[1]
		self.album = row[2]
		self.title = row[3]
		self.size = row[4]
		self.filePath = row[5]
	
	def setRating( self, rating ):
		print "not implemented"

	def setPlaycount( self, playcount ):
		print "not implemented"

class AmarokLibraryParser( BaseLibraryParser ):
	def __init__(self, server,  database,  username,  pwd):
		
		self.db = MySQLdb.connect( host=server, db=database, user=username, passwd=pwd)
	
	def getSongs(self):
		cursor = self.db.cursor()
		query = cursor.execute( "select tracks.id, artists.name, tracks.title, albums.name, tracks.filesize, urls.rpath from tracks " +
		                       "inner join artists on artists.id = tracks.artist " + 
							  "inner join albums on albums.id = tracks.album " +
							 "inner join urls on urls.id = tracks.url " )
		
		results = cursor.fetchall()
		
		allSongs = []
		for row in results:
				amarokSong = AmarokSong(row)
				allSongs.append( amarokSong )
		
		return allSongs
		
if __name__ == "__main__":
        main(sys.argv)

