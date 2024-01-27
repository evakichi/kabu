import requests
class BrandData:

    Date = ""
    Code = 0
    CompanyName =""
    CompanyNameEnglish = ""
    Sector17Code = ""
    Sector17CodeName = ""
    Sector33Code = ""
    Sector33CodeName = ""
    ScaleCategory = ""
    MarketCode = ""
    MarketCodeName =""

    def __init__(self,data) -> None:
        self.Date = data['Date']
        self.Code = data['Code']
        self.CompanyName = data['CompanyName']
        self.CompanyNameEnglish = data['CompanyNameEnglish']
        self.Sector17Code = data['Sector17Code']
        self.Sector17CodeName = data['Sector17CodeName']
        self.Sector33Code = data['Sector33Code']
        self.Sector33CodeName = data['Sector33CodeName']
        self.ScaleCategory = data['ScaleCategory']
        self.MarketCode = data['MarketCode']
        self.MarketCodeName = data['MarketCodeName']
        pass

    def getBrandInfo(idToken):
        headers = {'Authorization': 'Bearer {}'.format(idToken)}
        information_get = requests.get(f"https://api.jquants.com/v1/listed/info", headers=headers)
        information_json = information_get.json()
        return information_json['info']    

    def print(self):
        print(f'{self.getDate()}:{self.getCode()}:{self.getCompanyName()}({self.getCompanyNameEnglish()}):',end="")
        print(f'{self.getSector17CodeName()}({self.getSector17Code()}):{self.getSector33CodeName()}({self.getSector33Code()}):',end="")
        print(f'{self.getScaleCategory()}:{self.getMarketCodeName()}({self.getMarketCode()}):')


    def getDate(self):
        return self.Date
    
    def getCode(self):
        return self.Code
    
    def getCompanyName(self):
        return self.CompanyName

    def getCompanyNameEnglish(self):
        return self.CompanyNameEnglish
    
    def getSector17Code(self):
        return self.Sector17Code
    
    def getSector17CodeName(self):
        return self.Sector17CodeName

    def getSector33Code(self):
        return self.Sector33Code

    def getSector33CodeName(self):
        return self.Sector33CodeName

    def getScaleCategory(self):
        return self.ScaleCategory
    
    def getMarketCode(self):
        return self.MarketCode

    def getMarketCodeName(self):
        return self.MarketCodeName

