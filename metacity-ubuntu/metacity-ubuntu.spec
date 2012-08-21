# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

# Partially based off of Fedora 17's metacity spec file
# This package is required for Compiz and Unity 2D

%define _obsolete_ver 2.35.0-100

%define _ubuntu_rel 1ubuntu11

Name:		metacity-ubuntu
Version:	2.34.1
Release:	1.%{_ubuntu_rel}%{?dist}
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
BuildRequires:	control-center
BuildRequires:	desktop-file-utils
BuildRequires:	gettext
BuildRequires:	gnome-common
BuildRequires:	gnome-doc-utils
BuildRequires:	libtool
BuildRequires:	intltool
BuildRequires:	zenity

BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(fontconfig)
BuildRequires:	pkgconfig(gconf-2.0)
BuildRequires:	pkgconfig(gsettings-desktop-schemas)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(ice)
BuildRequires:	pkgconfig(libcanberra)
BuildRequires:	pkgconfig(libglade-2.0)
BuildRequires:	pkgconfig(libstartup-notification-1.0)
BuildRequires:	pkgconfig(pango)
BuildRequires:	pkgconfig(sm)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xcomposite)
BuildRequires:	pkgconfig(xcursor)
BuildRequires:	pkgconfig(xdamage)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xinerama)
BuildRequires:	pkgconfig(xrandr)
Buildrequires:	pkgconfig(xrender)

BuildRequires:	xorg-x11-proto-devel

Requires:	control-center-filesystem
Requires:	GConf2
Requires:	gsettings-desktop-schemas
Requires:	startup-notification
Requires:	zenity

Provides:	firstboot(windowmanager) = metacity

Requires(pre):	GConf2
Requires(post):	GConf2
Requires(preun):	GConf2

# Replace official verison
Provides:	metacity%{?_isa} = %{version}-%{release}
Provides:	metacity         = %{version}-%{release}
Obsoletes:	metacity%{?_isa} < %{_obsolete_ver}
Obsoletes:	metacity         < %{_obsolete_ver}

%description
Metacity is a window manager that integrates nicely with the GNOME desktop.
It strives to be quiet, small, stable, get on with its job, and stay out of
your attention.


%package devel
Summary:	Development files for metacity
Group:		Development/Libraries

Requires:	%{name}%{?_isa} = %{version}-%{release}

# Replace official version
Provides:	metacity-devel%{?_isa} = %{version}-%{release}
Provides:	metacity-devel         = %{version}-%{release}
Obsoletes:	metacity-devel%{?_isa} < %{_obsolete_ver}
Obsoletes:	metacity-devel         < %{_obsolete_ver}

%description devel
This package contains the files needed for compiling programs using
the metacity-private library. Note that you are not supposed to write
programs using the metacity-private library, since it is a private
API. This package exists purely for technical reasons.


%prep
%setup -q -n metacity-%{version}

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

%find_lang metacity


%post
/sbin/ldconfig
%gconf_schema_upgrade metacity

%pre
# Only if upgrading
if [ ${1} -gt 1 ]; then
  %gconf_schema_upgrade metacity
fi

%preun
%gconf_schema_remove metacity

%postun -p /sbin/ldconfig


%files -f metacity.lang
%doc README AUTHORS COPYING NEWS HACKING doc/theme-format.txt doc/metacity-theme.dtd rationales.txt
%{_bindir}/metacity
%{_bindir}/metacity.bin
%{_bindir}/metacity-message
%{_sysconfdir}/gconf/schemas/metacity.schemas
%{_libdir}/libmetacity-private.so.0
%{_libdir}/libmetacity-private.so.0.0.0
%{_datadir}/applications/metacity.desktop
%{_datadir}/gnome-control-center/keybindings/50-metacity-*.xml
%{_datadir}/gnome/help/creating-metacity-themes/
%{_datadir}/gnome/wm-properties/metacity-wm.desktop
%{_mandir}/man1/metacity.1.gz
%{_mandir}/man1/metacity-message.1.gz
%dir %{_datadir}/metacity/
%dir %{_datadir}/metacity/icons/
%{_datadir}/metacity/icons/metacity-window-demo.png
%{_datadir}/metacity/metacity.gconf-defaults
%dir %{_datadir}/sgml/metacity-common/
%{_datadir}/sgml/metacity-common/metacity-common.catalog
%{_datadir}/sgml/metacity-common/metacity-theme.dtd
%{_datadir}/themes/AgingGorilla/
%{_datadir}/themes/Atlanta/
%{_datadir}/themes/Bright/
%{_datadir}/themes/Crux/
%{_datadir}/themes/Esco/
%{_datadir}/themes/Metabox/
%{_datadir}/themes/Simple/


%files devel
%{_bindir}/metacity-theme-viewer
%{_bindir}/metacity-window-demo
%dir %{_includedir}/metacity-1/
%dir %{_includedir}/metacity-1/metacity-private/
%{_includedir}/metacity-1/metacity-private/*.h
%{_libdir}/libmetacity-private.so
%{_libdir}/pkgconfig/libmetacity-private.pc
%{_mandir}/man1/metacity-theme-viewer.1.gz
%{_mandir}/man1/metacity-window-demo.1.gz


%changelog
* Tue Aug 21 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 2.34.1-2.1ubuntu11
- Fix directory ownership
- Use pkgconfig for dependencies

* Sun Jul 01 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 2.34.1-1.1ubuntu11
- Initial release
- Based on Fedora 17's spec file
- Version 2.34.1
- Ubuntu release 1ubuntu11
