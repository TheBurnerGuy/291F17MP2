#Phase 2
#Runs on python2
#Remember to use these commands after running phase 1
#Taken from https://www.computerhope.com/unix/usort.htm
'''
sort -u -o terms.txt terms.txt
sort -u -o years.txt years.txt
sort -u -o recs.txt recs.txt
'''

#Now make the textfile into files that can easily be read into berkeleyDB
terms = open("terms.txt", 'r')
years = open("years.txt", 'r')
recs = open("recs.txt", 'r')

#New textfiles
terms_new = open("terms_new.txt", 'w')
years_new = open("years_new.txt", 'w')
recs_new = open("recs_new.txt", 'w')

line = "example"

for file_o, file_n in [(terms, terms_new), (years, years_new), (recs, recs_new)]:
    while(line != "" or line != "\n"): #Keep looping until EOD found
        line = file_o.readline()
        if(line == "" or line == "\n"):
            #End of file has been reached
            file_o.close()
            file_n.close()
            break
        
        #Find colon then split line into two lines
        line = line.split(':', 1)
        file_n.write(line[0] + "\n" + line[1])

#In command line, use the following commands after phase2:
'''
db_load -f terms_new.txt -t btree -T terms.idx
db_load -f years_new.txt -t btree -T years.idx
db_load -f recs_new.txt -t hash -T recs.idx
'''
