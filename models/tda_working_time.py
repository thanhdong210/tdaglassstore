# -*- coding: utf-8 -*-
from odoo import fields, models, api, _

WEEKDAY_SELECTION = [
    ('MON', 'Monday'),
    ('TUE', 'Tuesday'),
    ('WED', 'Wednesday'),
    ('THU', 'Thursday'),
    ('FRI', 'Friday'),
    ('SAT', 'Saturday'),
    ('SUN', 'Sunday'),
]

class TDAWorkingTime(models.Model):
    _name = 'tda.working.time'
    _description = 'TDA Working Time'

    weekday = fields.Selection(WEEKDAY_SELECTION, string='Weekday')
    time_from = fields.Char(string="Time from")
    time_to = fields.Char(string="Time to")
    info_id = fields.Many2one('tda.info')