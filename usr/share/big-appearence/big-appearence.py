#!/usr/bin/env python3
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
gi.require_version('Pango', '1.0')
from gi.repository import Gtk, Adw, Gdk, Gio, GLib, Pango
import subprocess
import os
import sys
import locale
import threading
import time
import random
import xml.etree.ElementTree as ET
import re
import glob

# Complete translation dictionary
TRANSLATIONS = {
    "en": {
        "window_title": "Big Appearance",
        "layouts_tab": "Layouts",
        "effects_tab": "Effects",
        "themes_tab": "Themes",
        "select_layout": "Select Layout",
        "applying": "Applying {layout} layout...",
        "success": "Successfully applied {layout} layout",
        "error_config": "Error: Config file not found - {file}",
        "error_applying": "Error applying layout: {error}",
        "error": "Error: {error}",
        "apply": "Apply Layout",
        "about": "About",
        "quit": "Quit",
        "description_layout": "Apply the {layout} layout to your desktop.",
        "gnome": "GNOME",
        "effects_description": "Enhance your desktop with visual effects",
        "desktop_cube": "Desktop Cube",
        "desktop_cube_description": "Rotate your desktop on a 3D cube",
        "magic_lamp": "Magic Lamp",
        "magic_lamp_description": "Animated window minimizing effect",
        "windows_effects": "Windows Effects",
        "windows_effects_description": "Additional window animations",
        "not_installed": "Not installed",
        "install_extension": "Install Extension",
        "enable": "Enable",
        "disable": "Disable",
        "themes_description": "Customize your desktop appearance",
        "gtk_theme": "GTK Theme",
        "icon_theme": "Icon Theme",
        "shell_theme": "Shell Theme",
        "apply_theme": "Apply Theme",
        "no_themes_found": "No themes found",
        "license": "MIT License",
        "gnome_only": "This feature is only available on GNOME"
    },
    "es": {
        "window_title": "Big Appearance",
        "layouts_tab": "Diseños",
        "effects_tab": "Efectos",
        "themes_tab": "Temas",
        "select_layout": "Seleccionar Diseño",
        "applying": "Aplicando diseño {layout}...",
        "success": "Diseño {layout} aplicado con éxito",
        "error_config": "Error: Archivo de configuración no encontrado - {file}",
        "error_applying": "Error al aplicar el diseño: {error}",
        "error": "Error: {error}",
        "apply": "Aplicar Diseño",
        "about": "Acerca de",
        "quit": "Salir",
        "description_layout": "Aplica el diseño {layout} a tu escritorio.",
        "gnome": "GNOME",
        "effects_description": "Mejora tu escritorio con efectos visuales",
        "desktop_cube": "Cubo de Escritorio",
        "desktop_cube_description": "Rota tu escritorio en un cubo 3D",
        "magic_lamp": "Lámpara Mágica",
        "magic_lamp_description": "Efecto animado de minimización de ventanas",
        "windows_effects": "Efectos de Ventanas",
        "windows_effects_description": "Animaciones adicionales de ventanas",
        "not_installed": "No instalado",
        "install_extension": "Instalar Extensión",
        "enable": "Activar",
        "disable": "Desactivar",
        "themes_description": "Personaliza la apariencia de tu escritorio",
        "gtk_theme": "Tema GTK",
        "icon_theme": "Tema de Iconos",
        "shell_theme": "Tema del Shell",
        "apply_theme": "Aplicar Tema",
        "no_themes_found": "No se encontraron temas",
        "license": "Licencia MIT",
        "gnome_only": "Esta función solo está disponible en GNOME"
    },
    "fr": {
        "window_title": "Big Appearance",
        "layouts_tab": "Dispositions",
        "effects_tab": "Effets",
        "themes_tab": "Thèmes",
        "select_layout": "Sélectionner la disposition",
        "applying": "Application de la disposition {layout}...",
        "success": "Disposition {layout} appliquée avec succès",
        "error_config": "Erreur: Fichier de configuration non trouvé - {file}",
        "error_applying": "Erreur lors de l'application de la disposition: {error}",
        "error": "Erreur: {error}",
        "apply": "Appliquer la disposition",
        "about": "À propos",
        "quit": "Quitter",
        "description_layout": "Applique la disposition {layout} à votre bureau.",
        "gnome": "GNOME",
        "effects_description": "Améliorez votre bureau avec des effets visuels",
        "desktop_cube": "Cube de Bureau",
        "desktop_cube_description": "Faites pivoter votre bureau sur un cube 3D",
        "magic_lamp": "Lampe Magique",
        "magic_lamp_description": "Effet animé de réduction des fenêtres",
        "windows_effects": "Effets de Fenêtres",
        "windows_effects_description": "Animations de fenêtres supplémentaires",
        "not_installed": "Non installé",
        "install_extension": "Installer l'Extension",
        "enable": "Activer",
        "disable": "Désactiver",
        "themes_description": "Personnalisez l'apparence de votre bureau",
        "gtk_theme": "Thème GTK",
        "icon_theme": "Thème d'Icônes",
        "shell_theme": "Thème du Shell",
        "apply_theme": "Appliquer le Thème",
        "no_themes_found": "Aucun thème trouvé",
        "license": "Licence MIT",
        "gnome_only": "Cette fonctionnalité n'est disponible que sur GNOME"
    },
    "de": {
        "window_title": "Big Appearance",
        "layouts_tab": "Layouts",
        "effects_tab": "Effekte",
        "themes_tab": "Themen",
        "select_layout": "Layout auswählen",
        "applying": "Wende {layout} Layout an...",
        "success": "{layout} Layout erfolgreich angewendet",
        "error_config": "Fehler: Konfigurationsdatei nicht gefunden - {file}",
        "error_applying": "Fehler beim Anwenden des Layouts: {error}",
        "error": "Fehler: {error}",
        "apply": "Layout anwenden",
        "about": "Über",
        "quit": "Beenden",
        "description_layout": "Wende das {layout} Layout auf deinen Desktop an.",
        "gnome": "GNOME",
        "effects_description": "Verbessere deinen Desktop mit visuellen Effekten",
        "desktop_cube": "Desktop-Würfel",
        "desktop_cube_description": "Drehe deinen Desktop auf einem 3D-Würfel",
        "magic_lamp": "Magische Lampe",
        "magic_lamp_description": "Animierter Fensterminimierungseffekt",
        "windows_effects": "Fenstereffekte",
        "windows_effects_description": "Zusätzliche Fensteranimationen",
        "not_installed": "Nicht installiert",
        "install_extension": "Erweiterung installieren",
        "enable": "Aktivieren",
        "disable": "Deaktivieren",
        "themes_description": "Passe das Aussehen deines Desktops an",
        "gtk_theme": "GTK-Thema",
        "icon_theme": "Symbol-Thema",
        "shell_theme": "Shell-Thema",
        "apply_theme": "Thema anwenden",
        "no_themes_found": "Keine Themen gefunden",
        "license": "MIT-Lizenz",
        "gnome_only": "Diese Funktion ist nur unter GNOME verfügbar"
    },
    "pt_BR": {
        "window_title": "Big Appearance",
        "layouts_tab": "Layouts",
        "effects_tab": "Efeitos",
        "themes_tab": "Temas",
        "select_layout": "Selecionar Layout",
        "applying": "Aplicando layout {layout}...",
        "success": "Layout {layout} aplicado com sucesso",
        "error_config": "Erro: Arquivo de configuração não encontrado - {file}",
        "error_applying": "Erro ao aplicar o layout: {error}",
        "error": "Erro: {error}",
        "apply": "Aplicar Layout",
        "about": "Sobre",
        "quit": "Sair",
        "description_layout": "Aplica o layout {layout} à sua área de trabalho.",
        "gnome": "GNOME",
        "effects_description": "Melhore sua área de trabalho com efeitos visuais",
        "desktop_cube": "Cubo da Área de Trabalho",
        "desktop_cube_description": "Gire sua área de trabalho em um cubo 3D",
        "magic_lamp": "Lâmpada Mágica",
        "magic_lamp_description": "Efeito animado de minimização de janelas",
        "windows_effects": "Efeitos de Janelas",
        "windows_effects_description": "Animações de janelas adicionais",
        "not_installed": "Não instalado",
        "install_extension": "Instalar Extensão",
        "enable": "Ativar",
        "disable": "Desativar",
        "themes_description": "Personalize a aparência da sua área de trabalho",
        "gtk_theme": "Tema GTK",
        "icon_theme": "Tema de Ícones",
        "shell_theme": "Tema do Shell",
        "apply_theme": "Aplicar Tema",
        "no_themes_found": "Nenhum tema encontrado",
        "license": "Licença MIT",
        "gnome_only": "Este recurso está disponível apenas no GNOME"
    }
}

# Get system language
def get_system_language():
    try:
        lang = locale.getdefaultlocale()[0]
        if lang:
            # Check if we have a translation for the full locale
            if lang in TRANSLATIONS:
                return lang
            # Extract primary language code (e.g., 'pt' from 'pt_BR')
            primary_lang = lang.split('_')[0]
            # Check if we have a translation for the primary language
            if primary_lang in TRANSLATIONS:
                return primary_lang
    except:
        pass
    return "en"  # Default to English

# Translation function
def _(text):
    lang = get_system_language()
    return TRANSLATIONS.get(lang, TRANSLATIONS["en"]).get(text, text)

# Detect desktop environment
def detect_desktop_environment():
    desktop = os.environ.get('XDG_CURRENT_DESKTOP', '').lower()
    if 'gnome' in desktop:
        return 'gnome'
    else:
        # Fallback to checking other environment variables
        if 'GNOME_DESKTOP_SESSION_ID' in os.environ:
            return 'gnome'
        return 'gnome'  # Default to GNOME

# Extract color from theme name
def extract_color_from_theme_name(theme_name):
    color_map = {
        'blue': '#3584e4',
        'green': '#26a269',
        'yellow': '#cd9309',
        'orange': '#e66100',
        'red': '#c01c28',
        'purple': '#9141ac',
        'pink': '#d16d9e',
        'teal': '#2190a4',
        'grey': '#5e5c64',
        'gray': '#5e5c64',
        'black': '#241f31',
        'white': '#ffffff',
        'dark': '#241f31',
        'light': '#ffffff',
        'brown': '#865e3c',
        'cyan': '#00b4c8',
        'magenta': '#c061cb',
        'lime': '#2ec27e',
        'indigo': '#1c71d8'
    }
    
    theme_lower = theme_name.lower()
    for color_name, hex_code in color_map.items():
        if color_name in theme_lower:
            return hex_code
    
    # Default colors if no match
    if 'dark' in theme_lower:
        return '#241f31'
    if 'light' in theme_lower:
        return '#ffffff'
    
    # Generate a color based on the theme name hash
    hash_value = hash(theme_name)
    r = (hash_value & 0xFF0000) >> 16
    g = (hash_value & 0x00FF00) >> 8
    b = hash_value & 0x0000FF
    return f'#{r:02x}{g:02x}{b:02x}'

class BigAppearanceWindow(Adw.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app)
        self.set_title(_("window_title"))
        self.set_default_size(900, 600)
        self.set_size_request(800, 500)
        
        # Detect desktop environment
        self.desktop_env = detect_desktop_environment()
        print(f"Detected desktop environment: {self.desktop_env}")
        
        # Initialize state variables
        self.applying = False
        self.updating_selection = False  # Flag to prevent selection loops
        
        # Create UI components
        self.create_ui()
        
        # Load CSS for styling
        self.load_css()
        
        # Connect to resize event for responsive adjustments
        self.connect("notify::default-width", self.on_resize)
        self.connect("notify::default-height", self.on_resize)
    
    def create_ui(self):
        """Create all UI components"""
        # Create toolbar view
        toolbar_view = Adw.ToolbarView()
        
        # Create header bar
        header_bar = Adw.HeaderBar()
        toolbar_view.add_top_bar(header_bar)
        
        # Add window title
        title_label = Gtk.Label()
        title_label.set_text(_("window_title"))
        title_label.add_css_class("title-3")
        header_bar.set_title_widget(title_label)
        
        # Add menu button
        menu_button = Gtk.MenuButton()
        menu_button.set_icon_name("open-menu-symbolic")
        
        # Create menu model
        menu = Gio.Menu()
        menu.append(_("about"), "app.about")
        menu.append(_("quit"), "app.quit")
        
        # Set menu to button
        menu_button.set_menu_model(menu)
        header_bar.pack_end(menu_button)
        
        # Create tab view for the three main sections
        self.tab_view = Adw.TabView()
        self.tab_view.set_vexpand(True)
        
        # Create tabs
        self.layouts_tab = self.create_layouts_tab()
        self.effects_tab = self.create_effects_tab()
        self.themes_tab = self.create_themes_tab()
        
        # Add tabs to tab view
        layouts_page = self.tab_view.append(self.layouts_tab)
        layouts_page.set_title(_("layouts_tab"))
        
        effects_page = self.tab_view.append(self.effects_tab)
        effects_page.set_title(_("effects_tab"))
        
        themes_page = self.tab_view.append(self.themes_tab)
        themes_page.set_title(_("themes_tab"))
        
        # Create tab bar
        tab_bar = Adw.TabBar()
        tab_bar.set_view(self.tab_view)
        tab_bar.set_autohide(False)
        
        # Create main container
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        main_box.append(tab_bar)
        main_box.append(self.tab_view)
        
        # Set main content
        toolbar_view.set_content(main_box)
        
        # Set toolbar view as window content
        self.set_content(toolbar_view)
    
    def create_layouts_tab(self):
        """Create the Layouts tab"""
        # Define layouts for GNOME
        layouts = [
            ("Classic", "classic.txt", "classic.png", "view-continuous-symbolic"),
            ("Vanilla", "vanilla.txt", "vanilla.png", "view-grid-symbolic"),
            ("G-Unity", "g-unity.txt", "g-unity.png", "view-app-grid-symbolic"),
            ("New", "new.txt", "new.png", "view-paged-symbolic"),
            ("Next-Gnome", "next-gnome.txt", "next-gnome.png", "view-paged-symbolic"),
            ("Modern", "modern.txt", "modern.png", "view-grid-symbolic")
        ]
        
        # Create main container
        container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        container.set_margin_start(20)
        container.set_margin_end(20)
        container.set_margin_top(20)
        container.set_margin_bottom(20)
        
        # Title
        title = Gtk.Label()
        title.set_text(_("layouts_tab"))
        title.add_css_class("title-1")
        title.set_margin_bottom(20)
        title.set_halign(Gtk.Align.START)
        container.append(title)
        
        # Description
        description = Gtk.Label()
        description.set_text(_("select_layout"))
        description.add_css_class("body")
        description.set_margin_bottom(30)
        description.set_halign(Gtk.Align.START)
        container.append(description)
        
        # Create paned widget for main layout
        paned = Gtk.Paned(orientation=Gtk.Orientation.HORIZONTAL)
        paned.set_position(500)
        paned.set_resize_start_child(True)
        paned.set_shrink_start_child(False)
        paned.set_resize_end_child(False)
        paned.set_shrink_end_child(False)
        
        # Create preview area
        preview_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        preview_container.set_halign(Gtk.Align.CENTER)
        preview_container.set_valign(Gtk.Align.CENTER)
        preview_container.set_vexpand(True)
        
        # Preview card
        preview_card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        preview_card.add_css_class("card")
        preview_card.set_size_request(400, 300)
        
        # Preview title
        self.preview_title = Gtk.Label()
        self.preview_title.add_css_class("title-2")
        self.preview_title.set_margin_bottom(15)
        self.preview_title.set_halign(Gtk.Align.CENTER)
        preview_card.append(self.preview_title)
        
        # Preview image with frame
        image_frame = Gtk.Box()
        image_frame.add_css_class("frame")
        image_frame.set_halign(Gtk.Align.CENTER)
        image_frame.set_size_request(350, 180)
        
        self.preview_image = Gtk.Picture()
        self.preview_image.set_size_request(330, 160)
        self.preview_image.set_content_fit(Gtk.ContentFit.CONTAIN)
        image_frame.append(self.preview_image)
        preview_card.append(image_frame)
        
        # Preview description
        self.preview_description = Gtk.Label()
        self.preview_description.set_margin_top(15)
        self.preview_description.set_margin_bottom(20)
        self.preview_description.set_halign(Gtk.Align.CENTER)
        self.preview_description.set_wrap(True)
        self.preview_description.set_max_width_chars(40)
        preview_card.append(self.preview_description)
        
        # Apply button
        self.apply_button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.apply_button_box.set_halign(Gtk.Align.CENTER)
        
        self.apply_button = Gtk.Button(label=_("apply"))
        self.apply_button.add_css_class("suggested-action")
        self.apply_button.add_css_class("pill")
        self.apply_button.set_size_request(150, 40)
        self.apply_button.set_margin_top(5)
        self.apply_button.connect("clicked", self.on_apply_layout_clicked)
        self.apply_button_box.append(self.apply_button)
        
        # Spinner for loading state
        self.spinner = Gtk.Spinner()
        self.spinner.set_size_request(20, 20)
        self.spinner.set_margin_start(10)
        self.spinner.set_visible(False)
        self.apply_button_box.append(self.spinner)
        
        preview_card.append(self.apply_button_box)
        preview_container.append(preview_card)
        
        # Status bar
        status_container = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        status_container.set_halign(Gtk.Align.CENTER)
        status_container.set_margin_top(15)
        
        self.status_bar = Gtk.Label()
        self.status_bar.set_wrap(True)
        self.status_bar.set_max_width_chars(40)
        status_container.append(self.status_bar)
        preview_container.append(status_container)
        
        paned.set_start_child(preview_container)
        
        # Create sidebar
        sidebar_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        sidebar_box.set_size_request(200, -1)
        
        # Sidebar header
        sidebar_header = Gtk.Label()
        sidebar_header.set_text(_("select_layout"))
        sidebar_header.add_css_class("title-3")
        sidebar_header.set_margin_start(15)
        sidebar_header.set_margin_top(15)
        sidebar_header.set_margin_bottom(15)
        sidebar_header.set_halign(Gtk.Align.START)
        sidebar_box.append(sidebar_header)
        
        # Separator
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        separator.set_margin_start(10)
        separator.set_margin_end(10)
        separator.set_margin_bottom(5)
        sidebar_box.append(separator)
        
        # Create scrolled window for layout list
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled_window.set_vexpand(True)
        
        # Layout list box
        self.layout_list_box = Gtk.ListBox()
        self.layout_list_box.set_selection_mode(Gtk.SelectionMode.SINGLE)
        
        # Connect row-selected signal for single click selection
        self.layout_list_box.connect("row-selected", self.on_layout_row_selected)
        
        # Create layout buttons
        self.layout_buttons = []
        for name, config_file, icon_file, fallback_icon in layouts:
            row = self.create_layout_row(name, icon_file, fallback_icon, config_file)
            self.layout_list_box.append(row)
            self.layout_buttons.append((row, name, config_file))
        
        scrolled_window.set_child(self.layout_list_box)
        sidebar_box.append(scrolled_window)
        
        paned.set_end_child(sidebar_box)
        container.append(paned)
        
        # Store layouts for later use
        self.layouts = layouts
        
        # Select first layout by default
        if layouts:
            self.select_layout_item((layouts[0][0], layouts[0][1]))
        
        return container
    
    def create_layout_row(self, name, icon_file, fallback_icon, config_file):
        """Create a layout row for the sidebar with improved image sizing"""
        row = Gtk.ListBoxRow()
        row.add_css_class("layout-row")
        
        # Store the layout data in the row for easy access
        row.layout_name = name
        row.config_file = config_file
        
        # Row content with improved layout
        row_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        row_box.set_margin_start(12)
        row_box.set_margin_end(12)
        row_box.set_margin_top(10)
        row_box.set_margin_bottom(10)
        
        # Create icon container with consistent sizing
        icon_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        icon_container.set_size_request(60, 60)  # Fixed size for all icons
        icon_container.add_css_class("icon-container")
        
        # Icon frame with consistent styling
        icon_frame = Gtk.Box()
        icon_frame.set_size_request(48, 48)  # Fixed icon frame size
        icon_frame.add_css_class("icon-frame")
        icon_frame.set_halign(Gtk.Align.CENTER)
        icon_frame.set_valign(Gtk.Align.CENTER)
        
        # Create image with consistent sizing
        image = Gtk.Picture()
        image.set_size_request(40, 40)  # Fixed image size
        image.set_content_fit(Gtk.ContentFit.CONTAIN)
        image.set_halign(Gtk.Align.CENTER)
        image.set_valign(Gtk.Align.CENTER)
        
        # Try to load custom icon if icon_file is provided
        if icon_file:
            icon_path = self.find_icon(icon_file)
            if icon_path:
                image.set_filename(icon_path)
            else:
                # Use fallback icon
                fallback_image = Gtk.Image.new_from_icon_name(fallback_icon)
                fallback_image.set_pixel_size(32)  # Consistent fallback size
                image.set_paintable(fallback_image.get_paintable())
        else:
            # Use fallback icon
            fallback_image = Gtk.Image.new_from_icon_name(fallback_icon)
            fallback_image.set_pixel_size(32)  # Consistent fallback size
            image.set_paintable(fallback_image.get_paintable())
        
        icon_frame.append(image)
        icon_container.append(icon_frame)
        
        # Create label container
        label_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        label_container.set_halign(Gtk.Align.START)
        label_container.set_valign(Gtk.Align.CENTER)
        label_container.set_hexpand(True)
        
        # Create label with improved styling
        label = Gtk.Label(label=name)
        label.add_css_class("layout-label")
        label.set_halign(Gtk.Align.START)
        label.set_valign(Gtk.Align.CENTER)
        label.set_ellipsize(Pango.EllipsizeMode.END)
        label.set_max_width_chars(12)  # Consistent text width
        
        label_container.append(label)
        
        # Add to row box
        row_box.append(icon_container)
        row_box.append(label_container)
        row.set_child(row_box)
        
        return row
    
    def on_layout_row_selected(self, list_box, row):
        """Handle row selection (single click)"""
        if self.updating_selection:
            return
            
        if row is None:
            return
            
        # Get the layout data directly from the row
        name = row.layout_name
        config_file = row.config_file
        
        # Select the item
        self.select_layout_item((name, config_file))
    
    def select_layout_item(self, item):
        """Select an item and update the preview"""
        self.selected_layout_item = item
        
        # Clear previous selection
        self.clear_layout_selection()
        
        # Update preview
        name, config_file = item
        self.update_layout_preview(name)
        self.highlight_selected_layout_row(name)
    
    def update_layout_preview(self, name):
        """Update the preview area"""
        self.preview_title.set_text(name)
        self.preview_description.set_text(_("description_layout").format(layout=name))
        
        # Try to load preview image
        icon_path = None
        for layout in self.layouts:
            if layout[0] == name:
                icon_path = self.find_icon(layout[2])
                break
        
        # Set image or fallback
        if icon_path and isinstance(icon_path, str) and os.path.exists(icon_path):
            self.preview_image.set_filename(icon_path)
        else:
            # Use fallback icon
            fallback_image = Gtk.Image.new_from_icon_name("view-grid-symbolic")
            fallback_image.set_pixel_size(80)
            self.preview_image.set_paintable(fallback_image.get_paintable())
    
    def highlight_selected_layout_row(self, name):
        """Highlight the selected row in the list"""
        self.updating_selection = True
        
        for row, row_name, _ in self.layout_buttons:
            if row_name == name:
                row.add_css_class("selected")
                self.layout_list_box.select_row(row)
                break
        
        self.updating_selection = False
    
    def clear_layout_selection(self):
        """Clear selection from all rows"""
        self.updating_selection = True
        
        for row, _, _ in self.layout_buttons:
            row.remove_css_class("selected")
        
        self.updating_selection = False
    
    def on_apply_layout_clicked(self, widget):
        """Handle apply button click"""
        if self.applying or not hasattr(self, 'selected_layout_item'):
            return
        
        # Disable button and show spinner
        self.set_applying_state(True)
        
        # Start applying in a separate thread
        threading.Thread(target=self.apply_selected_layout, daemon=True).start()
    
    def set_applying_state(self, applying):
        """Set the applying state of the UI"""
        self.applying = applying
        self.apply_button.set_sensitive(not applying)
        
        if applying:
            self.spinner.set_visible(True)
            self.spinner.start()
        else:
            self.spinner.set_visible(False)
            self.spinner.stop()
    
    def apply_selected_layout(self):
        """Apply the selected layout in a separate thread"""
        try:
            name, config_file = self.selected_layout_item
            GLib.idle_add(self.update_status, _("applying").format(layout=name))
            
            # Find config file path
            config_path = self.find_config_file(config_file)
            if not config_path:
                GLib.idle_add(self.update_status, _("error_config").format(file=config_file))
                return
            
            # Apply GNOME layout
            self.apply_gnome_layout(config_path)
            
            # Give desktop time to apply changes
            time.sleep(0.5)
            
            GLib.idle_add(self.update_status, _("success").format(layout=name))
        except subprocess.TimeoutExpired:
            GLib.idle_add(self.update_status, _("error_applying").format(error="Operation timed out"))
        except subprocess.CalledProcessError as e:
            GLib.idle_add(self.update_status, _("error_applying").format(error=str(e)))
        except Exception as e:
            GLib.idle_add(self.update_status, _("error").format(error=str(e)))
        finally:
            # Always reset applying state
            GLib.idle_add(self.set_applying_state, False)
    
    def apply_gnome_layout(self, config_path):
        """Apply GNOME layout using dconf"""
        # Use a more robust approach to apply the layout
        with open(config_path, 'r') as f:
            config_data = f.read()
        
        # Write to a temporary file to avoid issues
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
            temp_file.write(config_data)
            temp_file_path = temp_file.name
        
        try:
            # Apply the configuration
            subprocess.run(
                ["dconf", "load", "/org/gnome/shell/"],
                stdin=open(temp_file_path, 'r'),
                check=True,
                timeout=10
            )
        finally:
            # Clean up temporary file
            os.unlink(temp_file_path)
    
    def update_status(self, message):
        """Update the status bar safely from any thread"""
        self.status_bar.set_label(message)
        return False  # Don't call again
    
    def create_effects_tab(self):
        """Create the Effects tab"""
        # Create main container
        container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        container.set_margin_start(20)
        container.set_margin_end(20)
        container.set_margin_top(20)
        container.set_margin_bottom(20)
        
        # Title
        title = Gtk.Label()
        title.set_text(_("effects_tab"))
        title.add_css_class("title-1")
        title.set_margin_bottom(20)
        title.set_halign(Gtk.Align.START)
        container.append(title)
        
        # Description
        description = Gtk.Label()
        description.set_text(_("effects_description"))
        description.add_css_class("body")
        description.set_margin_bottom(30)
        description.set_halign(Gtk.Align.START)
        container.append(description)
        
        # Check if running on GNOME
        if self.desktop_env != 'gnome':
            # Show message that effects are only available on GNOME
            info_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            info_box.set_halign(Gtk.Align.CENTER)
            info_box.set_valign(Gtk.Align.CENTER)
            info_box.set_vexpand(True)
            
            info_icon = Gtk.Image.new_from_icon_name("dialog-information-symbolic")
            info_icon.set_pixel_size(64)
            info_icon.set_margin_bottom(20)
            info_box.append(info_icon)
            
            info_label = Gtk.Label()
            info_label.set_text(_("gnome_only"))
            info_label.add_css_class("title-3")
            info_label.set_wrap(True)
            info_label.set_max_width_chars(30)
            info_box.append(info_label)
            
            container.append(info_box)
            return container
        
        # Create effects grid
        effects_grid = Gtk.Grid()
        effects_grid.set_row_spacing(20)
        effects_grid.set_column_spacing(20)
        effects_grid.set_halign(Gtk.Align.CENTER)
        effects_grid.set_valign(Gtk.Align.CENTER)
        effects_grid.set_vexpand(True)
        
        # Define effects with updated URLs
        effects = [
            {
                "name": _("desktop_cube"),
                "description": _("desktop_cube_description"),
                "uuid": "desktop-cube@schneegans.github.com",
                "url": "https://extensions.gnome.org/extension/4648/desktop-cube/"
            },
            {
                "name": _("magic_lamp"),
                "description": _("magic_lamp_description"),
                "uuid": "compiz-alike-magic-lamp-effect@hermes83.github.com",
                "url": "https://extensions.gnome.org/extension/3740/compiz-alike-magic-lamp-effect/"
            },
            {
                "name": _("windows_effects"),
                "description": _("windows_effects_description"),
                "uuid": "compiz-windows-effect@hermes83.github.com",
                "url": "https://extensions.gnome.org/extension/3210/compiz-windows-effect/"
            }
        ]
        
        # Create effect cards
        for i, effect in enumerate(effects):
            # Effect card
            effect_card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            effect_card.add_css_class("card")
            effect_card.set_size_request(250, 220)
            
            # Effect icon
            effect_icon = Gtk.Image.new_from_icon_name("applications-graphics-symbolic")
            effect_icon.set_pixel_size(48)
            effect_icon.set_margin_top(20)
            effect_icon.set_halign(Gtk.Align.CENTER)
            effect_card.append(effect_icon)
            
            # Effect name
            effect_name = Gtk.Label()
            effect_name.set_text(effect["name"])
            effect_name.add_css_class("title-3")
            effect_name.set_margin_top(10)
            effect_name.set_halign(Gtk.Align.CENTER)
            effect_card.append(effect_name)
            
            # Effect description
            effect_description = Gtk.Label()
            effect_description.set_text(effect["description"])
            effect_description.add_css_class("body")
            effect_description.set_margin_top(5)
            effect_description.set_margin_bottom(15)
            effect_description.set_halign(Gtk.Align.CENTER)
            effect_description.set_wrap(True)
            effect_description.set_max_width_chars(20)
            effect_card.append(effect_description)
            
            # Check if extension is installed
            installed = self.check_extension_installed(effect["uuid"])
            
            if installed:
                # Check if extension is enabled
                enabled = self.check_extension_enabled(effect["uuid"])
                
                # Create toggle switch
                toggle = Gtk.Switch()
                toggle.set_active(enabled)
                toggle.set_halign(Gtk.Align.CENTER)
                toggle.set_margin_bottom(20)
                toggle.connect("notify::active", lambda switch, _, uuid=effect["uuid"]: self.toggle_extension(uuid, switch.get_active()))
                effect_card.append(toggle)
                
                # Status label
                status_label = Gtk.Label()
                status_label.set_text(_("enable") if not enabled else _("disable"))
                status_label.add_css_class("body")
                status_label.set_halign(Gtk.Align.CENTER)
                status_label.set_margin_bottom(10)
                effect_card.append(status_label)
            else:
                # Install button
                install_button = Gtk.Button(label=_("install_extension"))
                install_button.add_css_class("pill")
                install_button.set_margin_bottom(20)
                install_button.connect("clicked", lambda btn, url=effect["url"]: self.open_url(url))
                effect_card.append(install_button)
            
            # Add to grid
            effects_grid.attach(effect_card, i % 3, i // 3, 1, 1)
        
        container.append(effects_grid)
        
        return container
    
    def check_extension_installed(self, uuid):
        """Check if a GNOME extension is installed"""
        user_extensions = os.path.expanduser("~/.local/share/gnome-shell/extensions")
        system_extensions = "/usr/share/gnome-shell/extensions"
        
        # Check user extensions
        if os.path.exists(os.path.join(user_extensions, uuid)):
            return True
        
        # Check system extensions
        if os.path.exists(os.path.join(system_extensions, uuid)):
            return True
        
        return False
    
    def check_extension_enabled(self, uuid):
        """Check if a GNOME extension is enabled"""
        try:
            # Get list of enabled extensions
            result = subprocess.run(
                ["gsettings", "get", "org.gnome.shell", "enabled-extensions"],
                capture_output=True,
                text=True,
                check=True
            )
            
            # Parse the list
            enabled_extensions = result.stdout.strip().strip("[]").replace("'", "").split(", ")
            
            # Check if our extension is in the list
            return uuid in enabled_extensions
        except:
            return False
    
    def toggle_extension(self, uuid, enable):
        """Enable or disable a GNOME extension"""
        try:
            # Get current list of enabled extensions
            result = subprocess.run(
                ["gsettings", "get", "org.gnome.shell", "enabled-extensions"],
                capture_output=True,
                text=True,
                check=True
            )
            
            # Parse the list
            enabled_extensions = result.stdout.strip().strip("[]").replace("'", "").split(", ")
            
            if enable:
                # Add extension to list if not already there
                if uuid not in enabled_extensions:
                    enabled_extensions.append(uuid)
            else:
                # Remove extension from list
                if uuid in enabled_extensions:
                    enabled_extensions.remove(uuid)
            
            # Set the new list
            new_list = "@as [" + ", ".join([f"'{ext}'" for ext in enabled_extensions if ext]) + "]"
            subprocess.run(
                ["gsettings", "set", "org.gnome.shell", "enabled-extensions", new_list],
                check=True
            )
            
            # Show notification
            self.show_toast(f"{uuid} {'enabled' if enable else 'disabled'}")
            
        except subprocess.CalledProcessError as e:
            self.show_toast(f"Error toggling extension: {str(e)}")
    
    def open_url(self, url):
        """Open a URL in the default browser"""
        subprocess.run(["xdg-open", url], check=True)
    
    def create_themes_tab(self):
        """Create the Themes tab"""
        # Create main container
        container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        container.set_margin_start(20)
        container.set_margin_end(20)
        container.set_margin_top(20)
        container.set_margin_bottom(20)
        
        # Title
        title = Gtk.Label()
        title.set_text(_("themes_tab"))
        title.add_css_class("title-1")
        title.set_margin_bottom(20)
        title.set_halign(Gtk.Align.START)
        container.append(title)
        
        # Description
        description = Gtk.Label()
        description.set_text(_("themes_description"))
        description.add_css_class("body")
        description.set_margin_bottom(30)
        description.set_halign(Gtk.Align.START)
        container.append(description)
        
        # Create theme categories
        theme_notebook = Gtk.Notebook()
        theme_notebook.set_vexpand(True)
        
        # GTK Themes
        gtk_themes_page = self.create_theme_page("gtk")
        gtk_themes_label = Gtk.Label(label=_("gtk_theme"))
        theme_notebook.append_page(gtk_themes_page, gtk_themes_label)
        
        # Icon Themes
        icon_themes_page = self.create_theme_page("icons")
        icon_themes_label = Gtk.Label(label=_("icon_theme"))
        theme_notebook.append_page(icon_themes_page, icon_themes_label)
        
        # Shell Themes
        shell_themes_page = self.create_theme_page("shell")
        shell_themes_label = Gtk.Label(label=_("shell_theme"))
        theme_notebook.append_page(shell_themes_page, shell_themes_label)
        
        container.append(theme_notebook)
        
        return container
    
    def create_theme_page(self, theme_type):
        """Create a theme page for a specific type"""
        # Create scrolled window
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled_window.set_vexpand(True)
        
        # Create flow box for themes
        flow_box = Gtk.FlowBox()
        flow_box.set_selection_mode(Gtk.SelectionMode.SINGLE)
        flow_box.set_max_children_per_line(4)
        flow_box.set_min_children_per_line(2)
        flow_box.set_halign(Gtk.Align.CENTER)
        flow_box.set_valign(Gtk.Align.START)
        flow_box.set_row_spacing(20)
        flow_box.set_column_spacing(20)
        
        # Get themes based on type
        themes = self.get_themes(theme_type)
        
        if not themes:
            # No themes found message
            no_themes_label = Gtk.Label()
            no_themes_label.set_text(_("no_themes_found"))
            no_themes_label.add_css_class("title-3")
            no_themes_label.set_margin_top(50)
            no_themes_label.set_halign(Gtk.Align.CENTER)
            flow_box.append(no_themes_label)
        else:
            # Create theme cards
            for theme_name, theme_path in themes:
                theme_card = self.create_theme_card(theme_name, theme_path, theme_type)
                flow_box.append(theme_card)
        
        scrolled_window.set_child(flow_box)
        return scrolled_window
    
    def create_theme_card(self, theme_name, theme_path, theme_type):
        """Create a theme card"""
        # Create card container
        card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        card.add_css_class("card")
        card.set_size_request(200, 200)
        card.set_margin_start(10)
        card.set_margin_end(10)
        card.set_margin_top(10)
        card.set_margin_bottom(10)
        
        # Extract color from theme name
        color = extract_color_from_theme_name(theme_name)
        
        # Create color circle
        color_circle = Gtk.DrawingArea()
        color_circle.set_size_request(80, 80)
        color_circle.set_halign(Gtk.Align.CENTER)
        color_circle.set_margin_top(20)
        color_circle.set_draw_func(self.draw_color_circle, color)
        card.append(color_circle)
        
        # Theme name
        name_label = Gtk.Label()
        name_label.set_text(theme_name)
        name_label.add_css_class("title-4")
        name_label.set_margin_top(15)
        name_label.set_halign(Gtk.Align.CENTER)
        name_label.set_ellipsize(Pango.EllipsizeMode.END)
        name_label.set_max_width_chars(15)
        card.append(name_label)
        
        # Apply button
        apply_button = Gtk.Button(label=_("apply_theme"))
        apply_button.add_css_class("pill")
        apply_button.set_margin_top(15)
        apply_button.set_margin_bottom(20)
        apply_button.set_halign(Gtk.Align.CENTER)
        apply_button.connect("clicked", lambda btn: self.apply_theme(theme_name, theme_type))
        card.append(apply_button)
        
        return card
    
    def draw_color_circle(self, drawing_area, ctx, width, height, color):
        """Draw a color circle"""
        # Set background color
        ctx.set_source_rgb(int(color[1:3], 16)/255, int(color[3:5], 16)/255, int(color[5:7], 16)/255)
        
        # Draw circle
        ctx.arc(width/2, height/2, min(width, height)/2 - 5, 0, 2 * 3.14159)
        ctx.fill()
    
    def get_themes(self, theme_type):
        """Get available themes of a specific type"""
        themes = []
        
        # User themes directory
        user_themes_dir = os.path.expanduser("~/.themes")
        
        # System themes directory
        system_themes_dir = "/usr/share/themes"
        
        # Check both directories
        for themes_dir in [user_themes_dir, system_themes_dir]:
            if not os.path.exists(themes_dir):
                continue
            
            # Get all theme directories
            for theme_dir in os.listdir(themes_dir):
                theme_path = os.path.join(themes_dir, theme_dir)
                
                # Skip if not a directory
                if not os.path.isdir(theme_path):
                    continue
                
                # Check based on theme type
                if theme_type == "gtk":
                    # Check for gtk-3.0 or gtk-2.0 directory
                    if os.path.exists(os.path.join(theme_path, "gtk-3.0")) or \
                       os.path.exists(os.path.join(theme_path, "gtk-2.0")):
                        themes.append((theme_dir, theme_path))
                
                elif theme_type == "icons":
                    # Check for index.theme file in icons directory
                    icons_dir = os.path.join(theme_path, "icons")
                    if os.path.exists(icons_dir) and \
                       os.path.exists(os.path.join(icons_dir, "index.theme")):
                        themes.append((theme_dir, theme_path))
                
                elif theme_type == "shell":
                    # Check for gnome-shell directory
                    if os.path.exists(os.path.join(theme_path, "gnome-shell")):
                        themes.append((theme_dir, theme_path))
        
        # Remove duplicates and sort
        themes = list(set(themes))
        themes.sort(key=lambda x: x[0].lower())
        
        return themes
    
    def apply_theme(self, theme_name, theme_type):
        """Apply a theme"""
        try:
            if theme_type == "gtk":
                # Apply GTK theme
                subprocess.run(["gsettings", "set", "org.gnome.desktop.interface", "gtk-theme", theme_name], check=True)
            
            elif theme_type == "icons":
                # Apply icon theme
                subprocess.run(["gsettings", "set", "org.gnome.desktop.interface", "icon-theme", theme_name], check=True)
            
            elif theme_type == "shell":
                # Apply shell theme
                subprocess.run(["gsettings", "set", "org.gnome.shell.extensions.user-theme", "name", theme_name], check=True)
            
            # Show success message
            self.show_toast(f"{theme_name} theme applied successfully")
        
        except subprocess.CalledProcessError as e:
            self.show_toast(f"Error applying theme: {str(e)}")
    
    def show_toast(self, message):
        """Show a toast notification"""
        toast = Adw.Toast.new(message)
        toast.set_timeout(3)
        
        # Get the toast overlay from the main window
        if hasattr(self, 'toast_overlay'):
            self.toast_overlay.add_toast(toast)
    
    def on_resize(self, widget, param):
        """Handle window resize for responsive adjustments"""
        width = self.get_width()
        
        # Adjust preview image size if in layouts tab
        if hasattr(self, 'preview_image'):
            if width < 700:
                self.preview_image.set_size_request(280, 140)
            else:
                self.preview_image.set_size_request(330, 160)
    
    def find_icon(self, icon_name):
        """Search for icon in common locations"""
        if not icon_name:
            return None
            
        possible_paths = [
            os.path.join(os.path.dirname(__file__), "icons", icon_name),
            os.path.expanduser(f"~/.local/share/icons/{icon_name}"),
            f"/usr/share/icons/{icon_name}",
            f"/usr/local/share/icons/{icon_name}"
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
        
        # Try with different extensions
        base_name, ext = os.path.splitext(icon_name)
        for ext in ['.png', '.jpg', '.jpeg', '.svg']:
            test_path = base_name + ext
            for path in possible_paths:
                test_path = os.path.join(os.path.dirname(path), os.path.basename(test_path))
                if os.path.exists(test_path):
                    return test_path
        
        return None
    
    def find_config_file(self, config_file):
        """Search for config file in common locations"""
        config_dir = "gnome-layouts"
        
        possible_paths = [
            os.path.join(os.path.dirname(__file__), config_dir, config_file),
            os.path.expanduser(f"~/.config/{config_dir}/{config_file}"),
            f"/usr/share/{config_dir}/{config_file}"
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
        
        return None
    
    def load_css(self):
        """Load CSS for styling"""
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(b"""
            .layout-row {
                border-radius: 8px;
                margin: 4px;
                transition: all 200ms ease;
                min-height: 70px;
            }
            .layout-row:hover {
                background-color: alpha(@theme_fg_color, 0.1);
            }
            .layout-row.selected {
                background-color: @theme_selected_bg_color;
                color: @theme_selected_fg_color;
            }
            .icon-container {
                background-color: alpha(@theme_fg_color, 0.05);
                border-radius: 12px;
                padding: 6px;
            }
            .icon-frame {
                background-color: alpha(@theme_fg_color, 0.1);
                border-radius: 8px;
                padding: 4px;
            }
            .layout-label {
                font-weight: 500;
                font-size: 13pt;
            }
            .success {
                color: #26a269;
                font-weight: bold;
            }
            .theme-card {
                transition: all 200ms ease;
            }
            .theme-card:hover {
                transform: translateY(-5px);
            }
        """)
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

class BigAppearanceApp(Adw.Application):
    def __init__(self):
        super().__init__(application_id='org.bigCommunity.big-appearance')
        self.connect('activate', self.on_activate)
        
        # Add actions
        about_action = Gio.SimpleAction.new("about", None)
        about_action.connect("activate", self.on_about)
        self.add_action(about_action)
        
        quit_action = Gio.SimpleAction.new("quit", None)
        quit_action.connect("activate", lambda *args: self.quit())
        self.add_action(quit_action)
    
    def on_activate(self, app):
        win = BigAppearanceWindow(app)
        win.present()
    
    def on_about(self, action, param):
        """Show about dialog"""
        about_dialog = Adw.AboutWindow()
        
        # Set transient parent
        active_window = self.get_active_window()
        if active_window:
            about_dialog.set_transient_for(active_window)
        
        # Set application information
        about_dialog.set_application_name(_("window_title"))
        about_dialog.set_version("1.0")
        about_dialog.set_developer_name("Big Community & Ari Novais")
        about_dialog.set_license_type(Gtk.License.MIT)
        about_dialog.set_license(_("license"))
        about_dialog.set_comments(_("select_layout"))
        about_dialog.set_website("https://communitybig.org/")
        about_dialog.set_issue_url("https://github.com/big-comm/comm-layout-changer/issues")
        
        # Set logo icon using the correct method
        about_dialog.set_icon_name("org.bigCommunity.big-appearance")
        
        # Add copyright information
        about_dialog.set_copyright("© 2022 - 2025 Big Community")
        
        # Show the about dialog
        about_dialog.present()

if __name__ == "__main__":
    app = BigAppearanceApp()
    app.run(sys.argv)
