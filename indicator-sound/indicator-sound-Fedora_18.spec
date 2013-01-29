# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

# Based off of Damian's spec file

Name:		indicator-sound
Version:	12.10.2daily12.11.21.1
Release:	1%{?dist}
Summary:	Indicator for displaying a unified sound menu

Group:		User Interface/Desktops
License:	GPLv3
URL:		https://launchpad.net/indicator-sound
Source0:	https://launchpad.net/ubuntu/+archive/primary/+files/indicator-sound_%{version}.orig.tar.gz

BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	pkgconfig
BuildRequires:	vala-tools

BuildRequires:	pkgconfig(dbusmenu-glib-0.4)
BuildRequires:	pkgconfig(dbusmenu-gtk3-0.4)
BuildRequires:	pkgconfig(gee-1.0)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(indicator3-0.4)
BuildRequires:	pkgconfig(libido3-0.1)
BuildRequires:	pkgconfig(libnotify)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(libpulse)

# Ubuntu's gnome-control-center is required
Requires:	control-center-ubuntu

%description
A system sound indicator which provides easy control of the PulseAudio sound
daemon. The sound menu also provides integration with several multimedia
players (ex: Banshee).


%prep
%setup -q

autoreconf -vfi
intltoolize -f


%build
%configure --disable-static
#make %{?_smp_mflags}
make -j1


%install
make install DESTDIR=$RPM_BUILD_ROOT

# Remove libtool files
find $RPM_BUILD_ROOT -type f -name '*.la' -delete


%postun
if [ ${1} -eq 0 ]; then
  glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :
fi

%posttrans
glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :


%files
%doc AUTHORS
%dir %{_libdir}/indicators3/
%dir %{_libdir}/indicators3/7/
%{_libdir}/indicators3/7/libsoundmenu.so
%{_libexecdir}/indicator-sound-service
%{_datadir}/dbus-1/services/indicator-sound.service
%{_datadir}/glib-2.0/schemas/com.canonical.indicator.sound.gschema.xml
%dir %{_datadir}/libindicator/
%{_datadir}/libindicator/icons/


%changelog
* Mon Nov 26 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 12.10.2daily12.11.21.1-1
- Version 12.10.2
- Ubuntu daily build from 2012-11-21

* Sat Oct 04 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 12.10.1-1.0ubuntu1
- Version 12.10.1
- Ubuntu release 0ubuntu1

* Sun Sep 23 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 12.10.0-3.0ubuntu2
- Drop GTK 2 build and ido doesn't provide a GTK 2 anymore

* Mon Aug 27 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 12.10.0-2.0ubuntu2
- Version 12.10.0
- Ubuntu release 0ubuntu2

* Mon Aug 20 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 12.10.0-2.0ubuntu1
- Fix directory ownership

* Mon Aug 13 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 12.10.0-1.0ubuntu1
- Version 12.10.0
- Ubuntu release 0ubuntu1

* Sun Jul 08 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.8.5.0-1.0ubuntu3
- Initial release
- Version 0.8.5.0
- Ubuntu release 0ubuntu3
