from bsddb3 import db

format_global = 0

def phase3():
	terms_db = db.DB()
	years_db = db.DB()
	recs_db = db.DB()
	terms_db.open("terms.idx",None, db.DB_BTREE, db.DB_CREATE)
	years_db.open("years.idx",None, db.DB_BTREE, db.DB_CREATE)
	recs_db.open("recs.idx",None, db.DB_HASH, db.DB_CREATE)

	while(True):
		
		inp = input("Enter a query or 'exit' to exit the program: ")
		if inp == 'exit':
			break
		
		results = parseAndSearch(inp, terms_db, years_db, recs_db)
		displayResults(results, recs_db)
		
	
def parseAndSearch(query, terms_db, years_db, recs_db):
	results = []
	finalResults = []
	for i in query.split():
		if len(i) >= 4 and i[:4] == 'year':
			results.append(searchYears(i[4:], years_db))
		else:
			checkOutput = searchTerms(i, terms_db, recs_db)
			if checkOutput != []:
				results.append(searchTerms(i, terms_db, recs_db))
			
				
	if len(results) > 1:
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
		if len(results) > 0: # Checks if only the format_global was changed
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

				
def searchTerms(query, terms_db, recs_db):
	global format_global
	
	keys = []
	results = []
	curs = terms_db.cursor()

	# Create the keys
	if len(query) >= 6 and query[:6] == 'title:':
		if query[6] == '"':
			temp = query[7:(len(query)-1)].split()
			for word in temp:
				# The special case where ordering actually matters
				keystemp.append('t-' + word.lower())
				
			for key in keystemp:
				key = key.encode('ascii','ignore')
				#print(key)
				result = curs.get(key, db.DB_SET)
				# Add all the duplicates aswell
				while result:
					results.append(result)
					result = curs.next_dup()					
				
			# Parse recs.idx
			curs = recs_db.cursor()
			for result in results:
				curs.get(result, db.DB_SET)
				
			
			return results
			#END SPECIAL CASE
		else:	
			keys.append('t-' + query[6:].lower())
	elif len(query) >= 7 and query[:7] == 'author:':
		keys.append('a-' + query[7:].lower())
	elif len(query) >= 6 and query[:6] == 'other:':
		keys.append('o-' + query[6:].lower())
	elif len(query) >= 7 and query[:7] == 'output=':
		if query[7:] == 'full':
			format_global = 1
		elif query[7:] == 'key':
			format_global = 0
	else:
		keys.append('t-' + query.lower())
		keys.append('a-' + query.lower())
		keys.append('o-' + query.lower())
		
	# Double check for fomatting
	#print(keys)
	
	for key in keys:
		key = key.encode('ascii','ignore')
		#print(key)
		result = curs.get(key, db.DB_SET)
		# Add all the duplicates aswell
		while result:
			results.append(result)
			result = curs.next_dup()

	curs.close()
	return results

def searchYears(query, years_db):
	results = []
	curs = years_db.cursor()
	
	key = query[1:].encode('ascii', 'ignore')
	
	if query[0] == ':':
		result = curs.get(key, db.DB_SET)
		
		if result == None:
			return results		
		
		#Get all duplicates
		while result:
			results.append(result)
			result = curs.next_dup()
	elif query[0] == '>':
		result = curs.get(key, db.DB_SET_RANGE)
		
		if result == None:
			return results
		elif result[0] == key:
			result = curs.next()
		
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
		result = curs.get(key, db.DB_SET_RANGE)
		result = curs.prev()
		
		if result == None:
			return results		
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


def displayResults(results, recs_db):
	global format_global
	
	if format_global == 0:
		for result in results:
			print(result[1].decode('utf-8'))
			
		return
	
	# Full Output
	
	recs = []
	curs = recs_db.cursor()
	for result in results:
		
		re = curs.get(result[1], db.DB_SET)
		if re:
			recs.append(re)
	curs.close()	
	
	
	for result in recs:
		words = result[1].decode('utf-8')
		print(words)
	
	
	return

if __name__ == "__main__":
	phase3()