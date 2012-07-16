# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

# The KDE parts of Compiz are disabled as they no longer work with KDE 4.8

%define _gconf_schemas compiz-annotate compiz-blur compiz-clone compiz-commands compiz-compiztoolbox compiz-composite compiz-copytex compiz-core compiz-cube compiz-dbus compiz-decor compiz-fade compiz-gnomecompat compiz-imgpng compiz-imgsvg compiz-inotify compiz-move compiz-obs compiz-opengl compiz-place compiz-regex compiz-resize compiz-rotate compiz-scale compiz-screenshot compiz-switcher compiz-water compiz-wobbly gwd

%define _ubuntu_rel 0ubuntu1

Name:		compiz
Version:	0.9.7.8
Release:	2.%{_ubuntu_rel}%{?dist}
Summary:	OpenGL compositing window manager

Group:		User Interface/X
License:	GPLv2 and LGPLv2 and MIT and X and Expat
URL:		https://launchpad.net/compiz
Source0:	https://launchpad.net/ubuntu/+archive/primary/+files/compiz_%{version}.orig.tar.bz2

# Wrapper for compiz to simulate Ubuntu's gconf-defaults mechanism
Source1:	compiz.wrapper

Source99:	https://launchpad.net/ubuntu/+archive/primary/+files/compiz_%{version}-%{_ubuntu_rel}.debian.tar.gz

# Do not hardcode /lib/ when setting PKG_CONFIG_PATH in FindCompiz.cmake
Patch0:		0001_Fix_library_directory.patch

BuildRequires:	cmake
BuildRequires:	desktop-file-utils
BuildRequires:	gcc-c++
BuildRequires:	gettext
BuildRequires:	intltool
BuildRequires:	libtool

BuildRequires:	boost-devel
BuildRequires:	cairo-devel
BuildRequires:	control-center
BuildRequires:	dbus-glib-devel
BuildRequires:	GConf2-devel
BuildRequires:	glib2-devel
BuildRequires:	glibmm24-devel
BuildRequires:	gnome-settings-daemon-ubuntu
BuildRequires:	gtk2-devel
BuildRequires:	gtk3-devel
BuildRequires:	libICE-devel
BuildRequires:	libpng-devel
BuildRequires:	librsvg2-devel
BuildRequires:	libSM-devel
BuildRequires:	libwnck-devel
BuildRequires:	libX11-devel
BuildRequires:	libXcomposite-devel
BuildRequires:	libXcursor-devel
BuildRequires:	libXdamage-devel
BuildRequires:	libXext-devel
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
BuildRequires:	startup-notification-devel
BuildRequires:	xorg-x11-proto-devel

Requires(pre):	GConf2
Requires(post):	GConf2
Requires(preun):	GConf2

# Required for wrapper script
Requires:	GConf2

# Satisfy OBS conflict on what provides PackageKit-backend
BuildRequires:  PackageKit-yum

# Satisfy OBS conflict on gsettings-desktop-schemas
BuildRequires:	gsettings-desktop-schemas

%description
Compiz is an OpenGL compositing manager that uses GLX_EXT_texture_from_pixmap
for binding redirected top-level windows to texture objects. It has a flexible
plug-in system and it is designed to run well on most graphics hardware.


%package devel
Summary:	Development files for compiz
Group:		Development/Libraries

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

%description devel
This packages contains the development files for creating Compiz plugins.


%package gnome
Summary:	OpenGL compositing window manager - GNOME support
Group:		User Interface/X

Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	control-center-filesystem

%description gnome
This package contains the GNOME window decorator and GNOME support files for
Compiz.


%prep
%setup -q

%patch0 -p1 -b .pkg_config_path

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
rm -rf $RPM_BUILD_ROOT
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
install -dm755 $RPM_BUILD_ROOT${_sysconfdir}/etc/compizconfig/upgrades/
install -dm755 $RPM_BUILD_ROOT%{_datadir}/gnome/wm-properties/

# Install compiz decorator
install -m755 ../debian/compiz-decorator $RPM_BUILD_ROOT%{_bindir}/

# Install manual pages
install -m644 \
  ../debian/{compiz,compiz-decorator,gtk-window-decorator}.1 \
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

# Compiz profile upgrade helper files for ensuring smooth upgrades from older
# configuration files
find ../debian/profile_upgrades/ -type f -name '*.upgrade' -exec \
  install -m644 {} $RPM_BUILD_ROOT${_sysconfdir}/compizconfig/upgrades/{} \;

# Simulate Ubuntu's gconf-defaults functionality with wrapper script
# Defaults are from debian/compiz-gnome.gconf-defaults
mv $RPM_BUILD_ROOT%{_bindir}/compiz{,.bin}
install -m644 ../debian/compiz-gnome.gconf-defaults \
              $RPM_BUILD_ROOT%{_datadir}/compiz/compiz.gconf-defaults
install -m755 '%{SOURCE1}' $RPM_BUILD_ROOT%{_bindir}/compiz

# Put GConf stuff in correct directory
mv $RPM_BUILD_ROOT%{_datadir}/gconf/ \
   $RPM_BUILD_ROOT%{_sysconfdir}/gconf/

# Validate desktop files
desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/compiz.desktop

%find_lang compiz


%post -p /usr/sbin/ldconfig

%postun -p /usr/sbin/ldconfig


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
%{_bindir}/compiz-decorator
# Manual pages
%{_mandir}/man1/compiz.1.gz
%{_mandir}/man1/compiz-decorator.1.gz
# Compiz base plugins
%{_libdir}/compiz/libannotate.so
%{_libdir}/compiz/libblur.so
%{_libdir}/compiz/libclone.so
%{_libdir}/compiz/libcommands.so
%{_libdir}/compiz/libcompiztoolbox.so
%{_libdir}/compiz/libcomposite.so
%{_libdir}/compiz/libcopytex.so
%{_libdir}/compiz/libcube.so
%{_libdir}/compiz/libdbus.so
%{_libdir}/compiz/libdecor.so
%{_libdir}/compiz/libfade.so
%{_libdir}/compiz/libgnomecompat.so
%{_libdir}/compiz/libimgpng.so
%{_libdir}/compiz/libimgsvg.so
%{_libdir}/compiz/libinotify.so
%{_libdir}/compiz/libmove.so
%{_libdir}/compiz/libobs.so
%{_libdir}/compiz/libopengl.so
%{_libdir}/compiz/libplace.so
%{_libdir}/compiz/libregex.so
%{_libdir}/compiz/libresize.so
%{_libdir}/compiz/librotate.so
%{_libdir}/compiz/libscale.so
%{_libdir}/compiz/libscreenshot.so
%{_libdir}/compiz/libswitcher.so
%{_libdir}/compiz/libwater.so
%{_libdir}/compiz/libwobbly.so
# Compiz libraries
%{_libdir}/libcompiz_core.so.0.9.7.8
%{_libdir}/libcompiz_core.so.ABI-20120305
%{_libdir}/libdecoration.so.0
%{_libdir}/libdecoration.so.0.0.0
# Desktop file
%{_datadir}/applications/compiz.desktop
# Compiz and plugin data files
%{_datadir}/compiz/annotate.xml
%{_datadir}/compiz/blur.xml
%{_datadir}/compiz/clone.xml
%{_datadir}/compiz/commands.xml
%{_datadir}/compiz/compiztoolbox.xml
%{_datadir}/compiz/composite.xml
%{_datadir}/compiz/copytex.xml
%{_datadir}/compiz/core.xml
%{_datadir}/compiz/cube.xml
%{_datadir}/compiz/cube/images/freedesktop.png
%{_datadir}/compiz/dbus.xml
%{_datadir}/compiz/decor.xml
%{_datadir}/compiz/fade.xml
%{_datadir}/compiz/gnomecompat.xml
%{_datadir}/compiz/icon.png
%{_datadir}/compiz/imgpng.xml
%{_datadir}/compiz/imgsvg.xml
%{_datadir}/compiz/inotify.xml
%{_datadir}/compiz/move.xml
%{_datadir}/compiz/obs.xml
%{_datadir}/compiz/opengl.xml
%{_datadir}/compiz/place.xml
%{_datadir}/compiz/regex.xml
%{_datadir}/compiz/resize.xml
%{_datadir}/compiz/rotate.xml
%{_datadir}/compiz/scale.xml
%{_datadir}/compiz/screenshot.xml
%{_datadir}/compiz/switcher.xml
%{_datadir}/compiz/water.xml
%{_datadir}/compiz/wobbly.xml
%{_datadir}/compiz/xslt/bcop.xslt
%{_datadir}/compiz/xslt/compiz_gconf_schemas.xslt
%{_datadir}/compiz/xslt/compiz_gsettings_schemas.xslt


%files devel
%doc AUTHORS NEWS README TODO
%{_libdir}/libcompiz_core.so
%{_libdir}/libdecoration.so
# Header files
%{_includedir}/compiz/compiztoolbox/compiztoolbox.h
%{_includedir}/compiz/composite/composite.h
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
%{_includedir}/compiz/cube/cube.h
%{_includedir}/compiz/decoration.h
%{_includedir}/compiz/opengl/fragment.h
%{_includedir}/compiz/opengl/matrix.h
%{_includedir}/compiz/opengl/opengl.h
%{_includedir}/compiz/opengl/texture.h
%{_includedir}/compiz/opengl/vector.h
%{_includedir}/compiz/scale/scale.h
# pkgconfig files
%{_libdir}/pkgconfig/compiz-compiztoolbox.pc
%{_libdir}/pkgconfig/compiz-composite.pc
%{_libdir}/pkgconfig/compiz-cube.pc
%{_libdir}/pkgconfig/compiz-opengl.pc
%{_libdir}/pkgconfig/compiz-scale.pc
%{_libdir}/pkgconfig/compiz.pc
%{_libdir}/pkgconfig/libdecoration.pc
# CMake files
%{_datadir}/cmake/Modules/FindCompiz.cmake
%{_datadir}/compiz/cmake/CompizBcop.cmake
%{_datadir}/compiz/cmake/CompizCommon.cmake
%{_datadir}/compiz/cmake/CompizDefaults.cmake
%{_datadir}/compiz/cmake/CompizGSettings.cmake
%{_datadir}/compiz/cmake/CompizGconf.cmake
%{_datadir}/compiz/cmake/CompizPackage.cmake
%{_datadir}/compiz/cmake/CompizPlugin.cmake
%{_datadir}/compiz/cmake/plugin_extensions/CompizGenGSettings.cmake
%{_datadir}/compiz/cmake/plugin_extensions/CompizGenGconf.cmake
%{_datadir}/compiz/cmake/plugin_extensions/CompizGenInstallData.cmake
%{_datadir}/compiz/cmake/plugin_extensions/CompizGenInstallImages.cmake


%files gnome
%doc AUTHORS NEWS README TODO
%{_bindir}/gtk-window-decorator
# Manual page
%{_mandir}/man1/gtk-window-decorator.1.gz
# X11 session script
%{_sysconfdir}/X11/xinit/xinitrc.d/65compiz_profile-on-session
# Compiz Unity profile configuration file
%config(noreplace) %{_sysconfdir}/compizconfig/unity.ini
# GNOME window manager desktop file
%{_datadir}/gnome/wm-properties/compiz.desktop
# GConf defaults
%{_datadir}/compiz/compiz.gconf-defaults
# GConf schemas
%{_sysconfdir}/gconf/schemas/compiz-annotate.schemas
%{_sysconfdir}/gconf/schemas/compiz-blur.schemas
%{_sysconfdir}/gconf/schemas/compiz-clone.schemas
%{_sysconfdir}/gconf/schemas/compiz-commands.schemas
%{_sysconfdir}/gconf/schemas/compiz-compiztoolbox.schemas
%{_sysconfdir}/gconf/schemas/compiz-composite.schemas
%{_sysconfdir}/gconf/schemas/compiz-copytex.schemas
%{_sysconfdir}/gconf/schemas/compiz-core.schemas
%{_sysconfdir}/gconf/schemas/compiz-cube.schemas
%{_sysconfdir}/gconf/schemas/compiz-dbus.schemas
%{_sysconfdir}/gconf/schemas/compiz-decor.schemas
%{_sysconfdir}/gconf/schemas/compiz-fade.schemas
%{_sysconfdir}/gconf/schemas/compiz-gnomecompat.schemas
%{_sysconfdir}/gconf/schemas/compiz-imgpng.schemas
%{_sysconfdir}/gconf/schemas/compiz-imgsvg.schemas
%{_sysconfdir}/gconf/schemas/compiz-inotify.schemas
%{_sysconfdir}/gconf/schemas/compiz-move.schemas
%{_sysconfdir}/gconf/schemas/compiz-obs.schemas
%{_sysconfdir}/gconf/schemas/compiz-opengl.schemas
%{_sysconfdir}/gconf/schemas/compiz-place.schemas
%{_sysconfdir}/gconf/schemas/compiz-regex.schemas
%{_sysconfdir}/gconf/schemas/compiz-resize.schemas
%{_sysconfdir}/gconf/schemas/compiz-rotate.schemas
%{_sysconfdir}/gconf/schemas/compiz-scale.schemas
%{_sysconfdir}/gconf/schemas/compiz-screenshot.schemas
%{_sysconfdir}/gconf/schemas/compiz-switcher.schemas
%{_sysconfdir}/gconf/schemas/compiz-water.schemas
%{_sysconfdir}/gconf/schemas/compiz-wobbly.schemas
%{_sysconfdir}/gconf/schemas/gwd.schemas
# GNOME Control Center keybinding files
%{_datadir}/gnome-control-center/keybindings/50-compiz-launchers.xml
%{_datadir}/gnome-control-center/keybindings/50-compiz-navigation.xml
%{_datadir}/gnome-control-center/keybindings/50-compiz-screenshot.xml
%{_datadir}/gnome-control-center/keybindings/50-compiz-system.xml
%{_datadir}/gnome-control-center/keybindings/50-compiz-windows.xml


%changelog
* Thu Jul 12 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.9.7.8-2.0ubuntu1
- Fix the hardcoded /lib/ when setting PKG_CONFIG_PATH in FindCompiz.cmake

* Sat Jul 01 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.9.7.8-1.0ubuntu1
- Initial release
- Version 0.9.7.8
- Ubuntu release 0ubuntu1
