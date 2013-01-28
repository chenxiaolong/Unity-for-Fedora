# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

# Partially based off of Fedora 18's spec file

%define _ubuntu_rel 0ubuntu3

Name:		gnome-session
Version:	3.6.2
Release:	101.%{_ubuntu_rel}%{?dist}
Summary:	GNOME session manager

Group:		User Interface/Desktops
License:	GPLv2+
URL:		http://www.gnome.org/
Source0:	http://download.gnome.org/sources/gnome-session/3.6/gnome-session-%{version}.tar.xz

Source98:	55gnome-session_gnomerc
Source99:	https://launchpad.net/ubuntu/+archive/primary/+files/gnome-session_%{version}-%{_ubuntu_rel}.debian.tar.gz

Source1:	gnome-authentication-agent.desktop

# Fedora's patches
Patch0:		gnome-session-3.3.1-llvmpipe.patch
Patch1:		gnome-session-3.3.92-nv30.patch
Patch2:		fedora_0001-main-Set-XDG_MENU_PREFIX.patch
Patch3:		fedora_reject-shutdown-clients.patch

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

Provides:	gnome-session-ubuntu = %{version}-%{release}

%description
gnome-session manages a GNOME desktop or GDM login session. It starts up the
other core GNOME components and handles logout and saving the session.


%package xsession
Summary:	Desktop files for gnome-session-ubuntu
Group:		User Interface/Desktops

Requires:	%{name}%{?_isa} = %{version}-%{release}

Provides:       gnome-session-ubuntu-xsession = %{version}-%{release}

%description xsession
This package contains the X session desktop files needed to add GNOME and Unity
to the display manager menus.


%prep
%setup -q -n gnome-session-%{version}

tar zxvf '%{SOURCE99}'

# Apply Fedora's patches
%patch0 -p1 -b .llvmpipe
%patch1 -p1 -b .nv30
%patch2 -p1 -b .set-xdg-menu-prefix
%patch3 -p1 -b .reject-shutdown-clients

# Apply Ubuntu's patches
tar zxvf '%{SOURCE99}'

# Disable patches
  # gnome-wm uses Debian's alternatives system (Fedora has it too, but other
  # packages need to use it)
    sed -i '/01_gnome-wm.patch/d' debian/patches/series
  # systemd should make these patches obsolete
    sed -i '/12_no_gdm_fallback.patch/d' debian/patches/series
  # We're not Ubuntu, do not hide stuff
    sed -i '/20_hide_nodisplay.patch/d' debian/patches/series
  # Only Ubuntu uses apport
    sed -i '/96_no_catch_sigsegv.patch/d' debian/patches/series
  # Fedora does not have sessionmigration
    sed -i '/53_add_sessionmigration.patch/d' debian/patches/series
  # Part of Fedora's patches
    sed -i '/97_dont_blacklist_llvmpipe.patch/d' debian/patches/series

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
  --enable-systemd

make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT

install -dm755 $RPM_BUILD_ROOT%{_datadir}/gnome/autostart/
desktop-file-install \
  --dir $RPM_BUILD_ROOT%{_datadir}/gnome/autostart/ \
  --add-only-show-in Unity \
  --set-comment "PolicyKit Authentication Agent for GNOME 3 Classic and Unity" \
  --remove-key "AutostartCondition" \
  %{SOURCE1}

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
%dir %{_datadir}/gnome-session/
%{_datadir}/gnome-session/gsm-inhibit-dialog.ui
%{_datadir}/gnome-session/hardware-compatibility
%{_datadir}/gnome-session/session-properties.ui
%dir %{_datadir}/gnome-session/sessions/
%{_datadir}/gnome-session/sessions/gnome-fallback-compiz.session
%{_datadir}/gnome-session/sessions/gnome-fallback.session
%{_datadir}/gnome-session/sessions/gnome.session
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
%{_datadir}/xsessions/gnome-fallback-compiz.desktop
%{_datadir}/xsessions/gnome-fallback.desktop
%{_datadir}/xsessions/gnome.desktop
%{_datadir}/xsessions/ubuntu.desktop


%changelog
* Mon Jan 28 2013 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.6.2-1.0ubuntu3
- Version 3.6.2
- Ubuntu release 0ubuntu3

* Sun Nov 18 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.6.2-1.0ubuntu2
- Version 3.6.2
- Ubuntu release 0ubuntu2
- Merge Fedora's changes
  - 3.6.2-1: Rebase the XDG_MENU_PREFIX patch
  - 3.6.2-2: Add upstream patch to fix handling of client registration during
  -          shutdown
  -        : Fixes slow gnome-session shutdown for maliit users

* Sat Oct 20 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.6.1-1.ubuntu3.6.0.0ubuntu1
- Version 3.6.1
- Merge Fedora's changes
  - 3.6.1-2: Set XDG_MENU_PREFIX to pick the correct menu layout in gnome-shell
    and alacarte

* Fri Sep 28 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.6.0-1.0ubuntu1
- Version 3.6.0
- Ubuntu release 0ubuntu1

* Fri Sep 21 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.5.91-1.0ubuntu2
- Initial release for Fedora 18
- Version 3.5.91
- Ubuntu release 0ubuntu2

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
