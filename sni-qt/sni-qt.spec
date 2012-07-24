# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

Name:		sni-qt
Version:	0.2.6
Release:	1%{?dist}
Summary:	Library that turns Qt tray icons into appindicators

Group:		System Environment/Libraries
License:	LGPLv3
URL:		https://launchpad.net/sni-qt
Source0:	https://launchpad.net/sni-qt/trunk/%{version}/+download/sni-qt-%{version}.tar.bz2

# From Ubuntu packaging version 0.2.5-0ubuntu3
Source1:	sni-qt.conf

BuildRequires:	cmake
BuildRequires:	gcc-c++

BuildRequires:	dbusmenu-qt-devel
BuildRequires:	qt-devel

# Satisfy OBS conflict on xorg-x11-proto-devel
BuildRequires:	xorg-x11-proto-devel

# Satisfy OBS conflict on libXfixes
BuildRequires:	libXfixes
BuildRequires:	libXfixes-devel

%description
This package contains a Qt plugin which turns all QSystemTrayIcon into
StatusNotifierItems (appindicators).


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

install -dm755 $RPM_BUILD_ROOT%{_sysconfdir}/xdg/
install -m644 '%{SOURCE1}' $RPM_BUILD_ROOT%{_sysconfdir}/xdg/


%files
%doc NEWS README
%config(noreplace) %{_sysconfdir}/xdg/sni-qt.conf
%dir %{_libdir}/qt4/plugins/systemtrayicon/
%{_libdir}/qt4/plugins/systemtrayicon/libsni-qt.so


%changelog
* Wed Jul 04 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.2.6-1
- Initial release
- Version 0.2.6
