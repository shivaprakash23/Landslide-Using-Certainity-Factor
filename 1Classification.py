import arcpy
from arcpy.sa import *

def DemClassification(DemR,outGDB):
    ClassifiedDEM =""
    ClassifiedDEM= Con((DemR > 500)  &  (DemR  <= 1000),1,
    Con((DemR > 1000)  &  (DemR  <= 2000),2,
    Con((DemR > 2000)  &  (DemR  <= 3000),3,
    Con((DemR > 3000)  &  (DemR  <= 4000),4,
    Con((DemR > 4000)  &  (DemR  <= 5000),5,
    Con((DemR > 5000)  &  (DemR  <= 6000),6,
    Con((DemR > 6000)  &  (DemR  <= 7000),7,
    0)))))))
    fileName= outGDB+"\\"+"Dem"
    ClassifiedDEM.save(fileName)

def SlopeClassification(Slope,outGDB):
    ClassifiedSlope =""
    ClassifiedSlope = Con((Slope > 0)  &  (Slope  <= 7),1,
    Con((Slope > 7)  &  (Slope  <= 14),2,
    Con((Slope > 14)  &  (Slope  <= 21),3,
    Con((Slope > 21)  &  (Slope  <= 28),4,
    Con((Slope > 28)  &  (Slope  <= 38),5,
    Con((Slope > 38)  &  (Slope  <= 50),6,
    Con((Slope > 50)  &  (Slope  <= 60),7,
    8)))))))
    fileName= outGDB+"\\"+"Slope"
    ClassifiedSlope.save(fileName)

def AspectClassification(aspect,outGDB):
    ClassifiedAspect=""
    ClassifiedAspect = Con((aspect >= 0)  &  (aspect  <= 22.5) & (aspect > 337.5)  &  (aspect  <= 360),1,
    Con((aspect > 22.5)  &  (aspect  <= 67.5),2,
    Con((aspect > 67.5)  &  (aspect  <= 112.5),3,
    Con((aspect > 112.5)  &  (aspect  <= 157.5),4,
    Con((aspect > 157.5)  &  (aspect  <= 202.5),5,
    Con((aspect > 202.5)  &  (aspect  <= 247.5),6,
    Con((aspect > 247.5)  &  (aspect  <= 292.5),7,
    Con((aspect > 292.5)  &  (aspect  <= 337.5),8,
    -1))))))))
    fileName= outGDB+"\\"+"Aspect"
    ClassifiedAspect.save(fileName)

def DistanceFromRiver(DistanceFromRivers,outGDB):
    ClassifiedDistanceFromRivers = ""
    ClassifiedDistanceFromRivers= Con((DistanceFromRivers> 0)  &  (DistanceFromRivers <= 100),1,
    Con((DistanceFromRivers> 100)  &  (DistanceFromRivers <= 200 ),2,
    Con((DistanceFromRivers> 200)  &  (DistanceFromRivers <= 300),3,
    Con((DistanceFromRivers> 300)  &  (DistanceFromRivers <= 400),4,
    Con((DistanceFromRivers> 400)  &  (DistanceFromRivers <= 500),5,
    Con((DistanceFromRivers> 500)  &  (DistanceFromRivers <= 1000),6,
    Con((DistanceFromRivers> 1000)  &  (DistanceFromRivers <= 2000),7,
    8)))))))
    fileName= outGDB+"\\"+"RiverDist"
    ClassifiedDistanceFromRivers.save(fileName)

def RainClassification(RainAverageInMM,outGDB):
    ClassifiedRainAverageInMM=""

    ClassifiedRainAverageInMM= Con((RainAverageInMM<= 150),1,
    Con((RainAverageInMM> 150)  &  (RainAverageInMM <= 160),2,
    Con((RainAverageInMM> 160)  &  (RainAverageInMM <= 170),3,
    Con((RainAverageInMM> 170)  &  (RainAverageInMM <= 180),4,
    5))))
    fileName= outGDB+"\\"+"Rain"
    ClassifiedRainAverageInMM.save(fileName)

def STIClassification(STI,outGDB):
    ClassifiedSTI=""
    ClassifiedSTI= Con((STI<= 3),1,
    Con((STI> 3)  &  (STI <= 9 ),2,
    Con((STI> 9)  &  (STI <= 15),3,
    Con((STI> 15),4,
    5))))
    fileName= outGDB+"\\"+"STI"
    ClassifiedSTI.save(fileName)

def SPIClassification(SPI,outGDB):
    ClassifiedSPI =""
    ClassifiedSPI= Con((SPI<= 5),1,
    Con((SPI> 5)  &  (SPI <= 10 ),2,
    Con((SPI> 10)  &  (SPI <= 40),3,
    Con((SPI> 40),4,
    5))))
    fileName= outGDB+"\\"+"SPI"
    ClassifiedSPI.save(fileName)


def GeneralCurvatureClassification(GeneralCurve,outGDB):
    ClassifiedGeneralCurvature = ""
    ClassifiedGeneralCurvature = Con((GeneralCurve >= -0.05),1,
    Con((GeneralCurve > -0.05)  &  (GeneralCurve  <= 0.05),2,
    Con((GeneralCurve > 0.05),3,
    4)))
    fileName= outGDB+"\\"+"GenCurve"
    ClassifiedGeneralCurvature.save(fileName)

def PlanCurvatureClassification(PlanCurve,outGDB):
    ClassifiedPlanCurvature = ""
    ClassifiedPlanCurvature = Con((PlanCurve >= -0.05) ,1,
    Con((PlanCurve > -0.05)  &  (PlanCurve  <= 0.05),2,
    Con((PlanCurve > 0.05),3,
    4)))
    fileName= outGDB+"\\"+"PlanCurve"
    ClassifiedPlanCurvature.save(fileName)

def ProfileCurvatureClassification(ProfileCurve,outGDB):
    ClassifiedProfileCurvature =""
    ClassifiedProfileCurvature = Con((ProfileCurve >= -0.05) ,1,
    Con((ProfileCurve > -0.05)  &  (ProfileCurve  <= 0.05),2,
    Con((ProfileCurve > 0.05),3,
    4)))
    fileName= outGDB+"\\"+"ProfileCurve"
    ClassifiedProfileCurvature.save(fileName)




if __name__== "__main__":
    
    inputRaster = arcpy.GetParameterAsText(0)
    outGDB=arcpy.GetParameterAsText(1)
    parameter= arcpy.GetParameterAsText(2)
    inputR= Raster(inputRaster)
    if (parameter == "Dem"):
        DemClassification(inputR,outGDB)
    elif (parameter == "Slope"):
        SlopeClassification(inputR,outGDB)
    elif (parameter == "Aspect"):
        AspectClassification(inputR,outGDB)
    elif (parameter == "DistanceFromRivers"):
        DistanceFromRiver(inputR,outGDB)
    elif (parameter == "AverageRain"):
        RainClassification(inputR,outGDB)
    elif (parameter == "STI"):
        STIClassification(inputR,outGDB)
    elif (parameter == "SPI"):
        SPIClassification(inputR,outGDB)
    elif (parameter == "GeneralCurvature"):
        GeneralCurvatureClassification(inputR,outGDB)
    elif (parameter == "PlanCurvature"):
        PlanCurvatureClassification(inputR,outGDB)
    elif (parameter == "ProfileCurvature"):
        ProfileCurvatureClassification(inputR,outGDB)
    else:
        print("Unknown Selection")
