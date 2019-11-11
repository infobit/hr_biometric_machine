# -*- encoding: utf-8 -*-
from openerp import api, models, fields, _
from openerp.exceptions import except_orm, Warning, RedirectWarning


class hr_attendance(models.Model):
	_name = "hr.attendance"
	_inherit = "hr.attendance"
  
	def updateAttendance(self):
	    	"""scheduler_line_obj = self.env['biometric.machine']
            	scheduler_lines = self.env['biometric.machine'].search_read([],['atten_ids'])
	            for scheduler_line in scheduler_lines:
			    for att in scheduler_line['atten_ids']:
				    attendance = self.env['biometric.data'].search([('id','=',att)])

				    employee = self.env['hr.employee'].search([('emp_code','=',attendance.emp_code)])
				    if employee.state == 'absent' and attendance.state == 'pending':
				            self.create({'employee_id':employee.id,'name':attendance.name,'action':'sign_in'})
					    attendance.state='count'
				    elif employee.state == 'present' and attendance.state == 'pending':
				            self.create({'employee_id':employee.id,'name':attendance.name,'action':'sign_out'})
					    attendance.state='count'
		"""
		att_ids = self.env['biometric.data'].search([('state','=','pending')],order='name')
		for att in att_ids:
			employee = self.env['hr.employee'].search([('emp_code','=',att.emp_code)])
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
	"""def schedule_attendance(self, cr, uid, context=None):
            scheduler_att_obj = self.pool.get('hr.attendance')
            scheduler_att_ids = self.pool.get('hr.attendance').search(cr, uid, [])
            for scheduler_att_id in scheduler_att_ids:
                scheduler_att =scheduler_att_obj.browse(cr, uid,scheduler_att_id,context=None)
                try:
                    scheduler_att.updateAttendance()
                except:
                    raise Warning(('Warning !'),("Machine with %s is not connected" %(scheduler_line.name)))"""

