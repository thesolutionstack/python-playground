#!/bin/env python3

from flask import render_template, request, redirect, url_for, flash
import json
import sys,traceback

from app import app
from database.sqlite_show import Shower
from database.utils import Utils
import config


# *** Note *** I commented out these lines and /data/ started working. I think it is because they grab a connecton to the db and then it restarts in another thread.
# db = database.DataBase(config.get_file_dir() + 'database new.xlsx')
# pr = calcroyalties.ProcessRoyalties()
# rw = calcroyalties.RoyaltyWorksheet()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/searchwells/')
def searchwells():
    return render_template('searchwells.html')

@app.route('/well/<wellid>')
def well(wellid):
    if wellid:
        well=db.getWell(int(wellid))
        return render_template('well.html', well=well)

@app.route('/leases')
def leases():
    all_leases = db.getAllLeases()
    return_leases = []
    if request.args:
        for l in all_leases:
#            if l.Lease == request.args['leaseid']:
            if (request.args['leaseid'] == "" or request.args['leaseid'] == l.lease) and \
                (request.args['prov'] == "" or request.args['prov'] == l.Prov):
                    return_leases.append(l)
        if len(return_leases) == 0:
            flash('No matching leases found.')
            return redirect(url_for('searchleases'))
        elif len(return_leases) == 1:
            return redirect(url_for('lease', leaseid=return_leases[0].lease))
        else:
            return render_template('leases.html', leases=return_leases)
    else:
        return render_template('leases.html', leases=all_leases)

@app.route('/lease/<leaseid>')
def lease(leaseid):
    if leaseid:
        lease=db.getLease(leaseid)
        rm=db.getRoyaltyMaster(leaseid)
        return render_template('lease.html', lease=lease, rm=rm)

@app.route('/wells')
def wells():
    all_wells = db.getAllWells()
    return_wells = []
    if request.args:
        for w in all_wells:
            if (request.args['wellid'] == "" or int(request.args['wellid']) == w.WellId) \
                and (request.args['welltype'] == "" or request.args['welltype'] == w.WellType) \
                and (request.args['uwi'] == "" or request.args['uwi'] == w.UWI):
                    return_wells.append(w)
        if len(return_wells) == 0:
            flash('No matching wells found.')
            return redirect(url_for('searchwells'))
        elif len(return_wells) == 1:
            return redirect(url_for('well', wellid=return_wells[0].WellId))
        else:
            return render_template('wells.html', wells=return_wells)
    else:
        return render_template('wells.html', wells=all_wells)

@app.route('/searchleases')
def searchleases():
    return render_template('searchleases.html')

@app.route('/worksheet')
def worksheet():
#    if request.args:
#        md = db.getMonthlyByWell(int(request.args["WellId"]))
#    pr.process('database/database.xlsx')
    with open("Royalty Worksheet.txt", 'r') as f:
        ws = f.read()
        return render_template('worksheet.html', ws=ws)

###
### New stuff below:
###

@app.route('/2')
def index2():
    return render_template('index2.html')

@app.route("/data/",methods=['GET','POST'])
def data():
    html =""
    try:
        db_instance = config.get_database_instance()
        shower = Shower()

        table=request.args.get('table')
        attr=request.args.get('attr')
        key=request.args.get('key')
        links = {}
        links['BAid'] = '?table=BAInfo&attr=BAid&key='
        links['WellEvent'] = '?table=WellInfo&attr=Well&key='

        tables = db_instance.get_table_names()
        header = None
        rows = None
        print('Table:',table)
        if table:
            header = shower.show_columns(table)
            rows = shower.show_table(table,attr,key)
        html = render_template('data.html',table=table,tables=tables,header=header,rows=rows,links=links)
    except Exception as e:
        print('views.data: ***Error:',e)
        traceback.print_exc(file=sys.stdout)
    return html

@staticmethod
@app.route("/data/updateLinkRow.json",methods=['POST'])
def update_link_row():
    utils = Utils()
    db = config.get_database()
    return_data = dict()
    try:
        print('AppServer.update_link_row running',request.method)
        data = utils.json_decode(request)
        print('data:',data)
        linktab = db.get_data_structure('LinkTab')
        utils.dict_to_obj(data,linktab)
        print('just before if data:',data)
        print('just before if data:',data['ID'])
        if data['ID'] == '0':
            db.insert(linktab)
        else:
            db.update(linktab)

        return_data['StatusCode'] = 0
        return json.dumps(return_data)
    except Exception as e:
        print('AppServer.link: ***Error:',e)
        traceback.print_exc(file=sys.stdout)
        return_data['StatusCode'] = -1
        return_data['Message'] = str(e)
        return json.dumps(return_data)

@staticmethod
@app.route("/data/getLinkRow.json",methods=['POST'])
def get_link_row():
    utils = Utils()
    db = config.get_database()
    try:
        print('AppServer.get_link_row running',request.method)
        print('Instance:',config.get_database_name(),config.get_environment())
        print('Tables',config.get_database_instance().get_table_names())
        data = utils.json_decode(request)
        link = db.select("LinkTab", TabName = data['TabName'], AttrName = data['AttrName'])
        print('link',link)
        if not link:
            data['ID'] = 0
            data['LinkName'] = ''
            data['BaseTab'] = 0
            data['ShowAttrs'] = ''
        else:
            data['ID'] = link[0].ID
            data['LinkName'] = link[0].LinkName
            data['BaseTab'] = link[0].BaseTab
            data['ShowAttrs'] = link[0].ShowAttrs

        return json.dumps(data)

    except Exception as e:
        print('AppServer.link: ***Error:',e)
        traceback.print_exc(file=sys.stdout)

@staticmethod
@app.route("/data/getLinkData.json",methods=['POST'])
def get_link_data():
    utils = Utils()
    db = config.get_database()
    try:
        data = utils.json_decode(request)
#             print('data', data)
        link = db.select("LinkTab", TabName = data['TabName'], AttrName = data['AttrName'])
#             print('link',link)
        if len(link) > 0:
            result_rows = db.select("LinkTab", LinkName=link[0].LinkName, BaseTab=1)
#                 print('result:',result_rows)
#                 print('result.type:',type(result_rows))

            # Get the base table
            for result in result_rows:
                print('We have a base table')
                attrs_to_show = result.ShowAttrs.split(',')
                args = dict()
                args[result.AttrName] = data['AttrValue']
                key_data_rows = db.select(result.TabName,**args)
                rows = []
                for keyData in key_data_rows:
                    row = []
                    for a in attrs_to_show:
                        row.append(keyData.__dict__[a])
                    rows.append(attrs_to_show)
                    rows.append(row)
                data['BaseData'] = rows

            # Get all the tables that the link uses
            result_rows = db.select("LinkTab", LinkName=link[0].LinkName)

            rows = []
            for result in result_rows:
                row = []
                row.append(result.TabName)
                row.append(result.AttrName)
                rows.append(row)
            data['Links'] = rows

        else:
            data["Message"] = data['AttrName'] + " has not been linked."
        return json.dumps(data)
#
    except Exception as e:
        print('AppServer.link: ***Error:',e)
        traceback.print_exc(file=sys.stdout)

    print("hello")

@staticmethod
@app.route('/adriennews')
def adriennews():
    if request.args:
        db = config.get_database()
        wellIds = request.args["WellId"]
        well_id = int(wellIds)
        prodMonth = 201501
        product = "Oil"
        well = db.select1('Well', ID=well_id)
        royalty = db.select1('Royaltymaster', ID=well.LeaseID)
        lease = db.select1('Lease', ID=well.LeaseID)
        monthly = db.select1('Monthly', WellID = well_id, prodMonth = prodMonth, product = product)
        calc_array = db.select('Calc', WellID=well_id, prodMonth = prodMonth)
        calc = calc_array[0]
        print(monthly)
    else:
        print("No monthly data for this well")
    return render_template('worksheetas.html', well=well, rm=royalty, m=monthly,  lease=lease, calc=calc)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html')


###
### Temporary place for new stuff:
###

@app.route('/new/well/index')
def new_indexwells():
    return render_template('new/searchwells.html')

@app.route('/new/well/search')
def new_searchwells():
    return render_template('new/searchwells.html')

@app.route('/new/api/wellresults')
def new_wellresults():
    try:
        db = config.get_database()
        results = db.select('Well')
        return render_template('new/wellresults.html', results = results)
    except:
        return "<h2>No results found</h2>"

@app.route('/new/api/wellinfo')
def new_wellinfo():
    try:
        db = config.get_database()
        result = db.select1('Well', ID=request.args.get('ID'))
        return render_template('new/wellinfo.html', result = result)
    except:
        return "<h2>Well details not found</h2>"
    
@app.route('/new/facility/search')
def new_search_facilities():
    return render_template('new/facilitysearch.html')

# Faclility Information 2016-03-26

@app.route('/new/api/facilityresults')
def new_facility_results():
    try:
        db = config.get_database()
        results = db.select('FacilityInfo')
        return render_template('new/facilityresults.html', results = results)
    except Exception as e:
        print('views.new_facility_results: ***Error:',e)
        traceback.print_exc(file=sys.stdout)
        return "<h2>No results found</h2>"


@app.route('/new/api/facilityinfo')
def new_facility_info():
    try:
        db = config.get_database()
        result = db.select1('FacilityInfo', Facility=request.args.get('ID'))
        wells  = db.select('WellFacilityLink', Facility=request.args.get('ID'))
        print('new_facility_info:',len(wells),"found")
        
        return render_template('new/facilityinfo.html', result = result, wells = wells)
    except Exception as e:
        print('views.new_facility_info: ***Error:',e)
        traceback.print_exc(file=sys.stdout)
        return "<h2>Facility details not found</h2>"
