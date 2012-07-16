# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

# Partially based off of Fedora 17's spec file

%define _ubuntu_ver 3.2.1
%define _ubuntu_rel 0ubuntu8

%define _obsolete_ver 3.5.0-100

Name:		gnome-session-ubuntu
Version:	3.4.2
Release:	2.ubuntu%{_ubuntu_ver}.%{_ubuntu_rel}%{?dist}
Summary:	GNOME session manager

Group:		User Interface/Desktops
License:	GPLv2+
URL:		http://www.gnome.org/
Source0:	http://download.gnome.org/sources/gnome-session/3.4/gnome-session-%{version}.tar.xz

Source98:	55gnome-session_gnomerc
Source99:	https://launchpad.net/ubuntu/+archive/primary/+files/gnome-session_%{_ubuntu_ver}-%{_ubuntu_rel}.debian.tar.gz

Source1:	gnome-authentication-agent.desktop

# Fedora's patches
Patch0:		gnome-session-3.3.1-llvmpipe.patch
Patch1:		gnome-session-3.3.92-nv30.patch

# Refreshed all of the patches for GNOME session 3.4.1
Patch100:	UBUNTU_01_gnome-wm.patch
Patch101:	UBUNTU_02_fallback_desktop.patch
Patch102:	UBUNTU_103_kill_the_fail_whale.patch
Patch103:	UBUNTU_104_dont_show_fallback_warning.patch
Patch104:	UBUNTU_105_hide_session_startup_help.patch
Patch105:	UBUNTU_12_no_gdm_fallback.patch
Patch106:	UBUNTU_20_hide_nodisplay.patch
Patch107:	UBUNTU_21_up_start_on_demand.patch
Patch108:	UBUNTU_22_support_autostart_delay.patch
Patch109:	UBUNTU_50_ubuntu_sessions.patch
Patch110:	UBUNTU_51_remove_session_saving_from_gui.patch
Patch111:	UBUNTU_52_xdg_current_desktop.patch
Patch112:	UBUNTU_95_dbus_request_shutdown.patch

BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	desktop-file-utils
BuildRequires:	gettext
BuildRequires:	gnome-common
BuildRequires:	intltool
BuildRequires:	libtool
BuildRequires:	usermode
BuildRequires:	xmlto

BuildRequires:	dbus-devel
BuildRequires:	dbus-glib-devel
BuildRequires:	GConf2-devel
BuildRequires:	gnome-keyring-devel
BuildRequires:	gnome-settings-daemon-ubuntu-devel
BuildRequires:	gtk3-devel
BuildRequires:	json-glib-devel
BuildRequires:	libnotify-devel
BuildRequires:	librsvg2-devel
BuildRequires:	libX11-devel
BuildRequires:	libXau-devel
BuildRequires:	libXrandr-devel
BuildRequires:	libXt-devel
BuildRequires:	libXtst-devel
BuildRequires:	mesa-libGL-devel
BuildRequires:	pango-devel
BuildRequires:	polkit-devel
BuildRequires:	systemd-devel
BuildRequires:	upower-devel
BuildRequires:	xorg-x11-xtrans-devel

# Satisfy OBS conflict on GTK 2 (installed by dependencies)
BuildRequires:	gtk2
BuildRequires:	gtk2-devel

# Satisfy OBS conflict on gsettings-desktop-schemas
BuildRequires:	gsettings-desktop-schemas

# Satisfy OBS conflict on what provides PackageKit-backend
BuildRequires:	PackageKit-yum

# Satisfy OBS conflict on libXfixes
BuildRequires:	libXfixes
BuildRequires:	libXfixes-devel

# Satisfy OBS conflict on xorg-x11-proto-devel
BuildRequires:	xorg-x11-proto-devel

# Satisfy OBS conflict on control-center-filesystem
BuildRequires:	control-center-filesystem

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
%patch100 -p1
%patch101 -p1
%patch102 -p1
%patch103 -p1
%patch104 -p1
%patch105 -p1
%patch106 -p1
%patch107 -p1
%patch108 -p1
%patch109 -p1
%patch110 -p1
%patch111 -p1
%patch112 -p1

autoreconf -vfi


%build
%configure \
  --enable-docbook-docs \
  --docdir=%{_datadir}/doc/%{name}-%{version} \
  --with-gtk=3.0 \
  --enable-systemd

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
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
install -m755 debian/scripts/gnome-wm $RPM_BUILD_ROOT%{_bindir}/

install -dm755 $RPM_BUILD_ROOT%{_sysconfdir}/X11/xinit/xinitrc.d/
install -m755 '%{SOURCE98}' $RPM_BUILD_ROOT%{_sysconfdir}/X11/xinit/xinitrc.d/

install -dm755 $RPM_BUILD_ROOT%{_sysconfdir}/gnome/
install -m644 debian/defaults.list $RPM_BUILD_ROOT%{_sysconfdir}/gnome/

install -dm755 $RPM_BUILD_ROOT%{_datadir}/gnome/applications/
ln -s %{_sysconfdir}/gnome/defaults.list \
  $RPM_BUILD_ROOT%{_datadir}/gnome/applications/

install -m644 debian/gnome-session-common.gsettings-override \
  $RPM_BUILD_ROOT%{_datadir}/glib-2.0/schemas/10_%{name}.gschema.override

desktop-file-install \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications/ \
  debian/gnome-wm.desktop

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
%{_bindir}/gnome-wm
%{_libexecdir}/gnome-session-check-accelerated
%{_libexecdir}/gnome-session-check-accelerated-helper
%{_sysconfdir}/X11/xinit/xinitrc.d/55gnome-session_gnomerc
%{_sysconfdir}/gnome/defaults.list
%{_datadir}/GConf/gsettings/gnome-session.convert
%{_datadir}/applications/gnome-wm.desktop
%{_datadir}/applications/session-properties.desktop
%{_datadir}/glib-2.0/schemas/10_gnome-session-ubuntu.gschema.override
%{_datadir}/glib-2.0/schemas/org.gnome.SessionManager.gschema.xml
%dir %{_datadir}/gnome/
%dir %{_datadir}/gnome/applications/
%dir %{_datadir}/gnome/autostart/
%{_datadir}/gnome/applications/defaults.list
%{_datadir}/gnome/autostart/gnome-authentication-agent.desktop
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
%{_datadir}/xsessions/gnome-shell.desktop
%{_datadir}/xsessions/gnome.desktop
%{_datadir}/xsessions/ubuntu-2d.desktop
%{_datadir}/xsessions/ubuntu.desktop


%changelog
* Mon Jul 16 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.4.2-2.ubuntu3.2.1.0ubuntu8
- Install Ubuntu's files

* Mon Jul 16 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.4.2-1.ubuntu3.2.1.0ubuntu8
- Initial release
- Based off of Fedora 17's spec
- Version 3.4.2
- Refreshed patches for 3.4.1
- Ubuntu version 3.2.1
- Ubuntu release 0ubuntu8
