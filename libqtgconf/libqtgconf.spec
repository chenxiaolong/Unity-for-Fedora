# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

Name:		libqtgconf
Version:	0.1
Release:	1%{?dist}
Summary:	Qt bindings for GConf

Group:		System Environment/Libraries
License:	LGPLv2
URL:		https://launchpad.net/gconf-qt
Source0:	https://launchpad.net/ubuntu/+archive/primary/+files/libqtgconf_%{version}.orig.tar.gz

Patch0:		0001_Fix_libdir.patch

BuildRequires:	cmake
BuildRequires:	gcc-c++

BuildRequires:	GConf2-devel
BuildRequires:	qt-devel

# Satisfy OBS conflict on xorg-x11-proto-devel
BuildRequires:	xorg-x11-proto-devel

# Satisfy OBS conflict on libXfixes
BuildRequires:	libXfixes
BuildRequires:	libXfixes-devel

%description
This package contains the Qt 4 bindings for the GConf configuration system.


%package devel
Summary:	Development files for libqtgconf
Group:		Development/Libraries

Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	qt-devel

%description devel
This package contains the development files for the qtgconf library.


%prep
%setup -q

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
%{_libdir}/libQtGConf.so.1
%{_libdir}/libQtGConf.so.1.0.0
%dir %{_libdir}/qt4/imports/gconf/
%{_libdir}/qt4/imports/gconf/libQtGConfQml.so
%{_libdir}/qt4/imports/gconf/qmldir


%files devel
%dir %{_includedir}/QtGConf/
%{_includedir}/QtGConf/gconfitem-qml-wrapper.h
%{_libdir}/libQtGConf.so
%{_libdir}/pkgconfig/libqtgconf.pc


%changelog
* Tue Jul 03 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.1-1
- Initial release
- Version 0.1
