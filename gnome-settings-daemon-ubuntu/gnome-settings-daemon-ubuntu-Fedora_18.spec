# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

# Partially based off of the Fedora 17 spec

%define _ubuntu_rel 0ubuntu13

Name:		gnome-settings-daemon
Version:	3.4.2
Release:	2.%{_ubuntu_rel}%{?dist}
Summary:	The daemon sharing settings from GNOME to GTK+/KDE applications

Group:		System Environment/Daemons
License:	GPLv2+
URL:		http://download.gnome.org/sources/gnome-settings-daemon
Source0:	http://download.gnome.org/sources/gnome-settings-daemon/3.4/gnome-settings-daemon-%{version}.tar.xz

Source99:	https://launchpad.net/ubuntu/+archive/primary/+files/gnome-settings-daemon_%{version}-%{_ubuntu_rel}.debian.tar.gz

# Fedora specific patch: do not install security updates automatically as the
# user can restart the system during the upgrades and mess up the rpm database.
#
# The features in the new version of systemd in Fedora 18 will make this patch
# obsolete.
Patch0:		gsd-auto-update-type-is-none.patch

BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext
BuildRequires:	intltool
BuildRequires:	libtool
BuildRequires:	pkgconfig

BuildRequires:	pkgconfig(colord)
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(fontconfig)
BuildRequires:	pkgconfig(gnome-desktop-3.0)
BuildRequires:	pkgconfig(gsettings-desktop-schemas)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(gudev-1.0)
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


%prep
%setup -q -n gnome-settings-daemon-%{version}

%patch0 -p1 -b .update-none

# Apply Ubuntu's patches
tar zxvf '%{SOURCE99}'

# Fix patches
  # Fedora 17 moved /bin to /usr/bin
    sed -i 's,/bin/,/usr/bin/,g' \
      debian/patches/revert_git_datetime_dropping.patch

for i in $(grep -v '#' debian/patches/series); do
  patch -Np1 -i "debian/patches/${i}"
done

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


%files -f gnome-settings-daemon.lang
%doc AUTHORS NEWS

%dir %{_sysconfdir}/gnome-settings-daemon/
%dir %{_sysconfdir}/gnome-settings-daemon/xrandr/

%{_libexecdir}/gnome-fallback-mount-helper
%{_libexecdir}/gnome-settings-daemon
%{_libexecdir}/gnome-update-wallpaper-cache
%{_libexecdir}/gsd-backlight-helper
%{_libexecdir}/gsd-datetime-mechanism
%{_libexecdir}/gsd-locate-pointer
%{_libexecdir}/gsd-printer
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
%{_libdir}/gnome-settings-daemon-3.0/updates.gnome-settings-plugin
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
%{_libdir}/gnome-settings-daemon-3.0/libupdates.so
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
%{_datadir}/glib-2.0/schemas/org.gnome.settings-daemon.plugins.updates.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.settings-daemon.plugins.xrandr.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.settings-daemon.plugins.xsettings.gschema.xml

# Data files
%dir %{_datadir}/gnome-settings-daemon/
%{_datadir}/gnome-settings-daemon/gsd-a11y-preferences-dialog.ui
%{_datadir}/gnome-settings-daemon/icons/

# DBus services
%{_datadir}/dbus-1/interfaces/org.gnome.SettingsDaemonUpdates.xml
%{_datadir}/dbus-1/services/org.gnome.SettingsDaemon.service
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


%changelog
* Thu Sep 20 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.4.2-2.0ubuntu13
- Initial release for Fedora 18

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
