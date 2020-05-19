# -*- encoding: utf-8 -*-
from openerp import api, models, fields, _
from .zklib import *

class hr_employee(models.Model):
	_name = "hr.employee"
	_inherit = "hr.employee"

	emp_code = fields.Char(string="Emp Code")
	emp_rfid = fields.Char(string="RFID")
	emp_psw = fields.Char(string="Password")
	category = fields.Selection(
		[('0000','User'),
		 ('0001','Admin')],
		)
	turn_day = fields.Boolean(string="daily turns", help="Marck if employee end turn in the same day", default = True)


	"""@api.one
	def saveUser(self):
		zk = zklib.ZKLib("192.168.188.202", 4370)
		ret = zk.connect()
		if ret:
			zk.disableDevice()
			zk.setUser(
				uid=self.id,
				userid=str(self.id),
				name=self.name,
				password=str(self.emp_psw),
				role=zkconst.LEVEL_ADMIN)
			zk.enableDevice()
		zk.clearAdmin()"""


