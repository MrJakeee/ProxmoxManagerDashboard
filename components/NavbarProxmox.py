import flet as ft


class NavbarProxmox(ft.Container):
    def __init__(self, color=ft.Colors.AMBER, name_user=""):
        super().__init__()
        self.content = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Column(
                        controls=[
                            ft.Text(
                                "Dashboard Proxmox",
                                size=24,
                                weight="bold",
                                color="white",
                            ),
                            ft.Text(
                                f"El nombre del usuario es: {name_user}",
                                size=14,
                                color="white70",
                            ),
                        ],
                        tight=True,
                        spacing=2,
                    ),
                    ft.Row(
                        controls=[
                            ft.ElevatedButton(
                                text="Nueva maquina virtual",
                                icon=ft.Icons.ADD,
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=8),
                                    color="white",
                                    bgcolor="#3d142d",  # Color oscuro vinotinto
                                ),
                            ),
                            ft.TextButton(
                                content=ft.Row(
                                    [
                                        ft.Icon(
                                            ft.Icons.PERSON_2_OUTLINED, color="white"
                                        ),
                                        ft.Text(f"{name_user}", color="white"),
                                    ]
                                )
                            ),
                            ft.Icon(ft.Icons.LOGOUT, color="white"),
                        ],
                        spacing=10,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            gradient=ft.LinearGradient(
                begin=ft.alignment.center_left,
                end=ft.alignment.center_right,
                colors=["#6b1039", "#4a0e2a"],
            ),
            padding=ft.padding.symmetric(horizontal=20, vertical=10),
            height=80,
        )

