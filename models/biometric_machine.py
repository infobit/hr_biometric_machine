from openerp import api, models, fields, _
from datetime import datetime , timedelta
from zklib import zklib
from openerp.tools.translate import _
import time
from zklib import zkconst

import pytz, datetime
from pytz import timezone
from datetime import datetime

import logging

_logger = logging.getLogger(__name__)



class biometric_machine(models.Model):
    _name= 'biometric.machine'

    name = fields.Char("Machine IP")
    ref_name = fields.Char("Location")
    port = fields.Char("Port Number")
    address_id = fields.Many2one("res.partner",'Working Address')
    company_id = fields.Many2one("res.company","Company Name")
    atten_ids = fields.One2many('biometric.data','mechine_id','Attendance')

    def download_attendance(self):
	machine_ip = self.name
	port = self.port

	_logger.debug('CONEXION MAQUINA %s : %s',machine_ip,port)

        zk = zklib.ZKLib(machine_ip, int(port))
        res = zk.connect()

	local = pytz.timezone ("Europe/Madrid")
        if res == True:
            zk.enableDevice()
            zk.disableDevice()
            attendance = zk.getsAtt(machine_ip)

            biometric_data = self.env['biometric.data']
 	    _logger.debug('FASISTENCIAS %s',attendance)

            if (attendance):
                for lattendance in attendance:
		    naive = local.localize(lattendance[1],is_dst=None)
		    exist=biometric_data.search([
			('name','=',str(naive.astimezone(timezone('UTC')))),
			('emp_code','=',lattendance[0])])
		    if not exist:
		            a = biometric_data.create({'name':naive.astimezone(timezone('UTC')) ,'emp_code':lattendance[0],'mechine_id':self.id,'state':'pending'})
			    _logger.debug('FICHADA %s : %s',lattendance[0],naive.astimezone(timezone('UTC')))

	    #zk.clearAttendance()
            zk.enableDevice()
            zk.disconnect()
            return True
        else:
            raise Warning(_('Warning !'),_("Unable to connect, please check the parameters and network connections."))
	    _logger.debug('ERROR CONEXION MAQUINA %s : %s',machine_ip,port)
            zk.enableDevice()
            zk.disconnect()
	    return False


    #Dowload attendence data regularly
    @api.model
    def schedule_download(self):
            scheduler_line_ids = self.env['biometric.machine'].search([])
            _logger.debug('MAQUINA ENCONTRADA %s',scheduler_line_ids)
            for scheduler_line_id in scheduler_line_ids:
                scheduler_line = scheduler_line_id
                _logger.debug('MAQUINA %s',scheduler_line)
                try:
                    scheduler_line.download_attendance()
                except:
                    raise Warning(('Warning !'),("Machine with %s is not connected" %(scheduler_line.name)))


    def clear_attendance(self):
        machine_ip = self.name
        port = self.port
        zk = zklib.ZKLib(machine_ip, int(port))
        res = zk.connect()
        if res == True:
            zk.enableDevice()
            zk.disableDevice()
            zk.clearAttendance()
            zk.enableDevice()
            zk.disconnect()
            return True
        else:
            raise Warning(_('Warning !'),_("Unable to connect, please check the parameters and network connections."))


class biometric_data(models.Model):
    _name = "biometric.data"
    name = fields.Datetime(string='Date')
    emp_code = fields.Char(string='Employee Code')
    mechine_id = fields.Many2one('biometric.machine','Mechine No')
    state = fields.Selection([('pending','Pending'),('count','Count'),('repeated','Repeated')])
