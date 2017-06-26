
# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
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

from openerp import models, fields, api, _
from openerp import tools


class report_daily_attendance(models.Model):
    _name = "report.daily.attendance"
    _auto = False

    name = fields.Many2one('hr.employee','Employee')
    day = fields.Date('Date')
    address_id = fields.Many2one('res.partner', 'Working Address')
    category = fields.Char('category')
    punch = fields.Integer('Number of Punch')
    in_punch = fields.Datetime('In Punch')
    out_punch = fields.Datetime('Out Punch')

    _order = 'day desc'

    def init(self):
        tools.drop_view_if_exists(self._cr, 'report_daily_attendance')
        cr.execute("""
            create or replace view report_daily_attendance as (
                select
                    min(id) as id,
                    employee_id as name,
                    Count(day) as punch,
                    day as day,
                    address_id as address_id,
                    category as category,
                    min(name) as in_punch ,
                    case when min(name) != max(name) then max(name)  end as out_punch
                from
                    hr_attendance
                GROUP BY
                    employee_id,day,address_id,category
            )
        """)
