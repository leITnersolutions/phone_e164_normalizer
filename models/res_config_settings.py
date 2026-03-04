# -*- coding: utf-8 -*-
from odoo import api, fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    e164_active = fields.Boolean(string='E.164 Normalisierung aktiv')
    e164_default_country_code = fields.Char(string='Default Country Code', default='+43')

    def set_values(self):
        res = super().set_values()
        ICP = self.env['ir.config_parameter'].sudo()
        ICP.set_param('e164.active', '1' if self.e164_active else '0')
        ICP.set_param('e164.default_cc', self.e164_default_country_code or '+43')
        return res

    @api.model
    def get_values(self):
        res = super().get_values()
        ICP = self.env['ir.config_parameter'].sudo()
        res.update(
            e164_active = ICP.get_param('e164.active','0') == '1',
            e164_default_country_code = ICP.get_param('e164.default_cc','+43'),
        )
        return res
