# -*- encoding: utf-8 -*-
from openerp import api, models, fields, _
from openerp.exceptions import except_orm, Warning, RedirectWarning


class hr_attendance(models.Model):
	_name = "hr.attendance"
	_inherit = "hr.attendance"
  
	def updateAttendance(self):
	    scheduler_line_obj = self.env['biometric.machine']
            scheduler_lines = self.env['biometric.machine'].search_read([],['atten_ids'])
            for scheduler_line in scheduler_lines:
		    for att in scheduler_line['atten_ids']:
			    #raise Warning (att.emp_code)
			    attendance = self.env['biometric.data'].search([('id','=',att)])
			    #raise Warning (attendance)

			    employee = self.env['hr.employee'].search([('emp_code','=',attendance.emp_code)])
			    #employee_id = employee_obj.search([('id','=',attendance.emp_code)])
			    #employee = employee_obj.browse(employee_id)
			    #raise Warning(employee.state)
			    if employee.state == 'absent' and attendance.state == 'pending':
			            self.create({'employee_id':employee.id,'name':attendance.name,'action':'sign_in'})
				    attendance.state='count'
				    #raise Warning('entrada')
			    elif employee.state == 'present' and attendance.state == 'pending':
				    #raise Warning('salida')
			            self.create({'employee_id':employee.id,'name':attendance.name,'action':'sign_out'})
				    attendance.state='count'


	#Dowload attendence data regularly
	def schedule_attendance(self, cr, uid, context=None):
            scheduler_att_obj = self.pool.get('hr.attendance')
            scheduler_att_ids = self.pool.get('hr.attendance').search(cr, uid, [])
            for scheduler_att_id in scheduler_att_ids:
                scheduler_att =scheduler_att_obj.browse(cr, uid,scheduler_att_id,context=None)
                try:
                    scheduler_att.updateAttendance()
                except:
                    raise osv.except_osv(('Warning !'),("Machine with %s is not connected" %(scheduler_line.name)))

