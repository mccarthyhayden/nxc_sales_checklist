from odoo import api, fields, models

class NxcSalesChecklistSaleOrder(models.Model):
    _inherit = 'sale.order'

    #Sales Checklist Status Indicator
    sales_checklist_status = fields.Selection([
        ('blocked','In-Progress'),
        ('done','Done'),
    ], string="Checklist Status", compute="_compute_sales_checklist_status", tracking = True)
    
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
    ], string="Feasability Rating" )
    device_master_record_complete = fields.Boolean(string="Device Master Record (DMR) completed")
    feasibility_remarks = fields.Html(string="Remarks")
    feasibility_review_complete = fields.Boolean(string="Feasbility Review Complete", compute="_compute_feasibility_review_complete", tracking = True)

    #Contract Review Checklist items
    contract_review_item_1 = fields.Boolean(string="Product Category is Accurately Configured")
    contract_review_item_2 = fields.Boolean(string="Quantities are Correct")
    contract_review_item_3 = fields.Boolean(string="Payment Terms are Correct")
    contract_review_item_4 = fields.Boolean(string="Pricing is Correct for Required Quantities")
    contract_review_item_5 = fields.Boolean(string="Latest CAD Data & Associated Specs Available")
    contract_review_item_6 = fields.Boolean(string="Customer Identity is Correct")
    contract_review_item_7 = fields.Boolean(string="Customer is Aware of Potential Risks")
    contract_review_item_8 = fields.Boolean(string="Delivery Date / Lead Time(s) Confirmed")
    contract_review_complete = fields.Boolean(string="Contract Review Complete", compute="_compute_contract_review_complete", Tracking = True)
    
    @api.onchange('feasibility_review_item_1', 'feasibility_review_item_2', 'feasibility_review_item_3', 'feasibility_review_item_4', 'feasibility_review_item_5', 'feasibility_review_item_6', 'feasibility_review_item_7', 'feasibility_review_item_8', 'feasibility_review_item_9')
    def _compute_feasibility_review_complete(self):
    #This function determines whether the feasibility review is complete.
    #Returns True if the feasibility review is complete, False otherwise.
      for record in self:
        if (
          record.feasibility_review_item_1 and
          record.feasibility_review_item_2 and
          record.feasibility_review_item_3 and
          record.feasibility_review_item_4 and
          record.feasibility_review_item_5 and
          record.feasibility_review_item_6 and
          record.feasibility_review_item_7 and
          record.feasibility_review_item_8 and
          record.feasibility_review_item_9 in ('1', '2', '3')
        ):
          record['feasibility_review_complete'] = True
        else:
          record['feasibility_review_complete'] = False

    @api.onchange('contract_review_item_1', 'contract_review_item_2', 'contract_review_item_3', 'contract_review_item_4', 'contract_review_item_5', 'contract_review_item_6', 'contract_review_item_7', 'contract_review_item_8')
    def _compute_contract_review_complete(self):
    #This function determines whether the contract review is complete.
    #Returns True if the contract review is complete, False otherwise.
      for record in self:
        if (
          record.contract_review_item_1 and
          record.contract_review_item_2 and
          record.contract_review_item_3 and
          record.contract_review_item_4 and
          record.contract_review_item_5 and
          record.contract_review_item_6 and
          record.contract_review_item_7 and
          record.contract_review_item_8
        ):
          record['contract_review_complete'] = True
        else:
          record['contract_review_complete'] = False
    
    @api.onchange('feasibility_review_complete', 'contract_review_complete')
    def _compute_sales_checklist_status(self):
    #This method computes the value of the `sales_checklist_status` field.
    #The value of the `sales_checklist_status` field.
      for record in self:
        if record.feasibility_review_complete and record.contract_review_complete:
          record['sales_checklist_status'] = 'done'
        else:
          record['sales_checklist_status'] = 'blocked'

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
              record['state'] = 'draft'
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
              record['state'] = 'sent'
              record.message_post(body="Cannot confirm Quotation: Awaiting sales checklists completion.")
      return action