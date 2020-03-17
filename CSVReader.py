import csv 

def CSVReader(filename):
	with open(filename) as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		
		print("Contest_id\tHandle\tSolve\tUpsolve");

		for row in csv_reader:
			string = "{0}\t{1}\t{2}\t{3}".format(row[0], row[1], row[2], row[3])
			'''
			row[0] = contestId
			row[1] = handle
			row[2] = Solve on contest time
			row[3] = upsolve
			'''
			print(string)

if __name__ == '__main__':
    CSVReader("Codeforces.csv")