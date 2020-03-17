'''
CF Parser 
Created By Rahat Hossain
Data : 18 March, 2020

Cautions:
CF does not allow api call more than five times in a second.
So you may use time.sleep(0.2) everytime you make a GET Request for safety :3
'''

import requests, json, time, csv

def parse():
	# gets input and calls further actions
	
	contestIds = []
	handles = []
	
	# takes contestIds from file : contestId.txt
	with open("contestIds.txt") as contestFile:
		contestIds = contestFile.read().split()

	# takes handles from file : handles.txt
	with open("handles.txt") as handleFile:
		handles = handleFile.read().split()

	# stores final data
	finalList = []

	# loops over all contests and handles
	for contestId in contestIds:
		for handle in handles:
			data = process(contestId, handle)
			finalList.append([contestId, handle, data[0], data[1]])
	
	writeCSV(finalList)
	print("Success: file located at Codeforces.csv")

def process(contestId, handle):
	# processes data for specific contestId and handle
	
	url = "https://codeforces.com/api/contest.status"
	params = {"contestId" : contestId, "handle" : handle} 

	# api call
	r = requests.get(url = url, params = params) 

	# sudhu data r data...
	wholeData = r.json()
	
	# check its status
	if(wholeData['status'] != 'OK'):
		raise Exception('Data not recieved for' + ' ' + handle + ' on contest : ' + contestId)
		return (0, 0)

	# retrieving actual data
	data = wholeData["result"]

	# holds data in respect of problems
	solutionDict = {}

	for submission in reversed(data):
		problemId = submission["problem"]["index"]
		participantType = submission["author"]["participantType"]
		verdict = submission["verdict"]
	
		if problemId not in solutionDict:
			if verdict == "OK" :
				if participantType == "CONTESTANT":
					solutionDict[problemId] = 1
				else :
					solutionDict[problemId] = 0.5
			else :
				solutionDict[problemId] = 0
		else :
			if solutionDict[problemId] == 0:
				if verdict == "OK" :
					if participantType == "CONTESTANT":
						solutionDict[problemId] = 1
					else :
						solutionDict[problemId] = 0.5

	downsolve, upsolve = 0, 0

	for key in solutionDict:
		if solutionDict[key] == 1:
			downsolve += 1
		elif solutionDict[key] == 0.5:
			upsolve += 1

	time.sleep(0.2)
	return (downsolve, upsolve)

def writeCSV(finalList):
	with open("Codeforces.csv", 'w') as file:
		writer = csv.writer(file)
		writer.writerows(finalList)

if __name__ == '__main__':
    parse()