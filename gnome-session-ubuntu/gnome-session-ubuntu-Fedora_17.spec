# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

# Partially based off of Fedora 17's spec file

%define _ubuntu_rel 0ubuntu1

%define _obsolete_ver 3.5.0-100

Name:		gnome-session-ubuntu
Version:	3.4.2.1
Release:	3.%{_ubuntu_rel}%{?dist}
Summary:	GNOME session manager

Group:		User Interface/Desktops
License:	GPLv2+
URL:		http://www.gnome.org/
Source0:	http://download.gnome.org/sources/gnome-session/3.4/gnome-session-%{version}.tar.xz

Source98:	55gnome-session_gnomerc
Source99:	https://launchpad.net/ubuntu/+archive/primary/+files/gnome-session_%{version}-%{_ubuntu_rel}.debian.tar.gz

Source1:	gnome-authentication-agent.desktop
Source2:	gnome-authentication-agent-unity.desktop

# Fedora's patches
Patch0:		gnome-session-3.3.1-llvmpipe.patch
Patch1:		gnome-session-3.3.92-nv30.patch

BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	desktop-file-utils
BuildRequires:	gettext
BuildRequires:	gnome-common
BuildRequires:	intltool
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	usermode
BuildRequires:	xmlto

BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(gconf-2.0)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(ice)
BuildRequires:	pkgconfig(json-glib-1.0)
BuildRequires:	pkgconfig(libsystemd-daemon)
BuildRequires:	pkgconfig(libsystemd-login)
BuildRequires:	pkgconfig(polkit-gobject-1)
BuildRequires:	pkgconfig(sm)
BuildRequires:	pkgconfig(upower-glib)
BuildRequires:	pkgconfig(xau)
BuildRequires:	pkgconfig(xcomposite)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xrender)
BuildRequires:	pkgconfig(xtst)

Requires:	control-center-filesystem
Requires:	dbus-x11
Requires:	dconf
Requires:	gsettings-desktop-schemas
Requires:	notification-daemon
Requires:	polkit-desktop-policy
Requires:	polkit-gnome
Requires:	system-logos

Provides:	gnome-session%{?_isa} = %{version}-%{release}
Provides:	gnome-session         = %{version}-%{release}
Obsoletes:	gnome-session%{?_isa} < %{_obsolete_ver}
Obsoletes:	gnome-session         < %{_obsolete_ver}

%description
gnome-session manages a GNOME desktop or GDM login session. It starts up the
other core GNOME components and handles logout and saving the session.


%package xsession
Summary:	Desktop files for gnome-session-ubuntu
Group:		User Interface/Desktops

Requires:	%{name}%{?_isa} = %{version}-%{release}

Provides:       gnome-session-xsession%{?_isa} = %{version}-%{release}
Provides:       gnome-session-xsession         = %{version}-%{release}
Obsoletes:      gnome-session-xsession%{?_isa} < %{_obsolete_ver}
Obsoletes:      gnome-session-xsession         < %{_obsolete_ver}

%description xsession
This package contains the X session desktop files needed to add GNOME and Unity
to the display manager menus.


%prep
%setup -q -n gnome-session-%{version}

tar zxvf '%{SOURCE99}'

# Apply Fedora's patches
%patch0 -p1
%patch1 -p1

# Apply Ubuntu's patches
tar zxvf '%{SOURCE99}'

# Disable patches
  # gnome-wm uses Debian's alternatives system (Fedora has it too, but other
  # packages need to use it)
    sed -i '/01_gnome-wm.patch/d' debian/patches/series
  # systemd should make these patches obsolete
    sed -i '/12_no_gdm_fallback.patch/d' debian/patches/series
    sed -i '/21_up_start_on_demand.patch/d' debian/patches/series
  # We're not Ubuntu, do not hide stuff
    sed -i '/20_hide_nodisplay.patch/d' debian/patches/series
  # Only Ubuntu uses apport
    sed -i '/96_no_catch_sigsegv.patch/d' debian/patches/series

# Fix patches
  # Needed because 01_gnome-wm.patch is disabled
    sed -i 's/gnome-wm/metacity/g' debian/patches/50_ubuntu_sessions.patch

for i in $(grep -v '#' debian/patches/series); do
  patch -Np1 -i "debian/patches/${i}"
done

autoreconf -vfi


%build
%configure \
  --enable-docbook-docs \
  --docdir=%{_datadir}/doc/%{name}-%{version} \
  --with-gtk=3.0 \
  --enable-systemd

make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT

install -dm755 $RPM_BUILD_ROOT%{_datadir}/gnome/autostart/
desktop-file-install \
  --dir $RPM_BUILD_ROOT%{_datadir}/gnome/autostart/ \
  %{SOURCE1}
desktop-file-install \
  --dir $RPM_BUILD_ROOT%{_datadir}/gnome/autostart/ \
  %{SOURCE2}

desktop-file-validate \
  $RPM_BUILD_ROOT%{_datadir}/applications/session-properties.desktop

# Install Ubuntu's files
install -m755 debian/scripts/gnome-session-fallback $RPM_BUILD_ROOT%{_bindir}/

install -dm755 $RPM_BUILD_ROOT%{_sysconfdir}/X11/xinit/xinitrc.d/
install -m755 '%{SOURCE98}' $RPM_BUILD_ROOT%{_sysconfdir}/X11/xinit/xinitrc.d/

# /usr/lib/nux -> /usr/libexec
sed -i 's,lib/nux,libexec,' \
  $RPM_BUILD_ROOT%{_datadir}/gnome-session/sessions/ubuntu.session

%find_lang gnome-session-3.0


%post
touch --no-create %{_datadir}/icons/hicolor/ &>/dev/null || :

%postun
if [ ${1} -eq 0 ]; then
  glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :
  touch --no-create %{_datadir}/icons/hicolor/ &>/dev/null || :
  gtk-update-icon-cache -f %{_datadir}/icons/hicolor/ &>/dev/null || :
fi

%posttrans
glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :
gtk-update-icon-cache -f %{_datadir}/icons/hicolor/ &>/dev/null || :


%files -f gnome-session-3.0.lang
%doc AUTHORS ChangeLog NEWS README
%doc %{_datadir}/doc/%{name}-%{version}/dbus/gnome-session.html
%{_bindir}/gnome-session
%{_bindir}/gnome-session-fallback
%{_bindir}/gnome-session-properties
%{_bindir}/gnome-session-quit
%{_libexecdir}/gnome-session-check-accelerated
%{_libexecdir}/gnome-session-check-accelerated-helper
%{_sysconfdir}/X11/xinit/xinitrc.d/55gnome-session_gnomerc
%{_datadir}/GConf/gsettings/gnome-session.convert
%{_datadir}/applications/session-properties.desktop
%{_datadir}/glib-2.0/schemas/org.gnome.SessionManager.gschema.xml
%dir %{_datadir}/gnome/
%dir %{_datadir}/gnome/autostart/
%{_datadir}/gnome/autostart/gnome-authentication-agent.desktop
%{_datadir}/gnome/autostart/gnome-authentication-agent-unity.desktop
%dir %{_datadir}/gnome-session/
%{_datadir}/gnome-session/gsm-inhibit-dialog.ui
%{_datadir}/gnome-session/hardware-compatibility
%{_datadir}/gnome-session/session-properties.ui
%dir %{_datadir}/gnome-session/sessions/
%{_datadir}/gnome-session/sessions/gnome-classic.session
%{_datadir}/gnome-session/sessions/gnome-fallback.session
%{_datadir}/gnome-session/sessions/gnome.session
%{_datadir}/gnome-session/sessions/ubuntu-2d.session
%{_datadir}/gnome-session/sessions/ubuntu.session
%{_datadir}/icons/hicolor/16x16/apps/session-properties.png
%{_datadir}/icons/hicolor/22x22/apps/session-properties.png
%{_datadir}/icons/hicolor/24x24/apps/session-properties.png
%{_datadir}/icons/hicolor/32x32/apps/session-properties.png
%{_datadir}/icons/hicolor/48x48/apps/session-properties.png
%{_datadir}/icons/hicolor/scalable/apps/session-properties.svg
%{_mandir}/man1/gnome-session-properties.1.gz
%{_mandir}/man1/gnome-session-quit.1.gz
%{_mandir}/man1/gnome-session.1.gz


%files xsession
%doc AUTHORS ChangeLog NEWS README
%{_datadir}/xsessions/gnome-classic.desktop
%{_datadir}/xsessions/gnome-fallback.desktop
%{_datadir}/xsessions/gnome.desktop
%{_datadir}/xsessions/ubuntu-2d.desktop
%{_datadir}/xsessions/ubuntu.desktop


%changelog
* Sat Feb 02 2013 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.4.2.1-3.0ubuntu1
- Make sure polkit-gnome-authentication-agent-1 does not start in GNOME Shell

* Fri Sep 14 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.4.2.1-2.0ubuntu1
- Version 3.4.2.1
- Ubuntu release 0ubuntu1

* Wed Aug 22 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.4.2.1-1.ubuntu3.2.1.0ubuntu8
- Version 3.4.2.1

* Thu Jul 19 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.4.2-3.ubuntu3.2.1.0ubuntu8
- Disable obsolete patches
- Do not install gnome-wm

* Mon Jul 16 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.4.2-2.ubuntu3.2.1.0ubuntu8
- Install Ubuntu's files

* Mon Jul 16 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.4.2-1.ubuntu3.2.1.0ubuntu8
- Initial release
- Based off of Fedora 17's spec
- Version 3.4.2
- Refreshed patches for 3.4.1
- Ubuntu version 3.2.1
- Ubuntu release 0ubuntu8
