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

{
    'name': "Send Mail From Crm.Claim",
    'version': '0.1',
    'category': 'CRM',
    'description': """This module allow to send mail, from
crm_claim object""",
    'author': 'Andre@ <a.gallina@cgsoftware.it>',
    'website': 'www.apuliasoftware.it',
    'license': 'AGPL-3',
    "depends": ['crm'],
    "init_xml": ['crm/crm_claim_view.xml'],
    "active": False,
    "installable": True
}
