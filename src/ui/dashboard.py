#!/usr/bin/env python3
"""
Main Dashboard UI

Professional desktop interface for the FPS Gaming Tweaker.
"""

import PySimpleGUI as sg
import logging
from pathlib import Path
from core.hardware import HardwareDetector
from core.admin import check_admin_privileges
from utils.benchmark import SystemBenchmark
from ui.themes import Theme
from ui.widgets import Widgets

logger = logging.getLogger(__name__)


class TweakerDashboard:
    """Main application dashboard."""
    
    def __init__(self, theme: str = 'DARK'):
        """Initialize dashboard.
        
        Args:
            theme: UI theme name
        """
        self.theme = Theme.get_theme(theme)
        sg.theme_background_color(self.theme['bg_color'])
        sg.theme_text_color(self.theme['fg_color'])
        sg.theme_button_color((self.theme['button_fg'], self.theme['button_color']))
        
        self.window = None
        self.hardware_detector = HardwareDetector()
        self.benchmark = SystemBenchmark()
        self.profile = self.hardware_detector.get_full_profile()
    
    def _create_system_overview_tab(self) -> sg.Tab:
        """Create system overview tab.
        
        Returns:
            sg.Tab: System overview tab
        """
        profile = self.profile
        
        info_text = (
            f"🖥️  SYSTEM PROFILE\n"
            f"{'='*50}\n\n"
            f"Windows: {profile.windows_version} (Build {profile.build_number})\n"
            f"Power Plan: {profile.power_plan}\n\n"
            f"CPU: {profile.cpu.brand}\n"
            f"  • Cores: {profile.cpu.cores} | Threads: {profile.cpu.threads}\n"
            f"  • Base: {profile.cpu.base_freq_ghz} GHz | Max: {profile.cpu.max_freq_ghz} GHz\n"
            f"  • Cache: {profile.cpu.cache_mb} MB\n\n"
            f"RAM: {profile.ram_gb} GB\n\n"
            f"GPU: {len(profile.gpus)} device(s)\n"
        )
        
        for i, gpu in enumerate(profile.gpus, 1):
            info_text += f"  {i}. {gpu.name} ({gpu.vram_gb} GB)\n"
        
        info_text += (
            f"\n"
            f"Storage: {profile.storage_type} ({profile.total_storage_gb} GB)\n"
            f"Monitor: {profile.monitor_refresh_rate} Hz\n"
        )
        
        layout = [
            [Widgets.create_info_box(info_text, color='#2a5cdb')],
            [sg.Button('🔄 Refresh', key='REFRESH_PROFILE'), 
             sg.Button('📊 Benchmark', key='RUN_BENCHMARK')]
        ]
        
        return sg.Tab('🖥️  System Overview', layout)
    
    def _create_optimizations_tab(self) -> sg.Tab:
        """Create optimizations tab.
        
        Returns:
            sg.Tab: Optimizations tab
        """
        layout = [
            [sg.Text('Select optimizations to apply:', font=('Arial', 11, 'bold'))],
            [sg.Listbox(
                ['Windows Performance', 'Gaming Tweaks', 'Input Latency', 'Power Management'],
                size=(40, 6),
                key='OPTIMIZATION_LIST'
            )],
            [sg.Button('ℹ️  Details', key='OPT_DETAILS'),
             sg.Button('✅ Apply', key='APPLY_OPT'),
             sg.Button('↩️  Rollback', key='ROLLBACK_OPT')]
        ]
        
        return sg.Tab('⚙️  Optimizations', layout)
    
    def _create_recommendations_tab(self) -> sg.Tab:
        """Create smart recommendations tab.
        
        Returns:
            sg.Tab: Recommendations tab
        """
        profile = self.profile
        
        # Determine PC category
        if profile.cpu.cores >= 16 and profile.ram_gb >= 32:
            category = "🏆 High-End Gaming PC"
        elif profile.cpu.cores >= 8 and profile.ram_gb >= 16:
            category = "⚡ Mid-Range Gaming PC"
        else:
            category = "💻 Entry-Level Gaming PC"
        
        recommendations = (
            f"System Category: {category}\n\n"
            f"Recommended Optimizations:\n"
            f"✓ Enable Game Mode\n"
            f"✓ Disable Visual Effects\n"
            f"✓ Set High Performance Power Plan\n"
            f"✓ Disable Background Apps\n"
            f"✓ Optimize Mouse Settings\n"
            f"✓ Disable USB Selective Suspend\n"
        )
        
        layout = [
            [Widgets.create_info_box(recommendations, color='#388e3c')],
            [sg.Button('🎮 Game-Specific Tips', key='GAME_TIPS'),
             sg.Button('📚 Optimization Guide', key='OPT_GUIDE')]
        ]
        
        return sg.Tab('💡 Recommendations', layout)
    
    def _create_logs_tab(self) -> sg.Tab:
        """Create logs viewer tab.
        
        Returns:
            sg.Tab: Logs tab
        """
        log_file = Path(__file__).parent.parent.parent / 'logs' / 'tweaker.log'
        
        log_content = ""
        if log_file.exists():
            with open(log_file, 'r') as f:
                lines = f.readlines()
                log_content = ''.join(lines[-50:])  # Last 50 lines
        
        layout = [
            [sg.Multiline(
                log_content,
                size=(70, 20),
                disabled=True,
                background_color='#1e1e1e',
                text_color='#00ff00',
                key='LOG_VIEWER'
            )],
            [sg.Button('🔄 Refresh Logs', key='REFRESH_LOGS'),
             sg.Button('📁 Open Log Dir', key='OPEN_LOG_DIR'),
             sg.Button('🗑️  Clear Logs', key='CLEAR_LOGS')]
        ]
        
        return sg.Tab('📋 Logs', layout)
    
    def _create_menu(self) -> list:
        """Create application menu.
        
        Returns:
            list: Menu layout
        """
        return [
            ['File', ['Export Profile', 'Import Profile', 'Exit']],
            ['Edit', ['Settings', 'Preferences']],
            ['Tools', ['Benchmark', 'Driver Info', 'Network Optimization']],
            ['Help', ['About', 'Documentation', 'GitHub']],
        ]
    
    def _create_main_layout(self) -> list:
        """Create main window layout.
        
        Returns:
            list: Main layout
        """
        is_admin, _ = check_admin_privileges()
        admin_status = "🔓 Administrator" if is_admin else "🔒 User"
        
        tab_group = sg.TabGroup([
            self._create_system_overview_tab(),
            self._create_optimizations_tab(),
            self._create_recommendations_tab(),
            self._create_logs_tab(),
        ])
        
        layout = [
            [sg.Menu(self._create_menu())],
            [sg.Text(
                '🎮 FPS Gaming Tweaker',
                font=('Arial', 16, 'bold'),
                text_color=self.theme['info_color']
            )],
            [sg.Text('Safe, Transparent, Reversible Performance Optimization', 
                     text_color='gray', font=('Arial', 9))],
            [sg.Text(f'Status: {admin_status}', key='STATUS', text_color='green')],
            [sg.Separator()],
            [tab_group],
            [sg.Separator()],
            [sg.Text(
                '⚠️  Always backup your system before applying optimizations. '
                'All changes are reversible.',
                text_color=self.theme['warning_color'],
                font=('Arial', 8)
            )],
            [sg.Button('✅ Apply Selected', key='APPLY_SELECTED'),
             sg.Button('↩️  Rollback All', key='ROLLBACK_ALL'),
             sg.Button('💾 Save Profile', key='SAVE_PROFILE'),
             sg.Button('📂 Load Profile', key='LOAD_PROFILE'),
             sg.Button('❌ Exit', key='EXIT')],
        ]
        
        return layout
    
    def run(self) -> None:
        """Run the dashboard."""
        layout = self._create_main_layout()
        
        self.window = sg.Window(
            'FPS Gaming Tweaker',
            layout,
            finalize=True,
            size=(900, 700),
            icon=None,
            resizable=True
        )
        
        logger.info("Dashboard started")
        
        while True:
            event, values = self.window.read(timeout=100)
            
            if event == sg.WINDOW_CLOSED or event == 'EXIT':
                break
            
            elif event == 'REFRESH_PROFILE':
                self.profile = self.hardware_detector.get_full_profile()
                sg.popup_ok('✅ System profile refreshed', title='Success')
            
            elif event == 'RUN_BENCHMARK':
                sg.popup_ok(
                    'Running benchmark...\n\n'
                    'This will take a few seconds.',
                    title='Benchmark'
                )
                self.benchmark.run()
            
            elif event == 'APPLY_SELECTED':
                sg.popup_ok(
                    '⚠️  This feature requires full implementation.\n\n'
                    'Current build focuses on structure and safety.\n'
                    'All changes are logged and reversible.',
                    title='Apply Optimizations'
                )
            
            elif event == 'GAME_TIPS':
                game = sg.popup_yes_no(
                    'Select a game for optimization tips:\n'
                    'Yes: Fortnite\nNo: Valorant',
                    title='Game Selection'
                )
                if game:
                    sg.popup_ok(
                        'Fortnite Optimization Tips:\n'
                        '✓ Set quality to LOW for FPS\n'
                        '✓ Disable shadows and effects\n'
                        '✓ Enable NVIDIA Reflex if available',
                        title='Fortnite Tips'
                    )
                else:
                    sg.popup_ok(
                        'Valorant Optimization Tips:\n'
                        '✓ Set resolution to 1280x960\n'
                        '✓ Max out FPS (usually 300+)\n'
                        '✓ Focus on monitor refresh rate',
                        title='Valorant Tips'
                    )
            
            elif event == 'REFRESH_LOGS':
                log_file = Path(__file__).parent.parent.parent / 'logs' / 'tweaker.log'
                if log_file.exists():
                    with open(log_file, 'r') as f:
                        lines = f.readlines()
                        self.window['LOG_VIEWER'].update(''.join(lines[-50:]))
        
        self.window.close()
        logger.info("Dashboard closed")
