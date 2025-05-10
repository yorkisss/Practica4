import reflex as rx

# Constantes de porcentajes actuales (2024)
TASA_SEGURIDAD_SOCIAL = 0.0591  # 5.91%
TASA_BONIFICACION = 0.10        # 10% del sueldo anual

class State(rx.State):
    sueldo_bruto: float = 0.0
    otros_descuentos: float = 0.0
    seguridad_social: float = 0.0
    isr_mensual: float = 0.0
    bonificacion: float = 0.0
    sueldo_neto: float = 0.0

    def calcular_seguridad_social(self):
        """
        Calcula el descuento por seguridad social (TSS) con base en el sueldo bruto.
        """
        self.seguridad_social = self.sueldo_bruto * TASA_SEGURIDAD_SOCIAL

    def calcular_isr_anual(self, sueldo_anual):
        """
        Calcula la retención del ISR en base a la DGII.
        Devuelve el total anual
        """
        # Formulas para el calculo de cada salrio
        if sueldo_anual <= 416220:
            return 0
        elif sueldo_anual <= 624329:
            excedente = sueldo_anual - 416220
            return excedente * 0.15
        elif sueldo_anual <= 867123:
            excedente = sueldo_anual - 624329
            return 31216 + excedente * 0.20
        else:
            excedente = sueldo_anual - 867123
            return 79776 + excedente * 0.25

    def calcular_isr_mensual(self):
        sueldo_anual = self.sueldo_bruto * 12
        isr_anual = self.calcular_isr_anual(sueldo_anual)
        self.isr_mensual = isr_anual / 12

    def calcular_bonificacion_mensual(self):
        """
        Calcula una bonificación mensual estimada, equivalente al 10% del sueldo anual dividido entre 12.
        """
        bonificacion_anual = self.sueldo_bruto * 12 * TASA_BONIFICACION
        self.bonificacion = bonificacion_anual / 12

    def calcular_todo(self):
        self.calcular_seguridad_social()
        self.calcular_isr_mensual()
        self.calcular_bonificacion_mensual()
        self.calcular_neto()

    def calcular_neto(self):
        """
        Calcula el sueldo neto.
        """
        self.sueldo_neto = (
            self.sueldo_bruto
            - self.seguridad_social
            - self.isr_mensual
            - self.otros_descuentos
            + self.bonificacion
        )

    def set_sueldo_bruto(self, sueldo):
        try:
            self.sueldo_bruto = float(sueldo)
        except ValueError:
            self.sueldo_bruto = 0.0

    def set_otros_descuentos(self, descuento):
        try:
            self.otros_descuentos = float(descuento)
        except ValueError:
            self.otros_descuentos = 0.0

def index():
    return rx.vstack(
        rx.heading("Cálculo de Sueldo Neto (República Dominicana)", font_size="1.5em", margin_bottom="1em"),
        rx.center(
            rx.vstack(
                rx.input(
                    placeholder="Sueldo Bruto Mensual (RD$)",
                    type="number",
                    on_change=State.set_sueldo_bruto,
                    margin_bottom="0.5em",
                ),
                rx.input(
                    placeholder="Otros Descuentos Mensuales (RD$)",
                    type="number",
                    on_change=State.set_otros_descuentos,
                    margin_bottom="1em",
                ),
                rx.button("Calcular", on_click=State.calcular_todo, style={"background_color": "green"}),
                spacing="1",
            )
        ),
        # Salidas
        rx.divider(margin_y="1em"),
        rx.heading("Resultados", font_size="1.2em", margin_bottom="0.5em"),
        rx.text(f"Sueldo Bruto: RD$ {State.sueldo_bruto.to_string()}", margin_bottom="0.25em"),
        rx.text(f"Seguridad Social (5.91%): RD$ {State.seguridad_social.to_string()}", margin_bottom="0.25em"),
        rx.text(f"Retención ISR mensual: RD$ {State.isr_mensual.to_string()}", margin_bottom="0.25em"),
        rx.text(f"Otros Descuentos: RD$ {State.otros_descuentos.to_string()}", margin_bottom="0.25em"),
        rx.text(f"Bonificación mensual estimada (10% anual): RD$ {State.bonificacion.to_string()}", font_weight="bold", margin_bottom="0.5em"),
        rx.heading(f"Sueldo Neto Estimado: RD$ {State.sueldo_neto.to_string()}", font_size="1.1em", color="pink"),
    )
app = rx.App()
app.add_page(index)