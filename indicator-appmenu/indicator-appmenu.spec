# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

Name:		indicator-appmenu
Version:	12.10.3
Release:	1%{?dist}
Summary:	Indicator to host the menus from an application

Group:		User Interface/Desktops
License:	GPLv3
URL:		https://launchpad.net/indicator-appmenu
Source0:	https://launchpad.net/indicator-appmenu/12.10/%{version}/+download/indicator-appmenu-%{version}.tar.gz

Patch0:		0001_Fix_dbusmenu-dumper_path.patch

BuildRequires:	gnome-doc-utils
BuildRequires:	intltool
BuildRequires:	pkgconfig
BuildRequires:	vala-tools

BuildRequires:	pkgconfig(appindicator3-0.1)
BuildRequires:	pkgconfig(dbusmenu-glib-0.4)
BuildRequires:	pkgconfig(dbusmenu-gtk3-0.4)
BuildRequires:	pkgconfig(dbusmenu-jsonloader-0.4)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(indicator3-0.4)
BuildRequires:	pkgconfig(libbamf3)
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	pkgconfig(sqlite3)

BuildRequires:	readline-devel

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
%dir %{_libdir}/indicators3/
%dir %{_libdir}/indicators3/7/
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
%dir %{_datadir}/hud-gtk/
%{_datadir}/hud-gtk/hud-gtk.ui


%changelog
* Sat Oct 06 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 12.10.3-1
- Version 12.10.3

* Thu Sep 20 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 12.10.1-1
- Version 12.10.1

* Sat Aug 18 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 12.10.0-2
- Fix directory ownership
- Use pkgconfig for dependencies

* Mon Aug 13 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 12.10.0-1
- Version 12.10.0
- Drop GTK 2 subpackage: no longer maintained upstream

* Wed Jul 04 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.3.97-1
- Initial release
- Version 0.3.97
