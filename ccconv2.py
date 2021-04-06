#----------------------------------------------------------------------------------#
# Church Calendar Converter (Anglican Church in North America)
# (C) David Marten, 2019
#----------------------------------------------------------------------------------#
# Basic format inspired by:
# Catholic DateUtils
# https://github.com/MRNL-/LiturgicalCalendarUtils
# (C) Martin Raynal, 2015-2016
#----------------------------------------------------------------------------------#
# The Calendar part of this module is inspired by and based on ROMCAL 6.2
# ROMCAL is Copyright (C) 1993-2003 Kenneth G. Bath (kbath@harris.com)
# See http://www.romcal.net/ for additional credits and informations
#----------------------------------------------------------------------------------#

import calendar, csv
from dateutil.easter import *
from datetime import date, timedelta

#=====================================
# NOTE Set Church Calendar Var
#=====================================

class churchCalendar:
    def __init__(self, datein):
        # Year
        try:
            self.year = ConvertYear(datein)
        except:
            print("Error: Could not determine year.")
        
        # Season
        try:
            self.churchseason = ConvertSeason(datein)
        except:
            print("Error: Could not determine season.")

        # Week
        try:
            self.churchweek = ConvertWeek(datein)
        except:
            print("Error: Could not determine week.")
        
        # Weekday
        self.day = calendar.day_name[datein.weekday()]
        
        # Holy Days
        try:
            self.holyday = HolyDays(datein)
        except:
            print("Error: Could not determine holy days")

#=====================================
# Library of Conversion Functions
#=====================================

#======== Special Dates ====================

def EndOfYear(year):
    return date(year, 12, 31)

def StartOfYear(year):
    return date(year, 1, 1)

def YearChangeConfusion(year):
    return date(year, 12, 1)

#======== Seasons ====================
# Calendar Seasons Overview:
# Advent 1-4
# Christmas  1-2 + Holy Days
# Epiphany 1-10 + Holy Days
# Lent 1-5 + Holy days
# Holy Week 1
# Easter 1-10 (6 easter, ascension 1-2, Pentacost)
# Ordinary Time 1-29 + Holy Days, Trinity Sunday, 29=Christ the King

def IsAdventTime(datein):
    return (datein >= FirstSundayOfAdvent(datein.year) and datein < Christmas(datein.year))

def IsChristmasTime(datein):
    if(datein >= YearChangeConfusion(datein.year) and datein <= EndOfYear(datein.year)):
        eyear = (datein.year + 1)
    else:
        eyear = datein.year
    if(datein >= StartOfYear(datein.year) and datein < Epiphany(datein.year)):
        cyear = (datein.year - 1)
    else:
        cyear = datein.year
    return (datein >= Christmas(cyear) and datein < Epiphany(eyear))

def IsEpiphanyTime(datein):
    return (datein >= Epiphany(datein.year) and datein < AshWednesday(datein.year))

def IsLentTime(datein):
    return (datein >= AshWednesday(datein.year) and datein < easter(datein.year))

def IsHolyWeek(datein):
    return (datein >= PalmSunday(datein.year) and datein < easter(datein.year))

def IsEasterTide(datein):
    return (datein >= easter(datein.year) and datein < Trinity(datein.year))

def IsOrdinaryTime(datein):
    return (datein >= Trinity(datein.year) and datein < FirstSundayOfAdvent(datein.year))



#======== ADVENT ==================

def FirstSundayOfAdvent(year):
    weeks = 4;
    correction = 0;
    christmas = date(year, 12, 25)
    if (christmas.weekday() != 6) :
        # 6 is Sunday
        weeks-= 1
        correction = (christmas.isoweekday())
    d=timedelta(days=(-1*((weeks*7)+correction)))
    return christmas+d

def SecondSundayOfAdvent(year):
    d=timedelta(weeks=1)
    return FirstSundayOfAdvent(year)+d

def ThirdSundayOfAdvent(year):
    d=timedelta(weeks=2)
    return FirstSundayOfAdvent(year)+d

def FourthSundayOfAdvent(year):
    d=timedelta(weeks=3)
    return FirstSundayOfAdvent(year)+d



#======== CHRISTMAS ==================

def Christmas(year):
    return date(year, 12, 25)

def ChristmasOne(year):
    s = date(year, 12, 26)
    e = date(year, 12, 31)
    delta = timedelta(days=1)
    while s <= e:
        if(s.weekday()==6):
            return s
        s+=delta
    return e

def ChristmasTwo(year):
    year = (year - 1)
    d=timedelta(days=7)
    christwo = ChristmasOne(year)+d
    if(christwo >= EpiphanyOne(year)):
        return False
    return christwo

def ChristmasBackOne(year):
    year = (year - 1)
    s = date(year, 12, 25)
    e = date(year, 12, 31)
    delta = timedelta(days=1)
    while s <= e:
        if(s.weekday()==6):
            return s
        s+=delta
    return e

def ChristmasBackTwo(year):
    d=timedelta(days=7)
    christwo = ChristmasBackOne(year)+d
    if(christwo >= Epiphany(year)):
        return False
    return christwo



#======== EPIPHANY ==================

def Epiphany(year):
    return date(year, 1, 6)

def EpiphanyOne(year):
    s = date(year, 1, 2)
    e = date(year, 1, 8)
    delta = timedelta(days=1)
    while s <= e:
        if(s.weekday()==6):
            return s
        s+=delta
    return e

def EpiphanyTwo(year):
    d=timedelta(days=7)
    return EpiphanyOne(year)+d

def EpiphanyThree(year):
    d=timedelta(days=14)
    return EpiphanyOne(year)+d

def EpiphanyFour(year):
    d=timedelta(days=21)
    epiphfour = EpiphanyOne(year)+d
    if(epiphfour >= EpiphanyPenultimate(year)):
        return False
    return epiphfour

def EpiphanyFive(year):
    d=timedelta(days=28)
    epiphfive = EpiphanyOne(year)+d
    if(epiphfive >= EpiphanyPenultimate(year)):
        return False
    return epiphfive

def EpiphanySix(year):
    d=timedelta(days=35)
    epiphsix = EpiphanyOne(year)+d
    if(epiphsix >= EpiphanyPenultimate(year)):
        return False
    return epiphsix

def EpiphanySeven(year):
    d=timedelta(days=42)
    epiphsev = EpiphanyOne(year)+d
    if(epiphsev >= EpiphanyPenultimate(year)):
        return False
    return epiphsev

def EpiphanyEight(year):
    d=timedelta(days=49)
    epipheig = EpiphanyOne(year)+d
    if(epipheig >= EpiphanyPenultimate(year)):
        return False
    return epipheig

def EpiphanyPenultimate(year):
    d=timedelta(weeks=-8)
    return easter(year)+d

def EpiphanyUltimate(year):
    d=timedelta(weeks=-7)
    return easter(year)+d



#======== LENT ==================

def AshWednesday(year):
    d=timedelta(days=-46)
    return easter(year)+d

def LentOne(year):
    d=timedelta(weeks=-6)
    return easter(year)+d

def LentTwo(year):
    d=timedelta(weeks=-5)
    return easter(year)+d

def LentThree(year):
    d=timedelta(weeks=-4)
    return easter(year)+d

def LentFour(year):
    d=timedelta(weeks=-3)
    return easter(year)+d

def LentFive(year):
    d=timedelta(weeks=-2)
    return easter(year)+d



#======== HOLY WEEK ==================

def PalmSunday(year):
    "Palm Sunday for given year. / Dimanche des Rameaux de l'anne year"
    d=timedelta(weeks=-1)
    return easter(year)+d

def HolyThursday(year):
    d=timedelta(days=-3)
    return easter(year)+d

def GoodFriday(year):
    d=timedelta(days=-2)
    return easter(year)+d

def EasterVigil(year):
    d=timedelta(days=-1)
    return easter(year)+d



#======== EASTER ==================

def Easter(year):
    "Easter of given year."
    return easter(year)

def EasterTwo(year):
    d=timedelta(weeks=1)
    return easter(year)+d

def EasterThree(year):
    d=timedelta(weeks=2)
    return easter(year)+d

def EasterFour(year):
    d=timedelta(weeks=3)
    return easter(year)+d

def EasterFive(year):
    d=timedelta(weeks=4)
    return easter(year)+d

def EasterSix(year):
    d=timedelta(weeks=5)
    return easter(year)+d

def Ascension(year):
    d=timedelta(days=40)
    return easter(year)+d

def SundayAscension(year):
    d=timedelta(weeks=6)
    return easter(year)+d

def Pentecost(year):
    d=timedelta(weeks=7)
    return easter(year)+d


#======== ORDINARY TIME ==================

def Trinity(year):
    d=timedelta(weeks=8)
    return easter(year)+d

def OrdOne(year):
    s = date(year, 5, 8)
    e = date(year, 5, 14)
    delta = timedelta(days=1)
    while s <= e:
        if(s.weekday()==6):
            ordone = s
        s+=delta
    if(ordone <= Trinity(year)):
        return False
    return ordone

def OrdTwo(year):
    s = date(year, 5, 15)
    e = date(year, 5, 21)
    delta = timedelta(days=1)
    while s <= e:
        if(s.weekday()==6):
            ordtwo = s
        s+=delta
    if(ordtwo <= Trinity(year)):
        return False
    return ordtwo

def OrdThree(year):
    s = date(year, 5, 22)
    e = date(year, 5, 28)
    delta = timedelta(days=1)
    while s <= e:
        if(s.weekday()==6):
            ordthree = s
        s+=delta
    if(ordthree <= Trinity(year)):
        return False
    return ordthree

def OrdFour(year):
    s = date(year, 5, 29)
    e = date(year, 6, 4)
    delta = timedelta(days=1)
    ordfour = s
    while s <= e:
        if(s.weekday()==6):
            ordfour = s
        s+=delta
    if(ordfour <= Trinity(year)):
        return False
    return ordfour

def OrdFive(year):
    s = date(year, 6, 5)
    e = date(year, 6, 11)
    delta = timedelta(days=1)
    while s <= e:
        if(s.weekday()==6):
            ordfive = s
        s+=delta
    if(ordfive <= Trinity(year)):
        return False
    return ordfive

def OrdSix(year):
    s = date(year, 6, 12)
    e = date(year, 6, 18)
    delta = timedelta(days=1)
    while s <= e:
        if(s.weekday()==6):
            ordsix = s
        s+=delta
    if(ordsix <= Trinity(year)):
        return False
    return ordsix

def OrdSeven(year):
    s = date(year, 6, 19)
    e = date(year, 6, 25)
    delta = timedelta(days=1)
    while s <= e:
        if(s.weekday()==6):
            ordseven = s
        s+=delta
    if(ordseven <= Trinity(year)):
        return False
    return ordseven

def OrdEight(year):
    s = date(year, 6, 26)
    e = date(year, 7, 2)
    delta = timedelta(days=1)
    while s <= e:
        if(s.weekday()==6):
            ordeight = s
        s+=delta
    if(ordeight <= Trinity(year)):
        return False
    return ordeight

def OrdNine(year):
    s = date(year, 7, 3)
    e = date(year, 7, 9)
    delta = timedelta(days=1)
    while s <= e:
        if(s.weekday()==6):
            ordnine = s
        s+=delta
    if(ordnine <= Trinity(year)):
        return False
    return ordnine

def OrdTen(year):
    s = date(year, 7, 10)
    e = date(year, 7, 16)
    delta = timedelta(days=1)
    while s <= e:
        if(s.weekday()==6):
            return s
        s+=delta
    return e

def OrdEleven(year):
    s = date(year, 7, 17)
    e = date(year, 7, 23)
    delta = timedelta(days=1)
    while s <= e:
        if(s.weekday()==6):
            return s
        s+=delta
    return e

def OrdTwelve(year):
    s = date(year, 7, 24)
    e = date(year, 7, 30)
    delta = timedelta(days=1)
    while s <= e:
        if(s.weekday()==6):
            return s
        s+=delta
    return e

def OrdThirteen(year):
    s = date(year, 7, 31)
    e = date(year, 8, 6)
    delta = timedelta(days=1)
    while s <= e:
        if(s.weekday()==6):
            return s
        s+=delta
    return e

def OrdFourteen(year):
    s = date(year, 8, 7)
    e = date(year, 8, 13)
    delta = timedelta(days=1)
    while s <= e:
        if(s.weekday()==6):
            return s
        s+=delta
    return e

def OrdFifteen(year):
    s = date(year, 8, 14)
    e = date(year, 8, 20)
    delta = timedelta(days=1)
    while s <= e:
        if(s.weekday()==6):
            return s
        s+=delta
    return e

def OrdSixteen(year):
    s = date(year, 8, 21)
    e = date(year, 8, 27)
    delta = timedelta(days=1)
    while s <= e:
        if(s.weekday()==6):
            return s
        s+=delta
    return e

def OrdSeventeen(year):
    s = date(year, 8, 28)
    e = date(year, 9, 3)
    delta = timedelta(days=1)
    while s <= e:
        if(s.weekday()==6):
            return s
        s+=delta
    return e

def OrdEighteen(year):
    s = date(year, 9, 4)
    e = date(year, 9, 10)
    delta = timedelta(days=1)
    while s <= e:
        if(s.weekday()==6):
            return s
        s+=delta
    return e

def OrdNineteen(year):
    s = date(year, 9, 11)
    e = date(year, 9, 17)
    delta = timedelta(days=1)
    while s <= e:
        if(s.weekday()==6):
            return s
        s+=delta
    return e

def OrdTwenty(year):
    s = date(year, 9, 18)
    e = date(year, 9, 24)
    delta = timedelta(days=1)
    while s <= e:
        if(s.weekday()==6):
            return s
        s+=delta
    return e

def OrdTwentyOne(year):
    s = date(year, 9, 25)
    e = date(year, 10, 1)
    delta = timedelta(days=1)
    while s <= e:
        if(s.weekday()==6):
            return s
        s+=delta
    return e

def OrdTwentyTwo(year):
    s = date(year, 10, 2)
    e = date(year, 10, 8)
    delta = timedelta(days=1)
    while s <= e:
        if(s.weekday()==6):
            return s
        s+=delta
    return e

def OrdTwentyThree(year):
    s = date(year, 10, 9)
    e = date(year, 10, 15)
    delta = timedelta(days=1)
    while s <= e:
        if(s.weekday()==6):
            return s
        s+=delta
    return e

def OrdTwentyFour(year):
    s = date(year, 10, 16)
    e = date(year, 10, 22)
    delta = timedelta(days=1)
    while s <= e:
        if(s.weekday()==6):
            return s
        s+=delta
    return e

def OrdTwentyFive(year):
    s = date(year, 10, 23)
    e = date(year, 10, 29)
    delta = timedelta(days=1)
    while s <= e:
        if(s.weekday()==6):
            return s
        s+=delta
    return e

def OrdTwentySix(year):
    s = date(year, 10, 30)
    e = date(year, 11, 5)
    delta = timedelta(days=1)
    while s <= e:
        if(s.weekday()==6):
            return s
        s+=delta
    return e

def OrdTwentySeven(year):
    s = date(year, 11, 6)
    e = date(year, 11, 12)
    delta = timedelta(days=1)
    while s <= e:
        if(s.weekday()==6):
            return s
        s+=delta
    return e

def OrdTwentyEight(year):
    s = date(year, 11, 13)
    e = date(year, 11, 19)
    delta = timedelta(days=1)
    while s <= e:
        if(s.weekday()==6):
            return s
        s+=delta
    return e

def ChristKing(year):
    # d=timedelta(weeks=-1)
    # return FirstSundayOfAdvent(year)+d
    s = date(year, 11, 20)
    e = date(year, 11, 26)
    delta = timedelta(days=1)
    while s <= e:
        if(s.weekday()==6):
            return s
        s+=delta
    return e



#======== HOLY DAYS ========================

def HolyName(year):
    return date(year, 1, 1)

def StPeter(year):
    return date(year, 1, 18)

def StPaul(year):
    return date(year, 1, 25)

def PresentationOfChrist(year):
    return date(year, 2, 2)

def StMatthias(year):
    return date(year, 2, 24)

def StJoseph(year):
    joseph = date(year, 3, 19)
    if(joseph == PalmSunday(year)):
        d = timedelta(days=-1)
        return joseph+d
    return joseph

def Annunciation(year):
    annunciation = date(year, 3, 25)
    easter_ = easter(year)

    # the second monday after easter if 25 is during holy week or Pascal week
    if(easter_<=date(year,4,2)):
        d = timedelta(weeks=1, days=1)
        return easter_+d

    # the following monday if 25/03 is a sunday
    if(annunciation.weekday()==6):
        d = timedelta(days=1)
        return annunciation+d

    return annunciation

def StMark(year):
    return date(year, 4, 25)

def StsPhilipAndJames(year):
    return date(year, 5, 1)

def Visitation(year):
    return date(year, 5, 31)

def StBarnabas(year):
    return date(year, 6, 11)

def NativityOfJohnTheBaptist(year):
    return date(year, 6, 24)

def StsPeterAndPaul(year):
    return date(year, 6, 29)

def CanadaDay(year):
    return date(year, 7, 1)

def IndependenceDay(year):
    return date(year, 7, 4)

def StMagdalene(year):
    return date(year, 7, 22)

def StJames(year):
    return date(year, 7, 25)

def JamesJerusalem(year):
    return date(year, 7, 26)

def Transfiguration(year):
    return date(year, 8, 6)

def StMary(year):
    return date(year, 8, 15)

def StBartholomew(year):
    return date(year, 8, 24)

def HolyCross(year):
    return date(year, 9, 14)

def StMatthew(year):
    return date(year, 9, 21)

def HolyMichaelAllAngels(year):
    return date(year, 9, 29)

def StLuke(year):
    return date(year, 10, 18)

def StSimonAndJude(year):
    return date(year, 10, 28)

def AllSaints(year):
    return date(year, 11, 1)

def Stephen(year):
    return date(year, 12, 26)

def HolyInnocents(year):
    return date(year, 12, 28)

def MemorialDay(year):
    # Monday closest to May 28
    s = date(year, 5, 28)
    e = s
    i = 0
    delta = timedelta(days=1)
    while i < 7:
        if(s.weekday()==0):
            memday = s
            return memday
        if(e.weekday()==0):
            memday = e
            return memday
        s+=delta
        e-=delta
        i+=1
    return "Error: Memorial Day not found."

def ThanksgivingDayUSA(year):
    # 4th Thursday in Nov.
    s = date(year, 11, 1)
    i = 0
    delta = timedelta(days=1)
    while i < 7:
        if(s.weekday()==3):
            tday = s+(delta*21)
            return tday
        s+=delta
        i+=1
    return "Error: Thanksgiving Day USA not found."

def ThanksgivingDayCanada(year):
    # 2nd Monday in Oct.
    s = date(year, 10, 1)
    i = 0
    delta = timedelta(days=1)
    while i < 7:
        if(s.weekday()==0):
            tday = s+(delta*7)
            return tday
        s+=delta
        i+=1
    return "Error: Thanksgiving Day Canada not found."

def RemembranceDay(year):
    return date(year, 11, 11)

def Andrew(year):
    return date(year, 11, 30)

def Thomas(year):
    return date(year, 12, 21)

def John(year):
    return date(year, 12, 27)


#=====================================
# NOTE Date Conversion Process
#=====================================

#----- Find Church Year -----------
# Year A, Year B, or Year C
# Church Year Begins on Advent 1
# 0:year a, 1:year b, 2:year c

def ConvertYear(datein):
    if (datein >= FirstSundayOfAdvent(datein.year) and datein <= EndOfYear(datein.year)):
        inyear = datein.year+1
    else:
        inyear = datein.year
    cyear = (inyear + 2) % 3
    yr=["Year A",
            "Year B",
            "Year C"
            ]
    return yr[cyear]

#----- Find Season ----------------
# Calendar Seasons Overview:
# 0 = Advent 1-4
# 1 = Christmas 1-2 + Holy Days
# 2 = Epiphany 1-10 + Holy Days
# 3 = Lent 1-5 + Holy days
# 4 = Holy Week 1
# 5 = Easter 1-10
# 6 = Ordinary Time 1-29 + Holy Days
# 7 = Holy Days

def ConvertSeason(datein):
    if (IsEasterTide(datein)):
        churchseason = "Easter"
    elif (IsHolyWeek(datein)):
        churchseason = "Holy Week"
    elif (IsLentTime(datein)):
        churchseason = "Lent"
    elif (IsAdventTime(datein)):
        churchseason = "Advent"
    elif (IsChristmasTime(datein)):
        churchseason = "Christmas"
    elif (IsEpiphanyTime(datein)):
        churchseason = "Epiphany"
    elif (IsOrdinaryTime(datein)):
        churchseason = "Ordinary"
    # NOTE elif (holyday)
    return churchseason

#----- Find Week ----------

def ConvertWeek(datein):
    # Changed Date is set to previous Sunday for easy comparisons
    churchseason = ConvertSeason(datein)
    changeddate = datein
    d = timedelta(days=(-1))
    i = date.weekday(datein)
    weeks = []
    while i < 6:
        if changeddate == Christmas(changeddate.year):
            break
        if changeddate == AshWednesday(changeddate.year):
            break
        if changeddate == Epiphany(changeddate.year):
            break
        changeddate += d
        i = date.weekday(changeddate)
    
    # Get dictionary
    inyear = datein.year
    dict = GetDictionary(inyear, churchseason)
    
    # Loop it
    for key in dict:
        if changeddate == key[0]:
            weeks.append(key[1])
    if len(weeks) == 0:
        return False
    else:
        return weeks[0]

#----- Find Holy Days ----------

def HolyDays(datein):

    inyear = datein.year
    holydays = []

    hds = [
        [HolyName(inyear), "The Circumcision and Holy Name"],
        [StPeter(inyear), "Confession of Peter the Apostle"],
        [StPaul(inyear), "Conversion of Paul the Apostle"],
        [PresentationOfChrist(inyear), "The Presentation of Christ"],
        [StMatthias(inyear), "Matthias the Apostle"],
        [StJoseph(inyear), "Joseph, the Guardian of Jesus"],
        [Annunciation(inyear), "The Annunciation"],
        [StMark(inyear), "Mark the Evangelist"],
        [StsPhilipAndJames(inyear), "Philip and James the Apostles"],
        [Visitation(inyear), "The Visitation"],
        [StBarnabas(inyear), "Barnabas the Apostle"],
        [NativityOfJohnTheBaptist(inyear), "The Nativity of John the Baptist"],
        [StsPeterAndPaul(inyear), "Peter and Paul the Apostles"],
        [CanadaDay(inyear), "Canada Day"],
        [IndependenceDay(inyear), "Independence Day"],
        [StMagdalene(inyear), "Mary Magdalene"],
        [StJames(inyear), "James the Elder and the Apostle"],
        [Transfiguration(inyear), "The Transfiguration"],
        [StMary(inyear), "The Virgin Mary"],
        [StBartholomew(inyear), "Bartholomew the Apostle"],
        [HolyCross(inyear), "Holy Cross Day"],
        [StMatthew(inyear), "Matthew the Apostle and Evangelist"],
        [HolyMichaelAllAngels(inyear), "Holy Michael and All Angels"],
        [StLuke(inyear), "Luke the Evangelist and Companion of Paul"],
        [JamesJerusalem(inyear), "James of Jerusalem"],
        [StSimonAndJude(inyear), "Simon and Jude the Apostles"],
        [AllSaints(inyear), "All Saints' Day"],
        [Stephen(inyear), "Stephen, Deacon and Martyr"],
        [HolyInnocents(inyear), "The Holy Innocents"],
        [Epiphany(inyear), "Epiphany"],
        [Christmas(inyear), "The Nativity of our Lord Jesus Christ"],
        [MemorialDay(inyear), "Memorial Day"],
        [ThanksgivingDayUSA(inyear), "Thanksgiving Day (USA)"],
        [ThanksgivingDayCanada(inyear), "Thanksgiving Day (Canada)"],
        [RemembranceDay(inyear), "Remembrance Day"],
        [Andrew(inyear), "Andrew the Apostle"],
        [Thomas(inyear), "Thomas the Apostle"],
        [John(inyear), "John the Apostle and Evangelist"]
    ]

    for key in hds:
        if key[0] == datein:
            holydays.append(key[1])
    if len(holydays) == 0:
        return False
    else:
        return holydays

#----- Get Dictionary for Week Conversion ----------

def GetDictionary(inyear, churchseason):

    if churchseason == "Advent":
        dictionary = [
            [FirstSundayOfAdvent(inyear), "First Sunday of Advent"],
            [SecondSundayOfAdvent(inyear), "Second Sunday of Advent"],
            [ThirdSundayOfAdvent(inyear), "Third Sunday of Advent"],
            [FourthSundayOfAdvent(inyear), "Fourth Sunday of Advent"]
            ]
    elif churchseason == "Christmas":
        dictionary = [
            [Christmas(inyear), "Christmas"],
            [ChristmasOne(inyear), "Christmas One"],
            [ChristmasTwo(inyear), "Christmas Two"],
            [ChristmasBackOne(inyear), "Christmas One"],
            [ChristmasBackTwo(inyear), "Christmas Two"]
            ]
    elif churchseason == "Epiphany":
        dictionary = [
            [Epiphany(inyear), "Epiphany"],
            [EpiphanyOne(inyear), "Epiphany One"],
            [EpiphanyTwo(inyear), "Epiphany Two"],
            [EpiphanyThree(inyear), "Epiphany Three"],
            [EpiphanyFour(inyear), "Epiphany Four"],
            [EpiphanyFive(inyear), "Epiphany Five"],
            [EpiphanySix(inyear), "Epiphany Six"],
            [EpiphanySeven(inyear), "Epiphany Seven"],
            [EpiphanyEight(inyear), "Epiphany Eight"],
            [EpiphanyPenultimate(inyear), "Epiphany Penultimate"],
            [EpiphanyUltimate(inyear), "Epiphany Ultimate"]
            ]
    elif churchseason == "Lent":
        dictionary = [
            [AshWednesday(inyear), "Ash Wednesday"],
            [LentOne(inyear), "Lent One"],
            [LentTwo(inyear), "Lent Two"],
            [LentThree(inyear), "Lent Three"],
            [LentFour(inyear), "Lent Four"],
            [LentFive(inyear), "Lent Five"]
            ]
    elif churchseason == "Holy Week":
        dictionary = [
            [PalmSunday(inyear), "Palm Sunday"],
            [HolyThursday(inyear), "Holy Thursday"],
            [GoodFriday(inyear), "Good Friday"]
            ]
    elif churchseason == "Easter":
        dictionary = [
            [EasterVigil(inyear), "Easter Vigil"],
            [Easter(inyear), "Easter One"],
            [EasterTwo(inyear), "Easter Two"],
            [EasterThree(inyear), "Easter Three"],
            [EasterFour(inyear), "Easter Four"],
            [EasterFive(inyear), "Easter Five"],
            [EasterSix(inyear), "Easter Six"],
            [Ascension(inyear), "Ascension"],
            [SundayAscension(inyear), "Sunday after Ascension"],
            [Pentecost(inyear), "Pentecost"]
            ]
    elif churchseason == "Ordinary":
        dictionary = [
            [Trinity(inyear), "Trinity Sunday"],
            [OrdOne(inyear), "Ordinary One"],
            [OrdTwo(inyear), "Ordinary Two"],
            [OrdThree(inyear), "Ordinary Three"],
            [OrdFour(inyear), "Ordinary Four"],
            [OrdFive(inyear), "Ordinary Five"],
            [OrdSix(inyear), "Ordinary Six"],
            [OrdSeven(inyear), "Ordinary Seven"],
            [OrdEight(inyear), "Ordinary Eight"],
            [OrdNine(inyear), "Ordinary Nine"],
            [OrdTen(inyear), "Ordinary Ten"],
            [OrdEleven(inyear), "Ordinary Eleven"],
            [OrdTwelve(inyear), "Ordinary Twelve"],
            [OrdThirteen(inyear), "Ordinary Thirteen"],
            [OrdFourteen(inyear), "Ordinary Fourteen"],
            [OrdFifteen(inyear), "Ordinary Fifteen"],
            [OrdSixteen(inyear), "Ordinary Sixteen"],
            [OrdSeventeen(inyear), "Ordinary Seventeen"],
            [OrdEighteen(inyear), "Ordinary Eighteen"],
            [OrdNineteen(inyear), "Ordinary Nineteen"],
            [OrdTwenty(inyear), "Ordinary Twenty"],
            [OrdTwentyOne(inyear), "Ordinary Twenty One"],
            [OrdTwentyTwo(inyear), "Ordinary Twenty Two"],
            [OrdTwentyThree(inyear), "Ordinary Twenty Three"],
            [OrdTwentyFour(inyear), "Ordinary Twenty Four"],
            [OrdTwentyFive(inyear), "Ordinary Twenty Five"],
            [OrdTwentySix(inyear), "Ordinary Twenty Six"],
            [OrdTwentySeven(inyear), "Ordinary Twenty Seven"],
            [OrdTwentyEight(inyear), "Ordinary Twenty Eight"],
            [ChristKing(inyear), "Christ the King"]
            ]
    else:
        return False
    return dictionary



#=====================================
# NOTE Test variable settings
# In order to test THIS PAGE ONLY
# unhash and set date.
#=====================================

# datein = date(2021,1,1)

# d = timedelta(days=(1))
# i = 0

# while i < 5:
#     date += d
#     i += 1

# rows = []
# headers = ["Date", "Week", "Season", "Holy Day", "Day", "Year"]

# while i < 730:
#     i += 1
#     date += d

#     cells = [str(date)]
#     output = churchCalendar(date)

#     for attr, value in output.__dict__.iteritems():
#         cell = str(value)
#         cells.append(cell)
#     rows += [cells]

# with open('data.csv', 'w') as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerow(headers)
#     writer.writerows(rows)

#---------- End -------------
