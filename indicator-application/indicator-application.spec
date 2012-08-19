# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

Name:		indicator-application
Version:	0.5.0
Release:	2%{?dist}
Summary:	Indicator that takes menus and puts them in the panel

Group:		User Interface/Desktops
License:	GPLv3
URL:		https://launchpad.net/indicator-application
Source0:	https://launchpad.net/indicator-application/0.5/%{version}/+download/indicator-application-%{version}.tar.gz

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


%package gtk2
Summary:	Indicator that takes menus and puts them in the panel - GTK 2
Group:		User Interface/Desktops

Requires:	%{name}%{?_isa} = %{version}-%{release}

%description gtk2
This packages contains the GTK 2 version of the application indicator.


%prep
%setup -q


%build
%global _configure ../configure
mkdir build-gtk2 build-gtk3

pushd build-gtk2
%configure --with-gtk=2 --disable-static
make %{?_smp_mflags}
popd

pushd build-gtk3
%configure --with-gtk=3 --disable-static
make %{?_smp_mflags}
popd


%install
pushd build-gtk2
make install DESTDIR=$RPM_BUILD_ROOT
popd

pushd build-gtk3
make install DESTDIR=$RPM_BUILD_ROOT
popd

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


%files gtk2
%doc AUTHORS ChangeLog README
%dir %{_libdir}/indicators/
%dir %{_libdir}/indicators/7/
%{_libdir}/indicators/7/libapplication.so


%changelog
* Sat Aug 18 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.5.0-2
- Fix directory ownership
- Use pkgconfig for dependencies

* Wed Jul 04 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.5.0-1
- Initial release
- Version 0.5.0
