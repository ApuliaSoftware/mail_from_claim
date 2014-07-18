# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Andre@ (<a.gallina@cgsoftware.it>)
#    All Rights Reserved
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from osv import osv
from tools.translate import _

CLAIM_STATES = {
    'draft': 'Nuovo',
    'cancel': 'Cancellato',
    'open': 'In corso',
    'pending': 'In sospeso',
    'done': 'Chiuso',
    }

class crm_claim(osv.osv):

    _inherit = "crm.claim"

    def action_send_mail(self, cr, uid, ids, context=None):
        '''
        This function opens a window to compose an email
        '''
        assert len(ids) == 1, 'This option should only be \
                               used for a single id at a time.'
        ir_model_data = self.pool.get('ir.model.data')
        try:
            compose_form_id = ir_model_data.get_object_reference(
                cr, uid, 'mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False
        claim = self.browse(cr, uid, ids, context)[0]
        if context is None: context = {}
        subject = '[%s] Segnalazione del %s' % (CLAIM_STATES[claim.state],
                                                claim.date or '')
        body = ''
        if claim.name:
            body = '%s<b>Oggetto</b>: %s<br />' % (body, claim.name)
        if claim.date:
            body = '%s<b>Data</b>: %s<br />' % (body, claim.date)
        if claim.state:
            body = '%s<b>Stato</b>: %s<br />' % (body, claim.state)
        if claim.date_action_next:
            body = '%s<b>Data Prossima Azione</b>: %s<br />' % (body, claim.date_action_next)
        if claim.action_next:
            body = '%s<b>Prossima Azione</b>: %s<br />' % (body, claim.action_next)
        if claim.date_closed:
            body = '%<b>sData Chiusura</b>: %s<br />' % (body, claim.date_closed)
        if claim.cause:
            body = '%s<b>Cause</b>: %s<br />' % (body, claim.cause)
        if claim.resolution:
            body = '%s<b>Risoluzione</b>: %s<br />' % (body, claim.resolution)
        context.update({
            'default_model': 'crm.claim',
            'default_res_id': ids[0],
            'default_partner_ids': [claim.user_id.partner_id.id],
            'default_body': body,
            'default_subject': subject,
            'mark_so_as_sent': True,
            'default_state': 'outgoing',
        })
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': context,
        }
