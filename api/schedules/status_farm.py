#
# Performs a REST call to controller (possibly localhost) of latest farm status.
#

import os
import traceback

from flask import g

from common.config import globals
from common.utils import converters
from api import app
from api.commands import chia_cli
from api import utils

def update():
    if not globals.farming_enabled():
        #app.logger.info("Skipping farm summary status collection on plotting-only instance.")
        return
    with app.app_context():
        try:
            hostname = utils.get_hostname()
            farm_summary = chia_cli.load_farm_summary()
            payload = {
                "hostname": hostname,
                "mode": os.environ['mode'],
                "status": farm_summary.status,
                "plot_count": farm_summary.plot_count,
                "plots_size": converters.str_to_gibs(farm_summary.plot_size),
                "total_chia": farm_summary.total_chia,
                "netspace_size": converters.str_to_gibs(farm_summary.netspace_size),
                "expected_time_to_win": farm_summary.time_to_win
            }
            utils.send_post('/farms/', payload, debug=False)
        except:
            app.logger.info("Failed to load farm summary and send.")
            app.logger.info(traceback.format_exc())