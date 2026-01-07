import flet as ft


class VMCard(ft.Container):
    def __init__(self, vm_id, name, status, cpu_usage, ram_usage, disk_size):
        super().__init__()
        # Configuración de la tarjeta
        self.width = 350
        self.bgcolor = ft.Colors.with_opacity(1, "#1a1c1e")
        self.border_radius = 15
        self.padding = 20
        self.border = ft.border.all(1, "white10")

        self.cpu_usage = cpu_usage
        self.ram_usage = ram_usage
        self.disk_size = disk_size

        self.cpu_text = ft.Text(
            value=f"{self.cpu_usage:.2f}%", size=10, weight=ft.FontWeight.BOLD
        )
        self.ram_text = ft.Text(
            value=f"{self.ram_usage:.2f}%", size=10, weight=ft.FontWeight.BOLD
        )

        self.disk_size = disk_size / 1024**3
        # Determinar color del estado (Running/Stopped)
        self.status_color = ft.Colors.CYAN_ACCENT if status == "running" else "white30"

        self.icon_vm = ft.Icon(
            ft.Icons.SCREEN_SHARE_OUTLINED,
            color=self.status_color,
            size=30,
        )

        self.status_text = ft.Text(
            value=status.capitalize(), size=10, color=self.status_color
        )
        self.content = ft.Column(
            controls=[
                # Fila Superior: Icono, ID/Nombre y Badge de Estado
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Row(
                            [
                                self.icon_vm,
                                ft.Column(
                                    [
                                        ft.Text(
                                            f"id: {vm_id}",
                                            weight=ft.FontWeight.BOLD,
                                            size=16,
                                        ),
                                        ft.Text(name, size=12, color="white70"),
                                    ],
                                    spacing=0,
                                ),
                            ]
                        ),
                        ft.Container(
                            self.status_text,
                            border=ft.border.all(1, self.status_color),
                            border_radius=10,
                            padding=ft.padding.symmetric(horizontal=8, vertical=2),
                        ),
                    ],
                ),
                ft.Divider(height=10, color="white10"),
                # Fila Inferior: Métricas Rápidas (CPU, RAM, DISK)
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        self.metric_components(ft.Icons.MEMORY, "CPU", self.cpu_text),
                        self.metric_components(
                            ft.Icons.RAMEN_DINING, "MEMORY", self.ram_text
                        ),
                        self.metric_components(
                            ft.Icons.STORAGE,
                            "STORAGE",
                            ft.Text(
                                value=f"{self.disk_size} GiB",
                                size=10,
                                weight=ft.FontWeight.BOLD,
                            ),
                        ),
                    ],
                ),
            ],
            spacing=10,
        )

    def metric_components(self, icon, text, value_control):
        return ft.Row(
            [
                ft.Icon(icon, size=24, color="pink400"),
                ft.Column(
                    [
                        ft.Text(text, size=10, color="white54"),
                        value_control,
                    ],
                    spacing=0,
                ),
            ],
            spacing=5,
        )

    def update_vm(self, cpu_value, ram_value, status):
        self.cpu_text.value = f"{cpu_value:.2f}%"
        self.ram_text.value = f"{ram_value:.2f}%"

        if status == "running":
            self.status_text.color = ft.Colors.CYAN_ACCENT
            self.icon_vm.color = ft.Colors.CYAN_ACCENT
            self.status_text.value = "Running"
        else:
            self.status_text.color = ft.Colors.WHITE30
            self.icon_vm.color = ft.Colors.WHITE30
            self.status_text.value = "Stopped"
