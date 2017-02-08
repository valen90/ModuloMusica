#-*- coding: utf-8 -*-
from openerp import models, fields, api

class Aplicacionejemplo01Task(models.Model):
    #_name debe ser el nombre de la clase empezando en minúscula
    # y al comienzo de otra mayúscula poner punto y ésta en minuscula
    _name = 'aplicacionejemplo01.task'
    name = fields.Char('Artista', required=True)
    name2 = fields.Char('Album', required=True)
    name3 = fields.Char('Año', required=True)
    name4 = fields.Char('Carátula', help='Elija carátula')
    is_done = fields.Boolean('Done?')
    active = fields.Boolean('Active?', default=True)

    @api.one  
    def do_toggle_done(self):
        self.is_done = not self.is_done
        return True

    @api.multi
    def do_clear_done(self):
        done_recs = self.search([('is_done', '=', True)])
        done_recs.write({'active': False})
        return True