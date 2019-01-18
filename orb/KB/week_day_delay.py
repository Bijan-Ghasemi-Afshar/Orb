import csv
'''
This class creates an object for predicting the delay related to a weekday
'''
class weekdayDelay():
    def __init__(self, day):
        self.day = day

    def get_weekday_delay(self):
        delay_data = []

        with open('graphing_data.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:                
                if row[7] == '0' and self.day == 'monday':                    
                    delay_data.append(row)
                elif row[7] == '1' and self.day == 'tuesday':
                    delay_data.append(row)
                elif row[7] == '2' and self.day == 'wednesday':
                    delay_data.append(row)
                elif row[7] == '3' and self.day == 'thursday':
                    delay_data.append(row)
                elif row[7] == '4' and self.day == 'friday':
                    delay_data.append(row)
                else:
                    pass

        total = 0
        for element in delay_data:            
            try:
                int(element[8])
            except:
                continue
            total += int(element[8])

        return total/len(delay_data)


if __name__=='__main__':
    weekday_delay = weekdayDelay("monday")
    print(weekday_delay.get_weekday_delay())
    weekday_delay = weekdayDelay("tuesday")
    print(weekday_delay.get_weekday_delay())
    weekday_delay = weekdayDelay("wednesday")
    print(weekday_delay.get_weekday_delay())
    weekday_delay = weekdayDelay("thursday")
    print(weekday_delay.get_weekday_delay())
    weekday_delay = weekdayDelay("friday")
    print(weekday_delay.get_weekday_delay())