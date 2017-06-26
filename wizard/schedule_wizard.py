from openerp import models, fields, api, _


class configure_attendence(models.TransientModel):
    _name = "configure.attendance"
    interval_number = fields.Integer(
		string="Interval Number",
		default = lambda self: self._get_interval_number())

    interval_type = fields.Selection([('minutes','Minutes'),
	('hours','Hours'),
	('work_days','Work Days'),
	('days','Days'),
	('weeks','Weeks'),
	('months','Months')],
	string="Interval Unit", 
	default = lambda self: self._get_interval_type())

    @api.model
    def _get_interval_number(self):
        line_id = self.env['ir.cron'].search([('name','ilike','Download Attendence')])
        return line_id.interval_number

    @api.model
    def _get_interval_type(self):
        line_id = self.env['ir.cron'].search([('name','ilike','Download Attendence')])
        return line_id.interval_type


    def update_interval(self):
        interval_number = self.interval_number
        interval_type = self.interval_type

        line_id = self.env['ir.cron'].search([('name','ilike','Download Attendence')])
        #schedule_obj = self.pool.get('ir.cron').browse(cr,uid,line_id)
        line_id.write({'interval_number': interval_number,'interval_type':interval_type})


