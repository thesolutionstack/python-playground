import sys
import traceback
from flask import Blueprint, request, config, render_template

import config
# from .permission_handler import PermissionHandler
from .main import get_proddate_int
from src.util.apperror import AppError

worksheet = Blueprint('worksheet', __name__)


@worksheet.route('/worksheet')
def calc_worksheet():
    if "ProdDate" in request.args:
        prod_month = int(request.args["ProdDate"])
    else:
        prod_month = get_proddate_int()

    if "RPBA" in request.args:
        rpba = request.args["RPBA"]
    else:
        rpba = None

    if "WellId" in request.args:
        well_id = int(request.args["WellId"])
        return generate_worksheet(well_id, prod_month, rpba)
    elif "WellStart" in request.args and "WellEnd" in request.args and "WellId" not in request.args:
        well_start = int(request.args["WellStart"])
        well_end = int(request.args["WellEnd"])
        result = ""
        for w in range(well_start, well_end + 1):
            result += generate_worksheet(w, prod_month, rpba)
            result += "<hr>"
        return result
    else:
        return "Something wasn't right"

def generate_worksheet(well_id, prod_month, rpba):
    try:
        db = config.get_database()
        product = "Oil"
        well = db.select1('WellRoyaltyMaster', ID=well_id)
        well_lease_link_array = db.select('WellLeaseLink', WellID=well_id)
        if len(well_lease_link_array) == 0:
            raise AppError("There were no well_lease_link records for " + str(well_id) + str(prod_month))
        well_lease_link = well_lease_link_array[0]
        royalty = db.select1('LeaseRoyaltyMaster', ID=well_lease_link.LeaseID)
        lease = db.select1('Lease', ID=well_lease_link.LeaseID)

        if rpba:
            monthly_array = db.select('Monthly', WellID=well_id, prodMonth=prod_month, product=product, RPBA=rpba)
        else:
            monthly_array = db.select('Monthly', WellID=well_id, prodMonth=prod_month, product=product)
        if len(monthly_array) == 0:
            raise AppError("There were no monthly records for " + str(well_id) + str(prod_month) + product)
        monthly = monthly_array[0]

        ba = db.select1('BAInfo',BAid=monthly.RPBA)
        calc = db.select1('Calc', WellID=well_id, ProdMonth=prod_month,RPBA=monthly.RPBA)
        # calc = calc_array[0]
        # print(monthly)
        return render_template('worksheet/calc_worksheet.html',
                               well=well, rm=royalty, m=monthly, lease=lease,
                               calc=calc, well_lease_link=well_lease_link, ba=ba)
    except Exception as e:
        print('views.worksheet: ***Error:', e)
        traceback.print_exc(file=sys.stdout)
        return "<h2>Error displaying worksheet for well %s</h2><br>" % well_id + str(e)
