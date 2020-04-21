#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import Warning
import time
from datetime import datetime, timedelta



STATES = [('open','Open'), ('baut','BAUT'), ('bast','BAST'), ('close','Close'), ('cancel','Cancel')]

class bill_plan(models.Model):
	_name = 'vit_project_billplan.bill_plan'
	_inherit = "vit_project_billplan.bill_plan"

	no_bast = fields.Char(string="Nomor BAST", states={'bast': [('readonly', False),('required', True)], 'open': [('readonly', True)], 'baut': [('readonly', True)], 'close': [('readonly', True)], 'cancel': [('readonly', True)]})
	no_baut = fields.Char(string="Nomor BAUT", states={'baut': [('readonly', False),('required', True)], 'open': [('readonly', True)], 'bast': [('readonly', True)], 'close': [('readonly', True)], 'cancel': [('readonly', True)]})
	bast_date = fields.Date( string="BAST Date", help="", states={'bast': [('readonly', False),('required', True)], 'open': [('readonly', True)], 'baut': [('readonly', True)], 'close': [('readonly', True)], 'cancel': [('readonly', True)]})
	baut_date = fields.Date( string="BAUT Date", help="", states={'baut': [('readonly', False),('required', True)], 'open': [('readonly', True)], 'bast': [('readonly', True)], 'close': [('readonly', True)], 'cancel': [('readonly', True)]})
	description = fields.Text(string="Deskripsi Fase")
	state = fields.Selection(string="State", selection=STATES, required=True, readonly=True, default=STATES[0][0])
	@api.multi
	def action_baut(self):
		self.write({'state': STATES[1][0]})
	@api.multi
	def action_bast(self):
		self.write({'state': STATES[2][0]})
	@api.multi
	def action_close(self):
		self.write({'state': STATES[3][0]})
	@api.multi
	def action_cancel(self):
		self.write({'state': STATES[4][0]})

class bill_planxlsx(models.AbstractModel):
	_name = 'report.vit_report_aging_billplan.bill_plan_xlsx'
	_inherit = 'report.report_xlsx.abstract'

	bill_id = fields.Many2one(comodel_name="vit_project_billplan.bill_plan")

	def generate_xlsx_report(self, workbook, data, lines):
		print("lines", lines, data)
		format0 = workbook.add_format({'font_size':14,'align':'vcenter','bold':True})
		format1 = workbook.add_format({'font_size':10,'align':'vcenter', 'bold':True})
		format2 = workbook.add_format({'font_size':10,'align':'vcenter'})
		date_1 = datetime.strftime(lines.date, '%d-%m-%Y')
		plan_date_1 = datetime.strftime(lines.plan_date, '%d-%m-%Y')
		baut_date = datetime.strftime(lines.baut_date, '%d-%m-%Y') if lines.baut_date else ''
		bast_date = datetime.strftime(lines.bast_date, '%d-%m-%Y') if lines.bast_date else ''
		y = lines.project_id.total_revenue
		x = lines.amount
		z = y-x
		fmt = '%Y-%m-%d'
		# if lines.bast_date != True:
		#   receive_date = 0
		# # if lines.bast_date
		#   start = datetime.strptime(lines.bast_date, fmt)
		#   sub = datetime.strptime(lines.date, fmt)
		#   receive_date = start - sub
		# else ''
		# lines = self.env['vit_project_billplan.bill_plan'].browse(self.id)
		sheet = workbook.add_worksheet('Report Billplan')
		sheet.write(0, 0, 'Report Billplan', format0)   
		sheet.write(4, 0, 'ID Project', format1)
		sheet.write(4, 1, 'Tanggal Periode', format1)
		sheet.write(4, 2, 'Unit', format1)
		sheet.write(4, 3, 'Wilayah', format1)
		sheet.write(4, 4, 'Bisnis', format1)
		sheet.write(4, 5, 'Jenis Project', format1)
		sheet.write(4, 6, 'Customer', format1)
		sheet.write(4, 7, 'Afiliasi', format1)
		sheet.write(4, 8, 'Nomor Billplan', format1)
		sheet.write(4, 9, 'Reference', format1)
		sheet.write(4, 10, 'Tanggal Billplan', format1)
		sheet.write(4, 11, 'Rencana Penagihan', format1)
		sheet.write(4, 12, 'Description Fase', format1)
		sheet.write(4, 13, 'Nilai Revenue', format1)
		sheet.write(4, 14, 'Nilai ID Project', format1)
		sheet.write(4, 15, 'Sisa ID Project', format1)
		sheet.write(4, 16, 'Nomor BAUT', format1)
		sheet.write(4, 17, 'Tanggal BAUT', format1)
		sheet.write(4, 18, 'Nomor BAST', format1)
		sheet.write(4, 19, 'Tanggal BAST', format1)
		sheet.write(4, 20, 'Status Fase', format1)
		sheet.write(4, 21, 'Umur Billplan(Days)', format1)
		# for row in lines:
		

		# for xi in range(0,22):
		sheet.write(5, 0, lines.name, format2)
		sheet.write(5, 1, date_1, format2)
		sheet.write(5, 2, lines.unit_id.name, format2)
		sheet.write(5, 3, lines.analytic_tag_ids.name, format2)
		sheet.write(5, 4, lines.analytic_tag_ids_b.name, format2)
		sheet.write(5, 5, lines.project_id.project_type_id.name, format2)
		sheet.write(5, 6, lines.project_id.partner_id.name, format2)
		if 'Telkomsel' in lines.project_id.partner_id.name or 'telkomsel' in lines.project_id.partner_id.name or 'TELKOMSEL' in lines.project_id.partner_id.name: 
			sheet.write(5, 7, 'Telkomsel', format2)
		else:
			sheet.write(5, 7, 'Non Telkomsel', format2)
		# if 'T'lines.project_id.partner_id.name != 'Telkomsel' and lines.project_id.partner_id.name != 'telkomsel' and lines.project_id.partner_id.name != 'TELKOMSEL':    
		# sheet.write(5, 8, '[' + lines.analytic_account_id.name + '] ' + lines.project_id.name '-' + lines.analytic_account_id.partner_id.name, format2)
		sheet.write(5, 8, lines.analytic_account_id.name, format2)
		sheet.write(5, 9, lines.reference, format2)
		sheet.write(5, 10, date_1, format2)
		sheet.write(5, 11, plan_date_1, format2)
		sheet.write(5, 12, lines.description, format2)
		sheet.write(5, 13,'{0:,.2f}'.format(x), format2)
		sheet.write(5, 14,'{0:,.2f}'.format(y), format2)
		sheet.write(5, 15,'{0:,.2f}'.format(z), format2)
		sheet.write(5, 16, lines.no_baut, format2)
		sheet.write(5, 17, baut_date, format2)
		sheet.write(5, 18, lines.no_bast, format2)
		sheet.write(5, 19, bast_date, format2)
		# @api.onchange('state')
		# def on_change_type(lines):
		if lines.state == 'open' and lines.no_baut == False:
			sheet.write(5, 20, 'Fase 1', format2)
		if lines.no_baut == False and lines.state == 'baut':
			sheet.write(5, 20, 'Fase 1', format2)
		if lines.no_baut == True:
			sheet.write(5, 20, 'Fase 2', format2)
		if lines.state == 'bast' and lines.no_bast == False:
			sheet.write(5, 20, 'Fase 2', format2)
		if lines.no_bast == True:
			sheet.write(5, 20, 'Fase 3', format2)
		if lines.state == 'close':
			sheet.write(5, 20, 'Fase 3', format2)
		if lines.bast_date == False:
			sheet.write(5, 21, 'BAST belum selesai', format2)
		else:   
			bast_date_2 = str(lines.bast_date)
			date_2 = str(lines.date)
			start = datetime.strptime(bast_date_2, '%Y-%m-%d') 
			sub = datetime.strptime(date_2, '%Y-%m-%d')
			receive_date = start-sub
			sheet.write(5, 21, receive_date, format2)

class bill_plan(models.Model):
	_inherit = "vit_project_billplan.bill_plan"

	name = fields.Char( required=False, readonly=True, string="Name",  help="")
	amount = fields.Float( compute="_calc_total", string="Amount",  help="")
	
	@api.depends('amount','line_ids')
	def _calc_total(self):
		am_total = 0.0
		for amou in self:
			for am in amou.line_ids:
				am_total += am.amount
				amou.amount = am_total

	@api.model
	def create(self, vals):
		vals['name']    = self.env['ir.sequence'].next_by_code('billplan.code')
		new_billplan = super(bill_plan, self).create(vals)
		new_billplan.fill_product()
		return new_billplan

	@api.multi
	def action_create_so(self):
		so_obj = self.env['sale.order']

		order_line = []

		for line in self.line_ids:
			if not line.product_id:
				raise Warning('Product di Project Revenue kosong!')
			order_line.append((0,0,{
				'analytic_account_id': line.bill_plan_id.analytic_account_id.id,
				'unit_id': line.bill_plan_id.unit_id.id,
				'analytic_tag_ids_l': line.bill_plan_id.analytic_tag_ids.id,
				'analytic_tag_ids_b': line.bill_plan_id.analytic_tag_ids_b.id,
				'product_id': line.product_id.id,
				'name':line.name,
				'product_uom_qty': line.quantity,
				'price_unit': line.amount
			}))

		so_obj.create({
			'partner_id': self.project_id.partner_id.id ,
			'date_order': fields.Datetime.now(),
			'billplan_id': self.id,
			'order_line': order_line
		})

	@api.depends('sale_ids')
	def _get_sale_count(self):
		for rec in self:
			rec.sale_count = len(rec.sale_ids)


	sale_count = fields.Integer( string="SO count",  help="", compute="_get_sale_count")
	sale_ids = fields.One2many(comodel_name="sale.order",  inverse_name="billplan_id",  string="SO(s)",  help="")


	@api.multi
	def action_view_sale(self):

		action = self.env.ref('sale.action_orders')
		result = action.read()[0]

		result['context'] = {
			'default_billplan_id': self.id,
			'default_partner_id': self.project_id.partner_id.id,
			# 'default_company_id': self.company_id.id,
			# 'company_id': self.company_id.id
		}
		# choose the view_mode accordingly
		if len(self.sale_ids) > 1 :
			result['domain'] = "[('id', 'in', " + str(self.sale_ids.ids) + ")]"
		else:
			res = self.env.ref('sale.view_order_form', False)
			result['views'] = [(res and res.id or False, 'form')]
			result['res_id'] = self.sale_ids.id or False
		return result

	line_ids = fields.One2many(comodel_name="vit_project_billplan.bill_plan_line", inverse_name="bill_plan_id", string="Line", required=False, )


	@api.multi
	def fill_product(self):
		lines = []
		sql = "delete from vit_project_billplan_bill_plan_line where bill_plan_id=%s"
		self.env.cr.execute(sql, (self.id,))
		# import pdb;pdb.set_trace()
		for project in self.project_id:
			for rev in project.revenue_ids:
				if not rev.product:
						raise Warning('Product di Project Revenue kosong!')
				total_qty = rev.quantity
				# bill_plan = self.search([('project_id','=',rev.name)])
				data_line = self.line_ids.search([('product_id','=',rev.product.id)])
				for x in data_line:
					if x.quantity != rev.quantity and x.unit_price == rev.amount and x.name == rev.name:
						total_qty -= x.quantity
				lines.append( (0,0,{
						'name'      : rev.name,
						'product_id': rev.product.id,
						'quantity'  : total_qty,
						'unit_price': rev.amount,
						'amount'    : rev.amount_total,
					}) )
		print(lines)

		self.line_ids = lines



class billplan_line(models.Model):
	_name = 'vit_project_billplan.bill_plan_line'

	name            = fields.Char(string="Name", required=False, )
	bill_plan_id    = fields.Many2one(comodel_name="vit_project_billplan.bill_plan", string="Bill Plan", required=False, )
	product_id      = fields.Many2one(comodel_name="product.product", string="Product", required=False, )
	quantity        = fields.Float(string="Quantity",  required=False, )
	amount          = fields.Float(compute="_calc_total", string="Amount",  required=False, )
	unit_price      = fields.Float( string="Unit Price",  help="")

	@api.depends('quantity','unit_price')
	def _calc_total(self):
		for rec in self:
			rec.amount = rec.quantity * rec.unit_price
