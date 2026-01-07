import flet as ft

from views.login_view import create_login_view
from views.dashboard_view import create_dashboard_view

def main(page: ft.Page):
    page.title = "Login Proxmox"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK
    
    ROUTE_MAP = {
        "/": create_login_view,
        "/login":  create_login_view,
        "/dashboard": create_dashboard_view
    }
    
    ROUTES_REQUIRING_MANAGER = [
        "/dashboard"
    ]
    
    def route_change(e):
        page.views.clear()
        
        view_builder = ROUTE_MAP.get(page.route, create_login_view)
        
        manager = getattr(page, "session_manager", None)
        view_to_add = None
        current_route = page.route
        
        if current_route in ROUTES_REQUIRING_MANAGER:
            if manager is not None:
                view_to_add = view_builder(page, manager)
            else:
                page.route = "/login"
                view_to_add = ROUTE_MAP["/login"](page)
        elif view_builder:
            view_to_add = view_builder(page)
        else:
            page.route = "/login"
            view_to_add = ROUTE_MAP["/login"](page)
            
        page.views.append(view_to_add)
        
        page.update()
    
    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)
        
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    
    page.go(page.route)
    
    
ft.app(target=main)