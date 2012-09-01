# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

Name:		bamf
Version:	0.3.0
Release:	1%{?dist}
Summary:	Application Matching Framework - GTK 2

Group:		System Environment/Libraries
License:	LGPLv3
URL:		https://launchpad.net/bamf
Source0:	https://launchpad.net/ubuntu/+archive/primary/+files/bamf_%{version}.orig.tar.gz

BuildRequires:	gtk-doc
BuildRequires:	vala-tools

BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(libgtop-2.0)
BuildRequires:	pkgconfig(libunity_webapps-0.2)
BuildRequires:	pkgconfig(libwnck-1.0)
BuildRequires:	pkgconfig(libwnck-3.0)

# No %{_isa} because the libraries are multilib, but bamf-daemon isn't
Requires:	bamf-daemon = %{version}-%{release}

%description
BAMF removes the headache of applications matching into a simple DBus daemon
and c wrapper library. Currently features application matching at amazing
levels of accuracy (covering nearly every corner case).

This package contains the GTK 2 version of this library.


%package daemon
Summary:	Application Matching Framework - Daemon
Group:		System Environment/Libraries

%description daemon
BAMF removes the headache of applications matching into a simple DBus daemon
and c wrapper library. Currently features application matching at amazing
levels of accuracy (covering nearly every corner case).

This package contains the daemon for the bamf library.


%package devel
Summary:	Development files for libbamf
Group:		Development/Libraries

Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	pkgconfig(glib-2.0)
Requires:	pkgconfig(libwnck-1.0)

%description devel
This package contains the development files for the GTK 2 version of the bamf
library.


%package -n %{name}3
Summary:	Application Matching Library - GTK 3
Group:		System Environment/Libraries

Requires:	bamf-daemon = %{version}-%{release}

%description -n %{name}3
BAMF removes the headache of applications matching into a simple DBus daemon
and c wrapper library. Currently features application matching at amazing
levels of accuracy (covering nearly every corner case).

This package contains the GTK 3 version of this library.


%package -n %{name}3-devel
Summary:	Development files for libbamf3
Group:		Development/Libraries

Requires:	%{name}3%{?_isa} = %{version}-%{release}
Requires:	pkgconfig(glib-2.0)
Requires:	pkgconfig(libwnck-3.0)

%description -n %{name}3-devel
This package contains the development files for the GTK 3 version of the bamf
library.


%package docs
Summary:	Documentation for libbamf and libbamf3
Group:		Documentation

BuildArch:	noarch

%description docs
This package contains the documentation for the bamf library.


%prep
%setup -q


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
pushd build-gtk2
make install DESTDIR=$RPM_BUILD_ROOT
popd

pushd build-gtk3
make install DESTDIR=$RPM_BUILD_ROOT
popd

# Remove libtool files
find $RPM_BUILD_ROOT -type f -name '*.la' -delete

install -dm755 $RPM_BUILD_ROOT%{_datadir}/applications/
touch $RPM_BUILD_ROOT%{_datadir}/applications/bamf.index


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%post -n %{name}3 -p /sbin/ldconfig

%postun -n %{name}3 -p /sbin/ldconfig


%files
%doc TODO
%{_libdir}/libbamf.so.*


%files daemon
%doc TODO
%{_libexecdir}/bamfdaemon
%{_datadir}/dbus-1/services/org.ayatana.bamf.service
%attr(644,root,root) %ghost %{_datadir}/applications/bamf.index


%files devel
%doc TODO
%dir %{_includedir}/libbamf/
%dir %{_includedir}/libbamf/libbamf/
%{_includedir}/libbamf/libbamf/*.h
%{_libdir}/libbamf.so
%{_libdir}/pkgconfig/libbamf.pc
%{_datadir}/vala/vapi/libbamf.vapi


%files -n %{name}3
%doc TODO
%{_libdir}/libbamf3.so.*
%{_libdir}/girepository-1.0/Bamf-0.2.typelib


%files -n %{name}3-devel
%doc TODO
%dir %{_includedir}/libbamf3/
%dir %{_includedir}/libbamf3/libbamf/
%{_includedir}/libbamf3/libbamf/*.h
%{_libdir}/libbamf3.so
%{_libdir}/pkgconfig/libbamf3.pc
%{_datadir}/gir-1.0/Bamf-0.2.gir
%{_datadir}/vala/vapi/libbamf3.vapi


%files docs
%doc %{_datadir}/gtk-doc/html/libbamf/


%changelog
* Sat Sep 01 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.3.0-1
- Version 0.3.0

* Sat Aug 18 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.2.122-2
- Clean up spec file
- Use pkgconfig for dependencies

* Mon Aug 13 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.2.122-1
- Version 0.2.122

* Tue Jul 03 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.2.118-1
- Initial release
- Version 0.2.118
