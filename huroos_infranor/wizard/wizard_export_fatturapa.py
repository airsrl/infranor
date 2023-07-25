from odoo import api, models

from odoo.addons.l10n_it_account.tools.account_tools import encode_for_export


CAUSALE_UNICA = 'CONTRIBUTO AMBIENTALE CONAI ASSOLTO'


class WizardExportFatturapa(models.TransientModel):
    _inherit = "wizard.export.fatturapa"

    @api.model
    def getTemplateValues(self, template_values):
        """
        Eredito la funzione getTemplateValues per cambiare la funzione get_causale.
        La richiesta del cliente è che nella fattura elettronica compaia solo CAUSALE_UNICA, tra i tag <causale> dell'xml.
        """

        template_values_dict = super(WizardExportFatturapa, self).getTemplateValues(template_values)

        if template_values_dict.get('get_causale', False):
            def get_causale(invoice):
                res = []
                if invoice.narration:
                    # see: OCA/server-tools/html_text/models/ir_fields_converter.py
                    # after server_tools/html_text is ported to 16.0 we could use:
                    # narration_text = self.env["ir.fields.converter"]
                    #                  .text_from_html(invoice.narration, 40, 100, "...")
                    # meanwhile: 8<
                    from lxml import html

                    try:
                        narration_text = "\n".join(
                            html.fromstring(invoice.narration).xpath("//text()")
                        )
                    except Exception:
                        narration_text = ""
                    # >8 end meanwhile

                    # max length of Causale is 200
                    caus_list = narration_text.split("\n")

                    skip_other_causali = False
                    if CAUSALE_UNICA in caus_list:
                        skip_other_causali = True

                    for causale in caus_list:
                        if not causale:
                            continue

                        if causale != CAUSALE_UNICA and skip_other_causali:
                            continue

                        causale_list_200 = [
                            causale[i: i + 200] for i in range(0, len(causale), 200)
                        ]
                        for causale200 in causale_list_200:
                            # Remove non latin chars, but go back to unicode string,
                            # as expected by String200LatinType
                            causale = encode_for_export(causale200, 200)
                            res.append(causale)
                return res

            template_values_dict['get_causale'] = get_causale

        return template_values_dict
