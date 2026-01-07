import flet as ft
from starlette.routing import Route

from core.ProxmoxManager import ProxmoxManager

def create_login_view(page: ft.Page):

    t_usuario = ft.Text(value="Usuario: ")
    t_password = ft.Text(value="Password: ")

    def textbox_changed(e):
        if e.control.label == "Usuario":
            t_usuario.value = f"Usuario: {e.control.value}"
        elif e.control.label == "Contraseña":
            t_password.value = f"Password: {'*' * len(e.control.value)}"
        page.update()

    user_field = ft.TextField(
        label="Usuario",
        on_change=textbox_changed,
        width=300
    )

    password_field = ft.TextField(
        label="Contraseña",
        on_change=textbox_changed,
        password=True,
        can_reveal_password=True,
        width=300
    )

    titulo_app = ft.Text(
        value="INICIAR SESIÓN",
        size=30,
        weight=ft.FontWeight.BOLD,
        color="#3E6773"
    )
    
    dropdown_realms_list = ft.DropdownM2(
        label="Realms",
        hint_text="Selecciona un realm",
        width=300,
        options=[
            ft.dropdown.Option("pve"),
            ft.dropdown.Option("pam"),
            ft.dropdown.Option("laboratoriosyc.itslp"),
        ]
    )
    
    def custom_snackbar(message):
        page.open(
            ft.SnackBar(
                content=ft.Text(message),
                bgcolor="#3E6773",
                duration=3000
            )
        )
    
    async def button_session_start_click(e):
        user_value = user_field.value
        password_value = password_field.value
        realm_value = dropdown_realms_list.value
        
        if all([user_value, password_value, realm_value]):
            manager_proxmox = ProxmoxManager(user_value, password_value, realm_value)
            if await manager_proxmox.login():
                print("Sesión iniciada correctamente")
                page.session_manager = manager_proxmox
                page.go("/dashboard")
            else:
                custom_snackbar("Error al iniciar sesión")
        else:
            custom_snackbar("Por favor, complete todos los campos")
            
    
    button_session_start = ft.ElevatedButton(
        text="Iniciar Sesión",
        adaptive=True,
        width=300,
        height=50,
        color="#FFFFFF",
        bgcolor="#3E6773",
        on_click=button_session_start_click
    )

    campos_apilados = ft.Column(
        controls=[
            titulo_app,
            ft.Divider(height=10, color="transparent"),
            user_field,
            password_field,
            dropdown_realms_list,
            ft.Divider(height=10, color="transparent"),
            button_session_start
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=15
    )

    contenido_centrado = ft.Container(
        content=campos_apilados,
        alignment=ft.alignment.center
    )
    
    return ft.View(
        route="/login",
        controls=[contenido_centrado],
        vertical_alignment=ft.MainAxisAlignment.CENTER
    )