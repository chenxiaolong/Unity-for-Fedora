# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

Name:		libtimezonemap
Version:	0.3.2
Release:	1%{?dist}
Summary:	Timezone map widget for GTK 3

Group:		System Environment/Libraries
License:	GPLv3+
URL:		https://launchpad.net/ubuntu/+source/libtimezonemap
Source0:	https://launchpad.net/ubuntu/+archive/primary/+files/libtimezonemap_%{version}.tar.gz

BuildRequires:	intltool
BuildRequires:	pkgconfig

BuildRequires:	pkgconfig(cairo)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(json-glib-1.0)

Requires:	%{name}-data = %{version}-%{release}

%description
This package contains a timezone map widget for GTK+3.


%package devel
Summary:	Development files for libtimezonemap
Group:		Development/Libraries

Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains the development files for the timezonemap library.


%package data
Summary:	Data files for libtimezonemap
Group:		System Environment/Libraries

BuildArch:	noarch

Requires:	%{name} = %{version}-%{release}

%description data
This package contains the data files needed by the timezonemap library.


%prep
%setup -q -n timezonemap


%build
%configure --disable-static --enable-introspection
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT

# Remove libtool files
find $RPM_BUILD_ROOT -type f -name '*.la' -delete


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc README
%{_libdir}/libtimezonemap.so.*
%{_libdir}/girepository-1.0/TimezoneMap-1.0.typelib


%files devel
%doc README
%dir %{_includedir}/timezonemap/
%dir %{_includedir}/timezonemap/timezonemap/
%{_includedir}/timezonemap/timezonemap/*.h
%{_libdir}/libtimezonemap.so
%{_libdir}/pkgconfig/timezonemap.pc
%{_datadir}/gir-1.0/TimezoneMap-1.0.gir


%files data
%doc README
%dir %{_datadir}/libtimezonemap/
%dir %{_datadir}/libtimezonemap/ui/
%{_datadir}/libtimezonemap/backward
%{_datadir}/libtimezonemap/ui/*.png


%changelog
* Sat Aug 18 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.3.2-2
- Fix directory ownership
- Use pkgconfig for dependencies

* Wed Jul 04 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.3.2-1
- Initial release
- Version 0.3.2
