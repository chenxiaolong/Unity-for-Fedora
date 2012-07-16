# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

# Partially based off of Fedora 17's spec file

%define _ubuntu_rel 0ubuntu0.3

%define _obsolete_ver 1:3.5.0-100

Name:		control-center-ubuntu
Version:	3.4.2
Release:	1.%{_ubuntu_rel}%{?dist}
Summary:	Utilities to configure the GNOME desktop

Group:		User Interface/Desktops
License:	GPLv2+ and GFDL
URL:		http://www.gnome.org
Source0:	http://download.gnome.org/sources/gnome-control-center/3.4/gnome-control-center-%{version}.tar.xz

Source99:	https://launchpad.net/ubuntu/+archive/primary/+files/gnome-control-center_%{version}-%{_ubuntu_rel}.debian.tar.gz

# https://bugzilla.gnome.org/show_bug.cgi?id=672682
# https://bugzilla.redhat.com/show_bug.cgi?id=802381
Patch0:		printers-firewalld1-api.patch

BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	desktop-file-utils
BuildRequires:	docbook-utils
BuildRequires:	gettext
BuildRequires:	gnome-common
BuildRequires:	gnome-doc-utils
BuildRequires:	intltool

BuildRequires:	cheese-libs-devel
BuildRequires:	clutter-gst-devel
BuildRequires:	clutter-gtk-devel
BuildRequires:	colord-devel
BuildRequires:	cups-devel
BuildRequires:	dbus-devel
BuildRequires:	dbus-glib-devel
BuildRequires:	GConf2-devel
BuildRequires:	gdk-pixbuf2-devel
BuildRequires:	glib2-devel
BuildRequires:	gnome-bluetooth-devel
BuildRequires:	gnome-desktop3-devel
BuildRequires:	gnome-menus-devel
BuildRequires:	gnome-online-accounts-devel
BuildRequires:	gnome-settings-daemon-ubuntu-devel
BuildRequires:	gsettings-desktop-schemas-ubuntu-devel
BuildRequires:	gtk3-ubuntu-devel
BuildRequires:	iso-codes-devel
BuildRequires:	libcanberra-devel
BuildRequires:	libglade2-devel
BuildRequires:	libgnomekbd-devel
BuildRequires:	libgtop2-devel
BuildRequires:	libnotify-devel
BuildRequires:	librsvg2-devel
BuildRequires:	libwacom-devel
BuildRequires:	libXcursor-devel
BuildRequires:	libxkbfile-devel
BuildRequires:	libxklavier-devel
BuildRequires:	libxml2-devel
BuildRequires:	libXrandr-devel
BuildRequires:	libXScrnSaver-devel
BuildRequires:	libXxf86misc-devel
BuildRequires:	NetworkManager-glib-devel
BuildRequires:	NetworkManager-gtk-devel
BuildRequires:	polkit-devel
BuildRequires:	pulseaudio-libs-devel >= 2.0-1
#BuildRequires:	scrollkeeper
BuildRequires:	systemd-devel
BuildRequires:	upower-devel

# Satisfy OBS conflict on gtk2 (installed by dependencies)
BuildRequires:	gtk2
BuildRequires:	gtk2-devel

# Satisfy OBS conflict on libXfixes (installed by dependencies)
BuildRequires:	libXfixes
BuildRequires:	libXfixes-devel

# Satisfy OBS conflict on xorg-x11-proto-devel (installed by dependencies)
BuildRequires:	xorg-x11-proto-devel

# Satisfy OBS conflict on what provides PackageKit-backend
BuildRequires:	PackageKit-yum

# Requires Ubuntu's patched gnome-settings-daemon
Requires:	gnome-settings-daemon-ubuntu

Requires:	control-center-ubuntu-filesystem = %{version}-%{release}

Requires:	alsa-lib
Requires:	dbus-x11
Requires:	gnome-desktop3
Requires:	gnome-icon-theme
Requires:	gnome-menus
Requires:	redhat-menus

# Display settings
Requires:	libXrandr

# User account settings
Requires:	accountsservice
Requires:	apg

# Languages
Requires:	iso-codes

# Sound applet and settings
Requires:	gnome-icon-theme-symbolic

# Printers
Requires:	cups-pk-helper

# Replace official version
# Provide epoch 1 since Fedora's package is at epoch 1
Provides:	control-center%{?_isa} = 1:%{version}-%{release}
Provides:	control-center         = 1:%{version}-%{release}
Obsoletes:	control-center%{?_isa} < %{_obsolete_ver}
Obsoletes:	control-center         < %{_obsolete_ver}

%description
This package contains configuration utilities for the GNOME desktop, which
allow to configure accessibility options, desktop fonts, keyboard and mouse
properties, sound setup, desktop theme and background, user interface
properties, screen resolution, and other settings.


%package devel
Summary:	Development files for the GNOME Control Center library
Group:		Development/Libraries

Requires:	%{name}%{?_isa} = %{version}-%{release}

Provides:       control-center-devel%{?_isa} = 1:%{version}-%{release}
Provides:       control-center-devel         = 1:%{version}-%{release}
Obsoletes:      control-center-devel%{?_isa} < %{_obsolete_ver}
Obsoletes:      control-center-devel         < %{_obsolete_ver}

%description devel
This package contains the development files for Ubuntu's patched version of the
GNOME Control Center library.


%package filesystem
Summary:	GNOME Control Center directories
Group:		Development/Libraries

Provides:       control-center-filesystem%{?_isa} = 1:%{version}-%{release}
Provides:       control-center-filesystem         = 1:%{version}-%{release}
Obsoletes:      control-center-filesystem%{?_isa} < %{_obsolete_ver}
Obsoletes:      control-center-filesystem         < %{_obsolete_ver}

%description filesystem
The GNOME control-center provides a number of extension points for applications.
This package contains directories where applications can install configuration
files that are picked up by the control-center utilities.


%prep
%setup -q -n gnome-control-center-%{version}

%patch0 -p1 -b .firewalld1

# Apply Ubuntu's patches
tar zxvf '%{SOURCE99}'

# Disable patches
  # Disable using Ubuntu's update manager
    sed -i '/05_run_update_manager.patch/d' debian/patches/series
  # Fedora does not use Ubuntu's language selector
    sed -i '/52_ubuntu_language_list_mods.patch/d' debian/patches/series
  # Don't use Ubuntu's help files
    sed -i '/53_use_ubuntu_help.patch/d' debian/patches/series
  # Don't use Ubuntu branding.
    sed -i '/56_use_ubuntu_info_branding.patch/d' debian/patches/series

for i in $(grep -v '#' debian/patches/series); do
  patch -Np1 -i "debian/patches/${i}"
done

autoreconf -vfi


%build
%configure \
  --disable-static \
  --disable-scrollkeeper \
  --disable-update-mimedb \
  --with-libsocialweb=no \
  --enable-systemd

# Disable rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

# From Fedora 17 spec: only link against necessary libraries
sed -i -e 's/ -shared / -Wl,-O1,--as-needed\0 /g' -e 's/    if test "$export_dynamic" = yes && test -n "$export_dynamic_flag_spec"; then/      func_append compile_command " -Wl,-O1,--as-needed"\n      func_append finalize_command " -Wl,-O1,--as-needed"\n\0/' libtool

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 make install DESTDIR=$RPM_BUILD_ROOT

desktop-file-install \
  --delete-original \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications/ \
  --add-only-show-in GNOME \
  --add-only-show-in Unity \
  $RPM_BUILD_ROOT%{_datadir}/applications/*.desktop

# Create directory from GNOME window manager desktop files
install -dm755 $RPM_BUILD_ROOT%{_datadir}/gnome/wm-properties/

# Remove unwanted directories (not packaged in Fedora)
rm -rvf $RPM_BUILD_ROOT%{_datadir}/gnome/autostart/
rm -rvf $RPM_BUILD_ROOT%{_datadir}/gnome/cursor-fonts/

# Install Ubuntu's manual page
pushd debian
install -dm755 $RPM_BUILD_ROOT%{_mandir}/man1/
docbook2man gnome-control-center.sgml || true
install -m644 gnome-control-center.1 $RPM_BUILD_ROOT%{_mandir}/man1/
popd

# Link gnome-control-center desktop file for indicators
install -dm755 $RPM_BUILD_ROOT%{_datadir}/indicators/session/applications/
ln -s %{_datadir}/applications/gnome-control-center.desktop \
  $RPM_BUILD_ROOT%{_datadir}/indicators/session/applications/

# Remove libtool files
find $RPM_BUILD_ROOT -type f -name '*.la' -delete

%find_lang gnome-control-center-2.0
%find_lang gnome-control-center-2.0-timezones


%post
/usr/sbin/ldconfig
update-desktop-database &>/dev/null || :
update-mime-database %{_datadir}/mime/ &>/dev/null || :
touch --no-create %{_datadir}/icons/hicolor/ &>/dev/null || :

%postun
/usr/sbin/ldconfig
update-desktop-database &>/dev/null || :
update-mime-database %{_datadir}/mime/ &>/dev/null || :
if [ ${1} -eq 0 ]; then
  touch --no-create %{_datadir}/icons/hicolor/ &>/dev/null || :
  gtk-update-icon-cache -f %{_datadir}/icons/hicolor/ &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache -f %{_datadir}/icons/hicolor/ &>/dev/null || :


%files -f gnome-control-center-2.0.lang -f gnome-control-center-2.0-timezones.lang
%doc AUTHORS ChangeLog NEWS README TODO
%{_bindir}/gnome-control-center
%{_bindir}/gnome-sound-applet

# XDG files
%{_sysconfdir}/xdg/autostart/gnome-sound-applet.desktop
%{_sysconfdir}/xdg/menus/gnomecc.menu

# GNOME Control Center panels
%dir %{_libdir}/control-center-1/
%dir %{_libdir}/control-center-1/panels/
%{_libdir}/control-center-1/panels/libbackground.so
%{_libdir}/control-center-1/panels/libbluetooth.so
%{_libdir}/control-center-1/panels/libcolor.so
%{_libdir}/control-center-1/panels/libdate_time.so
%{_libdir}/control-center-1/panels/libdisplay.so
%{_libdir}/control-center-1/panels/libinfo.so
%{_libdir}/control-center-1/panels/libkeyboard.so
%{_libdir}/control-center-1/panels/libmouse-properties.so
%{_libdir}/control-center-1/panels/libnetwork.so
%{_libdir}/control-center-1/panels/libonline-accounts.so
%{_libdir}/control-center-1/panels/libpower.so
%{_libdir}/control-center-1/panels/libprinters.so
%{_libdir}/control-center-1/panels/libregion.so
%{_libdir}/control-center-1/panels/libscreen.so
%{_libdir}/control-center-1/panels/libsound.so
%{_libdir}/control-center-1/panels/libsoundnua.so
%{_libdir}/control-center-1/panels/libuniversal-access.so
%{_libdir}/control-center-1/panels/libuser-accounts.so
%{_libdir}/control-center-1/panels/libwacom-properties.so

# GNOME Control Center libraries
%{_libdir}/libgnome-control-center.so.1
%{_libdir}/libgnome-control-center.so.1.0.0

# Desktop files
%dir %{_datadir}/indicators/
%dir %{_datadir}/indicators/session/
%dir %{_datadir}/indicators/session/applications/
%{_datadir}/indicators/session/applications/gnome-control-center.desktop
%{_datadir}/applications/bluetooth-properties.desktop
%{_datadir}/applications/gnome-background-panel.desktop
%{_datadir}/applications/gnome-color-panel.desktop
%{_datadir}/applications/gnome-control-center.desktop
%{_datadir}/applications/gnome-datetime-panel.desktop
%{_datadir}/applications/gnome-display-panel.desktop
%{_datadir}/applications/gnome-info-panel.desktop
%{_datadir}/applications/gnome-keyboard-panel.desktop
%{_datadir}/applications/gnome-mouse-panel.desktop
%{_datadir}/applications/gnome-network-panel.desktop
%{_datadir}/applications/gnome-online-accounts-panel.desktop
%{_datadir}/applications/gnome-power-panel.desktop
%{_datadir}/applications/gnome-printers-panel.desktop
%{_datadir}/applications/gnome-region-panel.desktop
%{_datadir}/applications/gnome-screen-panel.desktop
%{_datadir}/applications/gnome-sound-nua-panel.desktop
%{_datadir}/applications/gnome-sound-panel.desktop
%{_datadir}/applications/gnome-universal-access-panel.desktop
%{_datadir}/applications/gnome-user-accounts-panel.desktop
%{_datadir}/applications/gnome-wacom-panel.desktop

# XDG Desktop Directory files
%{_datadir}/desktop-directories/gnomecc.directory

# GNOME Control Center icons
%{_datadir}/gnome-control-center/icons/

# Regular icons
%{_datadir}/icons/hicolor/16x16/apps/*.png
%{_datadir}/icons/hicolor/16x16/apps/multimedia-volume-control.svg
%{_datadir}/icons/hicolor/22x22/apps/*.png
%{_datadir}/icons/hicolor/22x22/apps/multimedia-volume-control.svg
%{_datadir}/icons/hicolor/24x24/apps/*.png
%{_datadir}/icons/hicolor/32x32/apps/*.png
%{_datadir}/icons/hicolor/32x32/apps/multimedia-volume-control.svg
%{_datadir}/icons/hicolor/48x48/apps/*.png
%{_datadir}/icons/hicolor/48x48/devices/audio-headset.svg
%{_datadir}/icons/hicolor/64x64/apps/*.png
%{_datadir}/icons/hicolor/256x256/apps/*.png
%{_datadir}/icons/hicolor/scalable/apps/*.svg
%{_datadir}/icons/hicolor/scalable/categories/*.svg
%{_datadir}/icons/hicolor/scalable/emblems/*.svg
%{_datadir}/icons/hicolor/scalable/status/*.svg
%dir %{_datadir}/pixmaps/faces/
%{_datadir}/pixmaps/faces/*.jpg
%{_datadir}/pixmaps/faces/*.png

# GNOME Control Center keybindings
%{_datadir}/gnome-control-center/keybindings/00-multimedia.xml
%{_datadir}/gnome-control-center/keybindings/01-launchers.xml
%{_datadir}/gnome-control-center/keybindings/01-screenshot.xml
%{_datadir}/gnome-control-center/keybindings/01-system.xml
%{_datadir}/gnome-control-center/keybindings/50-accessibility.xml

# GNOME Control Center UI icons
%dir %{_datadir}/gnome-control-center/pixmaps/
%{_datadir}/gnome-control-center/pixmaps/*.png
%{_datadir}/gnome-control-center/pixmaps/*.svg

# GNOME Control Center user interface files
%dir %{_datadir}/gnome-control-center/ui/
%{_datadir}/gnome-control-center/bluetooth.ui
%{_datadir}/gnome-control-center/ui/datetime/datetime.ui
%{_datadir}/gnome-control-center/ui/background/background.ui
%{_datadir}/gnome-control-center/ui/button-mapping.ui
%{_datadir}/gnome-control-center/ui/color.ui
%{_datadir}/gnome-control-center/ui/display-capplet.ui
%{_datadir}/gnome-control-center/ui/gnome-keyboard-panel.ui
%{_datadir}/gnome-control-center/ui/gnome-mouse-properties.ui
%{_datadir}/gnome-control-center/ui/gnome-region-panel-layout-chooser.ui
%{_datadir}/gnome-control-center/ui/gnome-region-panel-options-dialog.ui
%{_datadir}/gnome-control-center/ui/gnome-region-panel.ui
%{_datadir}/gnome-control-center/ui/gnome-wacom-properties.ui
%{_datadir}/gnome-control-center/ui/info.ui
%{_datadir}/gnome-control-center/ui/language-chooser.ui
%{_datadir}/gnome-control-center/ui/network.ui
%{_datadir}/gnome-control-center/ui/online-accounts.ui
%{_datadir}/gnome-control-center/ui/power.ui
%dir %{_datadir}/gnome-control-center/ui/printers/
%{_datadir}/gnome-control-center/ui/printers/new-printer-dialog.ui
%{_datadir}/gnome-control-center/ui/printers/printers.ui
%{_datadir}/gnome-control-center/ui/screen.ui
%{_datadir}/gnome-control-center/ui/shell.ui
%{_datadir}/gnome-control-center/ui/uap.ui
%dir %{_datadir}/gnome-control-center/ui/user-accounts/
%{_datadir}/gnome-control-center/ui/user-accounts/account-dialog.ui
%{_datadir}/gnome-control-center/ui/user-accounts/account-fingerprint.ui
%{_datadir}/gnome-control-center/ui/user-accounts/password-dialog.ui
%{_datadir}/gnome-control-center/ui/user-accounts/photo-dialog.ui
%{_datadir}/gnome-control-center/ui/user-accounts/user-accounts-dialog.ui
%{_datadir}/gnome-control-center/ui/wacom-stylus-page.ui
%{_datadir}/gnome-control-center/ui/zoom-options.ui

# GNOME Control Center world map images and other datetime files
%dir %{_datadir}/gnome-control-center/ui/datetime/
%{_datadir}/gnome-control-center/ui/datetime/timezone_*.png
%{_datadir}/gnome-control-center/ui/datetime/bg.png
%{_datadir}/gnome-control-center/ui/datetime/cc.png
%{_datadir}/gnome-control-center/ui/datetime/pin.png

# GNOME Control Center background panel images
%dir %{_datadir}/gnome-control-center/ui/background/
%{_datadir}/gnome-control-center/ui/background/display-base.png
%{_datadir}/gnome-control-center/ui/background/display-overlay.png

# GNOME Control Center wacom settings panel images
%{_datadir}/gnome-control-center/ui/wacom-*.svg

# GNOME Control Center sounds
%dir %{_datadir}/gnome-control-center/sounds/
%{_datadir}/gnome-control-center/sounds/gnome-sounds-default.xml
%{_datadir}/sounds/gnome/default/alerts/bark.ogg
%{_datadir}/sounds/gnome/default/alerts/drip.ogg
%{_datadir}/sounds/gnome/default/alerts/glass.ogg
%{_datadir}/sounds/gnome/default/alerts/sonar.ogg

# Other GNOME Control Center data files
%{_datadir}/gnome-control-center/datetime/backward
%{_datadir}/gnome-control-center/ui/GnomeLogoVerticalMedium.svg

# GNOME Keybindings pkgconfig file
%{_datadir}/pkgconfig/gnome-keybindings.pc

# Manual pages
%{_mandir}/man1/gnome-control-center.1.gz


%files devel
%dir %{_includedir}/gnome-control-center-1/
%dir %{_includedir}/gnome-control-center-1/libgnome-control-center/
%{_includedir}/gnome-control-center-1/libgnome-control-center/cc-editable-entry.h
%{_includedir}/gnome-control-center-1/libgnome-control-center/cc-panel.h
%{_includedir}/gnome-control-center-1/libgnome-control-center/cc-shell.h
%{_libdir}/libgnome-control-center.so
%{_libdir}/pkgconfig/libgnome-control-center.pc


%files filesystem
%dir %{_datadir}/gnome/wm-properties/
%dir %{_datadir}/gnome-control-center/
%dir %{_datadir}/gnome-control-center/keybindings/


%changelog
* Sun Jul 15 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.4.2-1.0ubuntu0.3
- Initial release
- Based off of Fedora 17's spec file
- Version 3.4.2
- Ubuntu release 0ubuntu0.3