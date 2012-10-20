# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

# Partially based off of the Fedora 17 spec

%define _ubuntu_ver 3.4.2
%define _ubuntu_rel 0ubuntu14

Name:		gnome-settings-daemon
Version:	3.6.1
Release:	100.ubuntu%{_ubuntu_ver}.%{_ubuntu_rel}%{?dist}
Summary:	The daemon sharing settings from GNOME to GTK+/KDE applications

Group:		System Environment/Daemons
License:	GPLv2+
URL:		http://download.gnome.org/sources/gnome-settings-daemon
Source0:	http://download.gnome.org/sources/gnome-settings-daemon/3.6/gnome-settings-daemon-%{version}.tar.xz

Source99:	https://launchpad.net/ubuntu/+archive/primary/+files/gnome-settings-daemon_%{_ubuntu_ver}-%{_ubuntu_rel}.debian.tar.gz

# Refreshed useful patches from Ubuntu's gnome-settings-daemon packaging
# (version 3.4.2-0ubuntu13). We will not see updates to the patches until
# Ubuntu 13.04.
Patch0:		0001_16_use_synchronous_notifications.patch
Patch1:		0002_51_lock_screen_on_suspend.patch
Patch2:		0003_52_sync_background_to_accountsservice.patch
Patch3:		0004_60_unity_hide_status_icon.patch
Patch4:		0005_62_unity_disable_gsd_printer.patch
Patch5:		0006_63_unity_start_mounter.patch
Patch6:		0007_90_set_gmenus_xsettings.patch
Patch7:		0008_disable_three_touch_tap.patch
Patch8:		0009_revert_git_datetime_dropping.patch
Patch9:		0010_correct_logout_action.patch
Patch10:	0011_power-no-fallback-notifications.patch
Patch11:	0012_power-check-null-devices.patch
Patch12:	0013_64_restore_terminal_keyboard_shortcut_schema.patch

# Fedora's patches
# https://bugzilla.gnome.org/show_bug.cgi?id=680689
Patch21:	fedora_0001-power-and-media-keys-Use-logind-for-suspending-and-r.patch
# Wacom OSD window: https://bugzilla.gnome.org/show_bug.cgi?id=679062
Patch22:	fedora_0001-wacom-implement-OSD-help-window.patch

BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext
BuildRequires:	intltool
BuildRequires:	libtool
BuildRequires:	libxslt
BuildRequires:	pkgconfig

BuildRequires:	pkgconfig(colord)
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(fontconfig)
BuildRequires:	pkgconfig(gnome-desktop-3.0)
BuildRequires:	pkgconfig(gsettings-desktop-schemas)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(gudev-1.0)
BuildRequires:	pkgconfig(ibus-1.0)
BuildRequires:	pkgconfig(kbproto)
BuildRequires:	pkgconfig(lcms2)
BuildRequires:	pkgconfig(libcanberra-gtk3)
BuildRequires:	pkgconfig(libgnomekbd)
BuildRequires:	pkgconfig(libgnomekbdui)
BuildRequires:	pkgconfig(libnotify)
BuildRequires:	pkgconfig(libpulse)
BuildRequires:	pkgconfig(libsystemd-login)
BuildRequires:	pkgconfig(libwacom)
BuildRequires:	pkgconfig(libxklavier)
BuildRequires:	pkgconfig(nss)
BuildRequires:	pkgconfig(packagekit-glib2)
BuildRequires:	pkgconfig(polkit-gobject-1)
BuildRequires:	pkgconfig(upower-glib)
BuildRequires:	pkgconfig(xfixes)
BuildRequires:	pkgconfig(xi)
BuildRequires:	pkgconfig(xkbfile)
BuildRequires:	pkgconfig(xorg-wacom)
BuildRequires:	pkgconfig(xtst)

BuildRequires:	cups-devel

Requires:	control-center-filesystem

Provides:	gnome-settings-daemon-ubuntu = %{version}-%{release}

%description
This package contains a daemon to share settings from GNOME to other
applications. It also handles global keybindings, as well as a number of
desktop-wide settings.


%package devel
Summary:	Development files for gnome-settings-daemon-ubuntu
Group:		Development/Libraries

Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	pkgconfig(dbus-glib-1)

Provides:	gnome-settings-daemon-ubuntu-devel = %{version}-%{release}

%description devel
This package contains the development files Ubuntu's patched version of
gnome-settings-daemon.


%package updates
Summary:	Updates plugin for gnome-control-center
Group:		Development/Libraries

Requires:	%{name}%{?_isa} = %{version}-%{release}

%description updates
This package contains the PackageKit updates plugin for GNOME Control Center.


%prep
%setup -q -n gnome-settings-daemon-%{version}

# Apply Ubuntu's patches
tar zxvf '%{SOURCE99}'
%patch0 -p1
#patch1 -p1
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

# Apply Fedora's patches
%patch21 -p1
%patch22 -p1 -b .wacom-osd-window

autoreconf -vfi


%build
%configure \
  --disable-static \
  --enable-profiling \
  --enable-packagekit \
  --enable-systemd \
  --enable-polkit

make %{?_smp_mflags}

gcc -o gnome-settings-daemon/gnome-update-wallpaper-cache \
       debian/gnome-update-wallpaper-cache.c \
       $(pkg-config --cflags --libs \
         glib-2.0 \
         gdk-3.0 \
         gdk-x11-3.0 \
         gio-2.0 \
         gnome-desktop-3.0)


%install
make install DESTDIR=$RPM_BUILD_ROOT

install -dm755 $RPM_BUILD_ROOT%{_libexecdir}/
install -m755 gnome-settings-daemon/gnome-update-wallpaper-cache \
              $RPM_BUILD_ROOT%{_libexecdir}/

# Ubuntu's manual page contains GConf command line option information that was
# added by Ubuntu.
install -m644 debian/gnome-settings-daemon.1 $RPM_BUILD_ROOT%{_mandir}/man1/

# Remove libtool files
find $RPM_BUILD_ROOT -type f -name '*.la' -delete

%find_lang gnome-settings-daemon


%post
touch --no-create %{_datadir}/icons/hicolor/ &>/dev/null || :

%postun
if [ ${1} -eq 0 ]; then
  touch --no-create %{_datadir}/icons/hicolor/ &>/dev/null || :
  gtk-update-icon-cache -f %{_datadir}/icons/hicolor &>/dev/null || :
  glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache -f %{_datadir}/icons/hicolor &>/dev/null || :
glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :


%postun updates
if [ ${1} -eq 0 ]; then
  glib-compile-schemas %{_datadir}/glib-2.0/schemas/ &> /dev/null || :
fi

%posttrans updates
glib-compile-schemas %{_datadir}/glib-2.0/schemas/ &> /dev/null || :


%files -f gnome-settings-daemon.lang
%doc AUTHORS NEWS

%dir %{_sysconfdir}/gnome-settings-daemon/
%dir %{_sysconfdir}/gnome-settings-daemon/xrandr/

%{_libexecdir}/gnome-fallback-mount-helper
%{_libexecdir}/gnome-settings-daemon
%{_libexecdir}/gnome-update-wallpaper-cache
%{_libexecdir}/gsd-backlight-helper
%{_libexecdir}/gsd-datetime-mechanism
%{_libexecdir}/gsd-input-sources-switcher
%{_libexecdir}/gsd-locate-pointer
%{_libexecdir}/gsd-printer
%{_libexecdir}/gsd-test-wacom-osd
%{_libexecdir}/gsd-wacom-led-helper

# Plugins
%dir %{_libdir}/gnome-settings-daemon-3.0/
%{_libdir}/gnome-settings-daemon-3.0/a11y-keyboard.gnome-settings-plugin
%{_libdir}/gnome-settings-daemon-3.0/a11y-settings.gnome-settings-plugin
%{_libdir}/gnome-settings-daemon-3.0/background.gnome-settings-plugin
%{_libdir}/gnome-settings-daemon-3.0/clipboard.gnome-settings-plugin
%{_libdir}/gnome-settings-daemon-3.0/color.gnome-settings-plugin
%{_libdir}/gnome-settings-daemon-3.0/cursor.gnome-settings-plugin
%{_libdir}/gnome-settings-daemon-3.0/housekeeping.gnome-settings-plugin
%{_libdir}/gnome-settings-daemon-3.0/keyboard.gnome-settings-plugin
%{_libdir}/gnome-settings-daemon-3.0/media-keys.gnome-settings-plugin
%{_libdir}/gnome-settings-daemon-3.0/mouse.gnome-settings-plugin
%{_libdir}/gnome-settings-daemon-3.0/orientation.gnome-settings-plugin
%{_libdir}/gnome-settings-daemon-3.0/power.gnome-settings-plugin
%{_libdir}/gnome-settings-daemon-3.0/print-notifications.gnome-settings-plugin
%{_libdir}/gnome-settings-daemon-3.0/smartcard.gnome-settings-plugin
%{_libdir}/gnome-settings-daemon-3.0/sound.gnome-settings-plugin
%{_libdir}/gnome-settings-daemon-3.0/wacom.gnome-settings-plugin
%{_libdir}/gnome-settings-daemon-3.0/xrandr.gnome-settings-plugin
%{_libdir}/gnome-settings-daemon-3.0/xsettings.gnome-settings-plugin
%{_libdir}/gnome-settings-daemon-3.0/liba11y-keyboard.so
%{_libdir}/gnome-settings-daemon-3.0/liba11y-settings.so
%{_libdir}/gnome-settings-daemon-3.0/libbackground.so
%{_libdir}/gnome-settings-daemon-3.0/libclipboard.so
%{_libdir}/gnome-settings-daemon-3.0/libcolor.so
%{_libdir}/gnome-settings-daemon-3.0/libcursor.so
%{_libdir}/gnome-settings-daemon-3.0/libgsd.so
%{_libdir}/gnome-settings-daemon-3.0/libgsdwacom.so
%{_libdir}/gnome-settings-daemon-3.0/libhousekeeping.so
%{_libdir}/gnome-settings-daemon-3.0/libkeyboard.so
%{_libdir}/gnome-settings-daemon-3.0/libmedia-keys.so
%{_libdir}/gnome-settings-daemon-3.0/libmouse.so
%{_libdir}/gnome-settings-daemon-3.0/liborientation.so
%{_libdir}/gnome-settings-daemon-3.0/libpower.so
%{_libdir}/gnome-settings-daemon-3.0/libprint-notifications.so
%{_libdir}/gnome-settings-daemon-3.0/libsmartcard.so
%{_libdir}/gnome-settings-daemon-3.0/libsound.so
%{_libdir}/gnome-settings-daemon-3.0/libxrandr.so
%{_libdir}/gnome-settings-daemon-3.0/libxsettings.so

# GSettings schemas
%{_datadir}/glib-2.0/schemas/org.gnome.settings-daemon.enums.xml
%{_datadir}/glib-2.0/schemas/org.gnome.settings-daemon.peripherals.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.settings-daemon.peripherals.wacom.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.settings-daemon.plugins.color.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.settings-daemon.plugins.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.settings-daemon.plugins.housekeeping.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.settings-daemon.plugins.keyboard.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.settings-daemon.plugins.media-keys.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.settings-daemon.plugins.orientation.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.settings-daemon.plugins.power.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.settings-daemon.plugins.print-notifications.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.settings-daemon.plugins.xrandr.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.settings-daemon.plugins.xsettings.gschema.xml

# Data files
%dir %{_datadir}/gnome-settings-daemon/
%{_datadir}/gnome-settings-daemon/gsd-a11y-preferences-dialog.ui
%{_datadir}/gnome-settings-daemon/icons/

# DBus services
%{_datadir}/dbus-1/services/org.freedesktop.IBus.service
%{_datadir}/dbus-1/system-services/org.gnome.SettingsDaemon.DateTimeMechanism.service
%{_sysconfdir}/dbus-1/system.d/org.gnome.SettingsDaemon.DateTimeMechanism.conf

# Desktop files
%{_sysconfdir}/xdg/autostart/gnome-fallback-mount-helper.desktop
%{_sysconfdir}/xdg/autostart/gnome-settings-daemon.desktop

# GConf files
%{_datadir}/GConf/gsettings/gnome-settings-daemon.convert

# Icons
%{_datadir}/icons/hicolor/16x16/apps/gsd-xrandr.png
%{_datadir}/icons/hicolor/22x22/apps/gsd-xrandr.png
%{_datadir}/icons/hicolor/24x24/apps/gsd-xrandr.png
%{_datadir}/icons/hicolor/32x32/apps/gsd-xrandr.png
%{_datadir}/icons/hicolor/scalable/apps/gsd-xrandr.svg

# PolicyKit policies
%{_datadir}/polkit-1/actions/org.gnome.settings-daemon.plugins.power.policy
%{_datadir}/polkit-1/actions/org.gnome.settings-daemon.plugins.wacom.policy
%{_datadir}/polkit-1/actions/org.gnome.settingsdaemon.datetimemechanism.policy

# Manual pages
%{_mandir}/man1/gnome-settings-daemon.1.gz


%files devel
%doc AUTHORS NEWS
%dir %{_includedir}/gnome-settings-daemon-3.0/
%dir %{_includedir}/gnome-settings-daemon-3.0/gnome-settings-daemon/
%{_includedir}/gnome-settings-daemon-3.0/gnome-settings-daemon/gnome-settings-plugin.h
%{_includedir}/gnome-settings-daemon-3.0/gnome-settings-daemon/gsd-enums.h
%{_libdir}/pkgconfig/gnome-settings-daemon.pc
%dir %{_datadir}/gnome-settings-daemon-3.0/
%{_datadir}/gnome-settings-daemon-3.0/input-device-example.sh

# Tests
%{_libexecdir}/gsd-test-a11y-keyboard
%{_libexecdir}/gsd-test-a11y-settings
%{_libexecdir}/gsd-test-background
%{_libexecdir}/gsd-test-input-helper
%{_libexecdir}/gsd-test-keyboard
%{_libexecdir}/gsd-test-media-keys
%{_libexecdir}/gsd-test-mouse
%{_libexecdir}/gsd-test-orientation
%{_libexecdir}/gsd-test-power
%{_libexecdir}/gsd-test-print-notifications
%{_libexecdir}/gsd-test-smartcard
%{_libexecdir}/gsd-test-sound
%{_libexecdir}/gsd-test-xsettings
%{_libexecdir}/gsd-list-wacom
%{_libexecdir}/gsd-test-wacom


%files updates
%dir %{_libdir}/gnome-settings-daemon-3.0/
%{_libdir}/gnome-settings-daemon-3.0/updates.gnome-settings-plugin
%{_libdir}/gnome-settings-daemon-3.0/libupdates.so
%{_datadir}/dbus-1/interfaces/org.gnome.SettingsDaemonUpdates.xml
%{_datadir}/glib-2.0/schemas/org.gnome.settings-daemon.plugins.updates.gschema.xml


%changelog
* Sat Oct 20 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.6.1-100.ubuntu3.4.2.0ubuntu14
- Version 3.6.1
- Merge Fedora's changes
  - 3.6.1-3: Fix a typo in the suspend patch (#858259)
- fedora_0001-Clean-up-gsd_power_stop.patch
  - Dropped: merged upstream
- Add libxslt to build dependencies

* Mon Oct 08 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.6.0-3.ubuntu3.4.2.0ubuntu14
- Merge Fedora's changes
  - 3.6.0-2: Split out PackageKit into a sub package. Fixes #699348
  - 3.6.0-3: Fix lid close handling with new systemd
  - 3.6.0-4: Fix an inhibitor leak in the previous patch
  - 3.6.0-5: Adds Wacom OSD window from upstream bug #679062

* Mon Oct 01 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.6.0-2.ubuntu3.4.2.0ubuntu14
- Add 0013_64_restore_terminal_keyboard_shortcut_schema.patch

* Mon Oct 01 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.6.0-1.ubuntu3.4.2.0ubuntu14
- Ubuntu release 0ubuntu14

* Fri Sep 28 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.6.0-1.ubuntu3.4.2.0ubuntu13
- Version 3.6.0

* Thu Sep 20 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.5.92-1
- Initial release for Fedora 18
- Refreshed useful Ubuntu patches for version 3.5.92
  - Ubuntu will stay with the 3.4 series

* Fri Sep 14 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.4.2-1.0ubuntu13
- Version 3.4.2
- Ubuntu release 0ubuntu13

* Sun Aug 26 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.4.2-1.0ubuntu10
- Version 3.4.2
- Ubuntu release 0ubuntu10

* Fri Aug 24 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.4.2-2.0ubuntu0.4
- Fix directory ownership
- Use pkgconfig for dependencies

* Sat Jul 14 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.4.2-1.0ubuntu0.4
- Initial release
- Based on Fedora 17's spec file
- Version 3.4.2
- Ubuntu release 0ubuntu0.4
