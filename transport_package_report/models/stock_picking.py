from odoo import api, models, fields
import io
import xlwt
import os
import base64
class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    product_packages_ids = fields.One2many("product.packages", "picking_id")

    def print_transport_excel(self):
        book = xlwt.Workbook(encoding="utf-8")
        file_name = "Transport Package Report - %s"%fields.Datetime.now()
        filename = '/tmp/%s' % (file_name)
        try:
            os.remove(filename)
        except OSError:
            pass
        rec = self[0]
        sheet = book.add_sheet("Transport Package Report", cell_overwrite_ok=True)
        sheet.col(0).width = 256 * 30
        sheet.col(1).width = 256 * 30
        sheet.write(1, 0, 'Company Name')
        sheet.write(1, 1, rec.company_id.name)
        sheet.write(1, 2, 'Created On')
        sheet.write(1, 3, str(fields.Datetime.now().date()))
        
        sheet.write(3, 0, 'Product Packages')
        sheet.write(4, 0, 'Product')
        sheet.write(4, 1, 'Quantity')
        sheet.write(4, 2, 'Unit')
        
        total_packages = {}
        
        product_packages = {}
        for rec in self:
            for move_id in rec.move_ids:
                qty = move_id.quantity
                for package in move_id.product_id.product_packages_ids.filtered(lambda x:(rec.picking_type_code == 'incoming' and x.is_po) or (rec.picking_type_code == 'outgoing' and x.is_so)):
                    if '%s|%s'%(package.product_id.name,package.uom_id.name) in product_packages :
                        product_packages['%s|%s'%(package.product_id.name,package.uom_id.name)] = product_packages.get('%s|%s'%(package.product_id.name,package.uom_id.name)) + (qty*package.contained_quantity)
                        
                        total_packages['%s|%s'%(package.product_id.name,package.uom_id.name)] = total_packages.get('%s|%s'%(package.product_id.name,package.uom_id.name)) + (qty*package.contained_quantity)
                        
                    else:
                        product_packages['%s|%s'%(package.product_id.name,package.uom_id.name)] = (qty*package.contained_quantity)
                        total_packages['%s|%s'%(package.product_id.name,package.uom_id.name)] = (qty*package.contained_quantity)
        row = 5
        for product_package in product_packages:
            product,uom = product_package.split('|')
            sheet.write(row, 0, product)
            sheet.write(row, 1, product_packages.get(product_package))
            sheet.write(row, 2, uom)
            row += 1
        
        row += 1
        
        sheet.write(row, 0, 'Transport Packages')
        sheet.write(row+1, 0, 'Product')
        sheet.write(row+1, 1, 'Quantity')
        sheet.write(row+1, 2, 'Unit')
        
        product_packages = {}
        for rec in self:
            for package in rec.product_packages_ids:
                if '%s|%s'%(package.product_id.name,package.uom_id.name) in product_packages :
                    product_packages['%s|%s'%(package.product_id.name,package.uom_id.name)] = product_packages.get('%s|%s'%(package.product_id.name,package.uom_id.name)) + (package.contained_quantity)
                else:
                    product_packages['%s|%s'%(package.product_id.name,package.uom_id.name)] = (package.contained_quantity)
                
                if '%s|%s'%(package.product_id.name,package.uom_id.name) in total_packages :
                    total_packages['%s|%s'%(package.product_id.name,package.uom_id.name)] = total_packages.get('%s|%s'%(package.product_id.name,package.uom_id.name)) + (package.contained_quantity)
                else:
                    total_packages['%s|%s'%(package.product_id.name,package.uom_id.name)] = (package.contained_quantity)
        
        row += 2
        for product_package in product_packages:
            product,uom = product_package.split('|')
            sheet.write(row, 0, product)
            sheet.write(row, 1, product_packages.get(product_package))
            sheet.write(row, 2, uom)
            row += 1
        
        row += 1
        sheet.write(row, 0, 'Total Packages')
        sheet.write(row+1, 0, 'Product')
        sheet.write(row+1, 1, 'Quantity')
        sheet.write(row+1, 2, 'Unit')
        
        row += 2
        for product_package in total_packages:
            product,uom = product_package.split('|')
            sheet.write(row, 0, product)
            sheet.write(row, 1, total_packages.get(product_package))
            sheet.write(row, 2, uom)
            row += 1
            
        book.save(filename)
        with open(filename, "rb") as excel_file:
            generated_file = base64.b64encode(excel_file.read())
        vals = {
            'type':'binary',
            'datas':generated_file,
            'res_model':'stock.picking',
            'name':file_name
        }
        att = self.env['ir.attachment'].create(vals)
        url = ('web/content/?model=ir.attachment&download=true&field=datas&id=%s&filename=%s.xls' % (att.id, file_name))
        return {
                'type': 'ir.actions.act_url',
                'url': url,
                'target': 'new'
            }
        
