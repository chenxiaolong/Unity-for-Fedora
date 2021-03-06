# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

# Based off of the Fedora 18 spec file

%define _translations 20130418

%define _ubuntu_rel 0ubuntu3

Name:		gnome-screensaver
Version:	3.6.1
Release:	100.%{_ubuntu_rel}%{?dist}
Summary:	GNOME Screensaver

Group:		Amusements/Graphics
License:	GPLv2+
URL:		http://www.gnome.org
Source0:	http://download.gnome.org/sources/gnome-screensaver/3.6/gnome-screensaver-%{version}.tar.xz

Source98:	https://dl.dropboxusercontent.com/u/486665/Translations/translations-%{_translations}-gnome-screensaver.tar.gz
Source99:	https://launchpad.net/ubuntu/+archive/primary/+files/gnome-screensaver_%{version}-%{_ubuntu_rel}.debian.tar.gz

Patch0:		gnome-screensaver-2.20.0-selinux-permit.patch

BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	desktop-file-utils
BuildRequires:	gettext
BuildRequires:	gnome-common
BuildRequires:	intltool
BuildRequires:	libtool
BuildRequires:	pkgconfig

BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(gnome-desktop-3.0)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(libgnomekbdui)
BuildRequires:	pkgconfig(libsystemd-daemon)
BuildRequires:	pkgconfig(libsystemd-login)
BuildRequires:	pkgconfig(nss)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xinerama)
BuildRequires:	pkgconfig(xmu)
BuildRequires:	pkgconfig(xscrnsaver)
BuildRequires:	pkgconfig(xtst)
BuildRequires:	pkgconfig(xxf86misc)
BuildRequires:	pkgconfig(xxf86vm)

BuildRequires:	pam-devel
BuildRequires:	xorg-x11-proto-devel

# Not used, but required to build
BuildRequires:	pkgconfig(libxklavier)

Requires:	gnome-keyring-pam
Requires:	redhat-menus

Provides:	gnome-screensaver-ubuntu = %{version}-%{release}

%description
gnome-screensaver is a screen saver and locker that aims to have simple, sane,
secure defaults and be well integrated with the desktop.


%prep
%setup -q -n gnome-screensaver-%{version}

%patch0 -p1 -b .selinux-permit

# Apply Ubuntu's patches
tar zxvf '%{SOURCE99}'
for i in $(grep -v '#' debian/patches/series); do
  patch -p1 -i "debian/patches/${i}"
done

mkdir po_new
tar zxvf '%{SOURCE98}' -C po_new
rm -f po/LINGUAS po/*.pot
mv po_new/po/*.pot po/
for i in po_new/po/*.po; do
  FILE=$(sed -n "s|.*/%{name}-||p" <<< ${i})
  mv ${i} po/${FILE}
  echo ${FILE%.*} >> po/LINGUAS
done

autoreconf -vfi


%build
%configure --with-mit-ext=no --enable-systemd
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT

%find_lang gnome-screensaver


%files -f gnome-screensaver.lang
%doc AUTHORS NEWS README
%{_bindir}/gnome-screensaver
%{_bindir}/gnome-screensaver-command
%{_libexecdir}/gnome-screensaver-dialog
%{_sysconfdir}/pam.d/gnome-screensaver
%{_sysconfdir}/xdg/autostart/gnome-screensaver.desktop
%{_datadir}/dbus-1/services/org.gnome.ScreenSaver.service
%{_mandir}/man1/gnome-screensaver-command.1.gz
%{_mandir}/man1/gnome-screensaver.1.gz


%changelog
* Fri May 03 2013 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.6.1-100.0ubuntu3
- Version 3.6.1
- Ubuntu release 0ubuntu3

* Mon Jan 28 2013 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.6.1-100.0ubuntu2
- Version 3.6.1
- Ubuntu release 0ubuntu2

* Sun Nov 18 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.6.1-101.0ubuntu1
- Version 3.6.1
- Ubuntu release 0ubuntu1

* Mon Oct 29 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.6.1-100.ubuntu3.6.0.0ubuntu2
- Ubuntu release 0ubuntu2

* Sat Oct 20 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.6.1-100.ubuntu3.6.0.0ubuntu1
- Version 3.6.1

* Fri Sep 28 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.6.0-1.0ubuntu1
- Version 3.6.0
- Ubuntu release 0ubuntu1

* Sun Sep 23 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.5.5-1.0ubuntu1
- Initial release for Fedora 18
- Version 3.5.5
- Ubuntu release 0ubuntu1

* Mon Jul 30 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.4.1-1.0ubuntu1
- Initial release
- Based off of Fedora 17's spec file
- Version 3.4.1
- Ubuntu release 0ubuntu1
