# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

Name:		libdbusmenu
Version:	12.10.2
Release:	1%{?dist}
Summary:	Small library that passes a menu structure across DBus

Group:		System Environment/Libraries
License:	GPLv3 and LGPLv2 and LGPLv3
URL:		https://launchpad.net/dbusmenu
Source0:	https://launchpad.net/dbusmenu/12.10/%{version}/+download/libdbusmenu-%{version}.tar.gz

Patch0:		0001_Fix_sgml.patch

# Require Ubuntu versions of GTK2 and GTK3
BuildRequires:	gtk2-ubuntu-devel
BuildRequires:	gtk3-ubuntu-devel

BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gnome-doc-utils
BuildRequires:	gtk-doc
BuildRequires:	intltool
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	vala-tools

BuildRequires:	pkgconfig(atk)
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(gdk-pixbuf-2.0)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(json-glib-1.0)
BuildRequires:	pkgconfig(valgrind)
BuildRequires:	pkgconfig(x11)

%description
A small little library that was created by pulling out some comon code out of
indicator-applet. It passes a menu structure across DBus so that a program can
create a menu simply without worrying about how it is displayed on the other
side of the bus.


%package tools
Summary:	Development tools for the dbusmenu libraries
Group:		Development/Tools

Requires:	%{name}-glib = %{version}-%{release}

%description tools
This packages contains the development tools for the dbusmenu libraries.


%package glib
Summary:	Small library that passes a menu structure across DBus
Group:		System Environment/Libraries

%description glib
This package contains the shared libraries for the dbusmenu-glib library.


%package glib-devel
Summary:	Development files for libdbusmenu-glib
Group:		Development/Libraries

Requires:	%{name}-glib = %{version}-%{release}
Requires:	pkgconfig(dbus-glib-1)
# GTK 2 with Ubuntu's patches
Requires:	gtk2-ubuntu-devel

%description glib-devel
This package contains the development files for the dbusmenu-glib library.


%package glib-docs
Summary:	Documentation for libdbusmenu-glib
Group:		Documentation

BuildArch:	noarch

%description glib-docs
This package includes the documentation for the dbusmenu-glib library.


%package gtk2
Summary:	Small library that passes a menu structure across DBus - GTK2 version
Group:		System Environment/Libraries

Requires:	gtk2-ubuntu

%description gtk2
This package contains the shared libraries for the dbusmenu-gtk2 library.


%package gtk2-devel
Summary:	Development files for libdbusmenu-gtk2
Group:		Development/Libraries

Requires:	%{name}-gtk2 = %{version}-%{release}
Requires:	%{name}-glib-devel = %{version}-%{release}
# GTK 2 with Ubuntu's patches
Requires:	gtk2-ubuntu-devel
Requires:	pkgconfig(dbus-glib-1)

%description gtk2-devel
This package contains the development files for the dbusmenu-gtk2 library.


%package gtk3
Summary:	Small library that passes a menu structure across DBus - GTK3 version
Group:		System Environment/Libraries

Requires:	gtk3-ubuntu

%description gtk3
This package contains the shared libraries for the dbusmenu-gtk3 library.


%package gtk3-devel
Summary:	Development files for libdbusmenu-gtk3
Group:		Development/Libraries

Requires:	%{name}-gtk3 = %{version}-%{release}
Requires:	%{name}-glib-devel = %{version}-%{release}
# GTK 3 with Ubuntu patches
Requires:	gtk3-ubuntu-devel
Requires:	pkgconfig(dbus-glib-1)

%description gtk3-devel
This package contains the development files for the dbusmenu-gtk3 library.


%package gtk-docs
Summary:	Documentation for libdbusmenu-gtk2 and libdbusmenu-gtk3
Group:		Documentation

BuildArch:	noarch

%description gtk-docs
This package contains the documentation for the dbusmenu-gtk2 and dbusmenu-gtk3
libraries.


%package jsonloader
Summary:	Small library that passes a menu structure across DBus - Test library
Group:		System Environment/Libraries

%description jsonloader
This package contains the shared libraries for dbusmenu-jsonloader, a library
meant for test suites.


%package jsonloader-devel
Summary:	Development files for libdbusmenu-jsonloader
Group:		Development/Libraries

Requires:	%{name}-jsonloader = %{version}-%{release}
Requires:	%{name}-glib-devel = %{version}-%{release}
Requires:	pkgconfig(dbus-glib-1)
Requires:	pkgconfig(json-glib-1.0)

%description jsonloader-devel
This package contains the development files for the dbusmenu-jsonloader library.


%prep
%setup -q

%patch0 -p1 -b .fix-sgml

autoreconf -vfi

# Disable rpath (from Debian wiki)
sed -i -r 's/(hardcode_into_libs)=.*$/\1=no/' configure


%build
%global _configure ../configure
mkdir build-gtk2 build-gtk3

pushd build-gtk2
%configure --disable-scrollkeeper --enable-gtk-doc --enable-introspection \
           --with-gtk=2 --disable-static
make %{?_smp_mflags}
popd

pushd build-gtk3
%configure --disable-scrollkeeper --enable-gtk-doc --enable-introspection \
           --with-gtk=3 --disable-static
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
find $RPM_BUILD_ROOT -name '*.la' -delete

# Put documentation in correct directory
install -dm755 $RPM_BUILD_ROOT%{_docdir}/%{name}-tools-%{version}/
mv $RPM_BUILD_ROOT%{_docdir}/%{name}/README.dbusmenu-bench \
               $RPM_BUILD_ROOT%{_docdir}/%{name}-tools-%{version}/

# Put examples in correct documentation directory
install -dm755 $RPM_BUILD_ROOT%{_docdir}/%{name}-glib-devel-%{version}/examples/
mv $RPM_BUILD_ROOT%{_docdir}/%{name}/examples/glib-server-nomenu.c \
               $RPM_BUILD_ROOT%{_docdir}/%{name}-glib-devel-%{version}/examples/

# Remove empty directories
#find $RPM_BUILD_ROOT/ -type d -empty -delete


%post glib -p /sbin/ldconfig

%postun glib -p /sbin/ldconfig


%post gtk2 -p /sbin/ldconfig

%postun gtk2 -p /sbin/ldconfig


%post gtk3 -p /sbin/ldconfig

%postun gtk3 -p /sbin/ldconfig


%post jsonloader -p /sbin/ldconfig

%postun jsonloader -p /sbin/ldconfig


%files tools
%doc AUTHORS README
%{_libexecdir}/dbusmenu-bench
%{_libexecdir}/dbusmenu-dumper
%{_libexecdir}/dbusmenu-testapp
%dir %{_datadir}/%{name}/
%dir %{_datadir}/%{name}/json/
%{_datadir}/%{name}/json/test-gtk-label.json
%doc %dir %{_docdir}/%{name}-tools-%{version}/
%doc %{_docdir}/%{name}-tools-%{version}/README.dbusmenu-bench


%files glib
%doc AUTHORS README
%{_libdir}/libdbusmenu-glib.so.*
%{_libdir}/girepository-1.0/Dbusmenu-0.4.typelib


%files glib-devel
%doc AUTHORS README
%dir %{_includedir}/libdbusmenu-glib-0.4/
%dir %{_includedir}/libdbusmenu-glib-0.4/libdbusmenu-glib/
%{_includedir}/libdbusmenu-glib-0.4/libdbusmenu-glib/client.h
%{_includedir}/libdbusmenu-glib-0.4/libdbusmenu-glib/dbusmenu-glib.h
%{_includedir}/libdbusmenu-glib-0.4/libdbusmenu-glib/enum-types.h
%{_includedir}/libdbusmenu-glib-0.4/libdbusmenu-glib/menuitem-proxy.h
%{_includedir}/libdbusmenu-glib-0.4/libdbusmenu-glib/menuitem.h
%{_includedir}/libdbusmenu-glib-0.4/libdbusmenu-glib/server.h
%{_includedir}/libdbusmenu-glib-0.4/libdbusmenu-glib/types.h
%{_libdir}/pkgconfig/dbusmenu-glib-0.4.pc
%{_libdir}/libdbusmenu-glib.so
%{_datadir}/gir-1.0/Dbusmenu-0.4.gir
%{_datadir}/vala/vapi/Dbusmenu-0.4.vapi
%doc %dir %{_docdir}/%{name}-glib-devel-%{version}/
%doc %dir %{_docdir}/%{name}-glib-devel-%{version}/examples/
%doc %{_docdir}/%{name}-glib-devel-%{version}/examples/glib-server-nomenu.c


%files glib-docs
%doc %{_datadir}/gtk-doc/html/libdbusmenu-glib/


%files gtk2
%doc AUTHORS README
%{_libdir}/libdbusmenu-gtk.so.*
%{_libdir}/girepository-1.0/DbusmenuGtk-0.4.typelib


%files gtk2-devel
%doc AUTHORS README
%dir %{_includedir}/libdbusmenu-gtk-0.4/
%dir %{_includedir}/libdbusmenu-gtk-0.4/libdbusmenu-gtk/
%{_includedir}/libdbusmenu-gtk-0.4/libdbusmenu-gtk/client.h
%{_includedir}/libdbusmenu-gtk-0.4/libdbusmenu-gtk/dbusmenu-gtk.h
%{_includedir}/libdbusmenu-gtk-0.4/libdbusmenu-gtk/menu.h
%{_includedir}/libdbusmenu-gtk-0.4/libdbusmenu-gtk/menuitem.h
%{_includedir}/libdbusmenu-gtk-0.4/libdbusmenu-gtk/parser.h
%{_libdir}/pkgconfig/dbusmenu-gtk-0.4.pc
%{_libdir}/libdbusmenu-gtk.so
%{_datadir}/gir-1.0/DbusmenuGtk-0.4.gir
%{_datadir}/vala/vapi/DbusmenuGtk-0.4.vapi


%files gtk3
%doc AUTHORS README
%{_libdir}/libdbusmenu-gtk3.so.*
%{_libdir}/girepository-1.0/DbusmenuGtk3-0.4.typelib


%files gtk3-devel
%doc AUTHORS README
%dir %{_includedir}/libdbusmenu-gtk3-0.4/
%dir %{_includedir}/libdbusmenu-gtk3-0.4/libdbusmenu-gtk/
%{_includedir}/libdbusmenu-gtk3-0.4/libdbusmenu-gtk/client.h
%{_includedir}/libdbusmenu-gtk3-0.4/libdbusmenu-gtk/dbusmenu-gtk.h
%{_includedir}/libdbusmenu-gtk3-0.4/libdbusmenu-gtk/menu.h
%{_includedir}/libdbusmenu-gtk3-0.4/libdbusmenu-gtk/menuitem.h
%{_includedir}/libdbusmenu-gtk3-0.4/libdbusmenu-gtk/parser.h
%{_libdir}/pkgconfig/dbusmenu-gtk3-0.4.pc
%{_libdir}/libdbusmenu-gtk3.so
%{_datadir}/gir-1.0/DbusmenuGtk3-0.4.gir
%{_datadir}/vala/vapi/DbusmenuGtk3-0.4.vapi


%files gtk-docs
%doc %{_datadir}/gtk-doc/html/libdbusmenu-gtk/


%files jsonloader
%doc AUTHORS README
%{_libdir}/libdbusmenu-jsonloader.so.*


%files jsonloader-devel
%doc AUTHORS README
%dir %{_includedir}/libdbusmenu-glib-0.4/
%dir %{_includedir}/libdbusmenu-glib-0.4/libdbusmenu-jsonloader/
%{_includedir}/libdbusmenu-glib-0.4/libdbusmenu-jsonloader/json-loader.h
%{_libdir}/pkgconfig/dbusmenu-jsonloader-0.4.pc
%{_libdir}/libdbusmenu-jsonloader.so


%changelog
* Sat Oct 06 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 12.10.2-1
- Version 12.10.2

* Thu Sep 20 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 12.10.1-1
- Version 12.10.1

* Fri Aug 17 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.6.2-2
- Clean up spec file
- Fix directory ownership

* Fri Jun 29 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.6.2-1
- Update to version 0.6.2
- Disable static libraries

* Mon Jun 04 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.6.1-1.0ubuntu3
- Initial release
- Version 0.6.1
- Ubuntu release 0ubuntu3
