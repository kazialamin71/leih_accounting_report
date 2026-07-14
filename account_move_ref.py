from openerp.osv import osv


class account_move(osv.osv):
    _inherit = 'account.move'

    def write(self, cr, uid, ids, vals, context=None):
        res = super(account_move, self).write(cr, uid, ids, vals, context=context)

        if 'ref' in vals:
            if isinstance(ids, (int, long)):
                ids = [ids]

            line_obj = self.pool.get('account.move.line')
            line_ids = line_obj.search(
                cr, uid, [('move_id', 'in', ids)], context=context)

            if line_ids:
                cr.execute(
                    "UPDATE account_move_line SET ref = %s WHERE id IN %s",
                    (vals['ref'], tuple(line_ids)))
                line_obj.invalidate_cache(cr, uid, ['ref'], line_ids, context=context)

        return res