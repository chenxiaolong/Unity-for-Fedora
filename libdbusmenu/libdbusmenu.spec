# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

Name:		libdbusmenu
Version:	0.6.2
Release:	1%{?dist}
Summary:	Small library that passes a menu structure across DBus

Group:		System Environment/Libraries
License:	GPLv3 and LGPLv2 and LGPLv3
URL:		https://launchpad.net/dbusmenu
Source0:	https://launchpad.net/dbusmenu/0.6/%{version}/+download/libdbusmenu-%{version}.tar.gz

# Require Ubuntu versions of GTK2 and GTK3
#BuildRequires:	gtk2-devel >= 1:
#BuildRequires:	gtk3-devel >= 1:
BuildRequires:	gtk2-devel
BuildRequires:	gtk3-devel

BuildRequires:	atk-devel
BuildRequires:	dbus-glib-devel
BuildRequires:	gdk-pixbuf2-devel
BuildRequires:	gnome-doc-utils
BuildRequires:	gobject-introspection-devel
BuildRequires:	gtk-doc
BuildRequires:	intltool
BuildRequires:	json-glib-devel
BuildRequires:	libtool
BuildRequires:	libX11-devel
BuildRequires:	vala-tools
BuildRequires:	valgrind-devel

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
This packages contains development tools for the dbusmenu libraries


%package glib
Summary:	Small library that passes a menu structure across DBus
Group:		System Environment/Libraries

%description glib
This package contains the shared libraries for dbusmenu-glib


%package glib-devel
Summary:	Development files for libdbusmenu-glib
Group:		Development/Libraries

Requires:	%{name}-glib = %{version}-%{release}
Requires:	dbus-glib-devel
# gtk2 with Ubuntu patches
#Requires:	gtk2 >= 1:
Requires:	gtk2

%description glib-devel
This package contains the development files for the dbusmenu-glib library


%package glib-docs
Summary:	Documentation for libdbusmenu-glib
Group:		Documentation

BuildArch:	noarch

%description glib-docs
This package includes the documentation for the dbusmenu-glib library


%package gtk2
Summary:	Small library that passes a menu structure across DBus - GTK2 version
Group:		System Environment/Libraries

%description gtk2
This package contains the shared libraries for dbusmenu-gtk2


%package gtk2-devel
Summary:	Development files for libdbusmenu-gtk2
Group:		Development/Libraries

Requires:	%{name}-gtk2 = %{version}-%{release}
Requires:	%{name}-glib-devel = %{version}-%{release}
# gtk2 with Ubuntu patches
#Requires:	gtk2-devel >= 1:
Requires:	gtk2-devel
Requires:	dbus-glib-devel

%description gtk2-devel
This package contains the development files for the dbusmenu-gtk2 library


%package gtk3
Summary:	Small library that passes a menu structure across DBus - GTK3 version
Group:		System Environment/Libraries

%description gtk3
This package contains the shared libraries for dbusmenu-gtk3


%package gtk3-devel
Summary:	Development files for libdbusmenu-gtk3
Group:		Development/Libraries

Requires:	%{name}-gtk3 = %{version}-%{release}
Requires:	%{name}-glib-devel = %{version}-%{release}
# gtk3 with Ubuntu patches
#Requires:	gtk3-devel >= 1:
Requires:	gtk3-devel
Requires:	dbus-glib-devel

%description gtk3-devel
This package contains the development files for the dbusmenu-gtk3 library


%package gtk-docs
Summary:	Documentation for libdbusmenu-gtk2 and libdbusmenu-gtk3
Group:		Documentation

BuildArch:	noarch

%description gtk-docs
This package contains the documentation for the dbusmenu-gtk2 and dbusmenu-gtk3
libraries


%package jsonloader
Summary:	Small library that passes a menu structure across DBus - Test library
Group:		System Environment/Libraries

%description jsonloader
This package contains the shared libraries for dbusmenu-jsonloader, a library
meant for test suites


%package jsonloader-devel
Summary:	Development files for libdbusmenu-jsonloader
Group:		Development/Libraries

Requires:	%{name}-jsonloader = %{version}-%{release}
Requires:	%{name}-glib-devel = %{version}-%{release}
Requires:	dbus-glib-devel
Requires:	json-glib-devel

%description jsonloader-devel
This package contains the development files for the dbusmenu-jsonloader library


%prep
%setup -q -c -T
tar zxvf "%{SOURCE0}"
mv %{name}-%{version} gtk2
tar zxvf "%{SOURCE0}"
mv %{name}-%{version} gtk3

# Apply Ubuntu patches
for i in gtk2 gtk3; do
  pushd ${i}

  autoreconf -vfi

  # Disable rpath (from Debian wiki)
  sed -i -r 's/(hardcode_into_libs)=.*$/\1=no/' configure

  popd
done


%build
pushd gtk2
%configure --disable-scrollkeeper --enable-gtk-doc --enable-introspection \
           --with-gtk=2 --disable-static
make %{?_smp_mflags}
popd

pushd gtk3
%configure --disable-scrollkeeper --enable-gtk-doc --enable-introspection \
           --with-gtk=3 --disable-static
make %{?_smp_mflags}
popd


%install
rm -rf $RPM_BUILD_ROOT

pushd gtk2
make install DESTDIR=$RPM_BUILD_ROOT
popd

pushd gtk3
make install DESTDIR=$RPM_BUILD_ROOT
popd

find $RPM_BUILD_ROOT -name '*.la' -delete

# Put documentation in correct directory
install -dm755 $RPM_BUILD_ROOT%{_docdir}/%{name}-tools-%{version}/
mv $RPM_BUILD_ROOT%{_docdir}/%{name}/README.dbusmenu-bench \
               $RPM_BUILD_ROOT%{_docdir}/%{name}-tools-%{version}/

# Put example in correct documentation directory
install -dm755 $RPM_BUILD_ROOT%{_docdir}/%{name}-glib-devel-%{version}/examples/
mv $RPM_BUILD_ROOT%{_docdir}/%{name}/examples/glib-server-nomenu.c \
               $RPM_BUILD_ROOT%{_docdir}/%{name}-glib-devel-%{version}/examples/

# Remove empty directories
#find $RPM_BUILD_ROOT/ -type d -empty -delete


%post glib -p /usr/sbin/ldconfig

%postun glib -p /usr/sbin/ldconfig


%post gtk2 -p /usr/sbin/ldconfig

%postun gtk2 -p /usr/sbin/ldconfig


%post gtk3 -p /usr/sbin/ldconfig

%postun gtk3 -p /usr/sbin/ldconfig


%post jsonloader -p /usr/sbin/ldconfig

%postun jsonloader -p /usr/sbin/ldconfig


%files tools
%doc gtk3/AUTHORS gtk3/README
%{_libexecdir}/dbusmenu-bench
%{_libexecdir}/dbusmenu-dumper
%{_libexecdir}/dbusmenu-testapp
%{_datadir}/%{name}/json/test-gtk-label.json
%{_docdir}/%{name}-tools-%{version}/README.dbusmenu-bench


%files glib
%{_libdir}/libdbusmenu-glib.so.4
%{_libdir}/libdbusmenu-glib.so.4.0.13
%{_libdir}/girepository-1.0/Dbusmenu-0.4.typelib


%files glib-devel
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
%{_docdir}/%{name}-glib-devel-%{version}/examples/glib-server-nomenu.c


%files glib-docs
%{_datadir}/gtk-doc/html/libdbusmenu-glib/annotation-glossary.html
%{_datadir}/gtk-doc/html/libdbusmenu-glib/api-index-deprecated.html
%{_datadir}/gtk-doc/html/libdbusmenu-glib/api-index-full.html
%{_datadir}/gtk-doc/html/libdbusmenu-glib/ch01.html
%{_datadir}/gtk-doc/html/libdbusmenu-glib/home.png
%{_datadir}/gtk-doc/html/libdbusmenu-glib/index.html
%{_datadir}/gtk-doc/html/libdbusmenu-glib/index.sgml
%{_datadir}/gtk-doc/html/libdbusmenu-glib/left.png
%{_datadir}/gtk-doc/html/libdbusmenu-glib/libdbusmenu-glib-DbusmenuClient.html
%{_datadir}/gtk-doc/html/libdbusmenu-glib/libdbusmenu-glib-DbusmenuMenuitem.html
%{_datadir}/gtk-doc/html/libdbusmenu-glib/libdbusmenu-glib-DbusmenuMenuitemProxy.html
%{_datadir}/gtk-doc/html/libdbusmenu-glib/libdbusmenu-glib-DbusmenuServer.html
%{_datadir}/gtk-doc/html/libdbusmenu-glib/libdbusmenu-glib-Types.html
%{_datadir}/gtk-doc/html/libdbusmenu-glib/libdbusmenu-glib.devhelp2
%{_datadir}/gtk-doc/html/libdbusmenu-glib/object-tree.html
%{_datadir}/gtk-doc/html/libdbusmenu-glib/right.png
%{_datadir}/gtk-doc/html/libdbusmenu-glib/style.css
%{_datadir}/gtk-doc/html/libdbusmenu-glib/up.png


%files gtk2
%{_libdir}/libdbusmenu-gtk.so.4
%{_libdir}/libdbusmenu-gtk.so.4.0.13
%{_libdir}/girepository-1.0/DbusmenuGtk-0.4.typelib


%files gtk2-devel
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
%{_libdir}/libdbusmenu-gtk3.so.4
%{_libdir}/libdbusmenu-gtk3.so.4.0.13
%{_libdir}/girepository-1.0/DbusmenuGtk3-0.4.typelib


%files gtk3-devel
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
%{_datadir}/gtk-doc/html/libdbusmenu-gtk/annotation-glossary.html
%{_datadir}/gtk-doc/html/libdbusmenu-gtk/api-index-deprecated.html
%{_datadir}/gtk-doc/html/libdbusmenu-gtk/api-index-full.html
%{_datadir}/gtk-doc/html/libdbusmenu-gtk/ch01.html
%{_datadir}/gtk-doc/html/libdbusmenu-gtk/home.png
%{_datadir}/gtk-doc/html/libdbusmenu-gtk/index.html
%{_datadir}/gtk-doc/html/libdbusmenu-gtk/index.sgml
%{_datadir}/gtk-doc/html/libdbusmenu-gtk/left.png
%{_datadir}/gtk-doc/html/libdbusmenu-gtk/libdbusmenu-gtk-DbusmenuGtkClient.html
%{_datadir}/gtk-doc/html/libdbusmenu-gtk/libdbusmenu-gtk-DbusmenuGtkMenu.html
%{_datadir}/gtk-doc/html/libdbusmenu-gtk/libdbusmenu-gtk-menuitem.html
%{_datadir}/gtk-doc/html/libdbusmenu-gtk/libdbusmenu-gtk-parser.html
%{_datadir}/gtk-doc/html/libdbusmenu-gtk/libdbusmenu-gtk.devhelp2
%{_datadir}/gtk-doc/html/libdbusmenu-gtk/object-tree.html
%{_datadir}/gtk-doc/html/libdbusmenu-gtk/right.png
%{_datadir}/gtk-doc/html/libdbusmenu-gtk/style.css
%{_datadir}/gtk-doc/html/libdbusmenu-gtk/up.png


%files jsonloader
%{_libdir}/libdbusmenu-jsonloader.so.4
%{_libdir}/libdbusmenu-jsonloader.so.4.0.13


%files jsonloader-devel
%{_includedir}/libdbusmenu-glib-0.4/libdbusmenu-jsonloader/json-loader.h
%{_libdir}/pkgconfig/dbusmenu-jsonloader-0.4.pc
%{_libdir}/libdbusmenu-jsonloader.so


%changelog
* Fri Jun 29 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.6.2-1
- Update to version 0.6.2
- Disable static libraries

* Mon Jun 04 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.6.1-1.0ubuntu3
- Initial release
- Version 0.6.1
- Ubuntu release 0ubuntu3
