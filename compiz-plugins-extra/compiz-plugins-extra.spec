# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

%define _bzr_rev 9

# For use by my scripts in my git repo
%define _ubuntu_match_rel 0ubuntu6

%define _gconf_schemas compiz-addhelper compiz-animationaddon compiz-bench compiz-bicubic compiz-crashhandler compiz-cubeaddon compiz-extrawm compiz-fadedesktop compiz-firepaint compiz-gears compiz-group compiz-loginout compiz-maximumize compiz-mblur compiz-notification compiz-reflex compiz-scalefilter compiz-shelf compiz-showdesktop compiz-showmouse compiz-splash compiz-td compiz-trailfocus compiz-wallpaper compiz-widget

Name:		compiz-plugins-extra
Version:	0.9.7.0
Release:	1.bzr%{_bzr_rev}%{?dist}
Summary:	Extra Compiz plugins and themes contributed by the community

Group:		User Interface/Desktops
License:	GPLv2 and GPLv3
URL:		https://launchpad.net/compiz-plugins-extra
Source0:	https://launchpad.net/ubuntu/+archive/primary/+files/compiz-plugins-extra_%{version}~bzr%{_bzr_rev}.orig.tar.bz2

BuildRequires:	cmake
BuildRequires:	gcc-c++
BuildRequires:	intltool

BuildRequires:	boost-devel
BuildRequires:	cairo-devel
BuildRequires:	compiz-devel
BuildRequires:	compiz-plugins-main-devel
BuildRequires:	dbus-devel
BuildRequires:	gtk2-devel
BuildRequires:	libjpeg-turbo-devel
BuildRequires:	libnotify-devel
BuildRequires:	librsvg2-devel
BuildRequires:	libSM-devel
BuildRequires:	libxslt-devel
BuildRequires:	mesa-libGLU-devel

BuildRequires:	GConf2
Requires(pre):	GConf2
Requires(post):	GConf2
Requires(preun):	GConf2

%description
This package provides extra plugins and themes contributed by the community
giving a rich desktop experience.


%prep
%setup -q


%build
mkdir build
cd build
%cmake .. \
  -DCOMPIZ_BUILD_WITH_RPATH=FALSE

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


%postun
if [ ${1} -eq 0 ]; then
  glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :
fi


%posttrans
glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :


%files
%doc AUTHORS NEWS
# Compiz plugins
%{_libdir}/compiz/libaddhelper.so
%{_libdir}/compiz/libanimationaddon.so
%{_libdir}/compiz/libbench.so
%{_libdir}/compiz/libbicubic.so
%{_libdir}/compiz/libcrashhandler.so
%{_libdir}/compiz/libcubeaddon.so
%{_libdir}/compiz/libextrawm.so
%{_libdir}/compiz/libfadedesktop.so
%{_libdir}/compiz/libfirepaint.so
%{_libdir}/compiz/libgears.so
%{_libdir}/compiz/libgroup.so
%{_libdir}/compiz/libloginout.so
%{_libdir}/compiz/libmaximumize.so
%{_libdir}/compiz/libmblur.so
%{_libdir}/compiz/libnotification.so
%{_libdir}/compiz/libreflex.so
%{_libdir}/compiz/libscalefilter.so
%{_libdir}/compiz/libshelf.so
%{_libdir}/compiz/libshowdesktop.so
%{_libdir}/compiz/libshowmouse.so
%{_libdir}/compiz/libsplash.so
%{_libdir}/compiz/libtd.so
%{_libdir}/compiz/libtrailfocus.so
%{_libdir}/compiz/libwallpaper.so
%{_libdir}/compiz/libwidget.so
# Compiz plugin data files
%{_datadir}/compiz/addhelper.xml
%{_datadir}/compiz/animationaddon.xml
%{_datadir}/compiz/bench.xml
%{_datadir}/compiz/bicubic.xml
%{_datadir}/compiz/crashhandler.xml
%{_datadir}/compiz/cubeaddon.xml
%{_datadir}/compiz/cubeaddon/images/compizcap.png
%{_datadir}/compiz/cubeaddon/images/cubecap_release.png
%{_datadir}/compiz/cubeaddon/images/fusioncap.png
%{_datadir}/compiz/extrawm.xml
%{_datadir}/compiz/fadedesktop.xml
%{_datadir}/compiz/firepaint.xml
%{_datadir}/compiz/gears.xml
%{_datadir}/compiz/group.xml
%{_datadir}/compiz/loginout.xml
%{_datadir}/compiz/maximumize.xml
%{_datadir}/compiz/mblur.xml
%{_datadir}/compiz/notification.xml
%{_datadir}/compiz/notification/images/compiz.png
%{_datadir}/compiz/reflex.xml
%{_datadir}/compiz/reflex/images/reflection.png
%{_datadir}/compiz/scalefilter.xml
%{_datadir}/compiz/shelf.xml
%{_datadir}/compiz/showdesktop.xml
%{_datadir}/compiz/showmouse.xml
%{_datadir}/compiz/showmouse/images/Star.png
%{_datadir}/compiz/splash.xml
%{_datadir}/compiz/splash/images/splash_background.png
%{_datadir}/compiz/splash/images/splash_logo.png
%{_datadir}/compiz/td.xml
%{_datadir}/compiz/trailfocus.xml
%{_datadir}/compiz/wallpaper.xml
%{_datadir}/compiz/widget.xml
# GConf schemas
%config(noreplace) %{_sysconfdir}/gconf/schemas/compiz-addhelper.schemas
%config(noreplace) %{_sysconfdir}/gconf/schemas/compiz-animationaddon.schemas
%config(noreplace) %{_sysconfdir}/gconf/schemas/compiz-bench.schemas
%config(noreplace) %{_sysconfdir}/gconf/schemas/compiz-bicubic.schemas
%config(noreplace) %{_sysconfdir}/gconf/schemas/compiz-crashhandler.schemas
%config(noreplace) %{_sysconfdir}/gconf/schemas/compiz-cubeaddon.schemas
%config(noreplace) %{_sysconfdir}/gconf/schemas/compiz-extrawm.schemas
%config(noreplace) %{_sysconfdir}/gconf/schemas/compiz-fadedesktop.schemas
%config(noreplace) %{_sysconfdir}/gconf/schemas/compiz-firepaint.schemas
%config(noreplace) %{_sysconfdir}/gconf/schemas/compiz-gears.schemas
%config(noreplace) %{_sysconfdir}/gconf/schemas/compiz-group.schemas
%config(noreplace) %{_sysconfdir}/gconf/schemas/compiz-loginout.schemas
%config(noreplace) %{_sysconfdir}/gconf/schemas/compiz-maximumize.schemas
%config(noreplace) %{_sysconfdir}/gconf/schemas/compiz-mblur.schemas
%config(noreplace) %{_sysconfdir}/gconf/schemas/compiz-notification.schemas
%config(noreplace) %{_sysconfdir}/gconf/schemas/compiz-reflex.schemas
%config(noreplace) %{_sysconfdir}/gconf/schemas/compiz-scalefilter.schemas
%config(noreplace) %{_sysconfdir}/gconf/schemas/compiz-shelf.schemas
%config(noreplace) %{_sysconfdir}/gconf/schemas/compiz-showdesktop.schemas
%config(noreplace) %{_sysconfdir}/gconf/schemas/compiz-showmouse.schemas
%config(noreplace) %{_sysconfdir}/gconf/schemas/compiz-splash.schemas
%config(noreplace) %{_sysconfdir}/gconf/schemas/compiz-td.schemas
%config(noreplace) %{_sysconfdir}/gconf/schemas/compiz-trailfocus.schemas
%config(noreplace) %{_sysconfdir}/gconf/schemas/compiz-wallpaper.schemas
%config(noreplace) %{_sysconfdir}/gconf/schemas/compiz-widget.schemas
# GSettings schemas
%{_datadir}/glib-2.0/schemas/org.freedesktop.compiz.addhelper.gschema.xml
%{_datadir}/glib-2.0/schemas/org.freedesktop.compiz.animationaddon.gschema.xml
%{_datadir}/glib-2.0/schemas/org.freedesktop.compiz.bench.gschema.xml
%{_datadir}/glib-2.0/schemas/org.freedesktop.compiz.bicubic.gschema.xml
%{_datadir}/glib-2.0/schemas/org.freedesktop.compiz.crashhandler.gschema.xml
%{_datadir}/glib-2.0/schemas/org.freedesktop.compiz.cubeaddon.gschema.xml
%{_datadir}/glib-2.0/schemas/org.freedesktop.compiz.extrawm.gschema.xml
%{_datadir}/glib-2.0/schemas/org.freedesktop.compiz.fadedesktop.gschema.xml
%{_datadir}/glib-2.0/schemas/org.freedesktop.compiz.firepaint.gschema.xml
%{_datadir}/glib-2.0/schemas/org.freedesktop.compiz.gears.gschema.xml
%{_datadir}/glib-2.0/schemas/org.freedesktop.compiz.group.gschema.xml
%{_datadir}/glib-2.0/schemas/org.freedesktop.compiz.loginout.gschema.xml
%{_datadir}/glib-2.0/schemas/org.freedesktop.compiz.maximumize.gschema.xml
%{_datadir}/glib-2.0/schemas/org.freedesktop.compiz.mblur.gschema.xml
%{_datadir}/glib-2.0/schemas/org.freedesktop.compiz.notification.gschema.xml
%{_datadir}/glib-2.0/schemas/org.freedesktop.compiz.reflex.gschema.xml
%{_datadir}/glib-2.0/schemas/org.freedesktop.compiz.scalefilter.gschema.xml
%{_datadir}/glib-2.0/schemas/org.freedesktop.compiz.shelf.gschema.xml
%{_datadir}/glib-2.0/schemas/org.freedesktop.compiz.showdesktop.gschema.xml
%{_datadir}/glib-2.0/schemas/org.freedesktop.compiz.showmouse.gschema.xml
%{_datadir}/glib-2.0/schemas/org.freedesktop.compiz.splash.gschema.xml
%{_datadir}/glib-2.0/schemas/org.freedesktop.compiz.td.gschema.xml
%{_datadir}/glib-2.0/schemas/org.freedesktop.compiz.trailfocus.gschema.xml
%{_datadir}/glib-2.0/schemas/org.freedesktop.compiz.wallpaper.gschema.xml
%{_datadir}/glib-2.0/schemas/org.freedesktop.compiz.widget.gschema.xml
# Ubuntu doesn't split the following development files into a '-dev' package,
# so we won't either
%{_includedir}/compiz/animationaddon/animationaddon.h
%{_libdir}/pkgconfig/compiz-animationaddon.pc



%changelog
* Mon Jul 02 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.9.7.0-1.bzr9
- Initial release
- Version 0.9.7.0~bzr9
