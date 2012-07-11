# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

%define _bzr_rev 19
%define _ubuntu_rel 0ubuntu10

%define _gconf_schemas compiz-animation compiz-colorfilter compiz-expo compiz-ezoom compiz-grid compiz-imgjpeg compiz-kdecompat compiz-mag compiz-mousepoll compiz-neg compiz-opacify compiz-put compiz-resizeinfo compiz-ring compiz-scaleaddon compiz-session compiz-shift compiz-snap compiz-staticswitcher compiz-text compiz-thumbnail compiz-titleinfo compiz-vpswitch compiz-wall compiz-winrules compiz-workarounds

Name:		compiz-plugins-main
Version:	0.9.7.0
Release:	1.bzr%{_bzr_rev}.%{_ubuntu_rel}%{?dist}
Summary:	Primary and well tested set of plugins from the Compiz project

Group:		User Interface/Desktops
License:	GPLv2
URL:		https://launchpad.net/compiz-plugins-main
Source0:	https://launchpad.net/ubuntu/+archive/primary/+files/compiz-plugins-main_%{version}~bzr%{_bzr_rev}.orig.tar.bz2

Source99:	https://launchpad.net/ubuntu/+archive/primary/+files/compiz-plugins-main_%{version}~bzr%{_bzr_rev}-%{_ubuntu_rel}.debian.tar.gz

BuildRequires:	cmake
BuildRequires:	gcc-c++
BuildRequires:	intltool
BuildRequires:	libtool

BuildRequires:	boost-devel
BuildRequires:	cairo-devel
BuildRequires:	compiz-devel
BuildRequires:	dbus-devel
BuildRequires:	GConf2-devel
BuildRequires:	glib2-devel
BuildRequires:	libjpeg-turbo-devel
BuildRequires:	librsvg2-devel
BuildRequires:	libSM-devel
BuildRequires:	libxml2-devel
BuildRequires:	libxslt-devel
BuildRequires:	mesa-libGLU-devel
BuildRequires:	pango-devel

Requires(pre):	GConf2
Requires(post):	GConf2
Requires(preun):	GConf2

# Satisfy OBS conflict on gtk3 (installed by build dependencies)
BuildRequires:	gtk3
BuildRequires:	gtk3-devel

# Satisfy OBS conflict on xorg-x11-proto-devel
BuildRequires:	xorg-x11-proto-devel

%description
This package provides the primary and most well tested set of plugins from the
Compiz project.


%package devel
Summary:	Development files for compiz-plugins-main
Group:		Development/Libraries

Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	compiz-devel

%description devel
This package contains the development files necessary for creating Compiz
plugins that depend on the plugins in compiz-plugins-main.


%prep
%setup -q

# Apply Ubuntu's patches
tar zxvf '%{SOURCE99}'
for i in $(grep -v '#' debian/patches/series); do
  patch -Np1 -i "debian/patches/${i}"
done


%build
mkdir build
cd build
%cmake .. \
  -DCOMPIZ_BUILD_WITH_RPATH=FALSE \
  -DCOMPIZ_PACKAGING_ENABLED=TRUE \
  -DCOMPIZ_PLUGIN_INSTALL_TYPE=package \
  -DUSE_GSETTINGS=OFF \
  -DCOMPIZ_DISABLE_GS_SCHEMAS_INSTALL=ON

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
cd build
GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 make install DESTDIR=$RPM_BUILD_ROOT

# Put GConf schemas in correct directory
install -dm755 $RPM_BUILD_ROOT%{_sysconfdir}/
mv $RPM_BUILD_ROOT{%{_datadir},%{_sysconfdir}}/gconf/


%pre
%gconf_schema_prepare %{_gconf_schemas}


%post
%gconf_schema_upgrade %{_gconf_schemas}


%preun
%gconf_schema_remove %{_gconf_schemas}


%files
%doc AUTHORS NEWS
# Compiz plugins
%{_libdir}/compiz/libanimation.so
%{_libdir}/compiz/libcolorfilter.so
%{_libdir}/compiz/libexpo.so
%{_libdir}/compiz/libezoom.so
%{_libdir}/compiz/libgrid.so
%{_libdir}/compiz/libimgjpeg.so
%{_libdir}/compiz/libkdecompat.so
%{_libdir}/compiz/libmag.so
%{_libdir}/compiz/libmousepoll.so
%{_libdir}/compiz/libneg.so
%{_libdir}/compiz/libopacify.so
%{_libdir}/compiz/libput.so
%{_libdir}/compiz/libresizeinfo.so
%{_libdir}/compiz/libring.so
%{_libdir}/compiz/libscaleaddon.so
%{_libdir}/compiz/libsession.so
%{_libdir}/compiz/libshift.so
%{_libdir}/compiz/libsnap.so
%{_libdir}/compiz/libstaticswitcher.so
%{_libdir}/compiz/libtext.so
%{_libdir}/compiz/libthumbnail.so
%{_libdir}/compiz/libtitleinfo.so
%{_libdir}/compiz/libvpswitch.so
%{_libdir}/compiz/libwall.so
%{_libdir}/compiz/libwinrules.so
%{_libdir}/compiz/libworkarounds.so
# Compiz plugin data files
%{_datadir}/compiz/animation.xml
%{_datadir}/compiz/colorfilter.xml
%{_datadir}/compiz/colorfilter/data/filters/blackandwhite
%{_datadir}/compiz/colorfilter/data/filters/blueish-filter
%{_datadir}/compiz/colorfilter/data/filters/contrast
%{_datadir}/compiz/colorfilter/data/filters/deuteranopia
%{_datadir}/compiz/colorfilter/data/filters/grayscale
%{_datadir}/compiz/colorfilter/data/filters/negative
%{_datadir}/compiz/colorfilter/data/filters/negative-green
%{_datadir}/compiz/colorfilter/data/filters/protanopia
%{_datadir}/compiz/colorfilter/data/filters/sepia
%{_datadir}/compiz/colorfilter/data/filters/swap-green-blue
%{_datadir}/compiz/colorfilter/data/filters/swap-red-blue
%{_datadir}/compiz/colorfilter/data/filters/swap-red-green
%{_datadir}/compiz/expo.xml
%{_datadir}/compiz/ezoom.xml
%{_datadir}/compiz/grid.xml
%{_datadir}/compiz/imgjpeg.xml
%{_datadir}/compiz/kdecompat.xml
%{_datadir}/compiz/mag.xml
%{_datadir}/compiz/mag/images/Gnome/image.svg
%{_datadir}/compiz/mag/images/Gnome/mask.png
%{_datadir}/compiz/mag/images/Gnome/overlay.png
%{_datadir}/compiz/mag/images/Oxygen/image.svg
%{_datadir}/compiz/mag/images/Oxygen/mask.png
%{_datadir}/compiz/mag/images/Oxygen/overlay.png
%{_datadir}/compiz/mousepoll.xml
%{_datadir}/compiz/neg.xml
%{_datadir}/compiz/opacify.xml
%{_datadir}/compiz/put.xml
%{_datadir}/compiz/resizeinfo.xml
%{_datadir}/compiz/ring.xml
%{_datadir}/compiz/scaleaddon.xml
%{_datadir}/compiz/session.xml
%{_datadir}/compiz/shift.xml
%{_datadir}/compiz/snap.xml
%{_datadir}/compiz/staticswitcher.xml
%{_datadir}/compiz/text.xml
%{_datadir}/compiz/thumbnail.xml
%{_datadir}/compiz/titleinfo.xml
%{_datadir}/compiz/vpswitch.xml
%{_datadir}/compiz/wall.xml
%{_datadir}/compiz/winrules.xml
%{_datadir}/compiz/workarounds.xml
# GConf schemas
%config(noreplace) %{_sysconfdir}/gconf/schemas/compiz-animation.schemas
%config(noreplace) %{_sysconfdir}/gconf/schemas/compiz-colorfilter.schemas
%config(noreplace) %{_sysconfdir}/gconf/schemas/compiz-expo.schemas
%config(noreplace) %{_sysconfdir}/gconf/schemas/compiz-ezoom.schemas
%config(noreplace) %{_sysconfdir}/gconf/schemas/compiz-grid.schemas
%config(noreplace) %{_sysconfdir}/gconf/schemas/compiz-imgjpeg.schemas
%config(noreplace) %{_sysconfdir}/gconf/schemas/compiz-kdecompat.schemas
%config(noreplace) %{_sysconfdir}/gconf/schemas/compiz-mag.schemas
%config(noreplace) %{_sysconfdir}/gconf/schemas/compiz-mousepoll.schemas
%config(noreplace) %{_sysconfdir}/gconf/schemas/compiz-neg.schemas
%config(noreplace) %{_sysconfdir}/gconf/schemas/compiz-opacify.schemas
%config(noreplace) %{_sysconfdir}/gconf/schemas/compiz-put.schemas
%config(noreplace) %{_sysconfdir}/gconf/schemas/compiz-resizeinfo.schemas
%config(noreplace) %{_sysconfdir}/gconf/schemas/compiz-ring.schemas
%config(noreplace) %{_sysconfdir}/gconf/schemas/compiz-scaleaddon.schemas
%config(noreplace) %{_sysconfdir}/gconf/schemas/compiz-session.schemas
%config(noreplace) %{_sysconfdir}/gconf/schemas/compiz-shift.schemas
%config(noreplace) %{_sysconfdir}/gconf/schemas/compiz-snap.schemas
%config(noreplace) %{_sysconfdir}/gconf/schemas/compiz-staticswitcher.schemas
%config(noreplace) %{_sysconfdir}/gconf/schemas/compiz-text.schemas
%config(noreplace) %{_sysconfdir}/gconf/schemas/compiz-thumbnail.schemas
%config(noreplace) %{_sysconfdir}/gconf/schemas/compiz-titleinfo.schemas
%config(noreplace) %{_sysconfdir}/gconf/schemas/compiz-vpswitch.schemas
%config(noreplace) %{_sysconfdir}/gconf/schemas/compiz-wall.schemas
%config(noreplace) %{_sysconfdir}/gconf/schemas/compiz-winrules.schemas
%config(noreplace) %{_sysconfdir}/gconf/schemas/compiz-workarounds.schemas


%files devel
%doc AUTHORS NEWS
# Header files
%{_includedir}/compiz/animation/animation.h
%{_includedir}/compiz/animation/animeffect.h
%{_includedir}/compiz/animation/extensionplugin.h
%{_includedir}/compiz/animation/fade.h
%{_includedir}/compiz/animation/grid.h
%{_includedir}/compiz/animation/gridtransform.h
%{_includedir}/compiz/animation/multi.h
%{_includedir}/compiz/animation/partialwindow.h
%{_includedir}/compiz/animation/persistent.h
%{_includedir}/compiz/animation/point3d.h
%{_includedir}/compiz/animation/screen.h
%{_includedir}/compiz/animation/transform.h
%{_includedir}/compiz/animation/window.h
%{_includedir}/compiz/animation/zoom.h
%{_includedir}/compiz/mousepoll/mousepoll.h
%{_includedir}/compiz/text/text.h
# pkgconfig files
%{_libdir}/pkgconfig/compiz-animation.pc
%{_libdir}/pkgconfig/compiz-mousepoll.pc
%{_libdir}/pkgconfig/compiz-text.pc


%changelog
* Mon Jul 02 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.9.7.0-1.bzr19.0ubuntu10
- Initial release
- Version 0.9.7.0-bzr19
- Ubuntu release 0ubuntu10
