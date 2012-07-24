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

BuildRequires:	cairo-devel
BuildRequires:	glib2-devel
BuildRequires:	gobject-introspection-devel
BuildRequires:	gtk3-devel
BuildRequires:	json-glib-devel

Requires:	%{name}-data = %{version}-%{release}

# Satisfy OBS conflict on xorg-x11-proto-devel
BuildRequires:	xorg-x11-proto-devel

# Satisfy OBS conflict on libXfixes
BuildRequires:	libXfixes
BuildRequires:	libXfixes-devel

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
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# Remove libtool files
find $RPM_BUILD_ROOT -type f -name '*.la' -delete


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc README
%{_libdir}/libtimezonemap.so.1
%{_libdir}/libtimezonemap.so.1.0.0
%{_libdir}/girepository-1.0/TimezoneMap-1.0.typelib


%files devel
%doc README
%dir %{_includedir}/timezonemap/
%{_includedir}/timezonemap/timezonemap/cc-timezone-map.h
%{_includedir}/timezonemap/timezonemap/timezone-completion.h
%{_includedir}/timezonemap/timezonemap/tz.h
%{_libdir}/libtimezonemap.so
%{_libdir}/pkgconfig/timezonemap.pc
%{_datadir}/gir-1.0/TimezoneMap-1.0.gir


%files data
%doc README
%{_datadir}/libtimezonemap/backward
%{_datadir}/libtimezonemap/ui/bg.png
%{_datadir}/libtimezonemap/ui/cc.png
%{_datadir}/libtimezonemap/ui/olsen_map.png
%{_datadir}/libtimezonemap/ui/pin.png
%{_datadir}/libtimezonemap/ui/timezone_-1.png
%{_datadir}/libtimezonemap/ui/timezone_-10.png
%{_datadir}/libtimezonemap/ui/timezone_-11.png
%{_datadir}/libtimezonemap/ui/timezone_-2.png
%{_datadir}/libtimezonemap/ui/timezone_-3.5.png
%{_datadir}/libtimezonemap/ui/timezone_-3.png
%{_datadir}/libtimezonemap/ui/timezone_-4.5.png
%{_datadir}/libtimezonemap/ui/timezone_-4.png
%{_datadir}/libtimezonemap/ui/timezone_-5.5.png
%{_datadir}/libtimezonemap/ui/timezone_-5.png
%{_datadir}/libtimezonemap/ui/timezone_-6.png
%{_datadir}/libtimezonemap/ui/timezone_-7.png
%{_datadir}/libtimezonemap/ui/timezone_-8.png
%{_datadir}/libtimezonemap/ui/timezone_-9.5.png
%{_datadir}/libtimezonemap/ui/timezone_-9.png
%{_datadir}/libtimezonemap/ui/timezone_0.png
%{_datadir}/libtimezonemap/ui/timezone_1.png
%{_datadir}/libtimezonemap/ui/timezone_10.5.png
%{_datadir}/libtimezonemap/ui/timezone_10.png
%{_datadir}/libtimezonemap/ui/timezone_11.5.png
%{_datadir}/libtimezonemap/ui/timezone_11.png
%{_datadir}/libtimezonemap/ui/timezone_12.75.png
%{_datadir}/libtimezonemap/ui/timezone_12.png
%{_datadir}/libtimezonemap/ui/timezone_13.png
%{_datadir}/libtimezonemap/ui/timezone_2.png
%{_datadir}/libtimezonemap/ui/timezone_3.5.png
%{_datadir}/libtimezonemap/ui/timezone_3.png
%{_datadir}/libtimezonemap/ui/timezone_4.5.png
%{_datadir}/libtimezonemap/ui/timezone_4.png
%{_datadir}/libtimezonemap/ui/timezone_5.5.png
%{_datadir}/libtimezonemap/ui/timezone_5.75.png
%{_datadir}/libtimezonemap/ui/timezone_5.png
%{_datadir}/libtimezonemap/ui/timezone_6.5.png
%{_datadir}/libtimezonemap/ui/timezone_6.png
%{_datadir}/libtimezonemap/ui/timezone_7.png
%{_datadir}/libtimezonemap/ui/timezone_8.png
%{_datadir}/libtimezonemap/ui/timezone_9.5.png
%{_datadir}/libtimezonemap/ui/timezone_9.png


%changelog
* Wed Jul 04 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.3.2-1
- Initial release
- Version 0.3.2
