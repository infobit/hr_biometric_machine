# -*- encoding: utf-8 -*-
from openerp import api, models, fields, _
from openerp.exceptions import except_orm, Warning, RedirectWarning
import logging

_logger = logging.getLogger(__name__)

class hr_attendance(models.Model):
	_name = "hr.attendance"
	_inherit = "hr.attendance"


	def updateAttendance(self):
		att_ids = self.env['biometric.data'].search([('state','=','pending')],order='name')
		#raise Warning((att_ids))
		#scheduler_line_obj = self.env['biometric.machine']
		#scheduler_lines = self.env['biometric.machine'].search([])
		#for scheduler_line in scheduler_lines:
		#for att in scheduler_line.atten_ids:
		for att in att_ids:
		#buscar empleado
			employee = self.env['hr.employee'].search([('barcode','=',att.emp_code)])
			#buscar asistencia para el empleado x con entrada o salida igual a la fecha
			a = self.env['hr.attendance'].search(['|',('check_in','=',att.name),('check_out','=',att.name),('employee_id','=',employee.id)])
			last = self.env['hr.attendance'].search([('employee_id','=',employee.id)])
			#entrada creo nueva entrada
			# si no existe asistancia en la hora fichamos
			if not a:
				#empleado tiene que marcar una salida y la asistencia no a sido procesada
				if employee.attendance_state == 'checked_out' and att.state == 'pending': #and att.name > last[0].check_out:
					_logger.error('creada entrada %s para %s', att.name, employee.barcode)
					self.create({'employee_id':employee.id,'check_in':att.name})
					att.state='count'
				#raise Warning (("asistencias",last[0].check_out,att.name,last[0].check_out < att.name))
				#salida grabo salida en ultima entrada
				#empleado tiene que marcar una entrada y la asistencia no a sido procesada
				elif employee.attendance_state == 'checked_in' and att.state == 'pending': #and att.name > last[0].check_in:
					_logger.error('creada salida %s para %s', att.name,employee.barcode)
					attendance = self.search([('employee_id','=',employee.id)])
					_logger.error('salida %s para %s hora entrada %s', attendance[0],employee.barcode,attendance[0].check_in)
					attendance[0].check_out=att.name
					att.state='count'
			#si existe la marco como repetido
			else:
				if not att.state == 'count':
					att.state = 'repeated'



	#Dowload attendence data regularly
	@api.model
	def schedule_attendance(self):
		self.updateAttendance()

