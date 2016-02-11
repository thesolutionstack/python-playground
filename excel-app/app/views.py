#!/bin/env python3

from app import app
from flask import render_template, request, redirect, url_for, flash
from database import database
from database import calcroyalties

db = database.DataBase('database.xlsx')
pr = calcroyalties.ProcessRoyalties()
rw = calcroyalties.RoyaltyWorksheet()

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
#			if l.Lease == request.args['leaseid']:
			if (request.args['leaseid'] == "" or request.args['leaseid'] == l.Lease) and \
				(request.args['prov'] == "" or request.args['prov'] == l.Prov):
					return_leases.append(l)
		if len(return_leases) == 0:
			flash('No matching leases found.')
			return redirect(url_for('searchleases'))
		elif len(return_leases) == 1:
			return redirect(url_for('lease', leaseid=return_leases[0].Lease))
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
#	if request.args:
#		md = db.getMonthlyByWell(int(request.args["WellId"]))
#	pr.process('database/database.xlsx')
	with open("Royalty Worksheet.txt", 'r') as f:
		ws = f.read()
		return render_template('worksheet.html', ws=ws)


@app.route('/adriennews')
def adriennews():
	if request.args:
		wellId = request.args["WellId"]
		well=db.getWell(int(wellId))
		lease=db.getLease(well.Lease)
		monthly=db.getMonthlyByWell(wellId)
		rm=db.getRoyaltyMaster(well.Lease)


	return render_template('worksheetas.html', well=well, lease=lease, rm=rm, monthly=monthly)
#	return "from adriennes well is" + wellId + "and the well is " + str(well.headers()) + str(well.data())



@app.errorhandler(404)
def not_found(error):
    return render_template('404.html')
