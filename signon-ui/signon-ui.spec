# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

Name:		signon-ui
Version:	0.11
Release:	1%{?dist}
Summary:	Single Sign On UI

Group:		User Interface/Desktops
License:	GPLv3
URL:		https://launchpad.net/online-accounts-signon-ui
Source0:	https://launchpad.net/online-accounts-signon-ui/trunk/%{version}/+download/signon-ui-%{version}.tar.bz2

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

# Disable tests for now. They fail to build properly.
sed -i '/tests/d' signon-ui.pro


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
%{_datadir}/dbus-1/services/com.canonical.indicators.webcredentials.service
%{_datadir}/dbus-1/services/com.nokia.singlesignonui.service


%changelog
* Thu Sep 27 2012 Xiao-Long chen <chenxiaolong@cxl.epac.to> - 0.11-1
- Initial release
- Version 0.11
