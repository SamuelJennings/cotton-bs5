import flex_menu


class SidebarGroup(flex_menu.Menu):
    template = "cotton_bs5/menus/sidebar_group.html"


class SidebarItem(flex_menu.MenuItem):
    template = "cotton_bs5/menus/sidebar_group.html"
