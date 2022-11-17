from flask import Flask
from flask_restful import Api, Resource
import requests
from bs4 import BeautifulSoup


app = Flask(__name__)
api = Api(app)

class dvlaAPI(Resource):

    def post(self, regPlate):
        dvla_url = 'https://driver-vehicle-licensing.api.gov.uk/vehicle-enquiry/v1/vehicles'
        head = {'x-api-key':'U8eDaSElCE5V5doIvCQmP95TVOzNEXiM1pZ5jh47', 'Content-Type':'application/json'}
        body = {'registrationNumber': regPlate}

        x = requests.post(dvla_url, json = body, headers=head)

        return x.json()

class depthCheckAPI(Resource):
    
    def post(self, regPlate):

        data = {}

        def extract(regPlate):
            base_url = "https://www.rapidcarcheck.co.uk/results/?RegPlate="
            url = base_url + regPlate
            r = requests.get(url)
            if r.status_code != 200:
                r.raise_for_status()
            return r.text

        def parse(html):
            soup = BeautifulSoup(html, 'html.parser')
            selectSoup1 = soup.select('div.wpb_wrapper p')
            selectSoup2 = soup.select('strong')

            headers = ["Registration Plate", "Make", "Model", "Colour", "Vehicle Type", "Body Type", "Fuel", 
                    "Engine Capacity", "Horsepower", "Top Speed", "0-60mph Time", "Average Yearly Mileage",
                    "Insurance Group", "V5C Issue Date", "Vehicle Age", "Year of Manufacture", "NA1", "NA2",
                    "Mileage", "Salvage History", "Exported Vehicle", "NA3", "MOT Due", "MOT Due in",
                    "Previous MOT Records", "Last Mileage Record", "TAX Due", "Tax Due in", "Carbon Emissions", 
                    "Average Tax Cost (12 Months)", "Average Tax Cost (6 Months)", "NA4", "Total Mileage Records",
                    "Estimated Current Mileage", "Average Yearly Mileage", "Estimated Current Mileage", 
                    "Urban Fuel Economy", "Extra-Urban Fuel Economy", "Combined Fuel Economy", "Cost per mile", 
                    "Cost per 100 miles", "Cost per 12000 miles"]

            for x in range(2,5):
                #header = (((selectSoup1[x].text).split())[0])
                header = headers[x-2]######FIX#######################################
                key = (selectSoup2[x].text)
                data.update({header : key})
            
            for y in range(7,16):
                #header = (((selectSoup1[y].text).split())[0])
                header = headers[y-2]
                key = (selectSoup2[y].text)
                data.update({header : key})
            
            for y in range(18,44):
                #header = (((selectSoup1[y].text).split())[0])
                header = headers[y-2]
                key = (selectSoup2[y].text)
                data.update({header : key})
            
            return data

        extraction = extract(regPlate)
        result = parse(extraction)
        return result

class carImageURLs(Resource):
    def post(self, regPlate):

        def extract(regPlate):
            base_url = "https://www.rapidcarcheck.co.uk/results/?RegPlate="
            url = base_url + regPlate
            r = requests.get(url)
            if r.status_code != 200:
                r.raise_for_status()
            return r.text

        def getCarImageURL(html):
            soup = BeautifulSoup(html, 'html.parser')
            refinedSoup = soup.select("img.image1")
            refinedSoup1 = soup.select("img.image2")
            carImageOutput = (refinedSoup[0])['src']
            logoImageOutput = (refinedSoup1[0])['src']

            URLS = {"carImageURL":carImageOutput, "logoImageURL":logoImageOutput}
            return URLS

        extraction = extract(regPlate)
        URLS = getCarImageURL(extraction)

        return URLS

class mileageHistory(Resource):
    def post(self, regPlate):
        def extract(regPlate):
            base_url = "https://www.rapidcarcheck.co.uk/results/?RegPlate="
            url = base_url + regPlate
            r = requests.get(url)
            if r.status_code != 200:
                r.raise_for_status()
            return r.text
            
        html = extract(regPlate)
        soup = BeautifulSoup(html,'html.parser')
        refinedSoup1 = soup.select('table.responsive-table td')
        check1 = False
        check2 = False
        for x in refinedSoup1:
            if x['data-title'] == "Date":
                date = x.text
                check1 = True
            
            if x['data-title'] == "Mileage recorded (MOT)":
                mileage = x.text
                check2 = True
        
            if check1 == True & check2 == True:
                mileageHistory.update({date:mileage})
                check1 = False
                check2 = False
        return mileageHistory

api.add_resource(dvlaAPI, "/DVLA-API/<string:regPlate>")
api.add_resource(depthCheckAPI, "/depthCheckAPI/<string:regPlate>")
api.add_resource(carImageURLs, "/getImages/<string:regPlate>")
api.add_resource(mileageHistory, "/getMileageHistory/<string:regPlate>")
if __name__ == "__main__":
    app.run(debug=True)
