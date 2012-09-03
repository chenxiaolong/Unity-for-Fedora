# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

Name:		indicator-application
Version:	12.10.0
Release:	1%{?dist}
Summary:	Indicator that takes menus and puts them in the panel

Group:		User Interface/Desktops
License:	GPLv3
URL:		https://launchpad.net/indicator-application
Source0:	https://launchpad.net/indicator-application/12.10/%{version}/+download/indicator-application-%{version}.tar.gz

BuildRequires:	intltool
BuildRequires:	pkgconfig

BuildRequires:	pkgconfig(appindicator-0.1)
BuildRequires:	pkgconfig(appindicator3-0.1)
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(dbusmenu-glib-0.4)
BuildRequires:	pkgconfig(dbusmenu-gtk-0.4)
BuildRequires:	pkgconfig(dbusmenu-gtk3-0.4)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(indicator-0.4)
BuildRequires:	pkgconfig(indicator3-0.4)
BuildRequires:	pkgconfig(json-glib-1.0)

%description
This package contains a library and indicator that takes menus from applications
and places them in the panel.


%prep
%setup -q


%build
%configure --disable-static
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT

# Remove libtool files
find $RPM_BUILD_ROOT -type f -name '*.la' -delete


%files
%doc AUTHORS ChangeLog README
%dir %{_libdir}/indicators3/
%dir %{_libdir}/indicators3/7/
%{_libdir}/indicators3/7/libapplication.so
%{_libexecdir}/indicator-application-service
%{_datadir}/dbus-1/services/indicator-application.service
%dir %{_datadir}/indicator-application/
%{_datadir}/indicator-application/ordering-override.keyfile


%changelog
* Mon Sep 03 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 12.10.0-1
- Version 12.10.0
- Drop GTK 2 subpackage

* Sat Aug 18 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.5.0-2
- Fix directory ownership
- Use pkgconfig for dependencies

* Wed Jul 04 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.5.0-1
- Initial release
- Version 0.5.0
