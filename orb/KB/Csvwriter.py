import csv


'''
Small class to create csv files for KB population
'''

class Csvwriter():


    def main():
        print("Populate the csv file for KB usage")

        name = input("input station \n")
        while name !="quit":
            name = input("input station \n")
            row = [name]

            with open('eastangliastations.csv', 'a', newline='') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow(row)

            csvFile.close()



if __name__== "__main__":
  Csvwriter.main()