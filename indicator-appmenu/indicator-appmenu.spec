# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

Name:		indicator-appmenu
Version:	12.10.0
Release:	1%{?dist}
Summary:	Indicator to host the menus from an application

Group:		User Interface/Desktops
License:	GPLv3
URL:		https://launchpad.net/indicator-appmenu
Source0:	https://launchpad.net/indicator-appmenu/12.10/%{version}/+download/indicator-appmenu-%{version}.tar.gz

Patch0:		0001_Fix_dbusmenu-dumper_path.patch

BuildRequires:	gnome-doc-utils
BuildRequires:	intltool

BuildRequires:	bamf-devel
BuildRequires:	bamf3-devel
BuildRequires:	gtk3-devel
BuildRequires:	libappindicator-gtk3-devel
BuildRequires:	libdbusmenu-glib-devel
BuildRequires:	libdbusmenu-gtk3-devel
BuildRequires:	libdbusmenu-jsonloader-devel
BuildRequires:	libindicator-devel
BuildRequires:	libindicator-gtk3-devel
BuildRequires:	ncurses-devel
BuildRequires:	readline-devel
BuildRequires:	sqlite-devel
BuildRequires:	vala-tools

%description
This package contains an indicator to host the menus from an application.


%package tools
Summary: 	Indicator to host the menus from an application - Tools
Group:		Development/Tools

Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	libdbusmenu-tools

%description tools
This package contains debugging tools for the appmenu indicator.


%prep
%setup -q

%patch0 -p1 -b .dbusmenu-dumper


%build
CFLAGS="$RPM_OPT_FLAGS"

# Disable -Werror
CFLAGS="${CFLAGS} -Wno-error"

# Cannot find gio/gdesktopappinfo.h
CFLAGS="${CFLAGS} $(pkg-config --cflags --libs gio-unix-2.0)"

%configure --disable-static
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT

# Remove libtool files
find $RPM_BUILD_ROOT -type f -name '*.la' -delete

# Remove documentation (Ubuntu doesn't package it)
rm -rv $RPM_BUILD_ROOT%{_datadir}/gtk-doc/


%postun
if [ ${1} -eq 0 ] ; then
  glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans
glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :


%files
%doc AUTHORS ChangeLog
%{_libdir}/indicators3/7/libappmenu.so
%{_libexecdir}/hud-service
%{_datadir}/dbus-1/services/com.canonical.hud.service
%{_datadir}/glib-2.0/schemas/com.canonical.indicator.appmenu.gschema.xml
%{_datadir}/glib-2.0/schemas/com.canonical.indicator.appmenu.hud.gschema.xml
%{_datadir}/glib-2.0/schemas/com.canonical.indicator.appmenu.hud.search.gschema.xml


%files tools
%doc AUTHORS ChangeLog
%{_bindir}/hud-cli
%{_bindir}/hud-dump-application
%{_bindir}/hud-gtk
%{_bindir}/hud-list-applications
%{_bindir}/hud-verify-app-info
%{_libexecdir}/current-menu
%{_libexecdir}/current-menu-dump
%{_libexecdir}/menu-pusher
%{_libexecdir}/mock-json-app
%{_mandir}/man1/hud-cli.1.gz
%{_mandir}/man1/hud-dump-application.1.gz
%{_mandir}/man1/hud-list-applications.1.gz
%{_mandir}/man1/hud-verify-app-info.1.gz
%{_datadir}/hud-gtk/hud-gtk.ui


%changelog
* Mon Aug 13 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 12.10.0-1
- Version 12.10.0
- Drop GTK 2 subpackage: no longer maintained upstream

* Wed Jul 04 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.3.97-1
- Initial release
- Version 0.3.97
