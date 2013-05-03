# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

Name:		signon-ui
Version:	0.14
Release:	1%{?dist}
Summary:	Single Sign On UI

Group:		User Interface/Desktops
License:	GPLv3
URL:		https://launchpad.net/online-accounts-signon-ui
Source0:	https://launchpad.net/ubuntu/+archive/primary/+files/signon-ui_%{version}.orig.tar.gz

BuildRequires:	signon-plugins-devel

BuildRequires:	pkgconfig(accounts-qt)
BuildRequires:	pkgconfig(libnotify)
BuildRequires:	pkgconfig(libproxy-1.0)
BuildRequires:	pkgconfig(libsignon-qt)
BuildRequires:	pkgconfig(QtWebKit)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xext)

%description
This package contains the user interface for the signond Single Sign On service.


%prep
%setup -q

# Fix libdir
sed -i 's/\/lib/\/%{_lib}/g' common-installs-config.pri


%build
%_qt4_qmake \
  PREFIX=%{_prefix} \
  LIBDIR=%{_libdir} \
  QMAKE_CXXFLAGS="%{optflags}"

make %{?_smp_mflags}


%install
make install INSTALL_ROOT=$RPM_BUILD_ROOT


%files
%doc COPYING
%{_bindir}/signon-ui
%{_bindir}/signon-ui-unittest
%{_bindir}/tst_inactivity_timer
%{_datadir}/dbus-1/services/com.canonical.indicators.webcredentials.service
%{_datadir}/dbus-1/services/com.nokia.singlesignonui.service


%changelog
* Fri May 03 2013 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.14-1
- Version 0.14

* Sun Jan 27 2013 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.12bzr13.01.09-1
- Version 0.12bzr13.01.09
- Fix libdir path

* Thu Sep 27 2012 Xiao-Long chen <chenxiaolong@cxl.epac.to> - 0.11-1
- Initial release
- Version 0.11
