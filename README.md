# nxc_sales_checklist

This custom module was developed for Next Chapter Manufacturing to prompt users with checklists on Quotations and Sales Orders. The addon includes stop-gates to prevent order confirmation prior to checklists completion.

## Features
- Creates 2 new tabs in the sale.order model (Feasiblity Review & Contract Review).
- Adds a status indicator to the sale order to indicate checklist completion status.
- Prevents order confirmation prior to checklists completion.
- Posts warning message in chatter when a user attempts to confirm an order prior to checklist completion.

## Installation
To install this module, you can use the following steps:

1. Copy this directory to addons folder.
2. Allow Odoo server to restart.
3. Go to Apps.
4. Click 'update apps list' button.
5. Clear search filter and search for this addon.
6. Click Install.

## Usage
To use this module, you can follow these steps:

1. Go to Sales > Orders.
2. Click Create.
3. Complete the 'Feasibility Review' checklist.
4. Complete the 'Contract Review' checklist.
5. When the checklists are completed, you be permitted to confirm the order.

## Support
If you have any questions or problems with this module, please contact the author at haydenmccarthy19@gmail.com