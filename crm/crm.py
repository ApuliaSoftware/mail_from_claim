# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Apulia Software
#    Authors: Francesco Apruzzese <f.apruzzese@apuliasoftware.it>
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

CLAIM_TYPE_ACTION = {
    'correction': 'Correttiva',
    'prevention': 'Preventiva',
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
        # ----- Second value in tupla set if the field is a relation field type
        # ----- Third value in tupla set iof the real value of field is in a dict
        fields_list = {'name': ('Oggetto', False, {}),
                       'date': ('Data', False, {}),
                       'date_deadline': ('Data Scadenza', False, {}),
                       'state': ('Stato', False, CLAIM_STATES),
                       'partner_id': ('Segnalato da', True, {}),
                       'partner_phone': ('Telefono', False, {}),
                       'email_from': ('Email', False, {}),
                       'user_fault': ('Responsabile Problematiche', False, {}),
                       'description': ('Descrizione Reclamo', False, {}),
                       'date_action_next': ('Data Prossima Azione', False, {}),
                       'action_next': ('Prossima Azione', False, {}),
                       'date_closed': ('Data Chiusura', False, {}),
                       'cause': ('Cause', False, {}),
                       'type_action': ('Azione risolutiva', False,
                                       CLAIM_TYPE_ACTION),
                       'resolution': ('Risoluzione', False, {}),
                       }
        for fl in fields_list:
            if claim[fl]:
                if fields_list[fl][1]:
                    content = claim[fl]['name']
                else:
                    content = claim[fl]
                    if fields_list[fl][2]:
                        if content in fields_list[fl][2].keys():
                            content = fields_list[fl][2][content]
                body = '%s<b>%s</b>: %s<br />' % (body, fields_list[fl][0],
                                                  content)
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
