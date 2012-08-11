# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

# Fedora's naming is kde-plasma + widget name

Name:		kde-plasma-menubar
Version:	0.1.18
Release:	1%{?dist}
Summary:	A plasma widget to display a global menubar

Group:		User Interface/Desktops
License:	GPLv3
URL:		https://launchpad.net/plasma-widget-menubar
Source0:	https://launchpad.net/plasma-widget-menubar/trunk/%{version}/+download/plasma-widget-menubar-%{version}.tar.bz2

BuildRequires:	cmake
BuildRequires:	gcc-c++
BuildRequires:	pkgconfig

BuildRequires:	pkgconfig(dbusmenu-qt)
BuildRequires:	kdelibs-devel
BuildRequires:	pkgconfig(QJson)
BuildRequires:	pkgconfig(x11)

Requires:	appmenu-qt

%description
This package contains a KDE plasma applet for displaying a global menubar.


%prep
%setup -q -n plasma-widget-menubar-%{version}


%build
mkdir build
cd build
%cmake ..
make %{?_smp_mflags}


%install
cd build
make install DESTDIR=$RPM_BUILD_ROOT


%files
%doc NEWS
%dir %{_libdir}/kde4/
%{_libdir}/kde4/plasma_applet_menubar.so
%dir %{_datadir}/kde4/
%dir %{_datadir}/kde4/services/
%{_datadir}/kde4/services/plasma-applet-menubar.desktop


%changelog
* Sat Aug 11 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.1.18-1
- Initial release
- Version 0.1.18
