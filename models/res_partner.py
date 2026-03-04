# -*- coding: utf-8 -*-
import re
from odoo import api, models

def _normalize_e164(raw: str, default_cc: str = "+43") -> str:
    if not raw:
        return raw
    s = str(raw)
    s = re.sub(r"[^\d+]", "", s)  # remove spaces and punctuation
    s = re.sub(r"^00", "+", s)     # 00 -> +
    if not s.startswith('+'):
        if s.startswith('0'):
            s = f"{default_cc}{s[1:]}"
        else:
            s = f"{default_cc}{s}"
    return s

class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model_create_multi
    def create(self, vals_list):
        ICP = self.env['ir.config_parameter'].sudo()
        active = ICP.get_param('e164.active','0') == '1'
        if active:
            cc = ICP.get_param('e164.default_cc','+43')
            for vals in vals_list:
                if vals.get('phone'):
                    vals['phone'] = _normalize_e164(vals['phone'], cc)
                if vals.get('mobile'):
                    vals['mobile'] = _normalize_e164(vals['mobile'], cc)
        return super().create(vals_list)

    def write(self, vals):
        ICP = self.env['ir.config_parameter'].sudo()
        active = ICP.get_param('e164.active','0') == '1'
        if active:
            cc = ICP.get_param('e164.default_cc','+43')
            if vals.get('phone'):
                vals['phone'] = _normalize_e164(vals['phone'], cc)
            if vals.get('mobile'):
                vals['mobile'] = _normalize_e164(vals['mobile'], cc)
        return super().write(vals)
