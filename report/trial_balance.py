from datetime import timedelta
import datetime
import pytz
import time
from openerp import tools
from openerp.osv import osv
from openerp.report import report_sxw


class collcetion_details(report_sxw.rml_parse):

    def _get_user_names(self, t_dat=None, end_date=None):
        st_dat=t_dat
        end_date= end_date
        user_id=self.uid
        adm_info = {}
        bill_other_info = {}
        optic_info = {}
        bill_info = {}
        opd_info = {}

        result = []
        result.append({
            'user_name':'test',
        })


        return result

    def _get_context_text(self, t_dat=None, end_date=None):
        datestr=str(t_dat)

        datetimeobj=datetime.datetime.strptime(datestr, "%Y-%m-%d %H:%M:%S")
        newtime = datetimeobj + timedelta(hours=6)
        newformate=newtime.strftime("%d-%m-%Y %H:%M:%S")

        datestr=str(end_date)

        datetimeobjs=datetime.datetime.strptime(datestr, "%Y-%m-%d %H:%M:%S")
        newtimes = datetimeobjs + timedelta(hours=6)
        newformates=newtimes.strftime("%d-%m-%Y %H:%M:%S")


        # import pdb
        # pdb.set_trace()
        txt = "Start Date " + newformate  + " End Date " + newformates
        return txt

    def __init__(self, cr, uid, name, context):



        super(collcetion_details, self).__init__(cr, uid, name, context=context)

        self.localcontext.update({
            'get_user_names': self._get_user_names,
            'get_user_context': self._get_context_text,
        })


class report_cash_flow(osv.AbstractModel):
    _name = 'report.leih_accounting_report.report_cash_flow'
    _inherit = 'report.abstract_report'
    _template = 'leih_accounting_report.report_cash_flow'
    _wrapped_report_class = collcetion_details
