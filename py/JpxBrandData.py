
class JpxBrandData:

    def __init__(self,brandData,jpxDataList) -> None:
        self.brandData=brandData
        self.jpxDataList=jpxDataList
    
    def getBrandCode(self):
        return self.brandData.getCode()
    
    def getJpxDataList(self):
        return self.jpxDataList