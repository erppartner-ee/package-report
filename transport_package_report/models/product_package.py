from odoo import models, fields, api, _

class ProductPackages(models.Model):
    _name = "product.packages"
    _description = "Product Packages"

    picking_id = fields.Many2one("stock.picking", string="Picking")
    product_tmpl_id = fields.Many2one("product.template", string="Product")
    product_id = fields.Many2one("product.template", string="Packages")
    contained_quantity = fields.Float("Contained Quantity")
    uom_id = fields.Many2one("uom.uom", string="Unit of Measure",related="product_id.uom_id")
    is_so = fields.Boolean("Is Sales")
    is_po = fields.Boolean("Is Purchase")
    company_id = fields.Many2one("res.company", string="Company")


