#!/usr/bin/env python3
"""
CPCReady Configuration GUI
Interfaz gráfica con PySide6 para configurar CPCReady usando TOML.
"""

import sys
from pathlib import Path
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QLabel, QLineEdit, QPushButton, QComboBox,
    QFileDialog, QMessageBox, QGroupBox, QFormLayout
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QIcon, QPixmap, QPainter, QColor

# Python 3.11+ tiene tomllib incluido, versiones anteriores necesitan tomli
try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

import tomli_w


def create_default_icon():
    """Crea un icono predeterminado si no existe archivo."""
    pixmap = QPixmap(64, 64)
    pixmap.fill(QColor("#2196F3"))  # Azul
    
    painter = QPainter(pixmap)
    painter.setPen(QColor("white"))
    font = painter.font()
    font.setPointSize(32)
    font.setBold(True)
    painter.setFont(font)
    painter.drawText(pixmap.rect(), Qt.AlignCenter, "C")
    painter.end()
    
    return QIcon(pixmap)


class ConfigManager:
    """Gestor de configuración basado en TOML."""
    
    def __init__(self, config_file: str = "cpcready.toml"):
        self.config_dir = Path.home() / ".config" / "cpcready"
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.config_path = self.config_dir / config_file
        self._ensure_config()
    
    def _default_config(self):
        return {
            "drive": {
                "drive_a": "",
                "drive_b": "",
                "selected_drive": "A"
            },
            "emulator": {
                "default": "RetroVirtualMachine",
                "retro_virtual_machine_path": "",
                "m4board_ip": ""
            },
            "system": {
                "user": 0,
                "model": "6128",
                "mode": 1
            }
        }
    
    def _ensure_config(self):
        if not self.config_path.exists():
            self._write(self._default_config())
    
    def _read(self):
        if not self.config_path.exists():
            return self._default_config()
        with open(self.config_path, "rb") as f:
            return tomllib.load(f)
    
    def _write(self, data):
        with open(self.config_path, "wb") as f:
            tomli_w.dump(data, f)
    
    def get_all(self):
        return self._read()
    
    def save_all(self, data):
        self._write(data)


class CPCReadyConfigGUI(QMainWindow):
    """Ventana principal de configuración."""
    
    def __init__(self, app_icon=None):
        super().__init__()
        self.config_manager = ConfigManager()
        self.config = self.config_manager.get_all()
        self.app_icon = app_icon  # Guardar referencia al icono
        
        self.setWindowTitle("CPCReady Configuration")
        self.setMinimumSize(600, 400)
        
        # Establecer icono de la ventana si existe
        if self.app_icon:
            self.setWindowIcon(self.app_icon)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        
        # Título
        title = QLabel("CPCReady Configuration Editor")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)
        
        # # Info del archivo TOML
        # toml_info = QLabel(f"File: {self.config_manager.config_path}")
        # toml_info.setStyleSheet("color: gray; font-size: 10px;")
        # toml_info.setAlignment(Qt.AlignCenter)
        # main_layout.addWidget(toml_info)
        
        # Tabs
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)
        
        # Crear pestañas
        self.create_drive_tab()
        self.create_emulator_tab()
        self.create_cpc_tab()
        
        # Botones de acción
        button_layout = QHBoxLayout()
        
        self.save_button = QPushButton("💾 Save")
        self.save_button.clicked.connect(self.save_config)
        
        self.cancel_button = QPushButton("❌ Cancel")
        self.cancel_button.clicked.connect(self.close)
        
        self.reload_button = QPushButton("🔄 Reload")
        self.reload_button.clicked.connect(self.reload_config)
        
        button_layout.addWidget(self.reload_button)
        button_layout.addStretch()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        
        main_layout.addLayout(button_layout)
    
    def create_drive_tab(self):
        """Crea la pestaña de configuración de drives."""
        drive_widget = QWidget()
        layout = QVBoxLayout(drive_widget)
        
        # GroupBox para drives
        drives_group = QGroupBox("Disc Drives")
        drives_layout = QFormLayout()
        
        # Drive A
        drive_a_layout = QHBoxLayout()
        self.drive_a_input = QLineEdit(self.config.get("drive", {}).get("drive_a", ""))
        self.drive_a_input.setPlaceholderText("Path to DSK file for Drive A")
        drive_a_browse = QPushButton("📁 Browse")
        drive_a_browse.clicked.connect(lambda: self.browse_dsk_file(self.drive_a_input))
        drive_a_layout.addWidget(self.drive_a_input)
        drive_a_layout.addWidget(drive_a_browse)
        drives_layout.addRow("Drive A:", drive_a_layout)
        
        # Drive B
        drive_b_layout = QHBoxLayout()
        self.drive_b_input = QLineEdit(self.config.get("drive", {}).get("drive_b", ""))
        self.drive_b_input.setPlaceholderText("Path to DSK file for Drive B")
        drive_b_browse = QPushButton("📁 Browse")
        drive_b_browse.clicked.connect(lambda: self.browse_dsk_file(self.drive_b_input))
        drive_b_layout.addWidget(self.drive_b_input)
        drive_b_layout.addWidget(drive_b_browse)
        drives_layout.addRow("Drive B:", drive_b_layout)
        
        # Selected Drive
        self.selected_drive_combo = QComboBox()
        self.selected_drive_combo.addItems(["A", "B"])
        current_selected = self.config.get("drive", {}).get("selected_drive", "A")
        self.selected_drive_combo.setCurrentText(current_selected)
        drives_layout.addRow("Selected Drive:", self.selected_drive_combo)
        
        drives_group.setLayout(drives_layout)
        layout.addWidget(drives_group)
        layout.addStretch()
        
        self.tabs.addTab(drive_widget, "💾 Drives")
    
    def create_emulator_tab(self):
        """Crea la pestaña de configuración de emulador."""
        emulator_widget = QWidget()
        layout = QVBoxLayout(emulator_widget)
        
        # GroupBox para emulador
        emulator_group = QGroupBox("Emulator Settings")
        emulator_layout = QFormLayout()
        
        # Default Emulator
        self.emulator_combo = QComboBox()
        self.emulator_combo.addItems(["RetroVirtualMachine", "M4Board", "CPCEmu"])
        current_emulator = self.config.get("emulator", {}).get("default", "RetroVirtualMachine")
        self.emulator_combo.setCurrentText(current_emulator)
        self.emulator_combo.currentTextChanged.connect(self.on_emulator_changed)
        emulator_layout.addRow("Default Emulator:", self.emulator_combo)
        
        emulator_group.setLayout(emulator_layout)
        layout.addWidget(emulator_group)
        
        # GroupBox para RetroVirtualMachine
        self.rvm_group = QGroupBox("RetroVirtualMachine")
        rvm_layout = QFormLayout()
        
        rvm_path_layout = QHBoxLayout()
        self.rvm_path_input = QLineEdit(self.config.get("emulator", {}).get("retro_virtual_machine_path", ""))
        self.rvm_path_input.setPlaceholderText("Path to RetroVirtualMachine executable")
        rvm_browse = QPushButton("📁 Browse")
        rvm_browse.clicked.connect(lambda: self.browse_executable(self.rvm_path_input))
        rvm_path_layout.addWidget(self.rvm_path_input)
        rvm_path_layout.addWidget(rvm_browse)
        rvm_layout.addRow("Executable Path:", rvm_path_layout)
        
        self.rvm_group.setLayout(rvm_layout)
        layout.addWidget(self.rvm_group)
        
        # GroupBox para M4Board
        self.m4board_group = QGroupBox("M4Board")
        m4board_layout = QFormLayout()
        
        self.m4board_ip_input = QLineEdit(self.config.get("emulator", {}).get("m4board_ip", ""))
        self.m4board_ip_input.setPlaceholderText("192.168.1.100")
        m4board_layout.addRow("IP Address:", self.m4board_ip_input)
        
        self.m4board_group.setLayout(m4board_layout)
        layout.addWidget(self.m4board_group)
        
        layout.addStretch()
        
        # Mostrar/ocultar grupos según emulador seleccionado
        self.on_emulator_changed(current_emulator)
        
        self.tabs.addTab(emulator_widget, "🎮 Emulator")
    
    def create_cpc_tab(self):
        """Crea la pestaña de configuración del CPC."""
        cpc_widget = QWidget()
        layout = QVBoxLayout(cpc_widget)
        
        # GroupBox para CPC Settings
        cpc_group = QGroupBox("CPC Settings")
        cpc_layout = QFormLayout()
        
        # CPC Model
        self.cpc_model_combo = QComboBox()
        self.cpc_model_combo.addItems(["464", "664", "6128"])
        current_model = str(self.config.get("system", {}).get("model", "6128"))
        self.cpc_model_combo.setCurrentText(current_model)
        cpc_layout.addRow("CPC Model:", self.cpc_model_combo)
        
        # CPC Mode
        self.cpc_mode_combo = QComboBox()
        self.cpc_mode_combo.addItems(["0", "1", "2"])
        current_mode = str(self.config.get("system", {}).get("mode", 1))
        self.cpc_mode_combo.setCurrentText(current_mode)
        cpc_layout.addRow("Video Mode:", self.cpc_mode_combo)
        
        # User Number
        self.user_number_combo = QComboBox()
        self.user_number_combo.addItems([str(i) for i in range(16)])  # 0-15
        current_user = str(self.config.get("system", {}).get("user", 0))
        self.user_number_combo.setCurrentText(current_user)
        cpc_layout.addRow("User Number:", self.user_number_combo)
        
        cpc_group.setLayout(cpc_layout)
        layout.addWidget(cpc_group)
        layout.addStretch()
        
        self.tabs.addTab(cpc_widget, "🖥️ CPC")
    
    def on_emulator_changed(self, emulator):
        """Muestra/oculta opciones según el emulador seleccionado."""
        self.rvm_group.setVisible(emulator == "RetroVirtualMachine")
        self.m4board_group.setVisible(emulator == "M4Board")
    
    def browse_dsk_file(self, line_edit):
        """Abre diálogo para seleccionar archivo DSK."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select DSK File",
            str(Path.home()),
            "DSK Files (*.dsk *.DSK);;All Files (*)"
        )
        if file_path:
            line_edit.setText(file_path)
    
    def browse_executable(self, line_edit):
        """Abre diálogo para seleccionar ejecutable."""
        if sys.platform == "darwin":
            # En macOS, permitir seleccionar .app
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "Select Executable",
                "/Applications",
                "Applications (*.app);;All Files (*)"
            )
        else:
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "Select Executable",
                str(Path.home()),
                "Executables (*.exe);;All Files (*)"
            )
        if file_path:
            line_edit.setText(file_path)
    
    def validate_ip(self, ip):
        """Valida formato de IP."""
        if not ip:
            return True  # Vacío es válido
        parts = ip.split('.')
        if len(parts) != 4:
            return False
        try:
            return all(0 <= int(p) <= 255 for p in parts)
        except:
            return False
    
    def save_config(self):
        """Guarda la configuración en TOML."""
        # Validar IP de M4Board si está configurado
        m4_ip = self.m4board_ip_input.text()
        if m4_ip and not self.validate_ip(m4_ip):
            msg = QMessageBox(self)
            msg.setWindowTitle("Invalid IP")
            msg.setText("M4Board IP address format is invalid.\nUse format: xxx.xxx.xxx.xxx")
            if self.app_icon:
                msg.setWindowIcon(self.app_icon)
                msg.setIconPixmap(self.app_icon.pixmap(64, 64))
            else:
                msg.setIcon(QMessageBox.Warning)
            msg.exec()
            return
        
        # Construir configuración
        new_config = {
            "drive": {
                "drive_a": self.drive_a_input.text(),
                "drive_b": self.drive_b_input.text(),
                "selected_drive": self.selected_drive_combo.currentText()
            },
            "emulator": {
                "default": self.emulator_combo.currentText(),
                "retro_virtual_machine_path": self.rvm_path_input.text(),
                "m4board_ip": m4_ip
            },
            "system": {
                "user": int(self.user_number_combo.currentText()),
                "model": self.cpc_model_combo.currentText(),
                "mode": int(self.cpc_mode_combo.currentText())
            }
        }
        
        # Guardar
        try:
            self.config_manager.save_all(new_config)
            msg = QMessageBox(self)
            msg.setWindowTitle("Success")
            msg.setText(f"Configuration saved successfully!")
            if self.app_icon:
                msg.setWindowIcon(self.app_icon)
                msg.setIconPixmap(self.app_icon.pixmap(64, 64))
            else:
                msg.setIcon(QMessageBox.Information)
            msg.exec()
            self.config = new_config
        except Exception as e:
            msg = QMessageBox(self)
            msg.setWindowTitle("Error")
            msg.setText(f"Failed to save configuration:\n{str(e)}")
            if self.app_icon:
                msg.setWindowIcon(self.app_icon)
                msg.setIconPixmap(self.app_icon.pixmap(64, 64))
            else:
                msg.setIcon(QMessageBox.Critical)
            msg.exec()
    
    def reload_config(self):
        """Recarga la configuración desde el archivo TOML."""
        msg = QMessageBox(self)
        msg.setWindowTitle("Reload Configuration")
        msg.setText("This will discard any unsaved changes.\nDo you want to continue?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.No)
        if self.app_icon:
            msg.setWindowIcon(self.app_icon)
            msg.setIconPixmap(self.app_icon.pixmap(64, 64))
        else:
            msg.setIcon(QMessageBox.Question)
        reply = msg.exec()
        
        if reply == QMessageBox.Yes:
            self.config = self.config_manager.get_all()
            
            # Actualizar campos de drive
            self.drive_a_input.setText(self.config.get("drive", {}).get("drive_a", ""))
            self.drive_b_input.setText(self.config.get("drive", {}).get("drive_b", ""))
            self.selected_drive_combo.setCurrentText(self.config.get("drive", {}).get("selected_drive", "A"))
            
            # Actualizar campos de emulator
            self.emulator_combo.setCurrentText(self.config.get("emulator", {}).get("default", "RetroVirtualMachine"))
            self.rvm_path_input.setText(self.config.get("emulator", {}).get("retro_virtual_machine_path", ""))
            self.m4board_ip_input.setText(self.config.get("emulator", {}).get("m4board_ip", ""))
            
            # Actualizar campos de CPC
            self.cpc_model_combo.setCurrentText(str(self.config.get("system", {}).get("model", "6128")))
            self.cpc_mode_combo.setCurrentText(str(self.config.get("system", {}).get("mode", 1)))
            self.user_number_combo.setCurrentText(str(self.config.get("system", {}).get("user", 0)))
            
            msg = QMessageBox(self)
            msg.setWindowTitle("Success")
            msg.setText("Configuration reloaded successfully!")
            if self.app_icon:
                msg.setWindowIcon(self.app_icon)
                msg.setIconPixmap(self.app_icon.pixmap(64, 64))
            else:
                msg.setIcon(QMessageBox.Information)
            msg.exec()


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # Estilo moderno
    
    # Configurar icono de la aplicación (para ventanas y diálogos)
    icon_path = Path(__file__).parent / "resources" / "icon.png"
    if icon_path.exists():
        app_icon = QIcon(str(icon_path))
    else:
        app_icon = create_default_icon()
    
    app.setWindowIcon(app_icon)
    
    # Intentar configurar el icono del Dock en macOS
    if sys.platform == "darwin":
        try:
            from AppKit import NSApplication, NSImage
            ns_app = NSApplication.sharedApplication()
            
            if icon_path.exists():
                # Usar archivo si existe
                logo_ns = NSImage.alloc().initWithContentsOfFile_(str(icon_path))
                ns_app.setApplicationIconImage_(logo_ns)
            else:
                # Crear icono temporal desde QPixmap
                temp_icon = Path("/tmp/cpcready_icon.png")
                pixmap = app_icon.pixmap(128, 128)
                pixmap.save(str(temp_icon))
                logo_ns = NSImage.alloc().initWithContentsOfFile_(str(temp_icon))
                ns_app.setApplicationIconImage_(logo_ns)
        except ImportError:
            # pyobjc-framework-Cocoa no está instalado
            pass
    
    window = CPCReadyConfigGUI(app_icon)
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
