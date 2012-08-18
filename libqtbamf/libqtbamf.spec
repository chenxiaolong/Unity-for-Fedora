# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

# An older version of this package is in Fedora's repos and they name it
# bamf-qt.
Name:		bamf-qt
Version:	0.2.4
Release:	2%{?dist}
Summary:	Qt bindings for the bamf library

Group:		System Environment/Libraries
License:	LGPLv3
URL:		https://launchpad.net/bamf-qt
Source0:	https://launchpad.net/ubuntu/+archive/primary/+files/libqtbamf_%{version}.orig.tar.gz

Patch0:		0001_Fix_pkgconfig_libdir.patch

BuildRequires:	cmake

BuildRequires:	pkgconfig(QtCore)

# No %{_isa} because the library is multilib, but bamf-daemon is not
Requires:	bamf-daemon

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

sed -i 's|/lib|/%{_lib}|g' libqtbamf.pc


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
%doc COPYING-GPL3 COPYING-LGPL3
%{_libdir}/libQtBamf.so.*
%dir %{_libdir}/qt4/imports/bamf/
%{_libdir}/qt4/imports/bamf/libQtBamfQml.so
%{_libdir}/qt4/imports/bamf/qmldir


%files devel
%dir %{_includedir}/QtBamf/
%{_includedir}/QtBamf/*.h
%{_libdir}/libQtBamf.so
%{_libdir}/pkgconfig/libqtbamf.pc


%changelog
* Sat Aug 18 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.2.4-2
- Remove gcc-c++ dependency
- Use pkgconfig for dependencies
- Fix libdir in pkgconfig file

* Tue Jul 03 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.2.4-1
- Initial release
- Version 0.2.4
