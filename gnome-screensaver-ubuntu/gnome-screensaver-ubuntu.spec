# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

# Based off of the Fedora 17 spec file

%define _ubuntu_rel 0ubuntu1
%define _obsolete_ver 3.5.0-100

Name:		gnome-screensaver-ubuntu
Version:	3.4.1
Release:	1.%{_ubuntu_rel}%{?dist}
Summary:	GNOME Screensaver

Group:		Amusements/Graphics
License:	GPLv2+
URL:		http://www.gnome.org
Source0:	http://download.gnome.org/sources/gnome-screensaver/3.4/gnome-screensaver-%{version}.tar.xz

Source99:	https://launchpad.net/ubuntu/+archive/primary/+files/gnome-screensaver_%{version}-%{_ubuntu_rel}.debian.tar.gz

Patch0:		gnome-screensaver-2.20.0-selinux-permit.patch

BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	desktop-file-utils
BuildRequires:	gettext
BuildRequires:	gnome-common
BuildRequires:	intltool
BuildRequires:	libtool

BuildRequires:	dbus-devel
BuildRequires:	dbus-glib-devel
BuildRequires:	gnome-desktop3-devel
BuildRequires:	gsettings-desktop-schemas
BuildRequires:	gtk3-devel
BuildRequires:	libgnomekbd-devel
BuildRequires:	libX11-devel
BuildRequires:	libXext-devel
BuildRequires:	libXinerama-devel
BuildRequires:	libXmu-devel
BuildRequires:	libXScrnSaver-devel
BuildRequires:	libXtst-devel
BuildRequires:	libXxf86misc-devel
BuildRequires:	libXxf86vm-devel
BuildRequires:	nss-devel
BuildRequires:	pam-devel
BuildRequires:	systemd-devel
BuildRequires:	xorg-x11-proto-devel

# Not used, but required to build
BuildRequires:	libxklavier-devel

Requires:	gnome-keyring-pam
Requires:	redhat-menus

# Replace official version
Provides:	gnome-screensaver%{?_isa} = %{version}-%{release}
Provides:	gnome-screensaver         = %{version}-%{release}
Obsoletes:	gnome-screensaver%{?_isa} < %{_obsolete_ver}
Obsoletes:	gnome-screensaver         < %{_obsolete_ver}

%description
gnome-screensaver is a screen saver and locker that aims to have simple, sane,
secure defaults and be well integrated with the desktop.


%prep
%setup -q -n gnome-screensaver-%{version}

%patch0 -p1 -b .selinux-permit

# Apply Ubuntu's patches
tar zxvf '%{SOURCE99}'
for i in $(grep -v '#' debian/patches/series); do
  patch -Np1 -i "debian/patches/${i}"
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
* Mon Jul 30 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.4.1-1.0ubuntu1
- Initial release
- Based off of Fedora 17's spec file
- Version 3.4.1
- Ubuntu release 0ubuntu1
