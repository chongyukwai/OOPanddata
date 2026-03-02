"""
Tabs package - contains all notebook tabs
"""

from gui.tabs.dashboard_tab import DashboardTab
from gui.tabs.catalog_tab import CatalogTab
from gui.tabs.users_tab import UsersTab
from gui.tabs.borrow_tab import BorrowTab
from gui.tabs.oop_demo_tab import OOPDemoTab

__all__ = [
    'DashboardTab',
    'CatalogTab',
    'UsersTab',
    'BorrowTab',
    'OOPDemoTab'
]