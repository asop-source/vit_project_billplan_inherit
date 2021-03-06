#-*- coding: utf-8 -*-

{
	"name": "Vit project billplan inherit",
	"version": "1.0", 
	"depends": [
		'vit_project_billplan',
		'sale',


	],
	"author": "Akhmad D. Sembiring [vitraining.com]",
	"category": "Utility",
	"website": "http://vitraining.com",
	"images": ["static/description/images/main_screenshot.jpg"],
	"price": "10",
	"license": "OPL-1",
	"currency": "USD",
	"summary": "This is the Vit project billplan inherited module generated by StarUML Odoo Generator Pro Version",
	"description": """

Information
======================================================================

* created menus
* created objects
* created views
* logics

""",
	"data": [
		"view/project.xml",
		"view/billplan.xml",
		# "view/analytic.xml",
		"data/ir_sequence.xml",
		"data/paperformat_template.xml",
		"security/ir.model.access.csv",

	],
	"installable": True,
	"auto_install": False,
	"application": True,
}