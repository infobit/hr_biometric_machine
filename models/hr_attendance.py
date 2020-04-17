# -*- encoding: utf-8 -*-
from openerp import api, models, fields, _
from openerp.exceptions import except_orm, Warning, RedirectWarning
import datetime


class hr_attendance(models.Model):
	_name = "hr.attendance"
	_inherit = "hr.attendance"


	#anulamos control de entrada salida
        def _altern_si_so(self, cr, uid, ids, context=None):
                return True

        _constraints = [(_altern_si_so, 'Error ! Sign in (resp. Sign out) must follow Sign out (resp. Sign in)', ['action'])]
  
	def updateAttendance(self):
		att_ids = self.env['biometric.data'].search([('state','=','pending')],order='name')
		for att in att_ids:
			employee = self.env['hr.employee'].search([('emp_code','=',att.emp_code)],limit=1)
			if employee.turn_day:
				#Comprobar ultima asistencia para cerrar día
				last_att = self.env['hr.attendance'].search([('employee_id','=',employee.id)],limit=1)
				if last_att:
					last_date = datetime.datetime.strptime(last_att.name,"%Y-%m-%d %H:%M:%S")
					att_date = datetime.datetime.strptime(att.name,"%Y-%m-%d %H:%M:%S")
					# ultima asistencia mas antigua y la nueva no es del mismo dia
					if last_date < att_date and last_date.strftime('%d') != att_date.strftime('%d'):
						#creamo asistencia fecha ultima asistencia a la 23:00 para cerrar turno
						if employee.state == 'present':
		       	                        	self.create({'employee_id':employee.id,'name':last_date.replace(hour=21,minute=59),'action':'sign_out'})

				
      	                if employee.state == 'absent' and att.state == 'pending':
               	        	self.create({'employee_id':employee.id,'name':att.name,'action':'sign_in'})
                       	        att.state='count'
                        elif employee.state == 'present' and att.state == 'pending':
       	                        self.create({'employee_id':employee.id,'name':att.name,'action':'sign_out'})
               	                att.state='count'



	#Dowload attendence data regularly
	@api.model
	def schedule_attendance(self):
	    self.updateAttendance()

