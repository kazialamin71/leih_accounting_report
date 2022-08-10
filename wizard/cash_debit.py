
import time
from openerp.osv import osv, fields


class cash_debit(osv.osv_memory):
    _name = 'cash.debit'
    _description = 'Cash Debit Report '

    _columns = {
        'date_start': fields.date('Date Start', required=True),
        'date_end': fields.date('Date End', required=True),
    }


    def print_report(self, cr, uid, ids, context=None):

        if context is None:
            context = {}
        datas = {'ids': context.get('active_ids', [])}
        res = self.read(cr, uid, ids, ['date_start', 'date_end',], context=context)
        res = res and res[0] or {}

        datas['form'] = res
        if res.get('id',False):
            datas['ids']=[res['id']]



        return self.pool['report'].get_action(cr, uid, [], 'leih_accounting_report.report_cash_debit', data=datas, context=context)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
