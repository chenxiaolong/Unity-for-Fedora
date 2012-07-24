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
BuildRequires:	gcc-c++

BuildRequires:	dbusmenu-qt-devel
BuildRequires:	qt-devel

%if 0%{?opensuse_bs}
# Satisfy OBS conflict on xorg-x11-proto-devel
BuildRequires:	xorg-x11-proto-devel

# Satisfy OBS conflict on libXfixes
BuildRequires:	libXfixes
BuildRequires:	libXfixes-devel
%endif

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
cd build
make install DESTDIR=$RPM_BUILD_ROOT


%files
%doc NEWS README
%dir %{_libdir}/qt4/plugins/menubar/
%{_libdir}/qt4/plugins/menubar/libappmenu-qt.so


%changelog
* Mon Jul 23 2012 Damian Ivanov <damianatorrpm@gmail.com> - 0.2.6-2
- Spec file fixes for https://bugzilla.redhat.com/show_bug.cgi?id=842124

* Thu Jun 28 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.2.6-1
- Initial release
- Version 0.2.6
