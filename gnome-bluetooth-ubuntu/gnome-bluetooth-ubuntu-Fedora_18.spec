# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

# Partially based off of Fedora 18's spec file

%define _ubuntu_rel 0ubuntu1

Name:		gnome-bluetooth
Version:	3.5.92
Epoch:		1
Release:	100.%{_ubuntu_rel}%{?dist}
Summary:	Utilities for connecting to bluetooth devices in GNOME and Unity

Group:		Applications/Communications
License:	GPLv2+
URL:		http://live.gnome.org/GnomeBluetooth
Source0:	http://download.gnome.org/sources/gnome-bluetooth/3.5/gnome-bluetooth-%{version}.tar.xz
Source1:	61-gnome-bluetooth-rfkill.rules

Source99:	https://launchpad.net/ubuntu/+archive/primary/+files/gnome-bluetooth_%{version}-%{_ubuntu_rel}.debian.tar.gz

BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	desktop-file-utils
BuildRequires:	gettext
BuildRequires:	gnome-common
BuildRequires:	gnome-doc-utils
BuildRequires:	gtk-doc
BuildRequires:	intltool
BuildRequires:	itstool
BuildRequires:	rarian-compat
BuildRequires:	pkgconfig

BuildRequires:	pkgconfig(appindicator3-0.1)
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(gconf-2.0)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(libnotify)
BuildRequires:	pkgconfig(nautilus-sendto)

Requires:	%{name}-libs = %{version}-%{release}
Requires:	bluez
Requires:	control-center
Requires:	desktop-notification-daemon
Requires:	gvfs-obexftp
Requires:	obexd
Requires:	pulseaudio-module-bluetooth

Provides:	dbus-bluez-pin-helper

Provides:	gnome-bluetooth-ubuntu = %{epoch}:%{version}-%{release}

%description
This package contains graphical utilities to setup, monitor, and use Bluetooth
devices.


%package libs
Summary:	GTK+ Bluetooth device selection widgets
Group:		System Environment/Libraries
License:	LGPLv2+

Requires:	gobject-introspection

Provides:       gnome-bluetooth-ubuntu-libs = %{epoch}:%{version}-%{release}

%description libs
This package contains the libraries needed for applications that want to display
a Bluetooth device selection widget.


%package libs-devel
Summary:	Development files for gnome-bluetooth-ubuntu-libs
Group:		Development/Libraries
License:	LGPLv2+

Requires:	%{name}-libs = %{version}-%{release}
Requires:	pkgconfig(gobject-introspection-1.0)

Provides:       gnome-bluetooth-ubuntu-libs-devel = %{epoch}:%{version}-%{release}

%description libs-devel
This package contains the development files needed for applications that want to
display a Bluetooth device selection widget.


%prep
%setup -q

# Apply Ubuntu's patches
tar zxvf '%{SOURCE99}'

for i in $(grep -v '#' debian/patches/series); do
  patch -Np1 -i "debian/patches/${i}"
done

autoreconf -vfi


%build
%configure \
  --disable-desktop-update \
  --disable-icon-update \
  --enable-nautilus-sendto=yes \
  --disable-schemas-compile

make %{?_smp_mflags}


%install
GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 make install DESTDIR=$RPM_BUILD_ROOT

# Install udev rule
install -dm755 $RPM_BUILD_ROOT%{_prefix}/lib/udev/rules.d/
install -m644 '%{SOURCE1}' $RPM_BUILD_ROOT%{_prefix}/lib/udev/rules.d/

# Install autostart file
desktop-file-install \
  --dir $RPM_BUILD_ROOT%{_sysconfdir}/xdg/autostart/ \
  --remove-key="NoDisplay" \
  debian/bluetooth-applet-unity.desktop

# Do not hide gnome-bluetooth from the startup applications tool
desktop-file-install \
  --dir $RPM_BUILD_ROOT%{_sysconfdir}/xdg/autostart/ \
  --delete-original \
  --remove-key="NoDisplay" \
  $RPM_BUILD_ROOT%{_sysconfdir}/xdg/autostart/bluetooth-applet-unity.desktop

# Validate desktop files
desktop-file-validate \
  $RPM_BUILD_ROOT%{_datadir}/applications/bluetooth-wizard.desktop
desktop-file-validate \
  $RPM_BUILD_ROOT%{_datadir}/applications/bluetooth-sendto.desktop

# Remove libtool files
find $RPM_BUILD_ROOT -type f -name '*.la' -delete

%find_lang gnome-bluetooth2
%find_lang gnome-bluetooth --with-gnome


%post
touch --no-create %{_datadir}/icons/hicolor/ &>/dev/null || :

%postun
if [ ${1} -eq 0 ]; then
  glib-compile-schemas %{_datadir}/glib-2.0/schemas/ &>/dev/null || :
  touch --no-create %{_datadir}/icons/hicolor/ &>/dev/null || :
  gtk-update-icon-cache -f %{_datadir}/icons/hicolor/ &>/dev/null || :
fi

%posttrans
glib-compile-schemas %{_datadir}/glib-2.0/schemas/ &>/dev/null || :
gtk-update-icon-cache -f %{_datadir}/icons/hicolor/ &>/dev/null || :


%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig


%files
%doc AUTHORS ChangeLog NEWS README
%{_bindir}/bluetooth-applet
%{_bindir}/bluetooth-sendto
%{_bindir}/bluetooth-wizard
%{_sysconfdir}/xdg/autostart/bluetooth-applet-unity.desktop
%{_sysconfdir}/xdg/autostart/bluetooth-applet.desktop
%dir %{_libdir}/gnome-bluetooth/
%dir %{_libdir}/gnome-bluetooth/plugins/
%{_libdir}/gnome-bluetooth/GnomeBluetoothApplet-1.0.typelib
%{_libdir}/gnome-bluetooth/libgnome-bluetooth-applet.so
%{_libdir}/gnome-bluetooth/libgnome-bluetooth-applet.so.0
%{_libdir}/gnome-bluetooth/libgnome-bluetooth-applet.so.0.0.0
%{_libdir}/gnome-bluetooth/plugins/libgbtgeoclue.so
%{_libdir}/nautilus-sendto/plugins/libnstbluetooth.so
%{_prefix}/lib/udev/rules.d/61-gnome-bluetooth-rfkill.rules
%{_datadir}/applications/bluetooth-sendto.desktop
%{_datadir}/applications/bluetooth-wizard.desktop
%{_datadir}/GConf/gsettings/gnome-bluetooth-nst
%{_datadir}/glib-2.0/schemas/com.canonical.indicator.bluetooth.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.Bluetooth.nst.gschema.xml
%dir %{_datadir}/gnome-bluetooth/
%{_datadir}/gnome-bluetooth/*.ui
%{_datadir}/gnome-bluetooth/pin-code-database.xml
%{_mandir}/man1/bluetooth-applet.1.gz
%{_mandir}/man1/bluetooth-sendto.1.gz
%{_mandir}/man1/bluetooth-wizard.1.gz


%files -f gnome-bluetooth2.lang -f gnome-bluetooth.lang libs
%doc AUTHORS ChangeLog NEWS README
%{_libdir}/libgnome-bluetooth.so.11
%{_libdir}/libgnome-bluetooth.so.11.0.0
%{_libdir}/girepository-1.0/GnomeBluetooth-1.0.typelib
%{_datadir}/icons/hicolor/16x16/apps/bluetooth.png
%{_datadir}/icons/hicolor/22x22/apps/bluetooth.png
%{_datadir}/icons/hicolor/24x24/apps/bluetooth.png
%{_datadir}/icons/hicolor/32x32/apps/bluetooth.png
%{_datadir}/icons/hicolor/48x48/apps/bluetooth.png
%{_datadir}/icons/hicolor/scalable/apps/bluetooth.svg
%{_datadir}/icons/hicolor/16x16/status/*.png
%{_datadir}/icons/hicolor/22x22/status/*.png
%{_datadir}/icons/hicolor/24x24/status/*.png
%{_datadir}/icons/hicolor/32x32/status/*.png
%{_datadir}/icons/hicolor/48x48/status/*.png
%{_datadir}/icons/hicolor/scalable/status/bluetooth-paired.svg


%files libs-devel
%doc AUTHORS ChangeLog NEWS README
%dir %{_includedir}/gnome-bluetooth/
%{_includedir}/gnome-bluetooth/bluetooth-chooser-button.h
%{_includedir}/gnome-bluetooth/bluetooth-chooser-combo.h
%{_includedir}/gnome-bluetooth/bluetooth-chooser.h
%{_includedir}/gnome-bluetooth/bluetooth-client.h
%{_includedir}/gnome-bluetooth/bluetooth-enums.h
%{_includedir}/gnome-bluetooth/bluetooth-filter-widget.h
%{_includedir}/gnome-bluetooth/bluetooth-killswitch.h
%{_includedir}/gnome-bluetooth/bluetooth-plugin-manager.h
%{_includedir}/gnome-bluetooth/bluetooth-plugin.h
%{_includedir}/gnome-bluetooth/bluetooth-utils.h
%{_libdir}/libgnome-bluetooth.so
%{_libdir}/pkgconfig/gnome-bluetooth-1.0.pc
%{_datadir}/gir-1.0/GnomeBluetooth-1.0.gir
%{_datadir}/gtk-doc/html/gnome-bluetooth/


%changelog
* Sun Sep 23 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.5.92-100.0ubuntu1
- Initial release for Fedora 18
- Version 3.5.92
- Ubuntu release 0ubuntu1

* Tue Jul 17 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.4.2-1.0ubuntu1
- Initial release
- Based off of Fedora 17's spec file
- Version 3.4.2
- Ubuntu release 0ubuntu1
