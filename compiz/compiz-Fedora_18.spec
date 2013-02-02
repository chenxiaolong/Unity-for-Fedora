# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

# The KDE parts of Compiz are disabled as they no longer work with KDE 4.8

# Do not provide the Python 2 binding library
%filter_provides_in %{python_sitearch}/compizconfig\.so$
%filter_setup

%define _gconf_schemas_obsolete compiz-animationaddon compiz-bicubic compiz-blur compiz-colorfilter compiz-cubeaddon compiz-gears compiz-group compiz-loginout compiz-reflex compiz-stackswitch compiz-thumbnail compiz-trip compiz-wallpaper
%define _gconf_schemas compiz-addhelper compiz-animation compiz-annotate compiz-bench compiz-ccp compiz-clone compiz-commands compiz-compiztoolbox compiz-composite compiz-copytex compiz-core compiz-crashhandler compiz-cube compiz-dbus compiz-decor compiz-expo compiz-extrawm compiz-ezoom compiz-fadedesktop compiz-fade compiz-firepaint compiz-gnomecompat compiz-grid compiz-imgjpeg compiz-imgpng compiz-imgsvg compiz-inotify compiz-kdecompat compiz-mag compiz-maximumize compiz-mblur compiz-mousepoll compiz-move compiz-neg compiz-notification compiz-obs compiz-opacify compiz-opengl compiz-place compiz-put compiz-regex compiz-resizeinfo compiz-resize compiz-ring compiz-rotate compiz-scaleaddon compiz-scalefilter compiz-scale compiz-screenshot compiz-session compiz-shelf compiz-shift compiz-showdesktop compiz-showmouse compiz-showrepaint compiz-snap compiz-splash compiz-staticswitcher compiz-switcher compiz-td compiz-text compiz-titleinfo compiz-trailfocus compiz-vpswitch compiz-wall compiz-water compiz-widget compiz-winrules compiz-wobbly compiz-workarounds compiz-workspacenames gwd

%define _ubuntu_rel 0ubuntu1
%define _compiz_abi 20121210
%define _disguised_as 0.9.9.0

Name:		compiz
Version:	0.9.9~daily13.01.25
Release:	1.%{_ubuntu_rel}%{?dist}
Summary:	OpenGL compositing window manager

Group:		User Interface/X
License:	GPLv2+
URL:		https://launchpad.net/compiz

Source0:	https://launchpad.net/ubuntu/+archive/primary/+files/compiz_%{version}.orig.tar.gz

# Script to reset all of Compiz's settings
Source2:	compiz.reset

Source99:	https://launchpad.net/ubuntu/+archive/primary/+files/compiz_%{version}-%{_ubuntu_rel}.diff.gz

# Do not hardcode /lib/ when setting PKG_CONFIG_PATH in FindCompiz.cmake
Patch0:		0001_Fix_library_directory_F18.patch

# Fix the directory for FindCompiz.cmake and FindCompizConfig.cmake
Patch1:		0002_Fix_cmake_install_dir_F18.patch

# Compiz's build system appends --install-layout=deb to the python install
# command (for python-compizconfig and ccsm) whether or not COMPIZ_DEB_BUILD is
# set to 1
Patch2:		0003_Fix_python_install_command.patch

# Install GSettings backend to libdir
Patch3:		0004_Fix_gsettings_backend_libdir_F18.patch

# Put profile conversion files in /usr/share instead of /usr/lib
Patch4:		0005_Convert_files_libdir_to_datadir.patch

# Make sure everything is installed to the proper libdir
Patch5:		0006_Fix_remaining_libdir_issues.patch

BuildRequires:	cmake
BuildRequires:	desktop-file-utils
BuildRequires:	gettext
BuildRequires:	intltool
BuildRequires:	libtool
BuildRequires:	pkgconfig

BuildRequires:	boost-devel
BuildRequires:	libjpeg-turbo-devel
BuildRequires:	metacity-devel

BuildRequires:	pkgconfig(cairo)
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(glibmm-2.4)
BuildRequires:	pkgconfig(glproto)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(gnome-keybindings)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(ice)
BuildRequires:	pkgconfig(libnotify)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(librsvg-2.0)
BuildRequires:	pkgconfig(libstartup-notification-1.0)
BuildRequires:	pkgconfig(libwnck-1.0)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(libxslt)
BuildRequires:	pkgconfig(pango)
BuildRequires:	pkgconfig(protobuf)
BuildRequires:	pkgconfig(python2)
BuildRequires:	pkgconfig(sm)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xcomposite)
BuildRequires:	pkgconfig(xcursor)
BuildRequires:	pkgconfig(xdamage)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xfixes)
BuildRequires:	pkgconfig(xinerama)
BuildRequires:	pkgconfig(xrandr)
BuildRequires:	pkgconfig(xrender)

BuildRequires:	Pyrex

Provides:	compiz-ABI = %{_compiz_abi}

%description
Compiz is an OpenGL compositing manager that uses GLX_EXT_texture_from_pixmap
for binding redirected top-level windows to texture objects. It has a flexible
plug-in system and it is designed to run well on most graphics hardware.


%package devel
Summary:	Development files for compiz
Group:		Development/Libraries
License:	MIT and X

Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	pkgconfig(gl)
Requires:	pkgconfig(glib-2.0)
Requires:	pkgconfig(glibmm-2.4)
Requires:	pkgconfig(gtk+-3.0)
Requires:	pkgconfig(ice)
Requires:	pkgconfig(libpng)
Requires:	pkgconfig(libstartup-notification-1.0)
Requires:	pkgconfig(libxml-2.0)
Requires:	pkgconfig(libxslt)
Requires:	pkgconfig(sm)
Requires:	pkgconfig(x11)
Requires:	pkgconfig(xcomposite)
Requires:	pkgconfig(xcursor)
Requires:	pkgconfig(xdamage)
Requires:	pkgconfig(xfixes)
Requires:	pkgconfig(xinerama)
Requires:	pkgconfig(xrandr)

%description devel
This packages contains the development files for creating Compiz plugins.


%package gnome
Summary:	OpenGL compositing window manager - GNOME support
Group:		User Interface/X

License:	LGPLv2+

Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	control-center-filesystem

# gtk-window-decorator reads its settings from metacity and mutter
Requires:	metacity >= 2.34.1
Requires:	mutter

Requires(preun):	GConf2

# Required for GSettings schemas
Requires:	gsettings-desktop-schemas

%description gnome
This package contains the GNOME window decorator and GNOME support files for
Compiz.


%package plugins
Summary:	OpenGL compositing window manager - Plugins
Group:		User Interface/X
License:	GPLv2+ and LGPLv2+ and MIT and X

Requires:	%{name}%{?_isa} = %{version}-%{release}

%description plugins
This package contains the set of plugins from the Compiz project.

This package replaces the previous compiz-plugins-main and compiz-plugins-extra
packages as the plugins are no longer separated upstream.


%package -n libcompizconfig
Summary:	OpenGL compositing window manager - Settings library
Group:		System Environment/Libraries
License:	LGPLv2+

Requires:	%{name}%{?_isa} = %{version}-%{release}

%description -n libcompizconfig
This package contains the library for configuring Compiz plugins' settings.


%package -n libcompizconfig-devel
Summary:	Development files for libcompizconfig
Group:		Development/Libraries
License:	LGPLv2+

Requires:	libcompizconfig%{?_isa} = %{version}-%{release}
Requires:	compiz-devel%{_isa} = %{version}-%{release}

%description -n libcompizconfig-devel
This package contains the development files for creating Compiz plugins with
settings support.


%package -n python-compizconfig
Summary:	OpenGL compositing window manager - Python 2 compizconfig bindings
Group:		System Environment/Libraries
License:	LGPLv2+

%description -n python-compizconfig
This package contains the Python 2 bindings for the compizconfig library.


%package -n ccsm
Summary:	OpenGL compositing window manager - Configuration manager
Group:		User Interface/X

BuildArch:	noarch

Requires:	%{name} = %{version}-%{release}
Requires:	python-compizconfig = %{version}-%{release}
Requires:	pygtk2

%description -n ccsm
This package contains the Compiz configuration manager for modifying Compiz and
its plugins' settings.


%prep
%setup -q

%patch0 -p1 -b .pkg_config_path
%patch1 -p1 -b .cmake_install_dir
%patch2 -p1 -b .py_install_command
%patch3 -p1 -b .backend_libdir
%patch4 -p1 -b .convert_files_datadir
%patch5 -p1 -b .remaining_libdir

# Apply Ubuntu's patches
zcat '%{SOURCE99}' | patch -Np1
for i in $(grep -v '#' debian/patches/series); do
  patch -Np1 -i "debian/patches/${i}"
done


%build
mkdir build
cd build

# Disable rpath in Python 2 bindings
export COMPIZ_DISABLE_RPATH=1

%cmake .. \
  -DCOMPIZ_BUILD_WITH_RPATH=FALSE \
  -DCOMPIZ_DEFAULT_PLUGINS="ccp" \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  -DCOMPIZ_PACKAGING_ENABLED=TRUE \
  -DUSE_GSETTINGS=ON \
  -DUSE_GCONF=OFF \
  -DCOMPIZ_DISABLE_GS_SCHEMAS_INSTALL=OFF \
  -DCOMPIZ_BUILD_TESTING=OFF \
  -DCOMPIZ_DISABLE_PLUGIN_KDE=ON \
  -DUSE_KDE4=OFF \
  -DBUILD_SHARED_LIBS:BOOL=OFF

make %{?_smp_mflags}


%install
cd build
GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 make install DESTDIR=$RPM_BUILD_ROOT

# make findcompiz_install does not work, so we'll install it manually
install -dm755 $RPM_BUILD_ROOT%{_datadir}/cmake/Modules/
install -m644 ../cmake/FindCompiz.cmake \
  $RPM_BUILD_ROOT%{_datadir}/cmake/Modules/

# Install Ubuntu's files
install -dm755 $RPM_BUILD_ROOT%{_mandir}/man1/
install -dm755 $RPM_BUILD_ROOT%{_sysconfdir}/X11/xinit/xinitrc.d/
install -dm755 $RPM_BUILD_ROOT%{_sysconfdir}/compizconfig/upgrades/
install -dm755 $RPM_BUILD_ROOT%{_datadir}/gnome/wm-properties/

# Install manual pages
install -m644 \
  ../debian/{ccsm,compiz,gtk-window-decorator}.1 \
  $RPM_BUILD_ROOT%{_mandir}/man1/

# Window manager desktop file for GNOME
install -m644 $RPM_BUILD_ROOT%{_datadir}/applications/compiz.desktop \
              $RPM_BUILD_ROOT%{_datadir}/gnome/wm-properties/

# Install X11 startup script
install -m755 ../debian/65compiz_profile-on-session \
              $RPM_BUILD_ROOT%{_sysconfdir}/X11/xinit/xinitrc.d/

# Fix rpmlint error script-without-shebang
sed -i '1 i #!/usr/bin/bash' \
  $RPM_BUILD_ROOT%{_sysconfdir}/X11/xinit/xinitrc.d/65compiz_profile-on-session

# Unity Compiz profile configuration file
install -m644 ../debian/unity.ini $RPM_BUILD_ROOT%{_sysconfdir}/compizconfig/

# Install Compiz profile configuration file
install -m644 ../debian/config $RPM_BUILD_ROOT%{_sysconfdir}/compizconfig/

# Compiz profile upgrade helper files for ensuring smooth upgrades from older
# configuration files
pushd ../debian/profile_upgrades/
find . -type f -name '*.upgrade' -exec \
  install -m644 {} $RPM_BUILD_ROOT%{_sysconfdir}/compizconfig/upgrades/{} \;
popd

install -dm755 $RPM_BUILD_ROOT%{_datadir}/compiz/migration/
pushd ../postinst/convert-files/
find . -type f -name '*.convert' -exec \
  install -m644 {} $RPM_BUILD_ROOT%{_datadir}/compiz/migration/{} \;
popd

# Install keybinding files
install -dm755 $RPM_BUILD_ROOT%{_datadir}/gnome-control-center/keybindings/
install -m644 gtk/gnome/50-*.xml \
  $RPM_BUILD_ROOT%{_datadir}/gnome-control-center/keybindings/

# Install script for resetting all of Compiz's settings
install -m755 '%{SOURCE2}' $RPM_BUILD_ROOT%{_bindir}/compiz.reset

# Default GSettings settings
install -m644 ../debian/compiz-gnome.gsettings-override \
  $RPM_BUILD_ROOT%{_datadir}/glib-2.0/schemas/10_compiz-ubuntu.gschema.override

# Validate desktop files
desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/compiz.desktop
desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/ccsm.desktop

# Fix dependency on '/bin/python' in ccsm
sed -i '/#!/ s|^.*$|#!/usr/bin/env python2|' $RPM_BUILD_ROOT%{_bindir}/ccsm

# Remove GConf schemas
rm -v $RPM_BUILD_ROOT%{_datadir}/gconf/schemas/*.schemas

# Ugly libdir hack
if [ "%{_libdir}" != "%{_prefix}/lib" ]; then
  mv $RPM_BUILD_ROOT%{_prefix}/lib/python2.7/site-packages/compizconfig_python-%{_disguised_as}-py2.7.egg-info \
     $RPM_BUILD_ROOT%{_libdir}/python2.7/site-packages/
fi

%find_lang compiz
%find_lang ccsm


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%post -n libcompizconfig -p /sbin/ldconfig

%postun -n libcompizconfig -p /sbin/ldconfig


%preun gnome
%gconf_schema_remove %{_gconf_schemas}

%postun gnome
if [ ${1} -eq 0 ] ; then
  glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans gnome
glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :


%files -f build/compiz.lang
%doc AUTHORS NEWS README
%{_bindir}/compiz
%{_bindir}/compiz.reset
%{_bindir}/compiz-decorator
# Manual pages
%{_mandir}/man1/compiz.1.gz
# Compiz libraries
%{_libdir}/libcompiz_core.so.%{_disguised_as}
%{_libdir}/libcompiz_core.so.ABI-%{_compiz_abi}
%{_libdir}/libdecoration.so.0
%{_libdir}/libdecoration.so.0.0.0
# Desktop file
%{_datadir}/applications/compiz.desktop


%files devel
%{_libdir}/libcompiz_core.so
%{_libdir}/libdecoration.so
# Header files
%dir %{_includedir}/compiz/
%dir %{_includedir}/compiz/animation/
%dir %{_includedir}/compiz/compiztoolbox/
%dir %{_includedir}/compiz/composite/
%dir %{_includedir}/compiz/core/
%dir %{_includedir}/compiz/cube/
%dir %{_includedir}/compiz/mousepoll/
%dir %{_includedir}/compiz/opengl/
%dir %{_includedir}/compiz/scale/
%dir %{_includedir}/compiz/text/
%{_includedir}/compiz/animation/*.h
%{_includedir}/compiz/compiztoolbox/compiztoolbox.h
%{_includedir}/compiz/composite/composite.h
%{_includedir}/compiz/core/*.h
%{_includedir}/compiz/cube/cube.h
%{_includedir}/compiz/decoration.h
%{_includedir}/compiz/mousepoll/mousepoll.h
%{_includedir}/compiz/opengl/*.h
%{_includedir}/compiz/scale/scale.h
%{_includedir}/compiz/text/text.h
# pkgconfig files
%{_libdir}/pkgconfig/compiz-animation.pc
%{_libdir}/pkgconfig/compiz-compiztoolbox.pc
%{_libdir}/pkgconfig/compiz-composite.pc
%{_libdir}/pkgconfig/compiz-cube.pc
%{_libdir}/pkgconfig/compiz-mousepoll.pc
%{_libdir}/pkgconfig/compiz-opengl.pc
%{_libdir}/pkgconfig/compiz-scale.pc
%{_libdir}/pkgconfig/compiz-text.pc
%{_libdir}/pkgconfig/compiz.pc
%{_libdir}/pkgconfig/libdecoration.pc
# xslt files
%dir %{_datadir}/compiz/
%dir %{_datadir}/compiz/xslt/
%{_datadir}/compiz/xslt/bcop.xslt
%{_datadir}/compiz/xslt/compiz_gsettings_schemas.xslt
# CMake files
%dir %{_datadir}/cmake/
%dir %{_datadir}/cmake/Modules/
%{_datadir}/cmake/Modules/FindCompiz.cmake
%{_datadir}/cmake/Modules/FindOpenGLES2.cmake
%dir %{_datadir}/compiz/cmake/
%{_datadir}/compiz/cmake/CompizBcop.cmake
%{_datadir}/compiz/cmake/CompizCommon.cmake
%{_datadir}/compiz/cmake/CompizDefaults.cmake
%{_datadir}/compiz/cmake/CompizGSettings.cmake
%{_datadir}/compiz/cmake/CompizPackage.cmake
%{_datadir}/compiz/cmake/CompizPlugin.cmake
%{_datadir}/compiz/cmake/copy_file_install_user_env.cmake
%{_datadir}/compiz/cmake/recompile_gsettings_schemas_in_dir_user_env.cmake
%dir %{_datadir}/compiz/cmake/plugin_extensions/
%{_datadir}/compiz/cmake/plugin_extensions/CompizGenGSettings.cmake
%{_datadir}/compiz/cmake/plugin_extensions/CompizGenInstallData.cmake
%{_datadir}/compiz/cmake/plugin_extensions/CompizGenInstallImages.cmake
%{_datadir}/compiz/cmake/plugin_extensions/CompizOpenGLFixups.cmake


%files gnome
%{_bindir}/gtk-window-decorator
# Manual page
%{_mandir}/man1/gtk-window-decorator.1.gz
# Compiz configuration backends
%dir %{_libdir}/compizconfig/
%dir %{_libdir}/compizconfig/backends/
%{_libdir}/compizconfig/backends/libgsettings.so
%{_libdir}/libcompizconfig_gsettings_backend.so
# X11 session script
%{_sysconfdir}/X11/xinit/xinitrc.d/65compiz_profile-on-session
# Compiz Unity profile configuration file
%dir %{_sysconfdir}/compizconfig/
%config(noreplace) %{_sysconfdir}/compizconfig/unity.ini
# GNOME window manager desktop file
%{_datadir}/gnome/wm-properties/compiz.desktop
# Compiz profile upgrade helper files
%dir %{_sysconfdir}/compizconfig/upgrades/
%{_sysconfdir}/compizconfig/upgrades/com.canonical.unity.unity.01.upgrade
%{_sysconfdir}/compizconfig/upgrades/com.canonical.unity.unity.02.upgrade
%dir %{_datadir}/compiz/migration/
%{_datadir}/compiz/migration/compiz-profile-Default.convert
%{_datadir}/compiz/migration/compiz-profile-active-Default.convert
%{_datadir}/compiz/migration/compiz-profile-independent-keys.convert
# GNOME Control Center keybinding files
%{_datadir}/gnome-control-center/keybindings/50-compiz-navigation.xml
%{_datadir}/gnome-control-center/keybindings/50-compiz-windows.xml
# GSettings schemas
%{_datadir}/glib-2.0/schemas/org.compiz.addhelper.gschema.xml
%{_datadir}/glib-2.0/schemas/org.compiz.animation.gschema.xml
%{_datadir}/glib-2.0/schemas/org.compiz.annotate.gschema.xml
%{_datadir}/glib-2.0/schemas/org.compiz.bench.gschema.xml
%{_datadir}/glib-2.0/schemas/org.compiz.ccp.gschema.xml
%{_datadir}/glib-2.0/schemas/org.compiz.clone.gschema.xml
%{_datadir}/glib-2.0/schemas/org.compiz.commands.gschema.xml
%{_datadir}/glib-2.0/schemas/org.compiz.compiztoolbox.gschema.xml
%{_datadir}/glib-2.0/schemas/org.compiz.composite.gschema.xml
%{_datadir}/glib-2.0/schemas/org.compiz.copytex.gschema.xml
%{_datadir}/glib-2.0/schemas/org.compiz.core.gschema.xml
%{_datadir}/glib-2.0/schemas/org.compiz.crashhandler.gschema.xml
%{_datadir}/glib-2.0/schemas/org.compiz.cube.gschema.xml
%{_datadir}/glib-2.0/schemas/org.compiz.cubeaddon.gschema.xml
%{_datadir}/glib-2.0/schemas/org.compiz.dbus.gschema.xml
%{_datadir}/glib-2.0/schemas/org.compiz.decor.gschema.xml
%{_datadir}/glib-2.0/schemas/org.compiz.expo.gschema.xml
%{_datadir}/glib-2.0/schemas/org.compiz.extrawm.gschema.xml
%{_datadir}/glib-2.0/schemas/org.compiz.ezoom.gschema.xml
%{_datadir}/glib-2.0/schemas/org.compiz.fade.gschema.xml
%{_datadir}/glib-2.0/schemas/org.compiz.fadedesktop.gschema.xml
%{_datadir}/glib-2.0/schemas/org.compiz.firepaint.gschema.xml
%{_datadir}/glib-2.0/schemas/org.compiz.gnomecompat.gschema.xml
%{_datadir}/glib-2.0/schemas/org.compiz.grid.gschema.xml
%{_datadir}/glib-2.0/schemas/org.compiz.gwd.gschema.xml
%{_datadir}/glib-2.0/schemas/org.compiz.gschema.xml
%{_datadir}/glib-2.0/schemas/org.compiz.imgjpeg.gschema.xml
%{_datadir}/glib-2.0/schemas/org.compiz.imgpng.gschema.xml
%{_datadir}/glib-2.0/schemas/org.compiz.imgsvg.gschema.xml
%{_datadir}/glib-2.0/schemas/org.compiz.inotify.gschema.xml
%{_datadir}/glib-2.0/schemas/org.compiz.integrated.gschema.xml
%{_datadir}/glib-2.0/schemas/org.compiz.kdecompat.gschema.xml
%{_datadir}/glib-2.0/schemas/org.compiz.mag.gschema.xml
%{_datadir}/glib-2.0/schemas/org.compiz.maximumize.gschema.xml
%{_datadir}/glib-2.0/schemas/org.compiz.mblur.gschema.xml
%{_datadir}/glib-2.0/schemas/org.compiz.mousepoll.gschema.xml
%{_datadir}/glib-2.0/schemas/org.compiz.move.gschema.xml
%{_datadir}/glib-2.0/schemas/org.compiz.neg.gschema.xml
%{_datadir}/glib-2.0/schemas/org.compiz.notification.gschema.xml
%{_datadir}/glib-2.0/schemas/org.compiz.obs.gschema.xml
%{_datadir}/glib-2.0/schemas/org.compiz.opacify.gschema.xml
%{_datadir}/glib-2.0/schemas/org.compiz.opengl.gschema.xml
%{_datadir}/glib-2.0/schemas/org.compiz.place.gschema.xml
%{_datadir}/glib-2.0/schemas/org.compiz.put.gschema.xml
%{_datadir}/glib-2.0/schemas/org.compiz.regex.gschema.xml
%{_datadir}/glib-2.0/schemas/org.compiz.resize.gschema.xml
%{_datadir}/glib-2.0/schemas/org.compiz.resizeinfo.gschema.xml
%{_datadir}/glib-2.0/schemas/org.compiz.ring.gschema.xml
%{_datadir}/glib-2.0/schemas/org.compiz.rotate.gschema.xml
%{_datadir}/glib-2.0/schemas/org.compiz.scale.gschema.xml
%{_datadir}/glib-2.0/schemas/org.compiz.scaleaddon.gschema.xml
%{_datadir}/glib-2.0/schemas/org.compiz.scalefilter.gschema.xml
%{_datadir}/glib-2.0/schemas/org.compiz.screenshot.gschema.xml
%{_datadir}/glib-2.0/schemas/org.compiz.session.gschema.xml
%{_datadir}/glib-2.0/schemas/org.compiz.shelf.gschema.xml
%{_datadir}/glib-2.0/schemas/org.compiz.shift.gschema.xml
%{_datadir}/glib-2.0/schemas/org.compiz.showdesktop.gschema.xml
%{_datadir}/glib-2.0/schemas/org.compiz.showmouse.gschema.xml
%{_datadir}/glib-2.0/schemas/org.compiz.showrepaint.gschema.xml
%{_datadir}/glib-2.0/schemas/org.compiz.snap.gschema.xml
%{_datadir}/glib-2.0/schemas/org.compiz.splash.gschema.xml
%{_datadir}/glib-2.0/schemas/org.compiz.staticswitcher.gschema.xml
%{_datadir}/glib-2.0/schemas/org.compiz.switcher.gschema.xml
%{_datadir}/glib-2.0/schemas/org.compiz.td.gschema.xml
%{_datadir}/glib-2.0/schemas/org.compiz.text.gschema.xml
%{_datadir}/glib-2.0/schemas/org.compiz.thumbnail.gschema.xml
%{_datadir}/glib-2.0/schemas/org.compiz.titleinfo.gschema.xml
%{_datadir}/glib-2.0/schemas/org.compiz.trailfocus.gschema.xml
%{_datadir}/glib-2.0/schemas/org.compiz.vpswitch.gschema.xml
%{_datadir}/glib-2.0/schemas/org.compiz.wall.gschema.xml
%{_datadir}/glib-2.0/schemas/org.compiz.wallpaper.gschema.xml
%{_datadir}/glib-2.0/schemas/org.compiz.water.gschema.xml
%{_datadir}/glib-2.0/schemas/org.compiz.widget.gschema.xml
%{_datadir}/glib-2.0/schemas/org.compiz.winrules.gschema.xml
%{_datadir}/glib-2.0/schemas/org.compiz.wizard.gschema.xml
%{_datadir}/glib-2.0/schemas/org.compiz.wobbly.gschema.xml
%{_datadir}/glib-2.0/schemas/org.compiz.workarounds.gschema.xml
%{_datadir}/glib-2.0/schemas/org.compiz.workspacenames.gschema.xml
# GSettings defaults
%{_datadir}/glib-2.0/schemas/10_compiz-ubuntu.gschema.override


%files plugins
%dir %{_libdir}/compiz/
%{_libdir}/compiz/libaddhelper.so
%{_libdir}/compiz/libanimation.so
%{_libdir}/compiz/libannotate.so
%{_libdir}/compiz/libbench.so
%{_libdir}/compiz/libclone.so
%{_libdir}/compiz/libcommands.so
%{_libdir}/compiz/libcompiztoolbox.so
%{_libdir}/compiz/libcomposite.so
%{_libdir}/compiz/libcopytex.so
%{_libdir}/compiz/libcrashhandler.so
%{_libdir}/compiz/libcube.so
%{_libdir}/compiz/libcubeaddon.so
%{_libdir}/compiz/libdbus.so
%{_libdir}/compiz/libdecor.so
%{_libdir}/compiz/libexpo.so
%{_libdir}/compiz/libextrawm.so
%{_libdir}/compiz/libezoom.so
%{_libdir}/compiz/libfade.so
%{_libdir}/compiz/libfadedesktop.so
%{_libdir}/compiz/libfirepaint.so
%{_libdir}/compiz/libgnomecompat.so
%{_libdir}/compiz/libgrid.so
%{_libdir}/compiz/libimgjpeg.so
%{_libdir}/compiz/libimgpng.so
%{_libdir}/compiz/libimgsvg.so
%{_libdir}/compiz/libinotify.so
%{_libdir}/compiz/libkdecompat.so
%{_libdir}/compiz/libmag.so
%{_libdir}/compiz/libmaximumize.so
%{_libdir}/compiz/libmblur.so
%{_libdir}/compiz/libmousepoll.so
%{_libdir}/compiz/libmove.so
%{_libdir}/compiz/libneg.so
%{_libdir}/compiz/libnotification.so
%{_libdir}/compiz/libobs.so
%{_libdir}/compiz/libopacify.so
%{_libdir}/compiz/libopengl.so
%{_libdir}/compiz/libplace.so
%{_libdir}/compiz/libput.so
%{_libdir}/compiz/libregex.so
%{_libdir}/compiz/libresize.so
%{_libdir}/compiz/libresizeinfo.so
%{_libdir}/compiz/libring.so
%{_libdir}/compiz/librotate.so
%{_libdir}/compiz/libscale.so
%{_libdir}/compiz/libscaleaddon.so
%{_libdir}/compiz/libscalefilter.so
%{_libdir}/compiz/libscreenshot.so
%{_libdir}/compiz/libsession.so
%{_libdir}/compiz/libshelf.so
%{_libdir}/compiz/libshift.so
%{_libdir}/compiz/libshowdesktop.so
%{_libdir}/compiz/libshowmouse.so
%{_libdir}/compiz/libshowrepaint.so
%{_libdir}/compiz/libsnap.so
%{_libdir}/compiz/libsplash.so
%{_libdir}/compiz/libstaticswitcher.so
%{_libdir}/compiz/libswitcher.so
%{_libdir}/compiz/libtd.so
%{_libdir}/compiz/libtext.so
%{_libdir}/compiz/libthumbnail.so
%{_libdir}/compiz/libtitleinfo.so
%{_libdir}/compiz/libtrailfocus.so
%{_libdir}/compiz/libvpswitch.so
%{_libdir}/compiz/libwall.so
%{_libdir}/compiz/libwallpaper.so
%{_libdir}/compiz/libwater.so
%{_libdir}/compiz/libwidget.so
%{_libdir}/compiz/libwinrules.so
%{_libdir}/compiz/libwizard.so
%{_libdir}/compiz/libwobbly.so
%{_libdir}/compiz/libworkarounds.so
%{_libdir}/compiz/libworkspacenames.so
%dir %{_datadir}/compiz/
%{_datadir}/compiz/addhelper.xml
%{_datadir}/compiz/animation.xml
%{_datadir}/compiz/annotate.xml
%{_datadir}/compiz/bench.xml
%{_datadir}/compiz/clone.xml
%{_datadir}/compiz/commands.xml
%{_datadir}/compiz/compiztoolbox.xml
%{_datadir}/compiz/composite.xml
%{_datadir}/compiz/copytex.xml
%{_datadir}/compiz/core.xml
%{_datadir}/compiz/crashhandler.xml
%{_datadir}/compiz/cube.xml
%{_datadir}/compiz/cubeaddon.xml
%dir %{_datadir}/compiz/cubeaddon/
%dir %{_datadir}/compiz/cubeaddon/images/
%{_datadir}/compiz/cubeaddon/images/compizcap.png
%{_datadir}/compiz/cubeaddon/images/cubecap_release.png
%{_datadir}/compiz/cubeaddon/images/fusioncap.png
%dir %{_datadir}/compiz/cube/
%dir %{_datadir}/compiz/cube/images/
%{_datadir}/compiz/cube/images/freedesktop.png
%{_datadir}/compiz/dbus.xml
%{_datadir}/compiz/decor.xml
%{_datadir}/compiz/expo.xml
%{_datadir}/compiz/extrawm.xml
%{_datadir}/compiz/ezoom.xml
%{_datadir}/compiz/fade.xml
%{_datadir}/compiz/fadedesktop.xml
%{_datadir}/compiz/firepaint.xml
%{_datadir}/compiz/gnomecompat.xml
%{_datadir}/compiz/grid.xml
%{_datadir}/compiz/icon.png
%{_datadir}/compiz/imgjpeg.xml
%{_datadir}/compiz/imgpng.xml
%{_datadir}/compiz/imgsvg.xml
%{_datadir}/compiz/inotify.xml
%{_datadir}/compiz/kdecompat.xml
%{_datadir}/compiz/mag.xml
%dir %{_datadir}/compiz/mag/
%dir %{_datadir}/compiz/mag/images/
%dir %{_datadir}/compiz/mag/images/Gnome/
%dir %{_datadir}/compiz/mag/images/Oxygen/
%{_datadir}/compiz/mag/images/Gnome/image.svg
%{_datadir}/compiz/mag/images/Gnome/mask.png
%{_datadir}/compiz/mag/images/Gnome/overlay.png
%{_datadir}/compiz/mag/images/Oxygen/image.svg
%{_datadir}/compiz/mag/images/Oxygen/mask.png
%{_datadir}/compiz/mag/images/Oxygen/overlay.png
%{_datadir}/compiz/maximumize.xml
%{_datadir}/compiz/mblur.xml
%{_datadir}/compiz/mousepoll.xml
%{_datadir}/compiz/move.xml
%{_datadir}/compiz/neg.xml
%{_datadir}/compiz/notification.xml
%dir %{_datadir}/compiz/notification/
%dir %{_datadir}/compiz/notification/images/
%{_datadir}/compiz/notification/images/compiz.png
%{_datadir}/compiz/obs.xml
%{_datadir}/compiz/opacify.xml
%{_datadir}/compiz/opengl.xml
%{_datadir}/compiz/place.xml
%{_datadir}/compiz/put.xml
%{_datadir}/compiz/regex.xml
%{_datadir}/compiz/resize.xml
%{_datadir}/compiz/resizeinfo.xml
%{_datadir}/compiz/ring.xml
%{_datadir}/compiz/rotate.xml
%{_datadir}/compiz/scale.xml
%{_datadir}/compiz/scaleaddon.xml
%{_datadir}/compiz/scalefilter.xml
%{_datadir}/compiz/screenshot.xml
%{_datadir}/compiz/session.xml
%{_datadir}/compiz/shelf.xml
%{_datadir}/compiz/shift.xml
%{_datadir}/compiz/showdesktop.xml
%{_datadir}/compiz/showmouse.xml
%dir %{_datadir}/compiz/showmouse/
%dir %{_datadir}/compiz/showmouse/images/
%{_datadir}/compiz/showmouse/images/Star.png
%{_datadir}/compiz/showrepaint.xml
%{_datadir}/compiz/snap.xml
%{_datadir}/compiz/splash.xml
%dir %{_datadir}/compiz/splash/
%dir %{_datadir}/compiz/splash/images/
%{_datadir}/compiz/splash/images/splash_background.png
%{_datadir}/compiz/splash/images/splash_logo.png
%{_datadir}/compiz/staticswitcher.xml
%{_datadir}/compiz/switcher.xml
%{_datadir}/compiz/td.xml
%{_datadir}/compiz/text.xml
%{_datadir}/compiz/thumbnail.xml
%{_datadir}/compiz/titleinfo.xml
%{_datadir}/compiz/trailfocus.xml
%{_datadir}/compiz/vpswitch.xml
%{_datadir}/compiz/wall.xml
%{_datadir}/compiz/wallpaper.xml
%{_datadir}/compiz/water.xml
%{_datadir}/compiz/widget.xml
%{_datadir}/compiz/winrules.xml
%{_datadir}/compiz/wizard.xml
%{_datadir}/compiz/wobbly.xml
%{_datadir}/compiz/workarounds.xml
%{_datadir}/compiz/workspacenames.xml


%files -n libcompizconfig
%{_libdir}/libcompizconfig.so.0
%{_libdir}/libcompizconfig.so.0.0.0
# Compiz configuration ini backend
%dir %{_libdir}/compizconfig/
%dir %{_libdir}/compizconfig/backends/
%{_libdir}/compizconfig/backends/libini.so
# Compiz CCP plugin
%dir %{_libdir}/compiz/
%{_libdir}/compiz/libccp.so
%dir %{_datadir}/compiz/
%{_datadir}/compiz/ccp.xml
# Default backend configuration
%dir %{_sysconfdir}/compizconfig/
%{_sysconfdir}/compizconfig/config


%files -n libcompizconfig-devel
%dir %{_includedir}/compizconfig/
%{_includedir}/compizconfig/ccs.h
%{_includedir}/compizconfig/ccs-backend.h
%{_includedir}/compizconfig/ccs-defs.h
%{_includedir}/compizconfig/ccs-fwd.h
%{_includedir}/compizconfig/ccs-list.h
%{_includedir}/compizconfig/ccs-object.h
%{_includedir}/compizconfig/ccs-setting-types.h
%{_includedir}/compizconfig/ccs-string.h
%{_libdir}/libcompizconfig.so
%{_libdir}/pkgconfig/compizconfig-python.pc
%{_libdir}/pkgconfig/libcompizconfig.pc
%dir %{_datadir}/cmake/
%dir %{_datadir}/cmake/Modules/
%{_datadir}/cmake/Modules/FindCompizConfig.cmake
%dir %{_datadir}/compiz/
%dir %{_datadir}/compiz/cmake/
%{_datadir}/compiz/cmake/LibCompizConfigCommon.cmake


%files -n python-compizconfig
%{python_sitearch}/compizconfig.so
%{python_sitearch}/compizconfig_python-%{_disguised_as}-py2.7.egg-info


%files -n ccsm -f build/ccsm.lang
%{_bindir}/ccsm
# Desktop file
%{_datadir}/applications/ccsm.desktop
# Manual page
%{_mandir}/man1/ccsm.1.gz
# Icons
%dir %{_datadir}/ccsm/
%{_datadir}/ccsm/icons/
%{_datadir}/icons/hicolor/*/apps/ccsm.png
%{_datadir}/icons/hicolor/*/apps/ccsm.svg
# Images
%{_datadir}/ccsm/images/
# Python 2 files
%dir %{python_sitelib}/ccm/
%{python_sitelib}/ccm/Conflicts.py*
%{python_sitelib}/ccm/Constants.py*
%{python_sitelib}/ccm/Pages.py*
%{python_sitelib}/ccm/Settings.py*
%{python_sitelib}/ccm/Utils.py*
%{python_sitelib}/ccm/Widgets.py*
%{python_sitelib}/ccm/Window.py*
%{python_sitelib}/ccm/__init__.py*
%{python_sitelib}/ccsm-%{_disguised_as}-py2.7.egg-info


%changelog
* Fri Feb 01 2013 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.9.9~daily13.01.25-1.0ubuntu1
- Version 0.9.9~daily13.01.25
- Ubuntu release 0ubuntu1
- Drop gconf -> dconf migration scripts

* Sun Nov 18 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.9.8.4-3.bzr3412.0ubuntu1
- Version 0.9.8.4
- BZR revision 2312
- Ubuntu release 0ubuntu1

* Wed Oct 31 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.9.8.4-2.0ubuntu1.bzr3407
- Version 0.9.8.4
- Ubuntu release 0ubuntu1
- BZR revision 3407

* Mon Oct 01 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.9.8.4-1.0ubuntu1
- Version 0.9.8.4
- Ubuntu release 0ubuntu1

* Sat Sep 22 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.9.8.2-2.bzr3377.0ubuntu1
- Version 0.9.8.2
- BZR revision 3377
- Ubuntu release 0ubuntu1
- Disabled the building and installing of GConf schemas
- Remove scriptlets for registering GConf schemas
  - Left preun scriptlet to unregister the old ones
- Removed wrapper script that simulated Ubuntu's gconf-defaults functionality
- Removed pkgconfig(gconf-2.0) from build dependencies
- Moved gnome-python2-gconf and GSettings dependencies to compiz-gnome package
- Remove GConf bits from compiz.reset script

* Fri Sep 14 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.9.8.2-1.ubuntu0.9.8.0.0ubuntu1
- Version 0.9.8.2
- Ubuntu packaging version 0.9.8.0 with release 0ubuntu1
- Drop 0006_GWD_use_GSettings.patch
-   Merged upstream
- Refreshed
-   0001_Fix_library_directory.patch
-   0003_Fix_python_install_command.patch

* Sat Sep 01 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.9.8.0-2.0ubuntu1
- Add patch from Launchpad bug 1042323
+   Ports gtk-window-decorator to GSettings

* Sat Sep 01 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.9.8.0-1.z0ubuntu1
- Version 0.9.8.0
- Ubuntu release 0ubuntu1
- Drop plugins (no longer supported)
+   animationaddon
+   blur
+   colorfilter
+   cubeaddon
+   gears
+   group
+   loginout
+   reflex
+   stackswitch
+   thumbnail
+   trip
+   wallpaper

* Tue Aug 28 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.9.8-1.bzr3319.0ubuntu3
- Version 0.9.8
- BZR revision 3319
- Ubuntu release 0ubuntu3

* Wed Aug 22 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.9.8-3.0ubuntu2
- Remove obsoletes
- Use pkgconfig for dependencies
- Clean up spec file

* Wed Aug 08 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.9.8-2.0ubuntu2
- Fix dependency on /bin/python2, which breaks upgrades

* Thu Jul 19 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.9.8-1.0ubuntu2
- Version 0.9.8
- Ubuntu release 0ubuntu2
- Major restructure - all Compiz stuff is now in one source package upstream
- Obsoletes all previous Compiz packages
- compiz-plugins-main and compia-plugins-extra merged into compiz-plugins

* Thu Jul 12 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.9.7.8-2.0ubuntu1
- Fix the hardcoded /lib/ when setting PKG_CONFIG_PATH in FindCompiz.cmake

* Sat Jul 01 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.9.7.8-1.0ubuntu1
- Initial release
- Version 0.9.7.8
- Ubuntu release 0ubuntu1
