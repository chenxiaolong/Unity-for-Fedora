# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

# Partially based off of Fedora 18's spec file

%define _ubuntu_ver 3.4.2
%define _ubuntu_rel 0ubuntu15

Name:		control-center
Version:	3.5.92
Release:	1%{?dist}
Summary:	Utilities to configure the GNOME desktop

Group:		User Interface/Desktops
License:	GPLv2+ and GFDL
URL:		http://www.gnome.org
Source0:	http://download.gnome.org/sources/gnome-control-center/3.5/gnome-control-center-%{version}.tar.xz

Source99:	https://launchpad.net/ubuntu/+archive/primary/+files/gnome-control-center_%{_ubuntu_ver}-%{_ubuntu_rel}.debian.tar.gz

# Useful patches refreshed for version 3.5.92
Patch0:		0001_04_new_appearance_settings.patch
Patch1:		0002_10_keyboard_layout_on_unity.patch
Patch2:		0003_11_power-configure_lid_action.patch
Patch3:		0004_12_add_never_turn_screen_off.patch
Patch4:		0005_51_unity_options_in_display_panel.patch
Patch5:		0006_54_enable_alt_tap_in_shortcut.patch
Patch6:		0007_55_user_accounts_hide_controls.patch
Patch7:		0008_57_use_nonsymbolic_keyboard_icon.patch
Patch8:		0009_61_workaround_online_account.patch
Patch9:		0010_62_update_translations_template.patch
Patch10:	0011_64_restore_terminal_keyboard_shortcut.patch
Patch11:	0012_90_force_fallback.patch
Patch12:	0013_96_sound_nua_panel.patch
Patch13:	0014_97_unity_power_ui.patch
Patch14:	0015_98_default_sound_theme.patch
Patch15:	0016_revert_git_drop_library.patch
Patch16:	0017_99_add_lock-on-suspend.patch
Patch17:	0018_dont_download_local_image.patch
Patch18:	0019_fix-crash-on-user-panel.patch
Patch19:	0020_classic_use_sound_indicator.patch
Patch20:	0021_accounts_fix_unsetting_icon.patch

BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	desktop-file-utils
BuildRequires:	docbook-utils
BuildRequires:	gettext
BuildRequires:	gnome-common
BuildRequires:	gnome-doc-utils
BuildRequires:	intltool
BuildRequires:	pkgconfig

BuildRequires:	pkgconfig(cheese)
BuildRequires:	pkgconfig(clutter-gst-1.0)
BuildRequires:	pkgconfig(clutter-gtk-1.0)
BuildRequires:	pkgconfig(colord)
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(gdk-pixbuf-2.0)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gnome-bluetooth-1.0)
BuildRequires:	pkgconfig(gnome-desktop-3.0)
BuildRequires:	pkgconfig(gnome-settings-daemon)
BuildRequires:	pkgconfig(goa-1.0)
BuildRequires:	pkgconfig(gsettings-desktop-schemas)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(ibus-1.0)
BuildRequires:	pkgconfig(iso-codes)
BuildRequires:	pkgconfig(libcanberra)
BuildRequires:	pkgconfig(libglade-2.0)
BuildRequires:	pkgconfig(libgnomekbd)
BuildRequires:	pkgconfig(libgnome-menu-3.0)
BuildRequires:	pkgconfig(libgtop-2.0)
BuildRequires:	pkgconfig(libnm-glib)
BuildRequires:	pkgconfig(libnm-gtk)
BuildRequires:	pkgconfig(libnotify)
BuildRequires:	pkgconfig(libpulse) >= 2.0-1
BuildRequires:	pkgconfig(librsvg-2.0)
BuildRequires:	pkgconfig(libsystemd-daemon)
BuildRequires:	pkgconfig(libwacom)
BuildRequires:	pkgconfig(libxklavier)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(polkit-agent-1)
BuildRequires:	pkgconfig(pwquality)
BuildRequires:	pkgconfig(upower-glib)
BuildRequires:	pkgconfig(xcursor)
BuildRequires:	pkgconfig(xkbfile)
BuildRequires:	pkgconfig(xrandr)
BuildRequires:	pkgconfig(xscrnsaver)
BuildRequires:	pkgconfig(xxf86misc)

BuildRequires:	cups-devel

# Requires Ubuntu's patched gnome-settings-daemon
Requires:	gnome-settings-daemon-ubuntu

Requires:	control-center-filesystem = %{version}-%{release}

Requires:	alsa-lib
Requires:	dbus-x11
Requires:	gnome-desktop3
Requires:	gnome-icon-theme
Requires:	gnome-menus
Requires:	redhat-menus

# Display settings
Requires:	libXrandr

# User account settings
Requires:	accountsservice

# Languages
Requires:	iso-codes

# Sound applet and settings
Requires:	gnome-icon-theme-symbolic

# Printers
Requires:	cups-pk-helper

# Network settings
Requires:	nm-connection-editor

# Ubuntu's new sound panel (requires XDG_CURRENT_DESKTOP to be set)
Requires:	gnome-session-ubuntu

Provides:	control-center-ubuntu = %{version}-%{release}

%description
This package contains configuration utilities for the GNOME desktop, which
allow to configure accessibility options, desktop fonts, keyboard and mouse
properties, sound setup, desktop theme and background, user interface
properties, screen resolution, and other settings.


%package devel
Summary:	Development files for the GNOME Control Center library
Group:		Development/Libraries

Requires:	%{name}%{?_isa} = %{version}-%{release}

Provides:       control-center-ubuntu-devel = %{version}-%{release}

%description devel
This package contains the development files for Ubuntu's patched version of the
GNOME Control Center library.


%package filesystem
Summary:	GNOME Control Center directories
Group:		Development/Libraries

Provides:	control-center-ubuntu-filesystem = %{version}-%{release}

%description filesystem
The GNOME control-center provides a number of extension points for applications.
This package contains directories where applications can install configuration
files that are picked up by the control-center utilities.


%prep
%setup -q -n gnome-control-center-%{version}

# Apply Ubuntu's patches
tar zxvf '%{SOURCE99}'

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1

autoreconf -vfi


%build
%configure \
  --disable-static \
  --disable-update-mimedb \
  --with-libsocialweb=no \
  --enable-systemd \
  --with-clutter

# Disable rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

# From Fedora 18 spec: only link against necessary libraries
sed -i -e 's/ -shared / -Wl,-O1,--as-needed\0 /g' -e 's/    if test "$export_dynamic" = yes && test -n "$export_dynamic_flag_spec"; then/      func_append compile_command " -Wl,-O1,--as-needed"\n      func_append finalize_command " -Wl,-O1,--as-needed"\n\0/' libtool

make %{?_smp_mflags}


%install
GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 make install DESTDIR=$RPM_BUILD_ROOT

desktop-file-install --delete-original \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications/ \
  $RPM_BUILD_ROOT%{_datadir}/applications/*.desktop

# Create directory from GNOME window manager desktop files
install -dm755 $RPM_BUILD_ROOT%{_datadir}/gnome/wm-properties/

# Remove unwanted directories (not packaged in Fedora)
rm -rvf $RPM_BUILD_ROOT%{_datadir}/gnome/autostart/
rm -rvf $RPM_BUILD_ROOT%{_datadir}/gnome/cursor-fonts/

# Link gnome-control-center desktop file for indicators
install -dm755 $RPM_BUILD_ROOT%{_datadir}/indicators/session/applications/
ln -s %{_datadir}/applications/gnome-control-center.desktop \
  $RPM_BUILD_ROOT%{_datadir}/indicators/session/applications/

# Remove libtool files
find $RPM_BUILD_ROOT -type f -name '*.la' -delete

%find_lang gnome-control-center-2.0
%find_lang gnome-control-center-2.0-timezones


%post
/sbin/ldconfig
update-desktop-database &>/dev/null || :
update-mime-database %{_datadir}/mime/ &>/dev/null || :
touch --no-create %{_datadir}/icons/hicolor/ &>/dev/null || :

%postun
/sbin/ldconfig
update-desktop-database &>/dev/null || :
update-mime-database %{_datadir}/mime/ &>/dev/null || :
if [ ${1} -eq 0 ]; then
  touch --no-create %{_datadir}/icons/hicolor/ &>/dev/null || :
  gtk-update-icon-cache -f %{_datadir}/icons/hicolor/ &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache -f %{_datadir}/icons/hicolor/ &>/dev/null || :


%files -f gnome-control-center-2.0.lang -f gnome-control-center-2.0-timezones.lang
%doc AUTHORS ChangeLog NEWS README TODO
%{_bindir}/gnome-control-center
%{_bindir}/gnome-sound-applet

# XDG files
%{_sysconfdir}/xdg/autostart/gnome-sound-applet.desktop
%{_sysconfdir}/xdg/menus/gnomecc.menu

# GNOME Control Center panels
%dir %{_libdir}/control-center-1/
%dir %{_libdir}/control-center-1/panels/
%{_libdir}/control-center-1/panels/libbackground.so
%{_libdir}/control-center-1/panels/libbluetooth.so
%{_libdir}/control-center-1/panels/libcolor.so
%{_libdir}/control-center-1/panels/libdate_time.so
%{_libdir}/control-center-1/panels/libdisplay.so
%{_libdir}/control-center-1/panels/libinfo.so
%{_libdir}/control-center-1/panels/libkeyboard.so
%{_libdir}/control-center-1/panels/libmouse-properties.so
%{_libdir}/control-center-1/panels/libnetwork.so
%{_libdir}/control-center-1/panels/libonline-accounts.so
%{_libdir}/control-center-1/panels/libpower.so
%{_libdir}/control-center-1/panels/libprinters.so
%{_libdir}/control-center-1/panels/libregion.so
%{_libdir}/control-center-1/panels/libscreen.so
%{_libdir}/control-center-1/panels/libsound.so
%{_libdir}/control-center-1/panels/libsoundnua.so
%{_libdir}/control-center-1/panels/libuniversal-access.so
%{_libdir}/control-center-1/panels/libuser-accounts.so
%{_libdir}/control-center-1/panels/libwacom-properties.so

# GNOME Control Center libraries
%{_libdir}/libgnome-control-center.so.1
%{_libdir}/libgnome-control-center.so.1.0.0

# PolicyKit policies
%{_datadir}/polkit-1/actions/org.gnome.controlcenter.datetime.policy
%{_datadir}/polkit-1/actions/org.gnome.controlcenter.user-accounts.policy
%{_datadir}/polkit-1/rules.d/gnome-control-center.rules

# Desktop files
%dir %{_datadir}/indicators/
%dir %{_datadir}/indicators/session/
%dir %{_datadir}/indicators/session/applications/
%{_datadir}/indicators/session/applications/gnome-control-center.desktop
%{_datadir}/applications/bluetooth-properties.desktop
%{_datadir}/applications/gnome-background-panel.desktop
%{_datadir}/applications/gnome-color-panel.desktop
%{_datadir}/applications/gnome-control-center.desktop
%{_datadir}/applications/gnome-datetime-panel.desktop
%{_datadir}/applications/gnome-display-panel.desktop
%{_datadir}/applications/gnome-info-panel.desktop
%{_datadir}/applications/gnome-keyboard-panel.desktop
%{_datadir}/applications/gnome-mouse-panel.desktop
%{_datadir}/applications/gnome-network-panel.desktop
%{_datadir}/applications/gnome-online-accounts-panel.desktop
%{_datadir}/applications/gnome-power-panel.desktop
%{_datadir}/applications/gnome-printers-panel.desktop
%{_datadir}/applications/gnome-region-panel.desktop
%{_datadir}/applications/gnome-screen-panel.desktop
%{_datadir}/applications/gnome-sound-nua-panel.desktop
%{_datadir}/applications/gnome-sound-panel.desktop
%{_datadir}/applications/gnome-universal-access-panel.desktop
%{_datadir}/applications/gnome-user-accounts-panel.desktop
%{_datadir}/applications/gnome-wacom-panel.desktop

# XDG Desktop Directory files
%{_datadir}/desktop-directories/gnomecc.directory

# GNOME Control Center icons
%{_datadir}/gnome-control-center/icons/

# Regular icons
%{_datadir}/icons/hicolor/16x16/apps/*.png
%{_datadir}/icons/hicolor/16x16/apps/multimedia-volume-control.svg
%{_datadir}/icons/hicolor/22x22/apps/*.png
%{_datadir}/icons/hicolor/22x22/apps/multimedia-volume-control.svg
%{_datadir}/icons/hicolor/24x24/apps/*.png
%{_datadir}/icons/hicolor/32x32/apps/*.png
%{_datadir}/icons/hicolor/32x32/apps/multimedia-volume-control.svg
%{_datadir}/icons/hicolor/48x48/apps/*.png
%{_datadir}/icons/hicolor/48x48/devices/audio-headset.svg
%{_datadir}/icons/hicolor/64x64/apps/*.png
%{_datadir}/icons/hicolor/256x256/apps/*.png
%{_datadir}/icons/hicolor/scalable/apps/*.svg
%{_datadir}/icons/hicolor/scalable/categories/*.svg
%{_datadir}/icons/hicolor/scalable/emblems/*.svg
%{_datadir}/icons/hicolor/scalable/status/*.svg
%dir %{_datadir}/pixmaps/faces/
%{_datadir}/pixmaps/faces/*.jpg
%{_datadir}/pixmaps/faces/*.png

# GNOME Control Center keybindings
%{_datadir}/gnome-control-center/keybindings/00-multimedia.xml
%{_datadir}/gnome-control-center/keybindings/01-input-sources.xml
%{_datadir}/gnome-control-center/keybindings/01-launchers.xml
%{_datadir}/gnome-control-center/keybindings/01-screenshot.xml
%{_datadir}/gnome-control-center/keybindings/01-system.xml
%{_datadir}/gnome-control-center/keybindings/50-accessibility.xml

# GNOME Control Center UI icons
%dir %{_datadir}/gnome-control-center/pixmaps/
%{_datadir}/gnome-control-center/pixmaps/*.png
%{_datadir}/gnome-control-center/pixmaps/*.svg

# GNOME Control Center user interface files
%dir %{_datadir}/gnome-control-center/ui/
%{_datadir}/gnome-control-center/bluetooth.ui
%{_datadir}/gnome-control-center/ui/datetime/datetime.ui
%dir %{_datadir}/gnome-control-center/ui/background/
%{_datadir}/gnome-control-center/ui/background/background.ui
%{_datadir}/gnome-control-center/ui/button-mapping.ui
%{_datadir}/gnome-control-center/ui/color.ui
%{_datadir}/gnome-control-center/ui/display-capplet.ui
%{_datadir}/gnome-control-center/ui/gnome-keyboard-panel.ui
%{_datadir}/gnome-control-center/ui/gnome-mouse-properties.ui
%{_datadir}/gnome-control-center/ui/gnome-mouse-test.ui
%{_datadir}/gnome-control-center/ui/gnome-region-panel.ui
%{_datadir}/gnome-control-center/ui/gnome-region-panel-input-chooser.ui
%{_datadir}/gnome-control-center/ui/gnome-wacom-properties.ui
%{_datadir}/gnome-control-center/ui/info.ui
%{_datadir}/gnome-control-center/ui/language-chooser.ui
%{_datadir}/gnome-control-center/ui/network.ui
%{_datadir}/gnome-control-center/ui/network-mobile.ui
%{_datadir}/gnome-control-center/ui/network-proxy.ui
%{_datadir}/gnome-control-center/ui/network-vpn.ui
%{_datadir}/gnome-control-center/ui/network-wifi.ui
%{_datadir}/gnome-control-center/ui/network-wired.ui
%{_datadir}/gnome-control-center/ui/online-accounts.ui
%{_datadir}/gnome-control-center/ui/power.ui
%dir %{_datadir}/gnome-control-center/ui/printers/
%{_datadir}/gnome-control-center/ui/printers/jobs-dialog.ui
%{_datadir}/gnome-control-center/ui/printers/new-printer-dialog.ui
%{_datadir}/gnome-control-center/ui/printers/options-dialog.ui
%{_datadir}/gnome-control-center/ui/printers/ppd-selection-dialog.ui
%{_datadir}/gnome-control-center/ui/printers/printers.ui
%{_datadir}/gnome-control-center/ui/screen.ui
%{_datadir}/gnome-control-center/ui/shell.ui
%{_datadir}/gnome-control-center/ui/uap.ui
%dir %{_datadir}/gnome-control-center/ui/user-accounts/
%{_datadir}/gnome-control-center/ui/user-accounts/account-dialog.ui
%{_datadir}/gnome-control-center/ui/user-accounts/account-fingerprint.ui
%{_datadir}/gnome-control-center/ui/user-accounts/password-dialog.ui
%{_datadir}/gnome-control-center/ui/user-accounts/photo-dialog.ui
%{_datadir}/gnome-control-center/ui/user-accounts/user-accounts-dialog.ui
%{_datadir}/gnome-control-center/ui/wacom-stylus-page.ui
%{_datadir}/gnome-control-center/ui/zoom-options.ui

# GNOME Control Center world map images and other datetime files
%dir %{_datadir}/gnome-control-center/ui/datetime/
%{_datadir}/gnome-control-center/ui/datetime/timezone_*.png
%{_datadir}/gnome-control-center/ui/datetime/bg.png
%{_datadir}/gnome-control-center/ui/datetime/bg_dim.png
%{_datadir}/gnome-control-center/ui/datetime/cc.png
%{_datadir}/gnome-control-center/ui/datetime/pin.png

# GNOME Control Center wacom settings panel images
%{_datadir}/gnome-control-center/ui/wacom-*.svg

# GNOME Control Center sounds
%dir %{_datadir}/gnome-control-center/sounds/
%{_datadir}/gnome-control-center/sounds/gnome-sounds-default.xml
%{_datadir}/sounds/gnome/default/alerts/bark.ogg
%{_datadir}/sounds/gnome/default/alerts/drip.ogg
%{_datadir}/sounds/gnome/default/alerts/glass.ogg
%{_datadir}/sounds/gnome/default/alerts/sonar.ogg

# Other GNOME Control Center data files
%{_datadir}/gnome-control-center/datetime/backward
%{_datadir}/gnome-control-center/ui/GnomeLogoVerticalMedium.svg
%{_datadir}/gnome-control-center/ui/scroll-test.svg
%{_datadir}/gnome-control-center/ui/scroll-test-gegl.svg

# GNOME Keybindings pkgconfig file
%{_datadir}/pkgconfig/gnome-keybindings.pc

# Manual pages
%{_mandir}/man1/gnome-control-center.1.gz


%files devel
%dir %{_includedir}/gnome-control-center-1/
%dir %{_includedir}/gnome-control-center-1/libgnome-control-center/
%{_includedir}/gnome-control-center-1/libgnome-control-center/cc-editable-entry.h
%{_includedir}/gnome-control-center-1/libgnome-control-center/cc-panel.h
%{_includedir}/gnome-control-center-1/libgnome-control-center/cc-shell.h
%{_libdir}/libgnome-control-center.so
%{_libdir}/pkgconfig/libgnome-control-center.pc


%files filesystem
%dir %{_datadir}/gnome/wm-properties/
%dir %{_datadir}/gnome-control-center/
%dir %{_datadir}/gnome-control-center/keybindings/


%changelog
* Fri Sep 21 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.5.92-1
- Version 3.5.92

* Thu Sep 20 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.4.2-3.0ubuntu15
- Initial release for Fedora 18
- Version 3.4.2
- Ubuntu release 0ubuntu15

* Sat Sep 08 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.4.2-3.0ubuntu14
- Version 3.4.2
- Ubuntu release 0ubuntu14

* Thu Aug 30 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.4.2-3.0ubuntu13
- Fix duplicate settings panels

* Thu Aug 30 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.4.2-2.0ubuntu13
- Version 3.4.2
- Ubuntu release 0ubuntu13

* Mon Aug 13 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.4.2-2.0ubuntu0.4
- Version 3.4.2
- Ubuntu release 0ubuntu0.4

* Mon Jul 16 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.4.2-2.0ubuntu0.3
- Do not revert the port to systemd's timedated
- Fedora does not have ubuntu-system-service

* Sun Jul 15 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.4.2-1.0ubuntu0.3
- Initial release
- Based off of Fedora 17's spec file
- Version 3.4.2
- Ubuntu release 0ubuntu0.3
