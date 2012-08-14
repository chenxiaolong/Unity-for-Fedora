# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

%global __provides_exclude_from %{python_sitearch}/indicate/_indicate.so

Name:		libindicate
Version:	12.10.0
Release:	1%{?dist}
Summary:	Small library for applications to raise "flags" on DBus

Group:		System Environment/Libraries
License:	LGPLv2 and LGPLv3
URL:		https://launchpad.net/libindicate
Source0:	https://launchpad.net/libindicate/12.10/%{version}/+download/libindicate-%{version}.tar.gz

Patch1:		0002_missing_documentation.patch
Patch2:		0003_libpyglib-linking.patch

BuildRequires:	dbus-glib-devel
BuildRequires:	gtk-sharp2-devel
BuildRequires:	gtk-sharp2-gapi
BuildRequires:	gnome-doc-utils
BuildRequires:	gobject-introspection-devel
BuildRequires:	gtk-doc
BuildRequires:	gtk2-devel
BuildRequires:	gtk3-devel
BuildRequires:	intltool
BuildRequires:	libdbusmenu-glib-devel
BuildRequires:	libtool
BuildRequires:	mono-core
BuildRequires:	mono-devel
BuildRequires:	pygobject2-devel
BuildRequires:	pygtk2-devel
BuildRequires:	python-devel
BuildRequires:	vala-tools

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
Requires:	dbus-glib-devel
Requires:	libdbusmenu-glib-devel

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
Requires:	dbus-glib-devel
Requires:	gtk3-devel

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
Requires:	dbus-glib-devel
Requires:	gtk2-devel

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
           --enable-introspection=yes
make -j1
popd

pushd build-gtk3
%configure --with-gtk=3 --disable-scrollkeeper --enable-gtk-doc \
           --enable-introspection=yes
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
%{_libdir}/libindicate.so.5
%{_libdir}/libindicate.so.5.0.7
%{_libdir}/girepository-1.0/Indicate-0.7.typelib


%files -n python-indicate
%{python_sitearch}/indicate/__init__.py*
%{python_sitearch}/indicate/_indicate.a
%{python_sitearch}/indicate/_indicate.so
%{_datadir}/pygtk/2.0/defs/indicate.defs


%files devel
%{_includedir}/libindicate-0.7/libindicate/indicate-enum-types.h
%{_includedir}/libindicate-0.7/libindicate/indicator-messages.h
%{_includedir}/libindicate-0.7/libindicate/indicator.h
%{_includedir}/libindicate-0.7/libindicate/interests.h
%{_includedir}/libindicate-0.7/libindicate/listener.h
%{_includedir}/libindicate-0.7/libindicate/server.h
%{_libdir}/pkgconfig/indicate-0.7.pc
%{_libdir}/libindicate.a
%{_libdir}/libindicate.so
%{_datadir}/gir-1.0/Indicate-0.7.gir
%{_datadir}/vala/vapi/Indicate-0.7.vapi


%files gtk3
%{_libdir}/libindicate-gtk3.so.3
%{_libdir}/libindicate-gtk3.so.3.0.3
%{_libdir}/girepository-1.0/IndicateGtk3-0.7.typelib


%files gtk3-devel
%{_includedir}/libindicate-gtk3-0.7/libindicate-gtk/indicator.h
%{_includedir}/libindicate-gtk3-0.7/libindicate-gtk/listener.h
%{_libdir}/pkgconfig/indicate-gtk3-0.7.pc
%{_libdir}/libindicate-gtk3.a
%{_libdir}/libindicate-gtk3.so
%{_datadir}/gir-1.0/IndicateGtk3-0.7.gir
%{_datadir}/vala/vapi/IndicateGtk3-0.7.vapi


%files gtk2
%{_libdir}/libindicate-gtk.so.3
%{_libdir}/libindicate-gtk.so.3.0.3
%{_libdir}/girepository-1.0/IndicateGtk-0.7.typelib


%files gtk2-devel
%{_includedir}/libindicate-gtk-0.7/libindicate-gtk/indicator.h
%{_includedir}/libindicate-gtk-0.7/libindicate-gtk/listener.h
%{_libdir}/pkgconfig/indicate-gtk-0.7.pc
%{_libdir}/libindicate-gtk.a
%{_libdir}/libindicate-gtk.so
%{_datadir}/gir-1.0/IndicateGtk-0.7.gir
%{_datadir}/vala/vapi/IndicateGtk-0.7.vapi


%files docs
%{_datadir}/gtk-doc/html/libindicate/IndicateIndicator.html
%{_datadir}/gtk-doc/html/libindicate/IndicateListener.html
%{_datadir}/gtk-doc/html/libindicate/IndicateServer.html
%{_datadir}/gtk-doc/html/libindicate/base.html
%{_datadir}/gtk-doc/html/libindicate/home.png
%{_datadir}/gtk-doc/html/libindicate/index.html
%{_datadir}/gtk-doc/html/libindicate/index.sgml
%{_datadir}/gtk-doc/html/libindicate/ix01.html
%{_datadir}/gtk-doc/html/libindicate/left.png
%{_datadir}/gtk-doc/html/libindicate/libindicate.devhelp2
%{_datadir}/gtk-doc/html/libindicate/listeners.html
%{_datadir}/gtk-doc/html/libindicate/right.png
%{_datadir}/gtk-doc/html/libindicate/style.css
%{_datadir}/gtk-doc/html/libindicate/subclass.html
%{_datadir}/gtk-doc/html/libindicate/up.png
%{_docdir}/%{name}-docs-%{version}/examples/im-client.c
%{_docdir}/%{name}-docs-%{version}/examples/im-client.py*
%{_docdir}/%{name}-docs-%{version}/examples/indicate-alot.c
%{_docdir}/%{name}-docs-%{version}/examples/indicate-and-crash.c
%{_docdir}/%{name}-docs-%{version}/examples/listen-and-print.c
%{_docdir}/%{name}-docs-%{version}/examples/listen-and-print.py*


%files sharp
%{_libdir}/indicate-sharp-0.1/indicate-sharp.dll
%{_libdir}/indicate-sharp-0.1/indicate-sharp.dll.config
%{_prefix}/lib/mono/gac/indicate-sharp/*/*.dll*
%{_prefix}/lib/mono/indicate/indicate-sharp.dll


%files sharp-devel
%{_libdir}/pkgconfig/indicate-sharp-0.1.pc


%files gtk2-sharp
%{_libdir}/indicate-gtk-sharp-0.1/indicate-gtk-sharp.dll
%{_libdir}/indicate-gtk-sharp-0.1/indicate-gtk-sharp.dll.config
%{_prefix}/lib/mono/gac/indicate-gtk-sharp/*/*.dll*
%{_prefix}/lib/mono/indicate-gtk/indicate-gtk-sharp.dll


%files gtk2-sharp-devel
%{_libdir}/pkgconfig/indicate-gtk-sharp-0.1.pc


%changelog
* Mon Aug 13 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 12.10.0-1
- Version 12.10.0

* Tue Jun 05 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.6.92-1
- Initial release
- Version 0.6.92
