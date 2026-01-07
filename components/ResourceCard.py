import flet as ft
class ResourceCard(ft.Container):
  def __init__(self, title, color):
    super().__init__()
    self.title_text = ft.Text(title, weight="bold", size=18)
    self.ring = ft.ProgressRing(
      width=180,
      height=180,
      stroke_width=15,
      value=0,
      color=color,
      bgcolor=ft.Colors.with_opacity(0.1, color)
    )
    self.percentage_text = ft.Text("0%", size=24, weight="bold")
    self.info_text = ft.Text("Cargando...", size=12, color="white70", text_align=ft.TextAlign.CENTER)

    self.padding = 20
    self.border_radius = 15
    self.content = ft.Column(
        controls=[
            self.title_text,
            ft.Stack(
                controls=[
                    self.ring,
                    ft.Container(
                        content=self.percentage_text,
                        alignment=ft.alignment.center,
                        width=180, height=180
                    )
                ]
            ),
            self.info_text
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=15
    )
  

  def update_value(self, value, info, porcentage_text):
    self.ring.value = value
    self.percentage_text.value = f"{porcentage_text:.2f}%"
    self.info_text.value = info