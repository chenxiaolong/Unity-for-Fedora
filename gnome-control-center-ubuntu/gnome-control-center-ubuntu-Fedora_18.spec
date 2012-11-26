# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

# Partially based off of Fedora 18's spec file

%define _ubuntu_rel 0ubuntu8

Name:		control-center
Epoch:		1
Version:	3.6.3
Release:	100.%{_ubuntu_rel}%{?dist}
Summary:	Utilities to configure the GNOME desktop

License:	GPLv2+ and GFDL
URL:		http://www.gnome.org
Source0:	http://download.gnome.org/sources/gnome-control-center/3.6/gnome-control-center-%{version}.tar.xz

Source99:	https://launchpad.net/ubuntu/+archive/primary/+files/gnome-control-center_%{version}-%{_ubuntu_rel}.debian.tar.gz

# Fedora's patches
# https://bugzilla.gnome.org/show_bug.cgi?id=683567
Patch30:	fedora_0001-wacom-Add-show-help-window-to-the-list-of-actions.patch

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
BuildRequires:	pkgconfig(libgnome-menu-3.0)
BuildRequires:	pkgconfig(libgtop-2.0)
BuildRequires:	pkgconfig(libnm-glib)
BuildRequires:	pkgconfig(libnm-gtk)
BuildRequires:	pkgconfig(libnotify)
BuildRequires:	pkgconfig(libpulse) >= 2.0-1
BuildRequires:	pkgconfig(librsvg-2.0)
BuildRequires:	pkgconfig(libsystemd-daemon)
BuildRequires:	pkgconfig(libwacom)
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

Requires:	control-center-filesystem = %{epoch}:%{version}-%{release}

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

# System Information
Requires:	glx-utils

# Ubuntu's new sound panel (requires XDG_CURRENT_DESKTOP to be set)
Requires:	gnome-session-ubuntu

Provides:	control-center-ubuntu = %{epoch}:%{version}-%{release}

%description
This package contains configuration utilities for the GNOME desktop, which
allow to configure accessibility options, desktop fonts, keyboard and mouse
properties, sound setup, desktop theme and background, user interface
properties, screen resolution, and other settings.


%package devel
Summary:	Development files for the GNOME Control Center library

Requires:	%{name}%{?_isa} = %{epoch}:%{version}-%{release}

Provides:       control-center-ubuntu-devel = %{epoch}:%{version}-%{release}

%description devel
This package contains the development files for Ubuntu's patched version of the
GNOME Control Center library.


%package filesystem
Summary:	GNOME Control Center directories

Provides:	control-center-ubuntu-filesystem = %{epoch}:%{version}-%{release}

%description filesystem
The GNOME control-center provides a number of extension points for applications.
This package contains directories where applications can install configuration
files that are picked up by the control-center utilities.


%prep
%setup -q -n gnome-control-center-%{version}

# Apply Ubuntu's patches
tar zxvf '%{SOURCE99}'

# Disable patches
  # Ubuntu is too lazy to port their patches to the latest version of IBus
    sed -i '/revert_new_ibus_keyboard_use.patch/d' debian/patches/series
  # systemd should make this obsolete
    sed -i '/revert_git_datetime_port.patch/d' debian/patches/series
  # The gnome-settings-daemon-ubuntu patch for this conflicts with Fedora's
  # patches
    sed -i '/99_add_lock-on-suspend.patch/d' debian/patches/series
  # Fedora uses PackageKit
    sed -i '/05_run_update_manager.patch/d' debian/patches/series
  # Ubuntu specific
    sed -i '/10_keyboard_layout_on_unity.patch/d' debian/patches/series
    sed -i '/50_ubuntu_systemwide_proxy.patch/d' debian/patches/series
    sed -i '/52_ubuntu_language_list_mods.patch/d' debian/patches/series
    sed -i '/53_use_ubuntu_help.patch/d' debian/patches/series
    sed -i '/56_use_ubuntu_info_branding.patch/d' debian/patches/series
    sed -i '/62_update_translations_template.patch/d' debian/patches/series

tar zxvf '%{SOURCE99}'
for i in $(grep -v '#' debian/patches/series); do
  patch -p1 -i "debian/patches/${i}"
done

# Apply Fedora's patches
%patch30 -p1 -b .wacom-osd-window

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
%dir %{_datadir}/gnome-control-center/sounds/


%changelog
* Mon Oct 29 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.6.3-100.0ubuntu8
- Version 3.6.3
- Ubuntu release 0ubuntu8
- Merge Fedora's changes
  - 3.6.2-2: Require glx-utils for the info panel

* Sat Oct 20 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.6.1-100.ubuntu3.4.2.0ubuntu19
- Version 3.6.1
- Ubuntu version 3.4.2
- Ubuntu release 0ubuntu19
  - Nothing new for Fedora
- Merge Fedora's changes
  - git: Update to recent packaging guidelines
         This removes the now obsolete 'Group:' tag, and update the scriptlets.
         It also makes the filesystem subpackage own a previously unowned dir.
  - 3.6.0-2: Add Wacom OSD window from upstream bug #683567
- Match Fedora's epoch of 1

* Sat Oct 06 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.6.0-1.ubuntu3.4.2.0ubuntu18
- Ubuntu release 0ubuntu18
  - Refreshed 0001_04_new_appearance_settings.patch
  - Refreshed 0014_97_unity_power_ui.patch

* Fri Sep 28 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.6.0-1.ubuntu3.4.2.0ubuntu16
- Version 3.6.0
- Ubuntu version 3.4.2
- Ubuntu release 0ubuntu16

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
