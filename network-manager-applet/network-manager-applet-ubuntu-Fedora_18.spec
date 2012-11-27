# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

# Based off of Fedora 18's spec file

%define _git_date 20121016
%define _nm_version 1:0.9.7.0
%define _obsolete_ver 1:0.9.7

Name:		network-manager-applet
Version:	0.9.7.0
# I will not put the Ubuntu version and release here. That would be way too long
Release:	100.git%{_git_date}%{?dist}
Summary:	A network control and status applet for NetworkManager

Group:		Applications/System
License:	GPLv2+
URL:		http://www.gnome.org/projects/NetworkManager/
# Tarball is from Fedora's git repo. It can be downloaded by running:
#   fedpkg co -a -B network-manager-applet
#   cd network-manager-applet/f18/
#   fedpkg sources
Source0:	network-manager-applet-%{version}.git%{_git_date}.tar.bz2

Source99:	https://launchpad.net/ubuntu/+archive/primary/+files/network-manager-applet_0.9.6.2+git201211052130.2d666bc-0ubuntu1.debian.tar.gz

Patch0:		fedora_nm-applet-no-notifications.patch
Patch1:		fedora_nm-applet-wifi-dialog-ui-fixes.patch
Patch2:		fedora_applet-ignore-deprecated.patch

BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	desktop-file-utils
BuildRequires:	gtk-doc
BuildRequires:	intltool
BuildRequires:	pkgconfig

BuildRequires:	gettext-devel
BuildRequires:	NetworkManager-devel >= %{_nm_version}
BuildRequires:	NetworkManager-glib-devel >= %{_nm_version}

BuildRequires:	pkgconfig(appindicator3-0.1)
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(gconf-2.0)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gnome-bluetooth-1.0)
BuildRequires:	pkgconfig(gnome-keyring-1)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(gudev-1.0) >= 147
BuildRequires:	pkgconfig(iso-codes)
BuildRequires:	pkgconfig(libnotify)

Requires:	libnm-gtk = %{version}-%{release}
Requires:	NetworkManager >= %{_nm_version}
Requires:	NetworkManager-glib >= %{_nm_version}
Requires:	nm-connection-editor = %{version}-%{release}

Requires:	dbus >= 1.4
Requires:	dbus-glib >= 0.94
Requires:	libnotify >= 0.4.3
Requires:	gnome-icon-theme
Requires:	gnome-keyring

Provides: 	network-manager-applet-ubuntu = %{version}-%{release}

Obsoletes:	NetworkManager-gnome < %{_obsolete_ver}

%description
This package contains a network control and status notification area applet for
use with NetworkManager.


%package -n nm-connection-editor
Summary:	A network connection configuration editor for NetworkManager

Requires:	NetworkManager-glib >= %{_nm_version}
Requires:	libnm-gtk = %{version}-%{release}

Requires:	dbus >= 1.4
Requires:	dbus-glib >= 0.94
Requires:	gnome-icon-theme
Requires:	gnome-keyring

Requires(post):	%{_bindir}/gtk-update-icon-cache

Provides:	nm-connection-editor-ubuntu = %{version}-%{release}

%description -n nm-connection-editor
This package contains a network configuration editor and Bluetooth modem
utility for use with NetworkManager.


%package -n libnm-gtk
Summary:	Private libraries for NetworkManager GUI support
Group:		Development/Libraries

Requires:	gtk3
Requires:	mobile-broadband-provider-info >= 0.20090602

Provides:	libnm-gtk-ubuntu = %{version}-%{release}

Obsoletes:	NetworkManager-gtk < %{_obsolete_ver}

%description -n libnm-gtk
This package contains private libraries to be used only by nm-applet,
nm-connection editor, and the GNOME Control Center.


%package -n libnm-gtk-devel
Summary:	Private header files for NetworkManager GUI support
Group:		Development/Libraries

Requires:	NetworkManager-devel >= %{_nm_version}
Requires:	NetworkManager-glib-devel >= %{_nm_version}
Requires:	libnm-gtk = %{version}-%{release}

Requires:	pkgconfig
Requires:	pkgconfig(gtk+-3.0)

Provides:	libnm-gtk-ubuntu-devel = %{version}-%{release}

Obsoletes:	NetworkManager-gtk-devel < %{_obsolete_ver}

%description -n libnm-gtk-devel
This package contains private header and pkg-config files to be used only by
nm-applet, nm-connection-editor, and the GNOME control center.


%prep
%setup -q

# Apply Fedora's patches
%patch0 -p1 -b .no-notifications
%patch1 -p1 -b .applet-wifi-ui
%patch2 -p1 -b .no-deprecated

# Apply Ubuntu's patches
tar zxvf '%{SOURCE99}'
for i in $(grep -v '#' debian/patches/series); do
  patch -p1 -i "debian/patches/${i}"
done

autoreconf -vfi


%build
%configure \
  --disable-static \
  --with-bluetooth \
  --enable-more-warnings=yes \
  --with-gtkver=3 \
  --enable-indicator

make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}

install -dm755 $RPM_BUILD_ROOT%{_datadir}/gnome-vpn-properties

# Remove libtool files
find $RPM_BUILD_ROOT -type f -name '*.la' -delete

# Validate desktop files
desktop-file-validate $RPM_BUILD_ROOT%{_sysconfdir}/xdg/autostart/nm-applet.desktop
desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/nm-connection-editor.desktop

%find_lang nm-applet


%post
touch --no-create %{_datadir}/icons/hicolor/ &>/dev/null || :

%postun
if [ ${1} -eq 0 ]; then
  touch --no-create %{_datadir}/icons/hicolor/ &>/dev/null
  gtk-update-icon-cache %{_datadir}/icons/hicolor/ &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor/ &>/dev/null || :


%post -n libnm-gtk -p /sbin/ldconfig

%postun -n libnm-gtk -p /sbin/ldconfig


%post -n nm-connection-editor
touch --no-create %{_datadir}/icons/hicolor/ &>/dev/null || :
glib-compile-schemas %{_datadir}/glib-2.0/schemas/ &>/dev/null || :

%postun -n nm-connection-editor
if [ ${1} -eq 0 ]; then
  touch --no-create %{_datadir}/icons/hicolor/ &>/dev/null
  gtk-update-icon-cache %{_datadir}/icons/hicolor/ &>/dev/null || :
fi
glib-compile-schemas %{_datadir}/glib-2.0/schemas/ &>/dev/null || :

%posttrans -n nm-connection-editor
gtk-update-icon-cache %{_datadir}/icons/hicolor/ &>/dev/null || :
glib-compile-schemas %{_datadir}/glib-2.0/schemas/ &>/dev/null || :


%files
%doc AUTHORS CONTRIBUTING NEWS README
%{_bindir}/nm-applet
%{_libexecdir}/nm-applet-migration-tool
%{_sysconfdir}/xdg/autostart/nm-applet.desktop
%{_datadir}/applications/nm-applet.desktop
%{_datadir}/GConf/gsettings/nm-applet.convert
%{_datadir}/icons/hicolor/22x22/apps/nm-adhoc.png
%{_datadir}/icons/hicolor/22x22/apps/nm-mb-roam.png
%{_datadir}/icons/hicolor/22x22/apps/nm-secure-lock.png
%{_datadir}/icons/hicolor/22x22/apps/nm-signal-*.png
%{_datadir}/icons/hicolor/22x22/apps/nm-stage*-connecting*.png
%{_datadir}/icons/hicolor/22x22/apps/nm-tech-*.png
%{_datadir}/icons/hicolor/22x22/apps/nm-vpn-active-lock.png
%{_datadir}/icons/hicolor/22x22/apps/nm-vpn-connecting*.png
%{_datadir}/icons/hicolor/22x22/apps/nm-wwan-tower.png
%dir %{_datadir}/nm-applet/
%{_datadir}/nm-applet/8021x.ui
%{_datadir}/nm-applet/gsm-unlock.ui
%{_datadir}/nm-applet/info.ui
%{_datadir}/nm-applet/keyring.png


%files -n nm-connection-editor -f nm-applet.lang
%{_bindir}/nm-connection-editor
%{_libdir}/gnome-bluetooth/plugins/libnma.so
%{_datadir}/applications/nm-connection-editor.desktop
%{_datadir}/glib-2.0/schemas/org.gnome.nm-applet.gschema.xml
%dir %{_datadir}/gnome-vpn-properties/
%{_datadir}/icons/hicolor/*/apps/nm-device-*.*
%{_datadir}/icons/hicolor/*/apps/nm-no-connection.*
%{_datadir}/icons/hicolor/16x16/apps/nm-vpn-standalone-lock.png
%dir %{_datadir}/nm-applet/
%{_datadir}/nm-applet/ce-*.ui
%{_datadir}/nm-applet/eap-method-*.ui
%{_datadir}/nm-applet/nag-user-dialog.ui
%{_datadir}/nm-applet/nm-connection-editor.ui
%{_datadir}/nm-applet/ws-*.ui


%files -n libnm-gtk
%{_libdir}/libnm-gtk.so.0
%{_libdir}/libnm-gtk.so.0.0.0
%{_libdir}/girepository-1.0/NMGtk-1.0.typelib
%dir %{_datadir}/libnm-gtk/
%{_datadir}/libnm-gtk/wifi.ui


%files -n libnm-gtk-devel
%dir %{_includedir}/libnm-gtk/
%{_includedir}/libnm-gtk/*.h
%{_libdir}/libnm-gtk.so
%{_libdir}/pkgconfig/libnm-gtk.pc
%{_datadir}/gir-1.0/NMGtk-1.0.gir


%changelog
* Mon Nov 26 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.9.7.0-100.git20121016
- Update to Fedora-git-snapshot 20121016
- Ubuntu version 0.9.6.2+git201211052130.2d666bc
- Ubuntu release 0ubuntu1

* Sat Oct 06 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.9.7.0-100.git20121004
- Update to Fedora git snapshot 20121004

* Sun Sep 23 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.9.7.0-100.git20120820
- Initial release
- Based on Fedora 18's spec file
- Version 0.9.7.0
- Git checkout date 2012-08-20
