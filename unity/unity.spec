# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

%define _ubuntu_ver 5.12
%define _ubuntu_rel 0ubuntu1.1

%define _gconf_schemas compiz-gtkloader compiz-unitymtgrabhandles compiz-unityshell

Name:		unity
Version:	5.12.0
Release:	1.%{_ubuntu_rel}%{?dist}
Summary:	A desktop experience designed for efficiency of space and interaction

Group:		User Interface/Desktops
License:	GPLv3 and LGPLv3
URL:		https://launchpad.net/unity
Source0:	https://launchpad.net/unity/5.0/%{version}/+download/unity-%{version}.tar.bz2

# Ubuntu's packaging contains quite a few backported patches
Source99:	https://launchpad.net/ubuntu/+archive/primary/+files/unity_%{_ubuntu_ver}-%{_ubuntu_rel}.diff.gz

# Fix the gtest search in CMake
Patch0:		0001_fix_gtest_directory.patch

# Fix directories in source code and CMake (/usr/lib hardcoded)
Patch1:		0002_fix_directories.patch

# Ignore error about deprecated paths in GSettings schemas
Patch2:		0003_Ignore_deprecated_schema_path.patch

# GCC 4.6 is required or else Unity will segfault
BuildRequires:	gcc46-devel
BuildRequires:	gcc46-static

# Ubuntu's patches fixesproto and libXfixes is needed
BuildRequires:	libXfixes-ubuntu-devel
BuildRequires:	xorg-x11-proto-ubuntu-devel

BuildRequires:	cmake
BuildRequires:	doxygen
BuildRequires:	gcc-c++
BuildRequires:	gettext
BuildRequires:	intltool

BuildRequires:	atk-devel
BuildRequires:	bamf3-devel
BuildRequires:	boost-devel
BuildRequires:	cairo-devel
BuildRequires:	compiz-devel
BuildRequires:	dee-devel
BuildRequires:	GConf2-devel
BuildRequires:	glib2-devel
BuildRequires:	gnome-desktop3-devel
BuildRequires:	gsettings-desktop-schemas-devel
BuildRequires:	gtk3-devel
BuildRequires:	json-glib-devel
BuildRequires:	libcompizconfig-devel
BuildRequires:	libdbusmenu-glib-devel
BuildRequires:	libgee06-devel
BuildRequires:	libgdu-devel
BuildRequires:	libindicator-devel
BuildRequires:	libindicator-gtk3-devel
BuildRequires:	libnotify-devel
BuildRequires:	libsigc++20-devel
BuildRequires:	libunity-devel
BuildRequires:	libunity-misc-devel
BuildRequires:	libXfixes-devel
BuildRequires:	nux-devel
BuildRequires:	pango-devel
BuildRequires:	startup-notification-devel
BuildRequires:	unique-devel
BuildRequires:	utouch-geis-devel
BuildRequires:	utouch-grail-devel
BuildRequires:	xcb-util-wm-devel

Requires:	unity-common%{?_isa} = %{version}-%{release}

Requires:	compiz-plugins-main
Requires:	nux-tools
Requires:	gnome-python2-gconf
Requires:	unity-asset-pool

Requires(pre):	GConf2
Requires(post):	GConf2
Requires(preun):	GConf2

%description
Unity is a desktop experience that sings. Designed by Canonical and the Ayatana
community, Unity is all about the combination of familiarity and the future. We
bring together visual design, analysis of user experience testing, modern
graphics technologies and a deep understanding of the free software landscape to
produce what we hope will be the lightest, most elegant and most delightful way
to use your PC.

The Unity desktop experience is designed to allow for multiple implementations,
currently, Unity consists of a Compiz plugin based visual interface only, which
is heavily dependent on OpenGL.


%package core
Summary:	Core library for the Unity shell
Group:		System Environment/Libraries

Requires:	%{name}-common = %{version}-%{release}

%description core
This package contains the core library needed for Unity and Unity 2D.


%package core-devel
Summary:	Development files for the core Unity library
Group:		Development/Libraries

Requires:	%{name}-core%{?_isa} = %{version}-%{release}
Requires:	dee-devel
Requires:	glib2-devel
Requires:	libsigc++20-devel
Requires:	libunity-devel
Requires:	nux-devel

%description core-devel
This package contains the development files the core Unity library.


%package common
Summary:	Common files for the Unity shell
Group:		User Interface/Desktops

Requires:	%{name}%{?_isa} = %{version}-%{release}

# gdu-format-tool needed by plugins/unityshell/src/DeviceLauncherIcon.cpp
Requires:	libgdu-tools

%description common
This package contains files common to Unity and Unity 2D.


%prep
%setup -q

%patch0 -p1 -b .gtestdir
%patch1 -p1 -b .fixdirs
%patch2 -p1 -b .gsettingsfail

# Apply Ubuntu's patches
zcat '%{SOURCE99}' | patch -Np1


%build
mkdir build
cd build

# Remove '-gnu' from target triplet
%global _gnu %{nil}

# Cannot find gmodule
OPT_FLAGS="%{optflags}"
OPT_FLAGS="${OPT_FLAGS} $(pkg-config --cflags --libs gmodule-2.0)"
%global optflags "${OPT_FLAGS}"

C_COMPILER=%{_bindir}/%{_target_platform}-gcc-4.6
CXX_COMPILER=%{_bindir}/%{_target_platform}-g++-4.6

%cmake .. \
  -DCOMPIZ_BUILD_WITH_RPATH=FALSE \
  -DCOMPIZ_PACKAGING_ENABLED=TRUE \
  -DCOMPIZ_PLUGIN_INSTALL_TYPE=package \
  -DCMAKE_C_COMPILER="${C_COMPILER}" \
  -DCMAKE_CXX_COMPILER="${CXX_COMPILER}"

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT

cd build
make install DESTDIR=$RPM_BUILD_ROOT

# Install Compiz profile upgrade helpers
install -dm755 $RPM_BUILD_ROOT%{_sysconfdir}/compizconfig/upgrades/
install -m644 ../debian/profile_upgrade/com.canonical.unity.unity.03.upgrade \
              $RPM_BUILD_ROOT%{_sysconfdir}/compizconfig/upgrades/

# Put GConf schemas in correct directory
mv $RPM_BUILD_ROOT{%{_datadir},%{_sysconfdir}}/gconf/

# From debian/rules
rm $RPM_BUILD_ROOT%{_libdir}/compiz/libnetworkarearegion.so
rm $RPM_BUILD_ROOT%{_libdir}/compiz/libunitydialog.so
rm $RPM_BUILD_ROOT%{_datadir}/compiz/networkarearegion.xml
rm $RPM_BUILD_ROOT%{_datadir}/compiz/unitydialog.xml
rm $RPM_BUILD_ROOT%{_sysconfdir}/gconf/schemas/compiz-networkarearegion.schemas
rm $RPM_BUILD_ROOT%{_sysconfdir}/gconf/schemas/compiz-unitydialog.schemas
rm $RPM_BUILD_ROOT%{_datadir}/glib-2.0/schemas/org.freedesktop.compiz.networkarearegion.gschema.xml
rm $RPM_BUILD_ROOT%{_datadir}/glib-2.0/schemas/org.freedesktop.compiz.unitydialog.gschema.xml

%find_lang unity


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


%post core -p /usr/sbin/ldconfig

%postun core -p /usr/sbin/ldconfig


%files -f build/unity.lang
%doc AUTHORS ChangeLog HACKING README
%{_bindir}/unity
%dir %{_libdir}/compiz/
%{_libdir}/compiz/libgtkloader.so
%{_libdir}/compiz/libunitymtgrabhandles.so
%{_libdir}/compiz/libunityshell.so
%{_mandir}/man1/unity.1.gz
%dir %{_datadir}/compiz/
%dir %{_datadir}/compiz/unitymtgrabhandles/
%dir %{_datadir}/compiz/unitymtgrabhandles/images/
%{_datadir}/compiz/gtkloader.xml
%{_datadir}/compiz/unitymtgrabhandles.xml
%{_datadir}/compiz/unityshell.xml
%{_datadir}/compiz/unitymtgrabhandles/images/handle-0.png
%{_datadir}/compiz/unitymtgrabhandles/images/handle-1.png
%{_datadir}/compiz/unitymtgrabhandles/images/handle-2.png
%{_datadir}/compiz/unitymtgrabhandles/images/handle-3.png
%{_datadir}/compiz/unitymtgrabhandles/images/handle-4.png
%{_datadir}/compiz/unitymtgrabhandles/images/handle-5.png
%{_datadir}/compiz/unitymtgrabhandles/images/handle-6.png
%{_datadir}/compiz/unitymtgrabhandles/images/handle-7.png
%{_datadir}/compiz/unitymtgrabhandles/images/handle-8.png


%files core
%doc AUTHORS ChangeLog HACKING README
%{_libdir}/libunity-core-5.0.so.5
%{_libdir}/libunity-core-5.0.so.5.0.0


%files core-devel
%doc AUTHORS ChangeLog HACKING README
%dir %{_includedir}/Unity-5.0/
%dir %{_includedir}/Unity-5.0/UnityCore/
%{_includedir}/Unity-5.0/UnityCore/*.h
%{_libdir}/libunity-core-5.0.so
%{_libdir}/pkgconfig/unity-core-5.0.pc


%files common
%doc AUTHORS ChangeLog HACKING README
%{_libexecdir}/makebootchart.py*
%{_libexecdir}/migrate_favorites.py*
%{_libexecdir}/unity-panel-service
%{_mandir}/man1/unity-panel-service.1.gz
%{_datadir}/ccsm/icons/hicolor/64x64/apps/plugin-unityshell.png
%{_datadir}/dbus-1/services/com.canonical.Unity.Panel.Service.service
%{_datadir}/glib-2.0/schemas/com.canonical.Unity.gschema.xml
%{_datadir}/glib-2.0/schemas/org.freedesktop.compiz.gtkloader.gschema.xml
%{_datadir}/glib-2.0/schemas/org.freedesktop.compiz.unitymtgrabhandles.gschema.xml
%{_datadir}/glib-2.0/schemas/org.freedesktop.compiz.unityshell.gschema.xml
%dir %{_sysconfdir}/compizconfig/
%dir %{_sysconfdir}/compizconfig/upgrades/
# No 'config' macro because the profile upgrade helpers aren't really
# configuration files. They should probably be in /usr/share, but compiz doesn't
# search there.
%{_sysconfdir}/compizconfig/upgrades/com.canonical.unity.unity.03.upgrade
%{_sysconfdir}/gconf/schemas/compiz-gtkloader.schemas
%{_sysconfdir}/gconf/schemas/compiz-unitymtgrabhandles.schemas
%{_sysconfdir}/gconf/schemas/compiz-unityshell.schemas
%dir %{_datadir}/unity/
%dir %{_datadir}/unity/5/
%dir %{_datadir}/unity/themes/
%{_datadir}/unity/5/dash-widgets.json
%{_datadir}/unity/5/*.png
%{_datadir}/unity/5/*.svg
%{_datadir}/unity/themes/dash-widgets.json


%changelog
* Wed Jul 11 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 5.12.0-1.0ubuntu1.1
- Initial release
- Version 5.12.0
- Ubuntu release 0ubuntu1.1
