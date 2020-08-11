import arcpy
from arcpy.sa import *

def CFAggregation(CFGDBPath,ResultGBDPath):

    arcpy.env.workspace = CFGDBPath
    CFList = arcpy.ListRasters()
    ZCF=""
    i=2
    ModXCF =""
    ModYCF =""
    MinOfMod=""
    Z1=""
    Z2=""
    Z3=""
    total= len(CFList)
    arcpy.AddMessage(total)
    XCF = Raster(CFList[0])
    YCF = Raster(CFList[1])
    arcpy.AddMessage("Going for Loop in CFAggregation function")
    
    while(i < total):
        arcpy.AddMessage("inside loop")
        ModXCF = Con(XCF < 0,(XCF * -1),XCF)
        ModYCF = Con(YCF < 0,(YCF * -1),YCF)
        arcpy.AddMessage("mod done")
        MinOfMod = Con(ModXCF<ModYCF,ModXCF,ModYCF)
        arcpy.AddMessage("min of mod done")
        Z1= XCF+YCF - (YCF * XCF)
        Z2=(XCF+YCF)/(1-MinOfMod)
        Z3= XCF+YCF + (YCF * XCF)
        ZCF= Con((XCF>= 0)&(YCF>=0),Z1,Con((XCF*YCF < 0),Z2,Z3))
        ZCF.save(ResultGBDPath+"\\"+"CF"+str(i))
        arcpy.AddMessage("CF agree done")
        XCF=ZCF
        arcpy.AddMessage(i)
        YCF=Raster(CFList[i])
        arcpy.AddMessage(i)
        arcpy.AddMessage("XCF  YCF")
        i=i+1
        arcpy.AddMessage(i)

    arcpy.AddMessage("out of while loop")
    ZCF.save(ResultGBDPath+"\\"+"CF")
    arcpy.AddMessage("CF Image classification")
    ClassifiedCF= Con((ZCF >=-1)  &  (ZCF  < -0.5),1,
    Con((ZCF >= -0.5)  &  (ZCF  <-0.05),2,
    Con((ZCF >= -0.05)  &  (ZCF  <0.05),3,
    Con((ZCF >= 0.05)  &  (ZCF  <0.5),4,
    Con((ZCF >= 0.5)  &  (ZCF  <= 1),5,
    0)))))
    

    ClassifiedCF.save(ResultGBDPath+"\\"+"ClassifiedCF")
    arcpy.AddMessage("{0} saved classifeid CF Image".format(ResultGBDPath))

if __name__== "__main__":


    CFGDBPath=arcpy.GetParameterAsText(0)
    ResultGBDPath = arcpy.GetParameterAsText(1)

    try:
        CFAggregation(CFGDBPath,ResultGBDPath)
    except Exception as e:
        arcpy.AddError(e.args[0])
        
    
    
    
    

    
