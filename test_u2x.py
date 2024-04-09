import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Gdk', '4.0')

from gi.repository import Gtk, Gdk
from unittest import TestCase
from u2x import Encoder, U2X, APP_ID, APP_TITLE, SPACING, SPACING_SM, APP_ICON

UNICODE_TEXT = 'درود به همه!'
XML_TEXT = '&#1583;&#1585;&#1608;&#1583; &#1576;&#1607; &#1607;&#1605;&#1607;!'
TOOL_DATA = {
    'label': 'Sample Tool',
    'icon': 'help-about',
    'tooltip': 'Alt + s',
    'keyval': Gdk.KEY_s,
    'callback': lambda w, d: d,
}


class TestEncoder(TestCase):
    def test_xml_to_unicode(self):
        self.assertEqual(Encoder.xml_to_unicode(XML_TEXT), UNICODE_TEXT)

    def test_unicode_to_xml(self):
        self.assertEqual(Encoder.unicode_to_xml(UNICODE_TEXT), XML_TEXT)


class TestU2X(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.u2x = U2X(application_id=APP_ID)

    def test_app(self):
        self.assertEqual(self.u2x.get_application_id(), APP_ID)

    def test_unicode_text(self):
        self.u2x.create_unicode_textview()
        self.u2x.set_unicode_text(UNICODE_TEXT)
        self.assertEqual(self.u2x.get_unicode_text(), UNICODE_TEXT)

    def test_xml_text(self):
        self.u2x.create_xml_textview()
        self.u2x.set_xml_text(XML_TEXT)
        self.assertEqual(self.u2x.get_xml_text(), XML_TEXT)

    def test_create_tool(self):
        tool = self.u2x.create_tool(TOOL_DATA)
        self.assertIsInstance(tool, Gtk.Button)

        tool_content = tool.get_child()
        self.assertIsInstance(tool_content, Gtk.Box)
        self.assertEqual(tool_content.get_halign(), Gtk.Align.CENTER)
        self.assertEqual(tool_content.get_spacing(), SPACING_SM)

        icon = tool_content.get_first_child()
        self.assertIsInstance(icon, Gtk.Image)
        self.assertEqual(icon.get_icon_name(), TOOL_DATA['icon'])

        label = tool_content.get_last_child()
        self.assertIsInstance(label, Gtk.Label)
        self.assertEqual(label.get_text(), TOOL_DATA['label'])

    def test_create_toolbar(self):
        toolbar = self.u2x.create_toolbar()
        self.assertEqual(toolbar.get_orientation(), Gtk.Orientation.HORIZONTAL)
        self.assertTrue(toolbar.get_homogeneous())
        self.assertEqual(toolbar.get_spacing(), SPACING)
        self.assertEqual(toolbar.get_margin_start(), SPACING)
        self.assertEqual(toolbar.get_margin_end(), SPACING)
        self.assertIsInstance(toolbar, Gtk.Box)

    def test_create_window_container(self):
        container = self.u2x.create_window_container()
        self.assertIsInstance(container, Gtk.Box)
        self.assertEqual(container.get_orientation(), Gtk.Orientation.VERTICAL)
        self.assertFalse(container.get_homogeneous())
        self.assertEqual(container.get_spacing(), SPACING)

        self.assertIsInstance(container.get_first_child(), Gtk.ScrolledWindow)
        self.assertIsInstance(container.get_first_child().get_next_sibling(), Gtk.Box)
        self.assertIsInstance(container.get_last_child(), Gtk.ScrolledWindow)

    def test_create_window(self):
        self.u2x.create_window(None)
        self.assertIsInstance(self.u2x.window, Gtk.ApplicationWindow)
        self.assertEqual(self.u2x.window.get_title(), APP_TITLE)
        self.assertEqual(self.u2x.window.get_default_icon_name(), APP_ICON)
