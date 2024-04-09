#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import html
import sys

import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Gdk', '4.0')

from gi.repository import Gtk, Gdk
from xml.sax.saxutils import escape

APP_ID = 'site.sadegh.u2x'
APP_TITLE = 'u2x'
APP_ICON = 'org.gnome.Characters'
WINDOW_SIZE = (1024, 768)
SPACING = 8
SPACING_SM = 4
SHORTCUT_MODIFIERS = Gdk.ModifierType.ALT_MASK


class Encoder:
    @staticmethod
    def xml_to_unicode(text):
        return html.unescape(text)

    @staticmethod
    def unicode_to_xml(text):
        return (escape(text)
                .encode('ascii', 'xmlcharrefreplace')
                .decode('ascii'))


class U2X(Gtk.Application):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)

        self.xml_textview = None
        self.unicode_textview = None
        self.window = None
        self.clipboard = Gdk.Display.get_default().get_clipboard()
        self.tools = [
            {
                'label': 'To Unicode',
                'icon': 'go-up',
                'tooltip': 'Alt + u',
                'keyval': Gdk.KEY_u,
                'callback': self.convert_to_unicode,
            },
            {
                'label': 'To XML',
                'icon': 'go-down',
                'tooltip': 'Alt + x',
                'keyval': Gdk.KEY_x,
                'callback': self.convert_to_xml,
            }
        ]
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        container = self.create_window_container()

        self.create_window(app)
        self.add_window_shortcuts()
        self.window.set_child(container)
        self.window.present()

    def set_clipboard_content(self, text):
        self.clipboard.set(text)

    def convert_to_xml(self, widget=None, data=None):
        xml_text = Encoder.unicode_to_xml(self.get_unicode_text())
        self.set_xml_text(xml_text)

    def convert_to_unicode(self, widget=None, data=None):
        unicode_text = Encoder.xml_to_unicode(self.get_xml_text())
        self.set_unicode_text(unicode_text)

    def set_unicode_text(self, text):
        self.unicode_textview.get_buffer().set_text(text)
        self.set_clipboard_content(text)

    def get_unicode_text(self):
        return self.unicode_textview.get_buffer().props.text

    def set_xml_text(self, text):
        self.xml_textview.get_buffer().set_text(text)
        self.set_clipboard_content(text)

    def get_xml_text(self):
        return self.xml_textview.get_buffer().props.text

    def create_scrolled_window(self, textview):
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled_window.set_vexpand(True)
        scrolled_window.set_child(textview)

        return scrolled_window

    def create_unicode_textview(self):
        self.unicode_textview = Gtk.TextView()

        return self.create_scrolled_window(self.unicode_textview)

    def create_xml_textview(self):
        self.xml_textview = Gtk.TextView()

        return self.create_scrolled_window(self.xml_textview)

    def create_shortcut(self, keyval, callback):
        return Gtk.Shortcut(
            trigger=Gtk.KeyvalTrigger(keyval=keyval, modifiers=SHORTCUT_MODIFIERS),
            action=Gtk.CallbackAction().new(callback)
        )

    def create_tool(self, tool):
        button_content = Gtk.Box(halign=Gtk.Align.CENTER, spacing=SPACING_SM)
        button_content.append(Gtk.Image(icon_name=tool['icon']))
        button_content.append(Gtk.Label(label=tool['label']))

        button = Gtk.Button(child=button_content, tooltip_text=tool['tooltip'])
        button.connect('clicked', tool['callback'])

        return button

    def create_toolbar(self):
        toolbar = Gtk.Box(
            homogeneous=True,
            spacing=SPACING,
            margin_start=SPACING,
            margin_end=SPACING
        )

        for tool in self.tools:
            toolbar.append(self.create_tool(tool))

        return toolbar

    def create_window_container(self):
        container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        container.set_spacing(SPACING)
        container.append(self.create_unicode_textview())
        container.append(self.create_toolbar())
        container.append(self.create_xml_textview())

        return container

    def add_window_shortcuts(self):
        for tool in self.tools:
            self.window.add_shortcut(
                self.create_shortcut(tool['keyval'], tool['callback'])
            )

    def create_window(self, app):
        if self.window:
            return

        self.window = Gtk.ApplicationWindow(application=app)
        self.window.set_title(APP_TITLE)
        self.window.set_default_icon_name(APP_ICON)
        self.window.set_default_size(*WINDOW_SIZE)


if __name__ == "__main__":
    u2x = U2X(application_id=APP_ID)
    u2x.run(sys.argv)
