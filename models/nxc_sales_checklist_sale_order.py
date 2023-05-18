from odoo import api, fields, models

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    #Sales Checklist Status Indicator
    sales_checklist_status = fields.Selection([
        ('blocked','In-Progress'),
        ('done','Done'),
    ], string="Checklist Status")
    
    #Feasiblity Review Checklist items
    feasibility_review_item_1 = fields.Boolean(string="Product(s) is/are Adequately Defined")
    feasibility_review_item_2 = fields.Boolean(string="Product(s) can be manufactured as designed/specified")
    feasibility_review_item_3 = fields.Boolean(string="Any special characteristics have been identified")
    feasibility_review_item_4 = fields.Boolean(string="Product performance requirements can be met")
    feasibility_review_item_5 = fields.Boolean(string="Statutory and regulatory requirements understood and can be met")
    feasibility_review_item_6 = fields.Boolean(string="Any nonstandard manufacturing methods are defined")
    feasibility_review_item_7 = fields.Boolean(string="Product meets customer-defined objectives (Price & Timing)")
    feasibility_review_item_8 = fields.Boolean(string="Product meets our goals for cost and margin")
    feasibility_review_item_9 = fields.Selection([
        ('1','NOT Feasible - Revisions Required'),
        ('2','Feasible - Revisions Recommended'),
        ('3','Feasible - No Revisions Needed'),
    ], string="Feasability Rating")
    device_master_record_complete = fields.Boolean(string="Device Master Record (DMR) completed")
    feasibility_remarks = fields.Html(string="Remarks")
    feasibility_review_complete = fields.boolean(string="Feasbility Review Complete")

    #Contract Review Checklist items
    contract_review_item_1 = fields.Boolean(string="Product Category is Accurately Configured")
    contract_review_item_2 = fields.Boolean(string="Quantities are Correct")
    contract_review_item_3 = fields.Boolean(string="Payment Terms are Correct")
    contract_review_item_4 = fields.Boolean(string="Pricing is Correct for Required Quantities")
    contract_review_item_5 = fields.Boolean(string="Latest CAD Data & Associated Specs Available")
    contract_review_item_6 = fields.Boolean(string="Customer Identity is Correct")
    contract_review_item_7 = fields.Boolean(string="Customer is Aware of Potential Risks")
    contract_review_item_8 = fields.Boolean(string="Delivery Date / Lead Time(s) Confirmed")
    contract_review_complete = fields.Boolean(string="Contract Review Complete")

    def _block_order_confirm_in_draft(self):
        action = self.env['ir.actions.server'].sudo().create({
            'name': 'block_order_confirm_in_draft',
            'type': 'ir.actions.server',
            'model_id': self._name,
            'trigger': 'on_update',
            'target': 'self',
            'action': 'block_order_confirm',
            'domain': [
                ['state', '=', 'draft'],
            ],
            'apply_on': [
                ['state', '=', 'sale'],
            ],
        })

        for record in self:
            if record.x_studio_sales_checklist_status == 'blocked':
                record.state = 'draft'
                record.message_post(body="Cannot confirm Quotation: Awaiting sales checklists completion.")

        return action
    
    def _block_order_confirm_in_sent(self):
        action = self.env['ir.actions.server'].sudo().create({
            'name': 'block_order_confirm_in_sent',
            'type': 'ir.actions.server',
            'model_id': self._name,
            'trigger': 'on_update',
            'target': 'self',
            'action': 'block_order_confirm',
            'domain': [
                ['state', '=', 'sent'],
            ],
            'apply_on': [
                ['state', '=', 'sale'],
            ],
        })

        for record in self:
            if record.x_studio_sales_checklist_status == 'blocked':
                record.state = 'sent'
                record.message_post(body="Cannot confirm Quotation: Awaiting sales checklists completion.")

        return action