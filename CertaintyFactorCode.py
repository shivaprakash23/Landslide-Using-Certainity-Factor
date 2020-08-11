import arcpy
from arcpy.sa import *


def addingAttributes(ClassifiedGDB):
    arcpy.AddMessage("Inside addingAttributes function")
    arcpy.env.workspace = ClassifiedGDB
    ClassifiedDataList = arcpy.ListRasters()
    field1="ClassValStr"
    field2="ppa"
    field3="pps"
    field4="LandSlides"
    field5 ="CF"
    expression = "!Value!"
    arcpy.AddMessage("Going for loop in addingAttributes function")
    
    for raster in ClassifiedDataList:
        arcpy.AddMessage("{0} : Adding feilds".format(raster))
        arcpy.AddField_management(raster, field1, "TEXT")
        arcpy.AddField_management(raster, field4, "LONG")
        arcpy.AddField_management(raster, field2, "DOUBLE")
        arcpy.AddField_management(raster, field3, "DOUBLE")
        arcpy.AddField_management(raster, field5, "DOUBLE")
        arcpy.CalculateField_management(raster,field1,expression,"PYTHON")
        arcpy.AddMessage("{0} : Finished adding feilds".format(raster))
    
    
def zonalHistogramFunction(ClassifiedGDB,PointRasterLandslide):

    arcpy.AddMessage("Inside ZonalHistogram function")
    arcpy.AddMessage("{0}{1} values".format(ClassifiedGDB,PointRasterLandslide))
    arcpy.env.workspace = ClassifiedGDB
    RasterLandslide=PointRasterLandslide
    ClassifiedDataList = arcpy.ListRasters()
    arcpy.AddMessage("Going for loop in ZonalHistogramFunction")
    for raster in ClassifiedDataList:
        dbfname="ZonalHistogram"+raster
        ZonalHistogram(RasterLandslide,"Value",raster,ClassifiedGDB+"\\"+dbfname)
        arcpy.AddMessage("{0} zonal histogram for ".format(dbfname))
        arcpy.JoinField_management(raster,"ClassValStr", ClassifiedGDB+"\\"+dbfname, "LABEL", ["Value_1"])
        arcpy.AddMessage("{0} Join fields for ".format(raster))
        field= "LandSlides"
        expression = "!Value_1!"
        arcpy.CalculateField_management(raster,field,expression,"PYTHON")
        arcpy.AddMessage("{0} calculating field for".format(raster))
    


def ppa_pps_calculation(ClassifiedGDB,CFGDBPath,pps):
    arcpy.env.workspace = ClassifiedGDB
    ClassifiedDataList = arcpy.ListRasters()
    CFGDB=CFGDBPath
    field1="ppa"
    field2="pps"
    field3="LandSlides"
    field4="CF"
    expression1 = pps
    expression2 = "!LandSlides!/!Count!"
    expression3 = "PPS( !ppa! , !pps! )"
    lookupField="CF"
    codeblock = """def  PPS (ppa,pps):
        if (ppa >= pps):
            cf = (ppa-pps) / (ppa * (1 - pps))
            return cf
        else :
            cf = (ppa-pps) / (pps * (1 - ppa))
            return cf
    """
    for raster in ClassifiedDataList:
        arcpy.CalculateField_management(raster,field2,expression1,"PYTHON")
        arcpy.AddMessage("{0} 's CalculateField: pps".format(raster))
        arcpy.CalculateField_management(raster,field1,expression2,"PYTHON")
        arcpy.AddMessage("{0} 's CalculateField: ppa".format(raster))
        arcpy.CalculateField_management(raster,field4,expression3,"PYTHON",codeblock)
        arcpy.AddMessage("{0} 's ClaculateField: CF".format(raster))
        outRaster = Lookup(raster, lookupField)
        arcpy.AddMessage("{0} Lookup for ".format(raster))
        outRaster.save(CFGDB+"\\"+raster)


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
    XCF = Raster(CFList[0])
    YCF = Raster(CFList[1])
    arcpy.AddMessage("Going for Loop in CFAggregation function")
    while(i < total):
        ModXCF = Con(XCF < 0,(XCF * -1),XCF)
        ModYCF = Con(YCF < 0,(YCF * -1),YCF)
        MinOfMod = Con(ModXCF<ModYCF,ModXCF,ModYCF)
        Z1= XCF+YCF - (YCF * XCF)
        Z2=(XCF+YCF)/(1-MinOfMod)
        Z3= XCF+YCF + (YCF * XCF)
        ZCF= Con((XCF>= 0)&(YCF>=0),Z1,Con((XCF*YCF < 0),Z2,Z3))
        XCF=ZCF
        YCF=Raster(CFList[i])
        i=i+1

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

    pps= 0.0
    CFGBD="CF.gdb"
    ResultGBD="Result.gdb"

    try:
        
        ClassifiedGDB=arcpy.GetParameterAsText(0)
        PointRasterLandslide = arcpy.GetParameterAsText(1)
        pps= float(arcpy.GetParameterAsText(2))
        ResultFolder= arcpy.GetParameterAsText(3)
        
    except Exception as e:
        arcpy.AddError(e.args[0])
    
    try:
        
        arcpy.CreateFileGDB_management(ResultFolder,CFGBD)
    except Exception as e:
        arcpy.AddError(e.args[0])

    try:
        arcpy.CreateFileGDB_management(ResultFolder,ResultGBD)
        
    except Exception as e:
        arcpy.AddError(e.args[0])

    CFGDBPath= ResultFolder+"\\"+CFGBD
    ResultGBDPath = ResultFolder+"\\"+ResultGBD
    try:
        addingAttributes(ClassifiedGDB)
    except Exception as e:
        arcpy.AddError(e.args[0])
    try:
        zonalHistogramFunction(ClassifiedGDB,PointRasterLandslide)
    except Exception as e:
        arcpy.AddError(e.args[0])
    try :
        ppa_pps_calculation(ClassifiedGDB,CFGDBPath,pps)
    except Exception as e:
        arcpy.AddError(e.args[0])
    try:
        CFAggregation(CFGDBPath,ResultGBDPath)
    except Exception as e:
        arcpy.AddError(e.args[0])
        
    
    
    
    

    
