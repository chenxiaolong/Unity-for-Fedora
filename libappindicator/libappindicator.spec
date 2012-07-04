# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

# The following line is for the scripts in my git repo
%define _ubuntu_match_rel 0ubuntu2

Name:		libappindicator
Version:	0.4.92
Release:	1%{?dist}
Summary:	Library to export menu bar to Unity

Group:		System Environment/Libraries
License:	LGPLv2 and LGPLv3
URL:		https://launchpad.net/libappindicator
Source0:	https://launchpad.net/libappindicator/0.5/%{version}/+download/libappindicator-%{version}.tar.gz
Patch0:		0001_Fix_mono_dir.patch

BuildRequires:	dbus-glib-devel
BuildRequires:	gobject-introspection-devel
BuildRequires:	gtk-doc
BuildRequires:	gtk-sharp2-devel
BuildRequires:	gtk-sharp2-gapi
BuildRequires:	gtk2-devel
BuildRequires:	gtk3-devel
BuildRequires:	libdbusmenu-glib-devel
BuildRequires:	libdbusmenu-gtk2-devel
BuildRequires:	libdbusmenu-gtk3-devel
BuildRequires:	libindicate-devel
BuildRequires:	libindicate-gtk2-devel
BuildRequires:	libindicator-devel
BuildRequires:	libindicator-gtk3-devel
BuildRequires:	mono-core
BuildRequires:	mono-devel
BuildRequires:	pygtk2-devel
BuildRequires:	vala-tools

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
Requires:	dbus-glib-devel
Requires:	libdbusmenu-glib-devel

%description devel
This package contains the development files for the appindicator library.


%package gtk3
Summary:	Library to export menu bar to Unity - GTK3
Group:		System Environment/Libraries

%description gtk3
A library to allow applications to export a menu into the Unity Menu bar. Based
on KSNI it also works in KDE and will fallback to generic Systray support if
none of those are available.

This package contains the GTK3 bindings for this library.


%package gtk3-devel
Summary:	Development files for libappindicator-gtk3
Group:		Development/Libraries

Requires:	%{name}-gtk3 = %{version}-%{release}
Requires:	dbus-glib-devel
Requires:	libdbusmenu-glib-devel

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
Summary:	Library to export menu bar to Unity - C#
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


%build
%global _configure ../configure
mkdir build-gtk2 build-gtk3

pushd build-gtk2
%configure --with-gtk=2 --enable-gtk-doc --disable-static
make %{?_smp_mflags}
popd

pushd build-gtk3
%configure --with-gtk=3 --enable-gtk-doc --disable-static
make %{?_smp_mflags}
popd


%install
rm -rf $RPM_BUILD_ROOT

pushd build-gtk2
make install DESTDIR=$RPM_BUILD_ROOT
popd


pushd build-gtk3
make install DESTDIR=$RPM_BUILD_ROOT
popd

find $RPM_BUILD_ROOT -type f -name '*.la' -delete


%post -p /usr/sbin/ldconfig

%postun -p /usr/sbin/ldconfig


%post gtk3 -p /usr/sbin/ldconfig

%postun gtk3 -p /usr/sbin/ldconfig


%files
%doc AUTHORS README
%{_libdir}/libappindicator.so.1
%{_libdir}/libappindicator.so.1.0.0
%{_libdir}/girepository-1.0/AppIndicator-0.1.typelib


%files -n python-appindicator
%dir %{python_sitearch}/appindicator/
%{python_sitearch}/appindicator/__init__.py*
%{python_sitearch}/appindicator/_appindicator.so
%{_datadir}/pygtk/2.0/defs/appindicator.defs


%files devel
%dir %{_includedir}/libappindicator-0.1/
%{_includedir}/libappindicator-0.1/libappindicator/app-indicator-enum-types.h
%{_includedir}/libappindicator-0.1/libappindicator/app-indicator.h
%{_libdir}/libappindicator.so
%{_libdir}/pkgconfig/appindicator-0.1.pc
%{_datadir}/gir-1.0/AppIndicator-0.1.gir
%{_datadir}/vala/vapi/appindicator-0.1.vapi
%{_datadir}/vala/vapi/appindicator-0.1.deps


%files gtk3
%{_libdir}/libappindicator3.so.1
%{_libdir}/libappindicator3.so.1.0.0
%{_libdir}/girepository-1.0/AppIndicator3-0.1.typelib


%files gtk3-devel
%dir %{_includedir}/libappindicator3-0.1/
%{_includedir}/libappindicator3-0.1/libappindicator/app-indicator-enum-types.h
%{_includedir}/libappindicator3-0.1/libappindicator/app-indicator.h
%{_libdir}/libappindicator3.so
%{_libdir}/pkgconfig/appindicator3-0.1.pc
%{_datadir}/gir-1.0/AppIndicator3-0.1.gir
%{_datadir}/vala/vapi/appindicator3-0.1.vapi
%{_datadir}/vala/vapi/appindicator3-0.1.deps


%files docs
%dir %{_datadir}/gtk-doc/html/libappindicator/
%{_datadir}/gtk-doc/html/libappindicator/annotation-glossary.html
%{_datadir}/gtk-doc/html/libappindicator/api-index-0-5.html
%{_datadir}/gtk-doc/html/libappindicator/api-index-deprecated.html
%{_datadir}/gtk-doc/html/libappindicator/api-index-full.html
%{_datadir}/gtk-doc/html/libappindicator/ch01.html
%{_datadir}/gtk-doc/html/libappindicator/home.png
%{_datadir}/gtk-doc/html/libappindicator/index.html
%{_datadir}/gtk-doc/html/libappindicator/index.sgml
%{_datadir}/gtk-doc/html/libappindicator/left.png
%{_datadir}/gtk-doc/html/libappindicator/libappindicator-app-indicator.html
%{_datadir}/gtk-doc/html/libappindicator/libappindicator.devhelp2
%{_datadir}/gtk-doc/html/libappindicator/object-tree.html
%{_datadir}/gtk-doc/html/libappindicator/right.png
%{_datadir}/gtk-doc/html/libappindicator/style.css
%{_datadir}/gtk-doc/html/libappindicator/up.png


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
%{_prefix}/lib/mono/gac/appindicator-sharp/*/appindicator-sharp.dll
%{_prefix}/lib/mono/gac/appindicator-sharp/*/appindicator-sharp.dll.config
%{_prefix}/lib/mono/gac/policy.0.0.appindicator-sharp/*/policy.0.0.appindicator-sharp.dll
%{_prefix}/lib/mono/gac/policy.0.0.appindicator-sharp/*/policy.0.0.appindicator-sharp.config


%files sharp-devel
%{_libdir}/pkgconfig/appindicator-sharp-0.1.pc


%changelog
* Wed Jun 27 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.4.92-1
- Initial release
- Version 0.4.92
