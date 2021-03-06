from flask import Blueprint, request, config, render_template

import config
from .main import get_proddate

from src.util.data_dictionary import resolve_lookups_in_description

lookups = Blueprint('lookups', __name__)


@lookups.route('/lookups/help')
def app_help():
    help_item = request.args['item']
    try:
        db = config.get_database()
        v = help_item.split('.')
        data = db.select1('DataDictionary', TableName=v[0], Attribute=v[1])
        if not data.Documentation:
            data.Documentation = 'Help text has not been entered for ' + help_item
        else:
            data.Documentation = resolve_lookups_in_description(data.Documentation)
        return data.Documentation
    except Exception as e:
        print(e)
        return 'Help text not found in the Data Dictionary...'


@lookups.route('/lookups/ba')
def ba():
    return render_template('lookups/ba.html')


@lookups.route('/lookups/band')
def band():
    try:
        db = config.get_database()
        statement = """SELECT * FROM FNBand
                       WHERE FNBandName LIKE "%{bandname}%"
                    """.format(bandname=request.args['FNBandName'])
        results = db.select_sql(statement)
        return render_template('lookups/band_results.html', results=results)
    except Exception as e:
        print(e)
        return 'Something went wrong fetching bands'


@lookups.route('/lookups/ba_results')
def ba_results():
    db = config.get_database()
    statement = """SELECT * FROM BAInfo
                    WHERE (DATE('{proddate}') BETWEEN BAInfo.StartDate AND BAInfo.EndDate OR
                    BAInfo.StartDate IS NULL)""".format(proddate=get_proddate())
    argument_tables = {'CorpLegalName': 'BAInfo', 'BAType': 'BAInfo', 'BAid': 'BAInfo'}
    kwargs = dict((k, v) for k, v in request.args.items() if v)  # this is to get rid of empty values coming from forms
    search_arguments = ""
    for arg in kwargs:
        if arg in argument_tables:
            compound = argument_tables[arg] + '.' + arg + '=' + '"' + kwargs[arg] + '"'
            if arg == 'CorpLegalName':
                compound = argument_tables[arg] + '.' + arg + ' LIKE ' + '"%' + kwargs[arg] + '%"'
            search_arguments += " AND " + compound
    print(statement + search_arguments)
    results = db.select_sql(statement + search_arguments)
    return render_template('lookups/ba_results.html', results=results)
