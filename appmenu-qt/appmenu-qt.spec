# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

Name:		appmenu-qt
Version:	0.2.6
Release:	1%{?dist}
Summary:	Application menu support for Qt

Group:		System Environment/Libraries
License:	LGPLv3
URL:		https://launchpad.net/appmenu-qt
Source0:	https://launchpad.net/appmenu-qt/trunk/%{version}/+download/appmenu-qt-%{version}.tar.bz2

BuildRequires:	cmake
BuildRequires:	dbusmenu-qt-devel
BuildRequires:	qt-devel

%description
This package allows Qt to export its menus over DBus.


%prep
%setup -q


%build
mkdir build
cd build
%cmake ..
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
cd build
make install DESTDIR=$RPM_BUILD_ROOT


%files
%doc NEWS README
%{_libdir}/qt4/plugins/menubar/libappmenu-qt.so


%changelog
* Thu Jun 28 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.2.6-1
- Initial release
- Version 0.2.6
