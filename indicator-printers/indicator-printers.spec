# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

%define _ubuntu_rel 0ubuntu3

Name:		indicator-printers
Version:	0.1.6
Release:	1.%{_ubuntu_rel}%{?dist}
Summary:	Indicator showing active print jobs

Group:		User Interface/Desktops
License:	GPLv3
URL:		https://launchpad.net/indicator-printers
Source0:	https://launchpad.net/indicator-printers/0.1/%{version}/+download/indicator-printers-%{version}.tar.gz

Source99:	https://launchpad.net/ubuntu/+archive/primary/+files/indicator-printers_%{version}-%{_ubuntu_rel}.diff.gz

BuildRequires:	cups-devel

BuildRequires:	pkgconfig(dbusmenu-glib-0.4)
BuildRequires:	pkgconfig(dbusmenu-gtk3-0.4)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(indicator3-0.4)

%description
This package contains an indicator that shows active print jobs in the panel.


%prep
%setup -q

# Apply Ubuntu's patches
cp src/indicator-printers-service.c{,.orig}
zcat '%{SOURCE99}' | patch -Np1
cp src/indicator-printers-service.c{.orig,}


%build
%configure --disable-static
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT

pushd debian/local/
find . -type f -exec install -Dm644 {} $RPM_BUILD_ROOT%{_datadir}/icons/{} \;
popd

# Remove libtool files
find $RPM_BUILD_ROOT -type f -name '*.la' -delete


%files
%doc AUTHORS
%dir %{_libdir}/indicators3/
%dir %{_libdir}/indicators3/7/
%{_libdir}/indicators3/7/libprintersmenu.so
%{_libexecdir}/indicator-printers-service
%{_datadir}/dbus-1/services/indicator-printers.service
%{_datadir}/icons/ubuntu-mono-dark/
%{_datadir}/icons/ubuntu-mono-light/


%changelog
* Thu Sep 27 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.1.6-1.0ubuntu3
- Initial release
- Version 0.1.6
- Ubuntu release 0ubuntu3
