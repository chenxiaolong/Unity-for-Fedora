# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

Name:		libqtdee
Version:	0.2.4
Release:	2%{?dist}
Summary:	Qt bindings and QML plugin for dee

Group:		System Environment/Libraries
License:	LGPLv3
URL:		https://launchpad.net/dee-qt
Source0:	https://launchpad.net/ubuntu/+archive/primary/+files/libqtdee_%{version}.orig.tar.gz

Patch0:		0001_Fix_imports_libdir.patch
Patch1:		0002_Fix_pkgconfig_libdir.patch

BuildRequires:	cmake
BuildRequires:	pkgconfig

BuildRequires:	pkgconfig(dee-1.0)
BuildRequires:	pkgconfig(QtCore)

%description
This package provides the Qt 4 bindings for the dee library.


%package devel
Summary:	Development files for libqtdee
Group:		Development/Libraries

Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	qt-devel

%description devel
This package contains the development files for the qtdee library.


%prep
%setup -q

%patch0 -p1 -b .imports
%patch1 -p1 -b .pkgconfig

sed -i 's|/lib|/%{_lib}|g' libqtdee.pc


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
%doc COPYING
%{_libdir}/libQtDee.so.*
%dir %{_libdir}/qt4/imports/dee/
%{_libdir}/qt4/imports/dee/libQtDeeQml.so
%{_libdir}/qt4/imports/dee/qmldir


%files devel
%dir %{_includedir}/QtDee/
%{_includedir}/QtDee/deelistmodel.h
%{_libdir}/libQtDee.so
%{_libdir}/pkgconfig/libqtdee.pc


%changelog
* Fri Aug 18 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.2.4-2
- Fix pkgconfig libdir
- Use pkgconfig for dependencies
- Remove gcc-c++ dependency

* Tue Jul 03 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.2.4-1
- Initial release
- Version 0.2.4
