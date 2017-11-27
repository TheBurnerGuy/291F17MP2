from bsddb3 import db

def phase3():
	terms_db = db.DB()
	years_db = db.DB()
	recs_db = db.DB()
	terms_db.open("terms.idx",None, db.DB_BTREE, DB_CREATE)
	years_db.open("years.idx",None, db.DB_BTREE, DB_CREATE)
	recs_db.open("recs.idx",None, db.DB_HASH, DB_CREATE)
	curs = database.cursor()
	global format
	format = 0

	while(True):
		
		inp = input("Enter a query or 'exit' to exit the program: ")
		if inp == 'exit':
			break
		
		results = parseAndSearch(inp, terms_db, years_db)
		recs = getRecs(results, recs_db)
		displayResults(recs)
		
	
def parseAndSearch(query, terms_db, years_db):
	results = []
	finalresults = []
	for i in query.split():
		if len(i) >= 4 and i[:4] == 'year':
			results.append(searchYears(i[5:], years_db))
		else:
			results.append(searchTerms(i, terms_db))
				
	if len(query.split()) > 1:
		# Keep only the ids that occur in each result set
		# Go through each result in the first result set and check if it is in all the others
		# If it is then add it to the final result set
		finalResultsTemp = []
		for result in results[0]:
			foundAll = True
			for resultSet in results[1:]:
				found = False
				for rslt in resultSet:
					if result[1] == rslt[1]:
						found = True
						break
				if not found:
					foundAll = False
					break
			if foundAll:
				finalResultsTemp.append(result)
		# Remove duplicate recs
		for index1 in range(len(finalResultsTemp)):
			if finalResultsTemp[0][index1] not in finalResults:
				finalResults.append(results[0][index1])
			#foundDuplicate = False
			#for index2 in range(index1+1, len(finalResultsTemp)):
				#if finalResultsTemp[index1][1] == finalResultsTemp[index2][1]:
					#foundDuplicate = True
			#if not foundDuplicate:
				#finalResults.append(finalResultsTemp[index1])
	else:
		# Remove duplicate recs
		for index1 in range(len(results[0])):
			if results[0][index1] not in finalResults:
				finalResults.append(results[0][index1])
			#foundDuplicate = False
			#for index2 in range(index1+1, len(results[0])):
				#if results[0][index1][1] == results[0][index2][1]:
				   #foundDuplicate = True
			#if not foundDuplicate:
				#finalResults.append(results[0][index1])
	return finalResults

				
def searchTerms(query, terms_db):
	keys = []
	results = []
	curs = terms_db.cursor()

	# Create the keys
	if len(query) >= 6 and query[:6] == 'title:':
		if query[6] == '"':
			temp = query[7:(len(query)-1)].split()
			for word in temp:
				keys.append('t-' + word.lower())
		else:	
			keys.append('t-' + query[6:].lower())
	elif len(query) >= 7 and query[:7] == 'author:':
		keys.append('a-' + query[7:].lower())
	elif len(query) >= 6 and query[:6] == 'other:':
		keys.append('o-' + query[6:].lower())
	elif len(query) >= 7 and query[:7] == 'output=':
		if query[7:] == 'full':
			format = 1
	else:
		keys.append('t-' + query.lower())
		keys.append('a-' + query.lower())
		keys.append('o-' + query.lower())
		
	# Double check for fomatting

	for key in keys:
		key = key.encode('ascii','ignore')
		result = curs.get(key)
		# Add all the duplicates aswell
		while result:
			results.append(result)
			result = curs.next_dup()

	curs.close()
	return results

def searchYears(query, years_db):
	results = []
	curs = years_db.cursor()
	
	key = query.encode('ascii', 'ignore')
	result = curs.get(key)
	
	if query[0] == ':':
		#Get all duplicates
		while result:
			results.append(result)
			result = curs.next_dup()
	elif query[0] == '>':
		#Get all duplicates
		while result:
			results.append(result)
			result = curs.next_dup()
			
		#Go forward until reach the end of the file
		result = curs.next()
		while result:
			results.append(result)
			result = curs.next()
	elif query[0] == '<':
		#Get all duplicates
		while result:
			results.append(result)
			result = curs.next_dup()
			#Go forward until reach the end of the file
		result = curs.prev()
		while result:
			results.append(result)
			result = curs.prev()		
	return results

def getRecs(results, recs_db):
	recs = []
	curs = recs_db.cursor()
	for result in results:
		re = curs.get(result[1])
		if re:
			recs.append(re)
	curs.close()
	return recs

def displayResults(recs):

	for result in recs:
		words = result[1].decode('utf-8').split()
		
		for i in range (len(words)):
			if words[i] == ':':
				key = words[:i]
		

		if format == 0:  # Full output
			print key
		else:
			print words
			



					

				
				
		
		
		
		
'''
Format

article key
author
title
pages
year
journal

journals/acta/Saxena96:<article key="journals/acta/Saxena96"><author>Sanjeev Saxena</author><title>Parallel Integer Sorting and Simulation Amongst CRCW Models.</title><pages>607-619</pages><year>1996</year><journal>Acta Inf.</journal></article>

inproceedings key
author
title
pages
year
booktitle

journals/lncs/Comon94:<inproceedings key="journals/lncs/Comon94"><author>Hubert Comon</author><title>Constraints in Term Algebras: An Overview of Constraint Solving Techniques</title><pages>62-67</pages><booktitle>Constraint Programming</booktitle><year>1994</year></inproceedings>
'''
		
'''
REFERENCE CODE

def displayResults(results):
	for result in results:
		words = result[1].decode('utf-8').split()
		id = words[1][4:-5]
		date = words[2][12:-13]

		# Find the beginning and end of the tweet text
		# Get rid of the <text> tag
		words[3] = words[3][6:]
		index_text = 3
		for word in words[3:]:
			if len(word) >= 7 and word[-7:] == '</text>':
				# Get rid of the </text> tag
				words[index_text] = words[index_text][:-7]
				break
			index_text = index_text + 1
		text = " ".join(words[3:index_text+1])

		# Get the retweet count
		retweet_count = words[index_text+1][15:-16]

		# Find the beginning and end of the tweet name
		index_name_start = 0
		index_name_end = 0
		index = index_text + 2
		for word in words[index:]:
			if len(word) >= 6 and word[:6] == '<name>':
				index_name_start = index
				# Get rid of the <name> tag
				words[index] = words[index][6:]
			if len(word) >= 7 and word[-7:] == '</name>':
				index_name_end = index
				# Get rid of the </name> tag
				words[index] = words[index][:-7]
				break
			index = index + 1
		name = " ".join(words[index_name_start:index_name_end+1])

		# Find the beginning and end of the tweet location
		index_location_start = 0
		index_location_end = 0
		index = index_name_end + 1
		for word in words[index:]:
			if len(word) >= 10 and word[:10] == '<location>':
				index_location_start = index
				# Get rid of the <location> tag
				words[index] = words[index][10:]
			if len(word) >= 11 and word[-11:] == '</location>':
				index_location_end = index
				# Get rid of the </location> tag
				words[index] = words[index][:-11]
				break
			index = index + 1
		location = " ".join(words[index_location_start:index_location_end+1])

		# Find the beginning and end of the tweet description
		index_description_start = 0
		index_description_end = 0
		index = index_location_end + 1
		for word in words[index:]:
			if len(word) >= 13 and word[:13] == '<description>':
				index_description_start = index
				# Get rid of the <description> tag
				words[index] = words[index][13:]
			if len(word) >= 14 and word[-14:] == '</description>':
				index_description_end = index
				# Get rid of the </description> tag
				words[index] = words[index][:-14]
				break
			index = index + 1
		description = " ".join(words[index_description_start:index_description_end+1])

		# Find the beginning and end of the tweet url
		index_url_start = 0
		index_url_end = 0
		index = index_description_end + 1
		for word in words[index:]:
			if len(word) >= 5 and word[:5] == '<url>':
				index_url_start = index
				# Get rid of the <url> tag
				words[index] = words[index][5:]
			if len(word) >= 6 and word[-6:] == '</url>':
				index_url_end = index
				# Get rid of the </url> tag
				words[index] = words[index][:-6]
				break
			index = index + 1
		url = " ".join(words[index_url_start:index_url_end+1])

		print("##################################################################")
		print("id: ", id)
		print("date: ", date)
		print("text: ", text)
		print("retweet count: ", retweet_count)
		print("name: ", name)
		print("location: ", location)
		print("description: ", description)
		print("url: ", url)

'''



'''
T E M P L A T E 
C O D E

while(True):
    name = input("Enter a student Name to look up: ")
    if(name == "q"): #Termination Condition
        break
    
    result = curs.set(name.encode("utf-8")) 
    #In the presence of duplicate key values, result will be set on the first data item for the given key. 
   
    if(result != None):
        print("List of students with this name and their marks:")
        print("Name: " + str(result[0].decode("utf-8")) + ", Mark: " + str(result[1].decode("utf-8")))
        
        #iterating through duplicates:
        dup = curs.next_dup()
        while(dup != None):
            print("Name: " + str(dup[0].decode("utf-8")) + ", Mark: " + str(dup[1].decode("utf-8")))
            dup = curs.next_dup()
    else:
        print("No Entry Found.")
            
    ToBeAdded = input("Do you want to insert the input name into the database?(Enter y for yes) ")
    
    if(ToBeAdded == "y"):
        database.put(name.encode("utf-8"), input("Insert Mark: "))

curs.close()
database.close()

'''
<<<<<<< HEAD