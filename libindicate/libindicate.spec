# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

%global __provides_exclude_from %{python_sitearch}/indicate/_indicate.so

Name:		libindicate
Version:	12.10.0
Release:	2%{?dist}
Summary:	Small library for applications to raise "flags" on DBus

Group:		System Environment/Libraries
License:	LGPLv2 and LGPLv3
URL:		https://launchpad.net/libindicate
Source0:	https://launchpad.net/libindicate/12.10/%{version}/+download/libindicate-%{version}.tar.gz

Patch1:		0002_missing_documentation.patch
Patch2:		0003_libpyglib-linking.patch

BuildRequires:	gnome-doc-utils
BuildRequires:	gtk-doc
BuildRequires:	intltool
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	vala-tools

BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(dbusmenu-glib-0.4)
BuildRequires:	pkgconfig(gapi-2.0)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(gtk-sharp-2.0)
BuildRequires:	pkgconfig(mono)
BuildRequires:	pkgconfig(pygobject-2.0)
BuildRequires:	pkgconfig(pygtk-2.0)
BuildRequires:	pkgconfig(python2)

%description
A small library for applications to raise "flags" on DBus for other components
of the desktop to pick up and visualize. Currently used by the messaging
indicator.


%package -n python-indicate
Summary:	Python 2 bindings for libindicate
Group:		System Environment/Libraries

Requires:	%{name} = %{version}-%{release}

%description -n python-indicate
This package contains the Python 2 bindings for the indicate library.


%package devel
Summary:	Development files for libindicate
Group:		Development/Libraries

Requires:	%{name} = %{version}-%{release}
Requires:	pkgconfig(dbus-glib-1)
Requires:	pkgconfig(dbusmenu-glib-0.4)

%description devel
This package contains the development files for the indicate library.


%package gtk3
Summary:	Small library for applications to raise "flags" on DBus - GTK3
Group:		System Environment/Libraries

%description gtk3
A small library for applications to raise "flags" on DBus for other components
of the desktop to pick up and visualize. Currently used by the messaging
indicator.

This package contains the GTK3 bindings for this library.


%package gtk3-devel
Summary:	Development files for libindicate-gtk3
Group:		Development/Libraries

Requires:	%{name}-gtk3 = %{version}-%{release}
Requires:	%{name}-devel = %{version}-%{release}
Requires:	pkgconfig(dbus-glib-1)
Requires:	pkgconfig(gtk+-3.0)

%description gtk3-devel
This package contains the development files for the indicate-gtk3 library.


%package gtk2
Summary:	Small library for applications to raise "flags" on DBus - GTK2
Group:		System Environment/Libraries

%description gtk2
A small library for applications to raise "flags" on DBus for other components
of the desktop to pick up and visualize. Currently used by the messaging
indicator.

This package contains the GTK2 bindings for this library.


%package gtk2-devel
Summary:	Development files for libindicate-gtk2
Group:		Development/Libraries

Requires:	%{name}-gtk2 = %{version}-%{release}
Requires:	%{name}-devel = %{version}-%{release}
Requires:	%{name}-gtk3-devel = %{version}-%{release}
Requires:	pkgconfig(dbus-glib-1)
Requires:	pkgconfig(gtk+-2.0)

%description gtk2-devel
This packages contains the development files for the indicate-gtk2 library.


%package docs
Summary:	Documentation for libindicate
Group:		Documentation

BuildArch:	noarch

%description docs
This package contains the documentation for the indicate library.


%package sharp
Summary:	Small library for applications to raise "flags" on DBus - C#
Group:		System Environment/Libraries

%description sharp
A small library for applications to raise "flags" on DBus for other components
of the desktop to pick up and visualize. Currently used by the messaging
indicator.

This package contains the Mono C# bindings for this library.


%package sharp-devel
Summary:	Development files for libindicate-sharp
Group:		Development/Libraries

Requires:	%{name}-sharp = %{version}-%{release}

%description sharp-devel
This package contains the development files for the indicate-sharp library.


%package gtk2-sharp
Summary:	Small library for applications to raise "flags" on DBus - GTK2 C#
Group:		System Environment/Libraries

Requires:	%{name}-sharp = %{version}-%{release}

%description gtk2-sharp
A small library for applications to raise "flags" on DBus for other components
of the desktop to pick up and visualize. Currently used by the messaging
indicator.

This package contains the GTK# bindings for this library.


%package gtk2-sharp-devel
Summary:	Development files for libindicate-gtk2-sharp
Group:		Development/Libraries

Requires:	%{name}-gtk2-sharp = %{version}-%{release}

%description gtk2-sharp-devel
This packages contains the development files for the indicate-gtk2-sharp
library.


%prep
%setup -q
%patch1 -p1 -b .documentation
%patch2 -p1 -b .libpygliblink

# Build fix (thanks to Damian!)
sed -i '/#include "glib\/gmessages.h"/d' libindicate/indicator.c

autoreconf -vfi


%build
%global _configure ../configure
mkdir build-gtk2 build-gtk3

pushd build-gtk2
%configure --with-gtk=2 --disable-scrollkeeper --enable-gtk-doc \
           --enable-introspection=yes --disable-static
make -j1
popd

pushd build-gtk3
%configure --with-gtk=3 --disable-scrollkeeper --enable-gtk-doc \
           --enable-introspection=yes --disable-static
make -j1
popd


%install
pushd build-gtk2
make install DESTDIR=$RPM_BUILD_ROOT
popd

pushd build-gtk3
make install DESTDIR=$RPM_BUILD_ROOT
popd

find $RPM_BUILD_ROOT -name '*.la' -delete

# Put documentation in correct directory
install -dm755 $RPM_BUILD_ROOT%{_docdir}/%{name}-docs-%{version}/examples/
mv $RPM_BUILD_ROOT%{_docdir}/libindicate/examples/* \
               $RPM_BUILD_ROOT%{_docdir}/%{name}-docs-%{version}/examples/


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%post gtk3 -p /sbin/ldconfig

%postun gtk3 -p /sbin/ldconfig


%post gtk2 -p /sbin/ldconfig

%postun gtk2 -p /sbin/ldconfig


%files
%doc AUTHORS
%{_libdir}/libindicate.so.*
%{_libdir}/girepository-1.0/Indicate-0.7.typelib


%files -n python-indicate
%dir %{python_sitearch}/indicate/
%{python_sitearch}/indicate/__init__.py*
%{python_sitearch}/indicate/_indicate.so
%dir %{_datadir}/pygtk/
%dir %{_datadir}/pygtk/2.0/
%dir %{_datadir}/pygtk/2.0/defs/
%{_datadir}/pygtk/2.0/defs/indicate.defs


%files devel
%dir %{_includedir}/libindicate-0.7/
%dir %{_includedir}/libindicate-0.7/libindicate/
%{_includedir}/libindicate-0.7/libindicate/*.h
%{_libdir}/pkgconfig/indicate-0.7.pc
%{_libdir}/libindicate.so
%{_datadir}/gir-1.0/Indicate-0.7.gir
%{_datadir}/vala/vapi/Indicate-0.7.vapi


%files gtk3
%{_libdir}/libindicate-gtk3.so.*
%{_libdir}/girepository-1.0/IndicateGtk3-0.7.typelib


%files gtk3-devel
%dir %{_includedir}/libindicate-gtk3-0.7/
%dir %{_includedir}/libindicate-gtk3-0.7/libindicate-gtk/
%{_includedir}/libindicate-gtk3-0.7/libindicate-gtk/*.h
%{_libdir}/pkgconfig/indicate-gtk3-0.7.pc
%{_libdir}/libindicate-gtk3.so
%{_datadir}/gir-1.0/IndicateGtk3-0.7.gir
%{_datadir}/vala/vapi/IndicateGtk3-0.7.vapi


%files gtk2
%{_libdir}/libindicate-gtk.so.*
%{_libdir}/girepository-1.0/IndicateGtk-0.7.typelib


%files gtk2-devel
%dir %{_includedir}/libindicate-gtk-0.7/
%dir %{_includedir}/libindicate-gtk-0.7/libindicate-gtk/
%{_includedir}/libindicate-gtk-0.7/libindicate-gtk/*.h
%{_libdir}/pkgconfig/indicate-gtk-0.7.pc
%{_libdir}/libindicate-gtk.so
%{_datadir}/gir-1.0/IndicateGtk-0.7.gir
%{_datadir}/vala/vapi/IndicateGtk-0.7.vapi


%files docs
%doc %{_datadir}/gtk-doc/html/libindicate/
%dir %{_docdir}/%{name}-docs-%{version}/
%dir %{_docdir}/%{name}-docs-%{version}/examples/
%{_docdir}/%{name}-docs-%{version}/examples/im-client.c
%{_docdir}/%{name}-docs-%{version}/examples/im-client.py*
%{_docdir}/%{name}-docs-%{version}/examples/indicate-alot.c
%{_docdir}/%{name}-docs-%{version}/examples/indicate-and-crash.c
%{_docdir}/%{name}-docs-%{version}/examples/listen-and-print.c
%{_docdir}/%{name}-docs-%{version}/examples/listen-and-print.py*


%files sharp
%dir %{_libdir}/indicate-sharp-0.1/
%{_libdir}/indicate-sharp-0.1/indicate-sharp.dll
%{_libdir}/indicate-sharp-0.1/indicate-sharp.dll.config
%dir %{_prefix}/lib/mono/gac/indicate-sharp/
%dir %{_prefix}/lib/mono/gac/indicate-sharp/*/
%{_prefix}/lib/mono/gac/indicate-sharp/*/*.dll*
%dir %{_prefix}/lib/mono/indicate/
%{_prefix}/lib/mono/indicate/indicate-sharp.dll


%files sharp-devel
%{_libdir}/pkgconfig/indicate-sharp-0.1.pc


%files gtk2-sharp
%dir %{_libdir}/indicate-gtk-sharp-0.1/
%{_libdir}/indicate-gtk-sharp-0.1/indicate-gtk-sharp.dll
%{_libdir}/indicate-gtk-sharp-0.1/indicate-gtk-sharp.dll.config
%dir %{_prefix}/lib/mono/gac/indicate-gtk-sharp/
%dir %{_prefix}/lib/mono/gac/indicate-gtk-sharp/*/
%{_prefix}/lib/mono/gac/indicate-gtk-sharp/*/*.dll*
%dir %{_prefix}/lib/mono/indicate-gtk/
%{_prefix}/lib/mono/indicate-gtk/indicate-gtk-sharp.dll


%files gtk2-sharp-devel
%{_libdir}/pkgconfig/indicate-gtk-sharp-0.1.pc


%changelog
* Sat Aug 18 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 12.10.0-2
- Clean up spec file
- Use pkgconfig for dependencies
- Fix directory ownership

* Mon Aug 13 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 12.10.0-1
- Version 12.10.0

* Tue Jun 05 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.6.92-1
- Initial release
- Version 0.6.92
