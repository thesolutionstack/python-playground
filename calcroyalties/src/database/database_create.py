#!/bin/env python3

"""
This is the system's only database creation script.

To Update, do the following:

1) Update the database version #
2) Make whatever updates you need

"""
import datetime

import config

class DatabaseCreate(object):
    
    DATABASE_VERSION = 1.1

    def __init__(self):
        self.dbi = config.get_database_instance()
        
    def create_all(self):
        tables = self.dbi.get_table_names()
        if 'Config' not in tables:
            self.Config()
        if 'Well' not in tables:
            self.Well()
        if 'RoyaltyMaster' not in tables:
            self.RoyaltyMaster()
        if 'Lease' not in tables:
            self.Lease()
        if 'WellLeaseLink' not in tables:
            self.WellLeaseLink()
        if 'Monthly' not in tables:
            self.Monthly()
        if 'Calc' not in tables:
            self.Calc()
        if 'ECONData' not in tables:
            self.ECONdata()
        if 'LinkTab' not in tables:
            self.Linktab()
        if 'Users' not in tables:
            self.Users()

        self.dbi.commit()

    def Config(self):
        statement = """
            CREATE TABLE Config ('ID' integer primary key autoincrement, 
            'Version' int, CreateDate timestamp);
        """
        self.dbi.execute_statement(statement)
        
        insert_statement = "insert into Config (Version, CreateDate) values(" + str(DatabaseCreate.DATABASE_VERSION) + ",'" + str(datetime.datetime.now()) + "');"
        self.dbi.execute(insert_statement)

    def Well(self):
        statement = """
            CREATE TABLE Well ('ID' integer primary key autoincrement, 
             "StartDate" timestamp,
             "EndDate" timestamp,
             'WellEvent' text, 'Prov' text, 'WellType' text, 'LeaseType' text,
             'LeaseID' int, 'RoyaltyClassification' text,
             'Classification' text, 'SRC' int, 'PEFNInterest' float,
             'CommencementDate' timestamp, 'ReferencePrice' int);
        """
        self.dbi.execute_statement(statement)
        
    def RoyaltyMaster(self):
        statement = """
            CREATE TABLE RoyaltyMaster ('ID' integer primary key autoincrement,
             "StartDate" timestamp,
             "EndDate" timestamp,
             "RightsGranted" text, "RoyaltyScheme" text,
             "CrownMultiplier" float, "MinRoyalty" int, "ValuationMethod" text,
             "TruckingDeducted" text, "ProcessingDeducted" text, "GCADeducted" text, "Gorr" text,
             "OverrideRoyaltyClassification" text, "Notes" text);
        """
        self.dbi.execute_statement(statement)
        
    def Lease(self):
        statement = """
            CREATE TABLE Lease ('ID' integer primary key autoincrement,
             "StartDate" timestamp,
             "EndDate" timestamp,
             "LeaseType" text, "Prov" text, "FNReserve" int, "FNBandID" int, "Lessor" text,
             "Notes" text);
        """
        self.dbi.execute_statement(statement)
        
    def WellLeaseLink(self):
        statement = """
            CREATE TABLE WellLeaseLink ('ID' integer primary key autoincrement,
             "StartDate" timestamp,
             "EndDate" timestamp,
             "WellEvent" text, "LeaseID" int, "PEFNInterest" float);
        """
        self.dbi.execute_statement(statement)

    def Monthly(self):
        statement = """
            CREATE TABLE Monthly ('ID' integer primary key autoincrement, 
            "ExtractMonth" timestamp, "ProdMonth" int, "WellID" int, "Product" text,
            "AmendNo" int, "ProdHours" int, "ProdVol" int, "TransPrice" float, 
            "WellHeadPrice" float, "TransRate" float, "ProcessingRate" float, "GCARate" float);
        """
        self.dbi.execute_statement(statement)
        
    def Calc(self):
        statement = """
            CREATE TABLE Calc ('ID' integer primary key autoincrement,
            "ProdMonth" int, "WellID" int, "Product" text,
            "K" int, "X" int, "C" int, "D" int, 
            "RoyaltyPrice" float, "RoyaltyVolume" int, "ProvCrownRoyaltyRate" int, 
            "ProvCrownUsedRoyaltyRate" int, "IOGR1995RoyaltyRate" int, 
            "GorrRoyaltyRate" int, "ProvCrownRoyaltyVolume" int, 
            "GorrRoyaltyVolume" int, "IOGR1995RoyaltyVolume" int, 
            "ProvCrownRoyaltyValue" int, "IOGR1995RoyaltyValue" float, 
            "GorrRoyaltyValue" float, "RoyaltyValuePreDeductions" float, 
            "RoyaltyTransportation" int, "RoyaltyProcessing" int, "RoyaltyGCA" int,
            "SupplementaryRoyalties" int, "RoyaltyRegulation" int,
            "RoyaltyDeductions" int, "RoyaltyValue" float, 
            "CommencementPeriod" float, "Message" text, "GorrMessage" text);
        """
        self.dbi.execute_statement(statement)
        
    def ECONdata(self):
        statement = """
            CREATE TABLE ECONData ('ID' integer primary key autoincrement,
            "CharMonth" text, "ProdMonth" int, 
            "HOP" int, "SOP" int, "NOP" int, 
            "H4T_C" float, "H4T_D" float, "H4T_K" float, "H4T_X" int, 
            "H3T_K" float, "H3T_X" int, 
            "HNEW_K" float, "HNEW_X" int, 
            "SW4T_C" float, "SW4T_D" float, "SW4T_K" float, "SW4T_X" int,
            "SW3T_K" float, "SW3T_X" int,
            "SWNEW_K" float, "SWNEW_X" int, 
            "O4T_C" float, "O4T_D" float, "O4T_K" float, "O4T_X" int, 
            "O3T_K" float, "O3T_X" int, 
            "ONEW_K" float, "ONEW_X" int, 
            "OOLD_K" float, "OOLD_X" int);
        """
        self.dbi.execute_statement(statement)


    def ECONGasdata(self):
        statement = """
            CREATE TABLE ECONGasData ('ID' integer primary key autoincrement,
            "CharMonth" text, "ProdMonth" int,
            "G4T_C" int, "G4T_D" int, "G4T_K" int,
            "G4T_X" float, "G3T_C" float, "G3T_K" float, "G3T_X" int,
            "GNEW_C" float, "GNEW_K" int,
            "GNEW_X" float, "GOLD_C" int,
            "GOLD_K" float, "GOLD_X" float);
        """
        self.dbi.execute_statement(statement)

    def Linktab(self):
        statement = """
            create table LinkTab ('ID' integer primary key autoincrement,
            TabName text, AttrName text, LinkName text, BaseTab boolean, ShowAttrs text);
        """
        self.dbi.execute_statement(statement)

    def Users(self):
        statement = """
            CREATE TABLE Users (
                "ID"	INTEGER PRIMARY KEY AUTOINCREMENT,
                "Login"	TEXT,
                "Name"	TEXT,
                "Email"	TEXT,
                "ProdMonth"	INTEGER,
                "Permissions"	TEXT)
        """
        self.dbi.execute_statement(statement)

        insert_statement = "insert into Users values(1,'admin','Admin Admin','info@thesolutionstack.com',201604, \
                           ' ,well_view,well_edit,wellevent_view,wellevent_edit,facility_view,lease_view,lease_edit,welllease_view,welllease_edit,data_view,data_edit,users_view,users_edit');"
        self.dbi.execute(insert_statement)
