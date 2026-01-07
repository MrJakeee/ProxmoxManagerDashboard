import asyncio
import flet as ft


from components.VMCard import VMCard
from core.ProxmoxManager import ProxmoxManager
from components.NavbarProxmox import NavbarProxmox
from components.ResourceCard import ResourceCard


cards_exits = {}


def create_dashboard_view(page: ft.Page, proxmox_manager: ProxmoxManager):
    # Logica
    name_user = proxmox_manager.getUser() or "Desconocido"

    navbar_main = NavbarProxmox(name_user=name_user)

    # --- 2. CONTENIDO PRINCIPAL
    # COMPONENTES DE RECURSOS DE CPU, RAM Y STORAGE
    title_text = ft.Text(
        value="Uso de Recursos del Sistema",
        size=20,
        weight=ft.FontWeight.BOLD,
        color="white",
        text_align=ft.TextAlign.CENTER,
    )

    cpu_card = ResourceCard("CPU", "#EC4899")
    memory_card = ResourceCard("Memory", "#A855F7")
    storage_card = ResourceCard("Storage", "#06B6D4")

    container_resources = ft.Container(
        content=ft.Row(
            controls=[cpu_card, memory_card, storage_card],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            vertical_alignment=ft.CrossAxisAlignment.START,
        ),
        bgcolor="#1a1c1e",
        border_radius=15,
        padding=20,
        border=ft.border.all(2, "#310E29"),
    )

    machines_vm_title = ft.Text(
        value="Lista de maquinas virtuales",
        size=20,
        weight=ft.FontWeight.BOLD,
        color="white",
    )

    vm_container = ft.Row(
        wrap=True,
        scroll=ft.ScrollMode.ADAPTIVE,
        expand=True,
    )

    machines_vm_container = ft.Container(
        content=ft.Column(
            controls=[
                machines_vm_title,
                vm_container,
            ],
        ),
    )

    main_area_container = ft.Container(
        content=ft.Column(
            controls=[title_text, container_resources, machines_vm_container],
            spacing=20,
        ),
        padding=20,
        expand=True,
        bgcolor="#111418",
        alignment=ft.alignment.top_left,
    )

    # Logica del dashboard
    async def refresh_main_container():
        await asyncio.sleep(0.1)

        while True:
            try:
                dataStatus = await proxmox_manager.getStatusProxmox()
                storage_data = await proxmox_manager.getStorageTotal()
                vms_data = await proxmox_manager.getAllVMS()

                if dataStatus and isinstance(dataStatus, dict):
                    cpu_data = dataStatus.get("cpu", "Desconocido")
                    cpu_info = dataStatus.get("cpuinfo", "Desconocido")

                    memory_data = dataStatus.get("memory", 0.0)

                    calculated_cpu_info(cpu_data, cpu_info)
                    calculated_memory_info(memory_data)

                else:
                    print("Error en la obtencion de datos")

                if storage_data and isinstance(storage_data, list):
                    calculated_storage_info(storage_data)
                else:
                    print("Error en la obtencion de datos del almacenamiento")

                if vms_data and isinstance(vms_data, list):
                    create_vms_cards(vms_data)
                else:
                    print("Error en la obtencion de datos de VMS")

            except Exception as e:
                print(f"Error (refresh_main_container): {e}")

            page.update()
            await asyncio.sleep(5)

    page.run_task(refresh_main_container)

    def calculated_cpu_info(cpu_data, cpu_info):
        porcentage_data = cpu_data * 100
        cpu_info_data = (
            f"Model: {cpu_info.get('model')} \n"
            + f"Cores: {cpu_info.get('cores')} \n"
            + f"Cpus: {cpu_info.get('cpus')} \n"
            + f"Socket: {cpu_info.get('sockets')}"
        )

        cpu_card.update_value(cpu_data, cpu_info_data, porcentage_data)

    def calculated_memory_info(ram_data):
        total_byte_ram = ram_data.get("total")
        used_byte_ram = ram_data.get("used")

        total_gib_ram = total_byte_ram / (1024**3)
        used_gib_ram = used_byte_ram / (1024**3)

        ratio = used_gib_ram / total_gib_ram if total_gib_ram > 0 else 0

        porcentage_text = ratio * 100

        memory_info_data = (
            "Ram Usage \n" + f"{used_gib_ram:.2f} GiB to {total_gib_ram:.2f} GiB"
        )
        memory_card.update_value(ratio, memory_info_data, porcentage_text)

    def calculated_storage_info(storage_data):
        total_storage = 0
        total_used_storage = 0
        for storage in storage_data:
            if storage["enabled"] == 1:
                total_storage += storage["total"]
                total_used_storage += storage["used"]

        if total_storage == 0:
            return 0.0

        total_storage_gib = total_storage / (1024**3)
        total_used_storage_gib = total_used_storage / (1024**3)

        value = total_used_storage / total_storage

        porcentage_text = value * 100

        storage_info_data = (
            f"{total_used_storage_gib:.2f}% GiB"
            + " To "
            + f"{total_storage_gib:.2f}% GiB"
        )

        storage_card.update_value(value, storage_info_data, porcentage_text)

    def create_vms_cards(vms_data):
        global cards_exits

        for vm in vms_data:
            id_vm = vm["vmid"]

            if id_vm in cards_exits:
                cpu_value = vm["cpu"] * 100
                ram_value = vm["mem"] / 1024**3
                cards_exits[id_vm].update_vm(cpu_value, ram_value, vm["status"])
            else:
                vm_card = VMCard(
                    vm["vmid"],
                    vm["name"],
                    vm["status"],
                    vm["cpu"],
                    vm["mem"],
                    vm["maxdisk"],
                )
                cards_exits[id_vm] = vm_card

                vm_container.controls.append(vm_card)

    # --- 3. CONTENEDOR PRINCIPAL DE DISTRIBUCIÓN (ROW) ---

    layout_row = ft.Column(
        controls=[main_area_container],
        spacing=0,
        expand=True,
    )

    # 4. Retorno de la Vista
    return ft.View(
        route="/dashboard",
        controls=[navbar_main, layout_row],
        vertical_alignment=ft.MainAxisAlignment.START,
        padding=0,
    )
