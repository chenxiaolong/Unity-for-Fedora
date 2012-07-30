# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

%define _ubuntu_rel 0ubuntu4

Name:		dconf-qt
Version:	0.0.0.110722
Release:	1.%{_ubuntu_rel}%{?dist}
Summary:	Qt bindings for DConf

Group:		System Environment/Libraries
License:	LGPLv3
URL:		https://gitorious.org/dconf-qt
Source0:	https://launchpad.net/ubuntu/+archive/primary/+files/dconf-qt_%{version}.orig.tar.bz2

Source99:	https://launchpad.net/ubuntu/+archive/primary/+files/dconf-qt_%{version}-%{_ubuntu_rel}.debian.tar.gz

Patch0:		0001_Fix_libdir.patch

BuildRequires:	cmake
BuildRequires:	gcc-c++

BuildRequires:	dconf-devel
BuildRequires:	glib2-devel
BuildRequires:	qt-devel

%description
This package contains the Qt 4 bindings for the DConf configuration system.


%package devel
Summary:	Development files for dconf-qt
Group:		Development/Libraries

Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	dconf-devel
Requires:	glib2-devel
Requires:	qt-devel

%description devel
This package contains the development files for the dconf-qt library.


%prep
%setup -q -n lib%{name}-0.0.0

# Apply Ubuntu's patches
tar zxvf '%{SOURCE99}'
for i in $(grep -v '#' debian/patches/series); do
  patch -Np1 -i "debian/patches/${i}"
done

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
%{_libdir}/libdconf-qt.so.0
%{_libdir}/libdconf-qt.so.0.0.0
%dir %{_libdir}/qt4/imports/QConf/
%{_libdir}/qt4/imports/QConf/libdconf-qml.so
%{_libdir}/qt4/imports/QConf/qmldir


%files devel
%dir %{_includedir}/dconf-qt/
%{_includedir}/dconf-qt/qconf.h
%{_libdir}/libdconf-qt.so
%{_libdir}/pkgconfig/dconf-qt.pc


%changelog
* Tue Jul 03 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.0.0.110722-1.0ubuntu4
- Initial release
- Version 0.0.0.110722
- Ubuntu release 0ubuntu4
