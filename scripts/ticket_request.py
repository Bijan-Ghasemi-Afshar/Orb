import requests, re, json
from bs4 import BeautifulSoup

# National rails_______________________________________________________________________
# url = 'http://ojp.nationalrail.co.uk/service/timesandfares/NRW/LST/140119/0015/dep'
url = 'http://ojp.nationalrail.co.uk/service/timesandfares/norwich/LST/140219/1212/dep/170219/1212/dep'

# GET data_________________________________________
r = requests.get(url)

# Create soup object_______________________________________________
soup = BeautifulSoup(r.text, 'html.parser')


# print("_____Ticket prices_____")
# matches = soup.findAll("label", class_="opreturn")
# ticket_prices = []
# for match in matches:
#     ticket_price = ''.join(match.findAll(text=True))
#     ticket_prices.append(re.sub('[^0-9]+', '', ticket_price))

# for price in ticket_prices:
#     print(price)


# print("_____Departure times_____")

# matches = soup.findAll("td", class_="dep")
# departure_times = []
# for match in matches:
#     departure_time = ''.join(match.findAll(text=True))
#     departure_times.append(re.sub('[^0-9]+', ':', departure_time))

# for dep_time in departure_times:
#     print(dep_time)


# print("_____Arrival times_____")

# matches = soup.findAll("td", class_="arr")
# departure_times = []
# for match in matches:
#     departure_time = ''.join(match.findAll(text=True))
#     departure_times.append(re.sub('[^0-9]+', ':', departure_time))

# for dep_time in departure_times:
#     print(dep_time)


# ________________________________Return Ticket___________________________________

print("_____outbound departure times_____")
outbound_tickets = soup.find("table", {"id": "oft"})
matches = outbound_tickets.findAll("td", class_="has-cheapest")[0]
some_data = matches.find('script')
some_data = ''.join(some_data.findAll(text=True))
some_data = re.sub('%s', '', some_data)
some_data = json.loads(some_data)
print(some_data['singleJsonFareBreakdowns'][0]['fullFarePrice'])
print(some_data['jsonJourneyBreakdown']['departureTime'])
print(some_data['jsonJourneyBreakdown']['arrivalTime'])


print("_____return departure times_____")
outbound_tickets = soup.find("table", {"id": "ift"})
matches = outbound_tickets.findAll("td", class_="has-cheapest")[0]
some_data = matches.find('script')
some_data = ''.join(some_data.findAll(text=True))
some_data = re.sub('%s', '', some_data)
some_data = json.loads(some_data)
print(some_data['singleJsonFareBreakdowns'][0]['fullFarePrice'])
print(some_data['jsonJourneyBreakdown']['departureTime'])
print(some_data['jsonJourneyBreakdown']['arrivalTime'])



# Print the results_________________________________________
# print(soup.prettify())
