from bsddb3 import db

def phase3():
	terms_db = db.DB()
	years_db = db.DB()
	recs_db = db.DB()
	terms_db.open("terms.idx",None, db.DB_BTREE, DB_CREATE)
	years_db.open("years.idx",None, db.DB_BTREE, DB_CREATE)
	recs_db.open("recs.idx",None, db.DB_HASH, DB_CREATE)
	curs = database.cursor()

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
			results.append(searchYears(i[4:], years_db))
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
			foundDuplicate = False
			for index2 in range(index1+1, len(finalResultsTemp)):
				if finalResultsTemp[index1][1] == finalResultsTemp[index2][1]:
				   foundDuplicate = True
			if not foundDuplicate:
			   finalResults.append(finalResultsTemp[index1])
	else:
		# Remove duplicate recs
		for index1 in range(len(results[0])):
			foundDuplicate = False
			for index2 in range(index1+1, len(results[0])):
				if results[0][index1][1] == results[0][index2][1]:
				   foundDuplicate = True
			if not foundDuplicate:
			   finalResults.append(results[0][index1])
	return finalResults

				
def searchTerms(query, terms_db):
	partialMatch = False
	keys = []
	results = []
	curs = terms_db.cursor()
	if query[-1] == '%':
		partialMatch = True

	# Create the keys
	if len(query) >= 6 and query[:6] == 'title:':
		keys.append('t-' + query[6:].lower())
	elif len(query) >= 7 and query[:7] == 'author:':
		keys.append('a-' + query[7:].lower())
	elif len(query) >= 6 and query[:6] == 'other:':
		keys.append('o-' + query[6:].lower())
	else:
		keys.append('t-' + query.lower())
		keys.append('a-' + query.lower())
		keys.append('o-' + query.lower())
		
	# Double check fot fomatting

	if partialMatch:
		for key in keys:
			skey = key[:-1]
			key = key[:-1].encode('ascii','ignore')
			result = curs.set_range(key)
			if result:
				resultKey = result[0].decode('utf-8')
				# Scan and add results until the prefix is no longer found
				while len(resultKey) >= len(skey) and resultKey[:len(key)] == skey:
					results.append(result)
					result = curs.next()
					resultKey = result[0].decode('utf-8')
	else:
		for key in keys:
			key = key.encode('ascii','ignore')
			result = curs.set(key)
			# Add all the duplicates aswell
			while result:
				results.append(result)
				result = curs.next_dup()

	curs.close()
	return results


def getRecs(results, recs_db):
	recs = []
	curs = recs_db.cursor()
	for result in results:
		re = curs.set(result[1])
		if re:
			recs.append(re)
	curs.close()
	return recs

def displayResults(recs)
	format = 0 # Default: key
# Prompt for full or key results
	if output == "output=full":
		format = 1 # Full





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
