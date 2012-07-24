# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

# An older version of this package is in Fedora's repos and they name it
# bamf-qt.
Name:		bamf-qt
Version:	0.2.4
Release:	1%{?dist}
Summary:	Qt bindings for the bamf library

Group:		System Environment/Libraries
License:	LGPLv3
URL:		https://launchpad.net/bamf-qt
Source0:	https://launchpad.net/ubuntu/+archive/primary/+files/libqtbamf_%{version}.orig.tar.gz

Patch0:		0001_Fix_pkgconfig_libdir.patch

BuildRequires:	cmake
BuildRequires:	gcc-c++

BuildRequires:	qt-devel

# No %{_isa} because the library is multilib, but bamf-daemon is not
Requires:	bamf-daemon

# Satisfy OBS conflict on xorg-x11-proto-devel
BuildRequires:	xorg-x11-proto-devel

# Satisfy OBS conflict on libXfixes-devel
BuildRequires:	libXfixes-devel

# Description from Ubuntu
%description
Qt binding and QML plugin for the bamf dbus daemon semi-automatically
generated with qdbusxml2cpp and matching the GObject library structure.


%package devel
Summary:	Development files for bamf-qt
Group:		Development/Libraries

Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	qt-devel


%description devel
This package contains the development files for the bamf-qt library.


%prep
%setup -q -n libqtbamf-%{version}

%patch0 -p1 -b .libdir


%build
mkdir build
cd build
%cmake ..
make %{?_smp_mflags}


%install
cd build
make install DESTDIR=$RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%{_libdir}/libQtBamf.so.1
%{_libdir}/libQtBamf.so.1.0.0
%{_libdir}/qt4/imports/bamf/libQtBamfQml.so
%{_libdir}/qt4/imports/bamf/qmldir


%files devel
%{_includedir}/QtBamf/bamf-application.h
%{_includedir}/QtBamf/bamf-control.h
%{_includedir}/QtBamf/bamf-factory.h
%{_includedir}/QtBamf/bamf-indicator.h
%{_includedir}/QtBamf/bamf-list.h
%{_includedir}/QtBamf/bamf-matcher.h
%{_includedir}/QtBamf/bamf-view.h
%{_includedir}/QtBamf/bamf-window.h
%{_libdir}/libQtBamf.so
%{_libdir}/pkgconfig/libqtbamf.pc


%changelog
* Tue Jul 03 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.2.4-1
- Initial release
- Version 0.2.4
