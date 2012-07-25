# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

# The KDE parts of Compiz are disabled as they no longer work with KDE 4.8

# Do not provide the Python 2 binding library
%filter_provides_in %{python_sitearch}/compizconfig\.so$
%filter_setup

%define _gconf_schemas compiz-addhelper compiz-animationaddon compiz-animation compiz-annotate compiz-bench compiz-bicubic compiz-blur compiz-ccp compiz-clone compiz-colorfilter compiz-commands compiz-compiztoolbox compiz-composite compiz-copytex compiz-core compiz-crashhandler compiz-cubeaddon compiz-cube compiz-dbus compiz-decor compiz-expo compiz-extrawm compiz-ezoom compiz-fadedesktop compiz-fade compiz-firepaint compiz-gears compiz-gnomecompat compiz-grid compiz-group compiz-imgjpeg compiz-imgpng compiz-imgsvg compiz-inotify compiz-kdecompat compiz-loginout compiz-mag compiz-maximumize compiz-mblur compiz-mousepoll compiz-move compiz-neg compiz-notification compiz-obs compiz-opacify compiz-opengl compiz-place compiz-put compiz-reflex compiz-regex compiz-resizeinfo compiz-resize compiz-ring compiz-rotate compiz-scaleaddon compiz-scalefilter compiz-scale compiz-screenshot compiz-session compiz-shelf compiz-shift compiz-showdesktop compiz-showmouse compiz-showrepaint compiz-snap compiz-splash compiz-staticswitcher compiz-switcher compiz-td compiz-text compiz-thumbnail compiz-titleinfo compiz-trailfocus compiz-vpswitch compiz-wallpaper compiz-wall compiz-water compiz-widget compiz-winrules compiz-wobbly compiz-workarounds compiz-workspacenames gwd

%define _ubuntu_rel 0ubuntu2
%define _bzr_rev 3249

Name:		compiz
Version:	0.9.8
Release:	1.bzr%{_bzr_rev}.%{_ubuntu_rel}%{?dist}
Summary:	OpenGL compositing window manager

Group:		User Interface/X
License:	GPLv2+
URL:		https://launchpad.net/compiz

# Ubuntu's packaging is now combined with the source tarball
Source0:	https://launchpad.net/ubuntu/+archive/primary/+files/compiz_%{version}+bzr%{_bzr_rev}-%{_ubuntu_rel}.tar.gz

# Wrapper for compiz to simulate Ubuntu's gconf-defaults mechanism
Source1:	compiz.wrapper

# Script to reset all of Compiz's settings
Source2:	compiz.reset

# Do not hardcode /lib/ when setting PKG_CONFIG_PATH in FindCompiz.cmake
Patch0:		0001_Fix_library_directory.patch

# Fix the directory for FindCompiz.cmakd and FindCompizConfig.cmake
Patch1:		0002_Fix_cmake_install_dir.patch

# Ubuntu's CMakeFiles.txt appends --install-layout=deb to python install command
# (for python-compizconfig and ccsm) whether or not COMPIZ_DEB_BUILD is set to 1
Patch2:		0003_Fix_python_install_command.patch

BuildRequires:	cmake
BuildRequires:	desktop-file-utils
BuildRequires:	gcc-c++
BuildRequires:	gettext
BuildRequires:	intltool
BuildRequires:	libtool

BuildRequires:	boost-devel
BuildRequires:	cairo-devel
BuildRequires:	control-center-devel
BuildRequires:	dbus-glib-devel
BuildRequires:	GConf2-devel
BuildRequires:	glib2-devel
BuildRequires:	glibmm24-devel
BuildRequires:	gtk2-devel
BuildRequires:	gtk3-devel
BuildRequires:	libICE-devel
BuildRequires:	libjpeg-turbo-devel
BuildRequires:	libnotify-devel
BuildRequires:	libpng-devel
BuildRequires:	librsvg2-devel
BuildRequires:	libSM-devel
BuildRequires:	libwnck-devel
BuildRequires:	libX11-devel
BuildRequires:	libXcomposite-devel
BuildRequires:	libXcursor-devel
BuildRequires:	libXdamage-devel
BuildRequires:	libXext-devel
# Ubuntu's libXfixes required
BuildRequires:	libXfixes-ubuntu-devel
BuildRequires:	libXinerama-devel
BuildRequires:	libxml2-devel
BuildRequires:	libXrandr-devel
BuildRequires:	libXrender-devel
BuildRequires:	libxslt-devel
BuildRequires:	mesa-libGL-devel
BuildRequires:	mesa-libGLU-devel
# Ubuntu's metacity required for the keybinding files
BuildRequires:	metacity-ubuntu-devel
BuildRequires:	pango-devel
#BuildRequires:	perl-XML-Parser
BuildRequires:	protobuf-devel
BuildRequires:	python-devel
BuildRequires:	startup-notification-devel
BuildRequires:	xorg-x11-proto-devel

BuildRequires:	Pyrex

Requires(pre):	GConf2
Requires(post):	GConf2
Requires(preun):	GConf2

# Required for wrapper script
Requires:	GConf2

%if 0%{?opensuse_bs}
# Satisfy OBS conflict on what provides PackageKit-backend
BuildRequires:  PackageKit-yum

# Satisfy OBS conflict on gsettings-desktop-schemas
BuildRequires:	gsettings-desktop-schemas

# Satisfy OBS conflict on gnome-bluetooth-libs
BuildRequires:	gnome-bluetooth-libs

# Satisfy OBS conflict on control-center
BuildRequires:	control-center
BuildRequires:	control-center-filesystem

# Satisfy OBS conflict on gnome-settings-daemon (required by control-center)
BuildRequires:	gnome-settings-daemon
%endif

%description
Compiz is an OpenGL compositing manager that uses GLX_EXT_texture_from_pixmap
for binding redirected top-level windows to texture objects. It has a flexible
plug-in system and it is designed to run well on most graphics hardware.


%package devel
Summary:	Development files for compiz
Group:		Development/Libraries
License:	MIT and X

Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	glib2-devel
Requires:	glibmm24-devel
Requires:	gtk3-devel
Requires:	libICE-devel
Requires:	libpng-devel
Requires:	libSM-devel
Requires:	libX11-devel
Requires:	libXcomposite-devel
Requires:	libXcursor-devel
Requires:	libXdamage-devel
Requires:	libXfixes-ubuntu-devel
Requires:	libXinerama-devel
Requires:	libxml2-devel
Requires:	libXrandr-devel
Requires:	libxslt-devel
Requires:	mesa-libGL-devel
Requires:	startup-notification-devel

Obsoletes:	compiz-plugins-main-devel < 0.9.8

%description devel
This packages contains the development files for creating Compiz plugins.


%package gnome
Summary:	OpenGL compositing window manager - GNOME support
Group:		User Interface/X

License:	LGPLv2+

Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	control-center-filesystem

Obsoletes:	compizconfig-backend-gconf < 0.9.8

%description gnome
This package contains the GNOME window decorator and GNOME support files for
Compiz.


%package plugins
Summary:	OpenGL compositing window manager - Plugins
Group:		User Interface/X
License:	GPLv2+ and LGPLv2+ and MIT and X

Requires:	%{name}%{?_isa} = %{version}-%{release}

Obsoletes:	compiz-plugins-main < 0.9.8
Obsoletes:	compiz-plugins-extra < 0.9.8

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
%setup -q -n %{name}-%{version}+bzr%{_bzr_rev}

%patch0 -p1 -b .pkg_config_path
%patch1 -p1 -b .cmake_install_dir
%patch2 -p1 -b .py_install_command

# Apply Ubuntu's patches
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
  -DUSE_GSETTINGS=OFF \
  -DCOMPIZ_DISABLE_GS_SCHEMAS_INSTALL=ON \
  -DCOMPIZ_BUILD_TESTING=OFF \
  -DCOMPIZ_DISABLE_PLUGIN_KDE=ON \
  -DUSE_KDE4=OFF

make %{?_smp_mflags}


%install
cd build
GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 make install DESTDIR=$RPM_BUILD_ROOT

# make findcompiz_install does not work, so we'll install it manually
install -dm755 $RPM_BUILD_ROOT%{_datadir}/cmake/Modules/
install -m644 ../cmake/FindCompiz.cmake \
  $RPM_BUILD_ROOT%{_datadir}/cmake/Modules/

# Create Compiz keybindings
KEYBIND_DIR=%{_datadir}/gnome-control-center/keybindings
install -dm755 $RPM_BUILD_ROOT${KEYBIND_DIR}
for i in launchers navigation screenshot system windows; do
  sed 's/wm_name=\"Metacity\"/wm_name=\"Compiz\"/' \
    ${KEYBIND_DIR}/50-metacity-${i}.xml \
    > $RPM_BUILD_ROOT${KEYBIND_DIR}/50-compiz-${i}.xml
done

# Add selected keys
sed -i 's#key=\"/apps/metacity/general/num_workspaces\" comparison=\"gt\"##g' \
  $RPM_BUILD_ROOT${KEYBIND_DIR}/50-compiz-navigation.xml

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

# Unity Compiz plugin configuration file
install -m644 ../debian/unity.ini $RPM_BUILD_ROOT%{_sysconfdir}/compizconfig/

# Install Compiz profile configuration file
install -m644 ../debian/config $RPM_BUILD_ROOT%{_sysconfdir}/compizconfig/

# Compiz profile upgrade helper files for ensuring smooth upgrades from older
# configuration files
pushd ../debian/profile_upgrades/
find . -type f -name '*.upgrade' -exec \
  install -m644 {} $RPM_BUILD_ROOT%{_sysconfdir}/compizconfig/upgrades/{} \;
popd

# Simulate Ubuntu's gconf-defaults functionality with wrapper script
# Defaults are from debian/compiz-gnome.gconf-defaults
mv $RPM_BUILD_ROOT%{_bindir}/compiz{,.bin}
install -m644 ../debian/compiz-gnome.gconf-defaults \
              $RPM_BUILD_ROOT%{_datadir}/compiz/compiz.gconf-defaults
install -m755 '%{SOURCE1}' $RPM_BUILD_ROOT%{_bindir}/compiz

# Install script to resetting all of Compiz's settings
install -m755 '%{SOURCE2}' $RPM_BUILD_ROOT%{_bindir}/compiz.reset

# Put GConf stuff in correct directory
mv $RPM_BUILD_ROOT%{_datadir}/gconf/ \
   $RPM_BUILD_ROOT%{_sysconfdir}/gconf/

# Validate desktop files
desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/compiz.desktop
desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/ccsm.desktop

%find_lang compiz
%find_lang ccsm


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%post -n libcompizconfig -p /sbin/ldconfig

%postun -n libcompizconfig -p /sbin/ldconfig


%pre gnome
%gconf_schema_prepare %{_gconf_schemas}

%post gnome
%gconf_schema_upgrade %{_gconf_schemas}

%preun gnome
%gconf_schema_remove %{_gconf_schemas}


%files -f build/compiz.lang
%doc AUTHORS NEWS README TODO
%{_bindir}/compiz
%{_bindir}/compiz.bin
%{_bindir}/compiz.reset
# Manual pages
%{_mandir}/man1/compiz.1.gz
# Compiz libraries
%{_libdir}/libcompiz_core.so.0.9.8
%{_libdir}/libcompiz_core.so.ABI-20120526
%{_libdir}/libdecoration.so.0
%{_libdir}/libdecoration.so.0.0.0
# Desktop file
%{_datadir}/applications/compiz.desktop


%files devel
%doc AUTHORS NEWS README TODO
%{_libdir}/libcompiz_core.so
%{_libdir}/libdecoration.so
# Header files
%dir %{_includedir}/compiz/
%dir %{_includedir}/compiz/animation/
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
%dir %{_includedir}/compiz/animationaddon/
%{_includedir}/compiz/animationaddon/animationaddon.h
%dir %{_includedir}/compiz/compiztoolbox/
%{_includedir}/compiz/compiztoolbox/compiztoolbox.h
%dir %{_includedir}/compiz/composite/
%{_includedir}/compiz/composite/composite.h
%dir %{_includedir}/compiz/core/
%{_includedir}/compiz/core/abiversion.h
%{_includedir}/compiz/core/action.h
%{_includedir}/compiz/core/atoms.h
%{_includedir}/compiz/core/core.h
%{_includedir}/compiz/core/countedlist.h
%{_includedir}/compiz/core/global.h
%{_includedir}/compiz/core/icon.h
%{_includedir}/compiz/core/logmessage.h
%{_includedir}/compiz/core/match.h
%{_includedir}/compiz/core/modifierhandler.h
%{_includedir}/compiz/core/option.h
%{_includedir}/compiz/core/output.h
%{_includedir}/compiz/core/plugin.h
%{_includedir}/compiz/core/pluginclasses.h
%{_includedir}/compiz/core/pluginclasshandler.h
%{_includedir}/compiz/core/point.h
%{_includedir}/compiz/core/privateunion.h
%{_includedir}/compiz/core/propertywriter.h
%{_includedir}/compiz/core/rect.h
%{_includedir}/compiz/core/region.h
%{_includedir}/compiz/core/screen.h
%{_includedir}/compiz/core/serialization.h
%{_includedir}/compiz/core/servergrab.h
%{_includedir}/compiz/core/session.h
%{_includedir}/compiz/core/size.h
%{_includedir}/compiz/core/string.h
%{_includedir}/compiz/core/timeouthandler.h
%{_includedir}/compiz/core/timer.h
%{_includedir}/compiz/core/valueholder.h
%{_includedir}/compiz/core/window.h
%{_includedir}/compiz/core/windowconstrainment.h
%{_includedir}/compiz/core/windowextents.h
%{_includedir}/compiz/core/windowgeometry.h
%{_includedir}/compiz/core/windowgeometrysaver.h
%{_includedir}/compiz/core/wrapsystem.h
%dir %{_includedir}/compiz/cube/
%{_includedir}/compiz/cube/cube.h
%{_includedir}/compiz/decoration.h
%dir %{_includedir}/compiz/mousepoll/
%{_includedir}/compiz/mousepoll/mousepoll.h
%dir %{_includedir}/compiz/opengl/
%{_includedir}/compiz/opengl/fragment.h
%{_includedir}/compiz/opengl/matrix.h
%{_includedir}/compiz/opengl/opengl.h
%{_includedir}/compiz/opengl/texture.h
%{_includedir}/compiz/opengl/vector.h
%dir %{_includedir}/compiz/scale/
%{_includedir}/compiz/scale/scale.h
%dir %{_includedir}/compiz/text/
%{_includedir}/compiz/text/text.h
# pkgconfig files
%{_libdir}/pkgconfig/compiz-animation.pc
%{_libdir}/pkgconfig/compiz-animationaddon.pc
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
%{_datadir}/compiz/xslt/compiz_gconf_schemas.xslt
%{_datadir}/compiz/xslt/compiz_gsettings_schemas.xslt
# CMake files
%dir %{_datadir}/cmake/
%dir %{_datadir}/cmake/Modules/
%{_datadir}/cmake/Modules/FindCompiz.cmake
%dir %{_datadir}/compiz/cmake/
%{_datadir}/compiz/cmake/CompizBcop.cmake
%{_datadir}/compiz/cmake/CompizCommon.cmake
%{_datadir}/compiz/cmake/CompizDefaults.cmake
%{_datadir}/compiz/cmake/CompizGSettings.cmake
%{_datadir}/compiz/cmake/CompizGconf.cmake
%{_datadir}/compiz/cmake/CompizPackage.cmake
%{_datadir}/compiz/cmake/CompizPlugin.cmake
%dir %{_datadir}/compiz/cmake/plugin_extensions/
%{_datadir}/compiz/cmake/plugin_extensions/CompizGenGSettings.cmake
%{_datadir}/compiz/cmake/plugin_extensions/CompizGenGconf.cmake
%{_datadir}/compiz/cmake/plugin_extensions/CompizGenInstallData.cmake
%{_datadir}/compiz/cmake/plugin_extensions/CompizGenInstallImages.cmake


%files gnome
%doc AUTHORS NEWS README TODO
%{_bindir}/gtk-window-decorator
# Manual page
%{_mandir}/man1/gtk-window-decorator.1.gz
# Compiz configuration backends
%dir %{_libdir}/compizconfig/
%dir %{_libdir}/compizconfig/backends/
%{_libdir}/compizconfig/backends/libgconf.so
%{_libdir}/compizconfig/backends/libgsettings.so
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
# GConf defaults
%{_datadir}/compiz/compiz.gconf-defaults
# GConf schemas
%{_sysconfdir}/gconf/schemas/compiz-addhelper.schemas
%{_sysconfdir}/gconf/schemas/compiz-animation.schemas
%{_sysconfdir}/gconf/schemas/compiz-animationaddon.schemas
%{_sysconfdir}/gconf/schemas/compiz-annotate.schemas
%{_sysconfdir}/gconf/schemas/compiz-bench.schemas
%{_sysconfdir}/gconf/schemas/compiz-bicubic.schemas
%{_sysconfdir}/gconf/schemas/compiz-blur.schemas
%{_sysconfdir}/gconf/schemas/compiz-ccp.schemas
%{_sysconfdir}/gconf/schemas/compiz-clone.schemas
%{_sysconfdir}/gconf/schemas/compiz-colorfilter.schemas
%{_sysconfdir}/gconf/schemas/compiz-commands.schemas
%{_sysconfdir}/gconf/schemas/compiz-compiztoolbox.schemas
%{_sysconfdir}/gconf/schemas/compiz-composite.schemas
%{_sysconfdir}/gconf/schemas/compiz-copytex.schemas
%{_sysconfdir}/gconf/schemas/compiz-core.schemas
%{_sysconfdir}/gconf/schemas/compiz-crashhandler.schemas
%{_sysconfdir}/gconf/schemas/compiz-cube.schemas
%{_sysconfdir}/gconf/schemas/compiz-cubeaddon.schemas
%{_sysconfdir}/gconf/schemas/compiz-dbus.schemas
%{_sysconfdir}/gconf/schemas/compiz-decor.schemas
%{_sysconfdir}/gconf/schemas/compiz-expo.schemas
%{_sysconfdir}/gconf/schemas/compiz-extrawm.schemas
%{_sysconfdir}/gconf/schemas/compiz-ezoom.schemas
%{_sysconfdir}/gconf/schemas/compiz-fade.schemas
%{_sysconfdir}/gconf/schemas/compiz-fadedesktop.schemas
%{_sysconfdir}/gconf/schemas/compiz-firepaint.schemas
%{_sysconfdir}/gconf/schemas/compiz-gears.schemas
%{_sysconfdir}/gconf/schemas/compiz-gnomecompat.schemas
%{_sysconfdir}/gconf/schemas/compiz-grid.schemas
%{_sysconfdir}/gconf/schemas/compiz-group.schemas
%{_sysconfdir}/gconf/schemas/compiz-imgjpeg.schemas
%{_sysconfdir}/gconf/schemas/compiz-imgpng.schemas
%{_sysconfdir}/gconf/schemas/compiz-imgsvg.schemas
%{_sysconfdir}/gconf/schemas/compiz-inotify.schemas
# Ubuntu packages the KDE schema too
%{_sysconfdir}/gconf/schemas/compiz-kdecompat.schemas
%{_sysconfdir}/gconf/schemas/compiz-loginout.schemas
%{_sysconfdir}/gconf/schemas/compiz-mag.schemas
%{_sysconfdir}/gconf/schemas/compiz-maximumize.schemas
%{_sysconfdir}/gconf/schemas/compiz-mblur.schemas
%{_sysconfdir}/gconf/schemas/compiz-mousepoll.schemas
%{_sysconfdir}/gconf/schemas/compiz-move.schemas
%{_sysconfdir}/gconf/schemas/compiz-neg.schemas
%{_sysconfdir}/gconf/schemas/compiz-notification.schemas
%{_sysconfdir}/gconf/schemas/compiz-obs.schemas
%{_sysconfdir}/gconf/schemas/compiz-opacify.schemas
%{_sysconfdir}/gconf/schemas/compiz-opengl.schemas
%{_sysconfdir}/gconf/schemas/compiz-place.schemas
%{_sysconfdir}/gconf/schemas/compiz-put.schemas
%{_sysconfdir}/gconf/schemas/compiz-reflex.schemas
%{_sysconfdir}/gconf/schemas/compiz-regex.schemas
%{_sysconfdir}/gconf/schemas/compiz-resize.schemas
%{_sysconfdir}/gconf/schemas/compiz-resizeinfo.schemas
%{_sysconfdir}/gconf/schemas/compiz-ring.schemas
%{_sysconfdir}/gconf/schemas/compiz-rotate.schemas
%{_sysconfdir}/gconf/schemas/compiz-scale.schemas
%{_sysconfdir}/gconf/schemas/compiz-scaleaddon.schemas
%{_sysconfdir}/gconf/schemas/compiz-scalefilter.schemas
%{_sysconfdir}/gconf/schemas/compiz-screenshot.schemas
%{_sysconfdir}/gconf/schemas/compiz-session.schemas
%{_sysconfdir}/gconf/schemas/compiz-shelf.schemas
%{_sysconfdir}/gconf/schemas/compiz-shift.schemas
%{_sysconfdir}/gconf/schemas/compiz-showdesktop.schemas
%{_sysconfdir}/gconf/schemas/compiz-showmouse.schemas
%{_sysconfdir}/gconf/schemas/compiz-showrepaint.schemas
%{_sysconfdir}/gconf/schemas/compiz-snap.schemas
%{_sysconfdir}/gconf/schemas/compiz-splash.schemas
%{_sysconfdir}/gconf/schemas/compiz-staticswitcher.schemas
%{_sysconfdir}/gconf/schemas/compiz-switcher.schemas
%{_sysconfdir}/gconf/schemas/compiz-td.schemas
%{_sysconfdir}/gconf/schemas/compiz-text.schemas
%{_sysconfdir}/gconf/schemas/compiz-thumbnail.schemas
%{_sysconfdir}/gconf/schemas/compiz-titleinfo.schemas
%{_sysconfdir}/gconf/schemas/compiz-trailfocus.schemas
%{_sysconfdir}/gconf/schemas/compiz-vpswitch.schemas
%{_sysconfdir}/gconf/schemas/compiz-wall.schemas
%{_sysconfdir}/gconf/schemas/compiz-wallpaper.schemas
%{_sysconfdir}/gconf/schemas/compiz-water.schemas
%{_sysconfdir}/gconf/schemas/compiz-widget.schemas
%{_sysconfdir}/gconf/schemas/compiz-winrules.schemas
%{_sysconfdir}/gconf/schemas/compiz-wobbly.schemas
%{_sysconfdir}/gconf/schemas/compiz-workarounds.schemas
%{_sysconfdir}/gconf/schemas/compiz-workspacenames.schemas
%{_sysconfdir}/gconf/schemas/gwd.schemas
# GNOME Control Center keybinding files
%{_datadir}/gnome-control-center/keybindings/50-compiz-launchers.xml
%{_datadir}/gnome-control-center/keybindings/50-compiz-navigation.xml
%{_datadir}/gnome-control-center/keybindings/50-compiz-screenshot.xml
%{_datadir}/gnome-control-center/keybindings/50-compiz-system.xml
%{_datadir}/gnome-control-center/keybindings/50-compiz-windows.xml


%files plugins
%doc AUTHORS NEWS README TODO
%dir %{_libdir}/compiz/
%{_libdir}/compiz/libaddhelper.so
%{_libdir}/compiz/libanimation.so
%{_libdir}/compiz/libanimationaddon.so
%{_libdir}/compiz/libannotate.so
%{_libdir}/compiz/libbench.so
%{_libdir}/compiz/libbicubic.so
%{_libdir}/compiz/libblur.so
%{_libdir}/compiz/libclone.so
%{_libdir}/compiz/libcolorfilter.so
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
%{_libdir}/compiz/libgears.so
%{_libdir}/compiz/libgnomecompat.so
%{_libdir}/compiz/libgrid.so
%{_libdir}/compiz/libgroup.so
%{_libdir}/compiz/libimgjpeg.so
%{_libdir}/compiz/libimgpng.so
%{_libdir}/compiz/libimgsvg.so
%{_libdir}/compiz/libinotify.so
%{_libdir}/compiz/libkdecompat.so
%{_libdir}/compiz/libloginout.so
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
%{_libdir}/compiz/libreflex.so
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
%{_libdir}/compiz/libwobbly.so
%{_libdir}/compiz/libworkarounds.so
%{_libdir}/compiz/libworkspacenames.so
%dir %{_datadir}/compiz/
%{_datadir}/compiz/addhelper.xml
%{_datadir}/compiz/animation.xml
%{_datadir}/compiz/animationaddon.xml
%{_datadir}/compiz/annotate.xml
%{_datadir}/compiz/bench.xml
%{_datadir}/compiz/bicubic.xml
%{_datadir}/compiz/blur.xml
%{_datadir}/compiz/clone.xml
%{_datadir}/compiz/colorfilter.xml
%dir %{_datadir}/compiz/colorfilter/
%dir %{_datadir}/compiz/colorfilter/data/
%dir %{_datadir}/compiz/colorfilter/data/filters/
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
%{_datadir}/compiz/commands.xml
%{_datadir}/compiz/compiztoolbox.xml
%{_datadir}/compiz/composite.xml
%{_datadir}/compiz/copytex.xml
%{_datadir}/compiz/core.xml
%{_datadir}/compiz/crashhandler.xml
%{_datadir}/compiz/cube.xml
%dir %{_datadir}/compiz/cube/
%dir %{_datadir}/compiz/cube/images/
%{_datadir}/compiz/cube/images/freedesktop.png
%{_datadir}/compiz/cubeaddon.xml
%dir %{_datadir}/compiz/cubeaddon/
%dir %{_datadir}/compiz/cubeaddon/images/
%{_datadir}/compiz/cubeaddon/images/compizcap.png
%{_datadir}/compiz/cubeaddon/images/cubecap_release.png
%{_datadir}/compiz/cubeaddon/images/fusioncap.png
%{_datadir}/compiz/dbus.xml
%{_datadir}/compiz/decor.xml
%{_datadir}/compiz/expo.xml
%{_datadir}/compiz/extrawm.xml
%{_datadir}/compiz/ezoom.xml
%{_datadir}/compiz/fade.xml
%{_datadir}/compiz/fadedesktop.xml
%{_datadir}/compiz/firepaint.xml
%{_datadir}/compiz/gears.xml
%{_datadir}/compiz/gnomecompat.xml
%{_datadir}/compiz/grid.xml
%{_datadir}/compiz/group.xml
%{_datadir}/compiz/icon.png
%{_datadir}/compiz/imgjpeg.xml
%{_datadir}/compiz/imgpng.xml
%{_datadir}/compiz/imgsvg.xml
%{_datadir}/compiz/inotify.xml
%{_datadir}/compiz/kdecompat.xml
%{_datadir}/compiz/loginout.xml
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
%{_datadir}/compiz/reflex.xml
%dir %{_datadir}/compiz/reflex/
%dir %{_datadir}/compiz/reflex/images/
%{_datadir}/compiz/reflex/images/reflection.png
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
%{_datadir}/compiz/wobbly.xml
%{_datadir}/compiz/workarounds.xml
%{_datadir}/compiz/workspacenames.xml


%files -n libcompizconfig
%doc AUTHORS NEWS README TODO
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
%doc AUTHORS NEWS README TODO
%dir %{_includedir}/compizconfig/
%{_includedir}/compizconfig/ccs-backend.h
%{_includedir}/compizconfig/ccs.h
%{_libdir}/libcompizconfig.so
%{_libdir}/pkgconfig/libcompizconfig.pc
%dir %{_datadir}/cmake/
%dir %{_datadir}/cmake/Modules/
%{_datadir}/cmake/Modules/FindCompizConfig.cmake
%dir %{_datadir}/compiz/
%dir %{_datadir}/compiz/cmake/
%{_datadir}/compiz/cmake/LibCompizConfigCommon.cmake


%files -n python-compizconfig
%doc AUTHORS NEWS README TODO
%{python_sitearch}/compizconfig.so
%{python_sitearch}/compizconfig_python-0.9.5.94-py2.7.egg-info


%files -n ccsm -f build/ccsm.lang
%doc AUTHORS NEWS README TODO
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
%{python_sitelib}/ccsm-0.9.5.94-py2.7.egg-info


%changelog
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
