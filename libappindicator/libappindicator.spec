# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

Name:		libappindicator
Version:	12.10.1daily13.04.15
Release:	1%{?dist}
Summary:	Application indicators library

Group:		System Environment/Libraries
License:	LGPLv2 and LGPLv3
URL:		https://launchpad.net/libappindicator
Source0:	https://launchpad.net/ubuntu/+archive/primary/+files/libappindicator_%{version}.orig.tar.gz
Patch0:		0001_Fix_mono_dir.patch
Patch1:		0002_g_type_init.patch

BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gtk-doc
BuildRequires:	vala-tools

BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(dbusmenu-glib-0.4)
BuildRequires:	pkgconfig(dbusmenu-gtk-0.4)
BuildRequires:	pkgconfig(dbusmenu-gtk3-0.4)
BuildRequires:	pkgconfig(gapi-2.0)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(gtk-sharp-2.0)
BuildRequires:	pkgconfig(indicate-0.7)
BuildRequires:	pkgconfig(indicate-gtk-0.7)
BuildRequires:	pkgconfig(indicator-0.4)
BuildRequires:	pkgconfig(indicator3-0.4)
BuildRequires:	pkgconfig(mono)
BuildRequires:	pkgconfig(mono-nunit)
BuildRequires:	pkgconfig(pygtk-2.0)

# CheckDepends
BuildRequires:	dbus-test-runner
BuildRequires:	xorg-x11-server-Xvfb

%description
A library to allow applications to export a menu into the Unity Menu bar. Based
on KSNI it also works in KDE and will fallback to generic Systray support if
none of those are available.


%package -n python-appindicator
Summary:	Python 2 bindings for libappindicator
Group:		System Environment/Libraries

Requires:	%{name} = %{version}-%{release}

%description -n python-appindicator
This package contains the Python 2 bindings for the appindicator library.


%package devel
Summary:	Development files for libappindicator
Group:		Development/Libraries

Requires:	%{name} = %{version}-%{release}
Requires:	pkgconfig(dbus-glib-1)
Requires:	pkgconfig(dbusmenu-glib-0.4)

%description devel
This package contains the development files for the appindicator library.


%package gtk3
Summary:	Application indicators library - GTK 3
Group:		System Environment/Libraries

%description gtk3
A library to allow applications to export a menu into the Unity Menu bar. Based
on KSNI it also works in KDE and will fallback to generic Systray support if
none of those are available.

This package contains the GTK 3 version of this library.


%package gtk3-devel
Summary:	Development files for libappindicator-gtk3
Group:		Development/Libraries

Requires:	%{name}-gtk3 = %{version}-%{release}
Requires:	pkgconfig(dbus-glib-1)
Requires:	pkgconfig(dbusmenu-glib-0.4)

%description gtk3-devel
This package contains the development files for the appindicator-gtk3 library.


%package docs
Summary:	Documentation for libappindicator and libappindicator-gtk3
Group:		Documentation

BuildArch:	noarch

%description docs
This package contains the documentation for the appindicator and
appindicator-gtk3 libraries.


%package sharp
Summary:	Application indicators library - C#
Group:		System Environment/Libraries

%description sharp
A library to allow applications to export a menu into the Unity Menu bar. Based
on KSNI it also works in KDE and will fallback to generic Systray support if
none of those are available.

This package contains the Mono C# bindings for this library.


%package sharp-devel
Summary:	Development files for libappindicator-sharp
Group:		Development/Libraries

Requires:	%{name}-sharp = %{version}-%{release}

%description sharp-devel
This package contains the development files for the appindicator-sharp library.


%prep
%setup -q
%patch0 -p1 -b .monodir
%patch1 -p1 -b .g_type_init

sed -i 's/2\.35\.4/2.34.0/g' configure.ac

gtkdocize
autoreconf -vfi


%build
%global _configure ../configure
mkdir build-gtk2 build-gtk3

pushd build-gtk2
%configure --with-gtk=2 --enable-gtk-doc --disable-static
make -j1
popd

pushd build-gtk3
%configure --with-gtk=3 --enable-gtk-doc --disable-static
make -j1
popd


%check
pushd build-gtk2
make check
popd

pushd build-gtk3
make check
popd


%install
pushd build-gtk2
make install DESTDIR=$RPM_BUILD_ROOT
popd

pushd build-gtk3
make install DESTDIR=$RPM_BUILD_ROOT
popd

find $RPM_BUILD_ROOT -type f -name '*.la' -delete


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%post gtk3 -p /sbin/ldconfig

%postun gtk3 -p /sbin/ldconfig


%files
%doc README
%{_libdir}/libappindicator.so.*
%{_libdir}/girepository-1.0/AppIndicator-0.1.typelib


%files -n python-appindicator
%dir %{python_sitearch}/appindicator/
%{python_sitearch}/appindicator/__init__.py*
%{python_sitearch}/appindicator/_appindicator.so
%dir %{_datadir}/pygtk/
%dir %{_datadir}/pygtk/2.0/
%dir %{_datadir}/pygtk/2.0/defs/
%{_datadir}/pygtk/2.0/defs/appindicator.defs


%files devel
%dir %{_includedir}/libappindicator-0.1/
%dir %{_includedir}/libappindicator-0.1/libappindicator/
%{_includedir}/libappindicator-0.1/libappindicator/*.h
%{_libdir}/libappindicator.so
%{_libdir}/pkgconfig/appindicator-0.1.pc
%{_datadir}/gir-1.0/AppIndicator-0.1.gir
%{_datadir}/vala/vapi/appindicator-0.1.vapi
%{_datadir}/vala/vapi/appindicator-0.1.deps


%files gtk3
%doc README
%{_libdir}/libappindicator3.so.*
%{_libdir}/girepository-1.0/AppIndicator3-0.1.typelib


%files gtk3-devel
%dir %{_includedir}/libappindicator3-0.1/
%dir %{_includedir}/libappindicator3-0.1/libappindicator/
%{_includedir}/libappindicator3-0.1/libappindicator/*.h
%{_libdir}/libappindicator3.so
%{_libdir}/pkgconfig/appindicator3-0.1.pc
%{_datadir}/gir-1.0/AppIndicator3-0.1.gir
%{_datadir}/vala/vapi/appindicator3-0.1.vapi
%{_datadir}/vala/vapi/appindicator3-0.1.deps


%files docs
%doc %{_datadir}/gtk-doc/html/libappindicator/


%files sharp
%dir %{_libdir}/appindicator-sharp-0.1/
%{_libdir}/appindicator-sharp-0.1/appindicator-sharp.dll
%{_libdir}/appindicator-sharp-0.1/appindicator-sharp.dll.config
%{_libdir}/appindicator-sharp-0.1/policy.0.0.appindicator-sharp.config
%{_libdir}/appindicator-sharp-0.1/policy.0.0.appindicator-sharp.dll
%{_libdir}/appindicator-sharp-0.1/policy.0.1.appindicator-sharp.config
%{_libdir}/appindicator-sharp-0.1/policy.0.1.appindicator-sharp.dll
%dir %{_prefix}/lib/mono/appindicator-sharp/
%{_prefix}/lib/mono/appindicator-sharp/appindicator-sharp.dll
%{_prefix}/lib/mono/appindicator-sharp/policy.0.0.appindicator-sharp.dll
%dir %{_prefix}/lib/mono/gac/appindicator-sharp/
%dir %{_prefix}/lib/mono/gac/appindicator-sharp/*/
%{_prefix}/lib/mono/gac/appindicator-sharp/*/appindicator-sharp.dll
%{_prefix}/lib/mono/gac/appindicator-sharp/*/appindicator-sharp.dll.config
%dir %{_prefix}/lib/mono/gac/policy.0.0.appindicator-sharp/
%dir %{_prefix}/lib/mono/gac/policy.0.0.appindicator-sharp/*/
%{_prefix}/lib/mono/gac/policy.0.0.appindicator-sharp/*/policy.0.0.appindicator-sharp.dll
%{_prefix}/lib/mono/gac/policy.0.0.appindicator-sharp/*/policy.0.0.appindicator-sharp.config


%files sharp-devel
%{_libdir}/pkgconfig/appindicator-sharp-0.1.pc


%changelog
* Fri May 03 2013 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 12.10.1daily13.04.15-1
- Version 12.10.1daily13.04.15

* Sat Aug 18 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 12.10.0-2
- Fix directory ownership
- Use pkgconfig for dependencies
- Enable mono-nunit tests

* Mon Aug 13 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 12.10.0-1
- Version 12.10.0

* Wed Jun 27 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.4.92-1
- Initial release
- Version 0.4.92
