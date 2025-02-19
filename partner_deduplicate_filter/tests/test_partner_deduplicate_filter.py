# Copyright 2016 Tecnativa - Pedro M. Baeza
# Copyright 2024 Tecnativa - Carolina Fernandez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests import common
from odoo.tools.safe_eval import safe_eval


class TestDeduplicateFilter(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner_1 = cls.env["res.partner"].create(
            {
                "name": "Partner 1",
                "email": "partner1@example.org",
                "is_company": True,
                "parent_id": False,
            }
        )
        cls.partner_1.copy()
        cls.partner_2 = cls.env["res.partner"].create(
            {
                "name": "Partner 2",
                "email": "partner2@example.org",
                "is_company": False,
                "parent_id": cls.partner_1.id,
            }
        )
        cls.partner_2.copy()
        cls.partner_3 = cls.env["res.partner"].create(
            {
                "name": "Partner 3",
                "email": "partner3@example.org",
                "is_company": False,
                "parent_id": False,
            }
        )
        cls.partner_3.copy()
        cls.wizard = cls.env["base.partner.merge.automatic.wizard"].create(
            {"group_by_email": True}
        )

    def test_deduplicate_exclude_is_company(self):
        self.wizard.exclude_is_company = True
        self.wizard.action_start_manual_process()
        matched_founds = 0
        for line in self.wizard.line_ids:
            match_ids = safe_eval(line.aggr_ids)
            if self.partner_1.id in match_ids:
                self.assertTrue(False, "Partner with is company not excluded")
            if self.partner_2.id in match_ids:
                matched_founds += 1
            if self.partner_3.id in match_ids:
                matched_founds += 1
        self.assertEqual(matched_founds, 2)

    def test_deduplicate_exclude_not_parent(self):
        self.wizard.exclude_not_parent = True
        self.wizard.action_start_manual_process()
        matched_founds = 0
        for line in self.wizard.line_ids:
            match_ids = safe_eval(line.aggr_ids)
            if self.partner_1.id in match_ids:
                self.assertTrue(False, "Partner without parent not excluded")
            if self.partner_3.id in match_ids:
                self.assertTrue(False, "Partner without parent not excluded")
            if self.partner_2.id in match_ids:
                matched_founds += 1
        self.assertEqual(matched_founds, 1)

    def test_deduplicate_exclude_parent(self):
        self.wizard.exclude_parent = True
        self.wizard.action_start_manual_process()
        matched_founds = 0
        for line in self.wizard.line_ids:
            match_ids = safe_eval(line.aggr_ids)
            if self.partner_2.id in match_ids:
                self.assertTrue(False, "Partner with parent not excluded")
            if self.partner_1.id in match_ids:
                matched_founds += 1
            if self.partner_3.id in match_ids:
                matched_founds += 1
        self.assertEqual(matched_founds, 2)
