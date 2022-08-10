from datetime import timedelta
import datetime
import pytz
import time
from openerp import tools
from openerp.osv import osv
from openerp.report import report_sxw
import operator


class collcetion_details(report_sxw.rml_parse):

    def _get_user_names(self, t_dat=None, end_date=None):

#         op_query = """
#         select sum(account_move_line.debit), sum(account_move_line.credit), account_move_line.account_id
# from account_move_line, account_move
# where account_move_line.move_id = account_move.id and  account_move_line.account_id in (select id from account_account where user_type=5) and  account_move.date < starts_date
# group by  account_move_line.account_id
#         """


#         query = """
#         select account_move_line.debit,account_move_line.credit,account_move.date,account_move.ref,account_move.name
# from account_move_line, account_move
# where account_move_line.move_id = account_move.id and  account_id in (select id from account_account where user_type=5) limit 100
#         """
        st_dat=t_dat
        end_date= end_date
        result = []
        voucher_info = []

        opening_q = "select sum(account_move_line.debit)as bd,sum(account_move_line.credit) as cr " \
                    "from account_move_line, account_move where account_move_line.move_id = account_move.id and  " \
                    "account_move_line.account_id in (select id from account_account where user_type=5) and account_move.date < %s"

        self.cr.execute(opening_q, (st_dat,))
        for items in self.cr.fetchall():
            voucher_info.append({
                'date': '',
                'ref': 'Opening Balance',
                'name': '',
                'debit': items[0],
                'credit': items[1],
            })

        query="select account_move.date,account_move.ref,account_move.name,account_move_line.debit,account_move_line.credit from account_move_line, " \
              "account_move where account_move_line.move_id = account_move.id and  account_move.journal_id !=8 and account_move.journal_id !=2 and " \
              "account_id in (select id from account_account where user_type=5) and account_move.date <=%s and account_move.date >=%s"

        pos_cash = "select sum(account_move_line.debit)as bd,sum(account_move_line.credit) as cr, account_move.date from account_move_line, " \
                     "account_move where account_move_line.move_id = account_move.id and  account_id in (select id from account_account where user_type=5)" \
                     " and account_move.ref like %s and account_move.date <=%s and account_move.date >=%s group by account_move.date"


        # voucher_info = []



        self.cr.execute(pos_cash, ("POS/%",end_date,st_dat,))
        for items in self.cr.fetchall():
            voucher_info.append({
                'date':items[2],
                'ref': 'Pharmacy Cash',
                'name': '',
                'debit': items[0],
                'credit': items[1],

            })


        self.cr.execute(pos_cash, ("Bill-%",end_date,st_dat,))
        for items in self.cr.fetchall():
            voucher_info.append({
                'date': items[2],
                'ref': 'Bill Cash',
                'name': '',
                'debit': items[0],
                'credit': items[1],

            })

        self.cr.execute(pos_cash, ("OPD-%",end_date,st_dat,))
        for items in self.cr.fetchall():
            voucher_info.append({
                'date': items[2],
                'ref': 'OPD Cash',
                'name': '',
                'debit': items[0],
                'credit': items[1],

            })

        self.cr.execute(pos_cash, ("OPT-%",end_date,st_dat,))
        for items in self.cr.fetchall():
            voucher_info.append({
                'date': items[2],
                'ref': 'Optics Cash',
                'name': '',
                'debit': items[0],
                'credit': items[1],

            })

        self.cr.execute(pos_cash, ("A-%",end_date,st_dat))
        for items in self.cr.fetchall():
            voucher_info.append({
                'date': items[2],
                'ref': 'Admission Cash',
                'name': '',
                'debit': items[0],
                'credit': items[1],

            })

        self.cr.execute(query, (end_date,st_dat))

        for items in self.cr.fetchall():
            voucher_info.append({
                'date': items[0],
                'ref': items[1],
                'name': items[2],
                'debit': items[3],
                'credit': items[4],
            })


        voucher_info = sorted(voucher_info, key=operator.itemgetter('date'))

        return voucher_info


    def _get_context_text(self, t_dat=None, end_date=None):

        txt = "Start Date " + str(t_dat)  + " End Date " + str(end_date)
        return txt

    def __init__(self, cr, uid, name, context):



        super(collcetion_details, self).__init__(cr, uid, name, context=context)

        self.localcontext.update({
            'get_user_names': self._get_user_names,
            'get_user_context': self._get_context_text,
        })


class report_cash_debit(osv.AbstractModel):
    _name = 'report.leih_accounting_report.report_cash_debit'
    _inherit = 'report.abstract_report'
    _template = 'leih_accounting_report.report_cash_debit'
    _wrapped_report_class = collcetion_details
