from odoo import models, fields, api, _

class ProductTemplate(models.Model):
    _inherit = "product.template"
    
    product_packages_ids = fields.One2many("product.packages", "product_tmpl_id")
