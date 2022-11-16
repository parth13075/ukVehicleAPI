import requests

def vehicleLookup(numberPlate):
    url = 'https://driver-vehicle-licensing.api.gov.uk/vehicle-enquiry/v1/vehicles'
    head = {'x-api-key':'U8eDaSElCE5V5doIvCQmP95TVOzNEXiM1pZ5jh47', 'Content-Type':'application/json'}
    body = {'registrationNumber': numberPlate}
    try:
        x = requests.post(url, json = body, headers=head)
        parsed = x.text.split(',')
        for parameter in parsed:
            print(parameter)
    except:
        return None

vehicleLookup("GN14ZVO")