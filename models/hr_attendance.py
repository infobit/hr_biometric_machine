# -*- encoding: utf-8 -*-
from openerp import api, models, fields, _
from openerp.exceptions import except_orm, Warning, RedirectWarning
import logging
import datetime

_logger = logging.getLogger(__name__)

class hr_attendance(models.Model):
	_name = "hr.attendance"
	_inherit = "hr.attendance"


	def updateAttendance(self):
		_logger.error('segunda funcion')
		att_ids = self.env['biometric.data'].search([('state','=','pending')],order='name')
		_logger.error(att_ids)
		for att in att_ids:
			employee = self.env['hr.employee'].search([('emp_code','=',att.emp_code)],limit=1)
			last_att = employee.last_attendance_id
			_logger.error(employee)
			_logger.error(last_att)
			#empleado tiene cierre automatico turno y se encuentra trabajando
			if employee.turn_day and last_att:
				last_date = datetime.datetime.strptime(last_att.check_in,"%Y-%m-%d %H:%M:%S")
				att_date = datetime.datetime.strptime(att.name,"%Y-%m-%d %H:%M:%S")
				#la ultima fecha es mejor que la asistencia y no son del mismo dia y el epleado tiene una entrada
				if last_date < att_date and last_date.strftime('%d') != att_date.strftime('%d') and employee.attendance_state == 'checked_in':
					_logger.error("cierro turno")
					#TODO buscar turno definido y cerrar con la salida del turno si existe
					last_att.check_out = last_date.replace(hour=21,minute=59)
			#empleado tiene que marcar una salida y la asistencia no a sido procesada
			if employee.attendance_state == 'checked_out' and att.state == 'pending': #and att.name > last[0].check_out:
				_logger.error('creada entrada %s para %s', att.name, employee.barcode)
				self.create({'employee_id':employee.id,'check_in':att.name})
				att.state='count'
			#salida grabo salida en ultima entrada
			#empleado tiene que marcar una entrada y la asistencia no a sido procesada
			elif employee.attendance_state == 'checked_in' and att.state == 'pending': #and att.name > last[0].check_in:
				_logger.error('creada salida %s para %s', att.name,employee.barcode)
				attendance = self.search([('employee_id','=',employee.id)])
				_logger.error('salida %s para %s hora entrada %s', attendance[0],employee.barcode,attendance[0].check_in)
				attendance[0].check_out=att.name
				att.state='count'


	#Dowload attendence data regularly
	@api.model
	def schedule_attendance(self):
		_logger.error('primera funcion')
		self.updateAttendance()

