# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

# Partially based off of Fedora 17's metacity spec file
# This package is required for Compiz and Unity 2D

%define _ubuntu_rel 1ubuntu11

Name:		metacity
Version:	2.34.1
Release:	1.%{_ubuntu_rel}%{?dist}
# Require "metacity >= 1:" in other packages to use this package
Epoch:		1
Summary:	Unobtrusive window manager

Group:		User Interface/Desktops
License:	GPLv2+
URL:		http://download.gnome.org/sources/metacity/
Source0:	http://ftp.gnome.org/pub/GNOME/sources/metacity/2.34/metacity-%{version}.tar.xz

# Wrapper for metacity to simulate Ubuntu's gconf-defaults mechanism
Source1:	metacity.wrapper

Source99:	https://launchpad.net/ubuntu/+archive/primary/+files/metacity_%{version}-%{_ubuntu_rel}.debian.tar.gz

BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	desktop-file-utils
BuildRequires:	gettext
BuildRequires:	libtool
BuildRequires:	intltool

BuildRequires:	control-center
BuildRequires:	dbus-devel
BuildRequires:	fontconfig-devel
BuildRequires:	gsettings-desktop-schemas-devel
BuildRequires:	GConf2-devel
BuildRequires:	gnome-common
BuildRequires:	gnome-doc-utils
BuildRequires:	gtk2-devel
BuildRequires:	libcanberra-devel
BuildRequires:	libglade2-devel
BuildRequires:	libICE-devel
BuildRequires:	libSM-devel
BuildRequires:	libX11-devel
BuildRequires:	libXcomposite-devel
BuildRequires:	libXcursor-devel
BuildRequires:	libXdamage-devel
BuildRequires:	libXext-devel
BuildRequires:	libXinerama-devel
BuildRequires:	libXrandr-devel
Buildrequires:	libXrender-devel
BuildRequires:	pango-devel
BuildRequires:	startup-notification-devel
BuildRequires:	xorg-x11-proto-devel
BuildRequires:	zenity

Requires:	control-center-filesystem
Requires:	GConf2
Requires:	gsettings-desktop-schemas
Requires:	startup-notification
Requires:	zenity

Provides:	firstboot(windowmanager) = metacity

Requires(pre):	GConf2
Requires(post):	GConf2
Requires(preun):	GConf2

# Satisfy obs conflict on what provides PackageKit-backend
BuildRequires:	PackageKit-yum

# Satisfy obs conflict on gtk2: use gtk2
BuildRequires:	gtk2

# Satisfy obs conflict on gtk3 too (installed by build dependencies)
BuildRequires:	gtk3
BuildRequires:	gtk3-devel

%description
Metacity is a window manager that integrates nicely with the GNOME desktop.
It strives to be quiet, small, stable, get on with its job, and stay out of
your attention.


%package devel
Summary:	Development files for metacity
Group:		Development/Libraries

Requires:	%{name}%{?_isa} = %{epoch}:%{version}-%{release}

%description devel
This package contains the files needed for compiling programs using
the metacity-private library. Note that you are not supposed to write
programs using the metacity-private library, since it is a private
API. This package exists purely for technical reasons.


%prep
%setup -q

# Apply Ubuntu's patches
tar zxvf %{SOURCE99}
for i in $(grep -v '#' debian/patches/series); do
  patch -Np1 -i "debian/patches/${i}"
done

autoreconf -vfi


%build
%configure --disable-static
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name '*.la' -delete

desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/metacity.desktop

# Install Ubuntu's files
install -dm755 $RPM_BUILD_ROOT%{_datadir}/sgml/metacity-common/
install -m644 doc/metacity-theme.dtd \
              $RPM_BUILD_ROOT%{_datadir}/sgml/metacity-common/
install -m644 debian/metacity-common.catalog \
              $RPM_BUILD_ROOT%{_datadir}/sgml/metacity-common/

# Simulate Ubuntu's gconf defaults functionality with wrapper script
# Defaults are from debian/metacity-common.gconf-defaults
mv $RPM_BUILD_ROOT%{_bindir}/metacity{,.bin}
install -m644 debian/metacity-common.gconf-defaults \
              $RPM_BUILD_ROOT%{_datadir}/metacity/metacity.gconf-defaults
install -m755 '%{SOURCE1}' $RPM_BUILD_ROOT%{_bindir}/metacity

%find_lang %{name}


%post
/usr/sbin/ldconfig
%gconf_schema_upgrade metacity

%pre
# Only if upgrading
if [ ${1} -gt 1 ]; then
  %gconf_schema_upgrade metacity
fi

%preun
%gconf_schema_remove metacity

%postun -p /usr/sbin/ldconfig


%files -f %{name}.lang
%doc README AUTHORS COPYING NEWS HACKING doc/theme-format.txt doc/metacity-theme.dtd rationales.txt
%{_bindir}/metacity
%{_bindir}/metacity.bin
%{_bindir}/metacity-message
%{_sysconfdir}/gconf/schemas/metacity.schemas
%{_libdir}/libmetacity-private.so.0
%{_libdir}/libmetacity-private.so.0.0.0
%{_datadir}/applications/metacity.desktop
%{_datadir}/gnome-control-center/keybindings/50-metacity-launchers.xml
%{_datadir}/gnome-control-center/keybindings/50-metacity-navigation.xml
%{_datadir}/gnome-control-center/keybindings/50-metacity-screenshot.xml
%{_datadir}/gnome-control-center/keybindings/50-metacity-system.xml
%{_datadir}/gnome-control-center/keybindings/50-metacity-windows.xml
%{_datadir}/gnome/help/creating-metacity-themes/
%{_datadir}/gnome/wm-properties/metacity-wm.desktop
%{_mandir}/man1/metacity.1.gz
%{_mandir}/man1/metacity-message.1.gz
%{_datadir}/metacity/icons/metacity-window-demo.png
%{_datadir}/metacity/metacity.gconf-defaults
%{_datadir}/sgml/metacity-common/metacity-common.catalog
%{_datadir}/sgml/metacity-common/metacity-theme.dtd
%{_datadir}/themes/*/metacity-1/*.png
%{_datadir}/themes/*/metacity-1/*.xml


%files devel
%{_bindir}/metacity-theme-viewer
%{_bindir}/metacity-window-demo
%{_includedir}/metacity-1/metacity-private/boxes.h
%{_includedir}/metacity-1/metacity-private/common.h
%{_includedir}/metacity-1/metacity-private/gradient.h
%{_includedir}/metacity-1/metacity-private/preview-widget.h
%{_includedir}/metacity-1/metacity-private/theme.h
%{_includedir}/metacity-1/metacity-private/theme-parser.h
%{_includedir}/metacity-1/metacity-private/util.h
%{_libdir}/libmetacity-private.so
%{_libdir}/pkgconfig/libmetacity-private.pc
%{_mandir}/man1/metacity-theme-viewer.1.gz
%{_mandir}/man1/metacity-window-demo.1.gz


%changelog
* Sun Jul 01 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 1:2.34.1-1.1ubuntu11
- Initial release
- Based on Fedora 17's spec file
- Version 2.34.1
- Ubuntu release 1ubuntu11
