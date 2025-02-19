# Copyright 2012 Camptocamp SA - Yannick Vaucher
# Copyright 2018 brain-tec AG - Raul Martin
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResPartner(models.Model):
    """Add relation affiliate_ids."""

    _inherit = "res.partner"

    # force "active_test" domain to bypass _search() override
    child_ids = fields.One2many(
        domain=[("active", "=", True), ("is_company", "=", False)]
    )

    # force "active_test" domain to bypass _search() override
    affiliate_ids = fields.One2many(
        "res.partner",
        "parent_id",
        string="Affiliates",
        domain=[("active", "=", True), ("is_company", "=", True)],
    )

    def open_affiliate_form(self):
        """Open affiliate contact form from the parent partner form view"""
        return {
            "type": "ir.actions.act_window",
            "res_model": "res.partner",
            "res_id": self.id,
            "view_mode": "form",
            "target": "current",
        }
