# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

%define _ubuntu_rel 5

Name:		libindicate-qt
Version:	0.2.5.91
Release:	1%{?dist}
Summary:	Qt bindings for libindicate

Group:		System Environment/Libraries
License:	LGPLv2 and LGPLv3
URL:		https://launchpad.net/libindicate-qt
Source0:	https://launchpad.net/ubuntu/+archive/primary/+files/libindicate-qt_%{version}.orig.tar.gz

Patch0:		0001_fix_pkgconfig_libindicate_version.patch
# Ubuntu patch to build with -fvisiblity=hidden
Patch1:		0002_build_with_fvisibility_hidden.patch

BuildRequires:	cmake

BuildRequires:	pkgconfig(indicate-0.7) >= 0.6.90
BuildRequires:	pkgconfig(QtCore)

%description
This project provides a set of Qt bindings for libindicate, the indicator system
developed by Canonical Desktop Experience team.


%package devel
Summary:	Development files for libindicate-qt
Group:		Development/Libraries

Requires:	%{name} = %{version}-%{release}

%description devel
This package contains the development files for the indicate-qt library.


%prep
%setup -q
%patch0 -p1 -b .pkgconfig
%patch1 -p1 -b .fvisibility


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
%doc NEWS README
%{_libdir}/libindicate-qt.so.1
%{_libdir}/libindicate-qt.so.1.4.1


%files devel
%dir %{_includedir}/libindicate-qt/
%{_includedir}/libindicate-qt/*.h
%{_libdir}/libindicate-qt.so
%{_libdir}/pkgconfig/indicate-qt.pc


%changelog
* Sat Aug 18 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.2.5.91-2
- Clean up spec file
- Fix directory ownership
- Use pkgconfig for dependencies
- Remove gcc-c++ dependency

* Wed Jun 27 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.2.5.91-1
- Initial release
- Version 0.2.5.91
