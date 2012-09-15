# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

%define _ubuntu_rel 0ubuntu6

%define _gconf_schemas compiz-unitymtgrabhandles compiz-unityshell
%define _gconf_obsolete_schemas compiz-gtkloader

Name:		unity
Version:	6.4.0
Release:	2.%{_ubuntu_rel}%{?dist}
Summary:	A desktop experience designed for efficiency of space and interaction

Group:		User Interface/Desktops
License:	GPLv3 and LGPLv3
URL:		https://launchpad.net/unity
Source0:	https://launchpad.net/ubuntu/+archive/primary/+files/unity_%{version}.orig.tar.gz

# Autostart file for migrating Unity's dconf path
Source1:	unity-migrate-dconf-path.desktop

# These are the translations for Unity exported from Launchpad. Launchpad does
# not allow hotlinking, so I have uploaded the tarball to ompldr. Source 91
# contains the GPG signature signed by my GPG key, which can be obtained by
# running:
#   $ gpg --keyserver keyserver.ubuntu.com --recv-keys 90EFF32C

# Exported on: Wed, 01 Aug 2012 01:24:23 -0400
Source90:	http://ompldr.org/vZXh3bw/launchpad-export.tar.gz
Source91:	http://ompldr.org/vZXh3cA/launchpad-export.tar.gz.asc

Source99:	https://launchpad.net/ubuntu/+archive/primary/+files/unity_%{version}-%{_ubuntu_rel}.diff.gz

# Fix the gtest search in CMake
Patch0:		0001_fix_gtest_directory.patch

# Fix directories in source code and CMake (/usr/lib hardcoded)
Patch1:		0002_fix_directories.patch

# Ignore error about deprecated paths in GSettings schemas
Patch2:		0003_Ignore_deprecated_schema_path.patch

# Link against dbus-glib to avoid:
#  /usr/bin/ld: CMakeFiles/panel.dir/StandalonePanel.cpp.o: undefined reference to symbol 'dbus_g_thread_init'
Patch4:		0005_link_dbus-glib.patch

# Make desktop show "Fedora Desktop" in the panel instead of "Ubuntu Desktop"
Patch5:		0006_Fedora_Desktop_branding.patch

# Link against gmodule-2.0
Patch6:		0007_link_gmodule.patch

# GCC 4.6 is required or else Unity will segfault
BuildRequires:	gcc46-devel
BuildRequires:	gcc46-static

# Ubuntu's patched fixesproto and libXfixes is needed
BuildRequires:	libXfixes-ubuntu-devel
BuildRequires:	xorg-x11-proto-ubuntu-devel

BuildRequires:	cmake
BuildRequires:	desktop-file-utils
BuildRequires:	doxygen
BuildRequires:	gettext
BuildRequires:	intltool
BuildRequires:	pkgconfig
BuildRequires:	python-setuptools

BuildRequires:	boost-devel
BuildRequires:	compiz-plugins

BuildRequires:	pkgconfig(atk)
BuildRequires:	pkgconfig(libbamf3)
BuildRequires:	pkgconfig(cairo)
BuildRequires:	pkgconfig(compiz)
BuildRequires:	pkgconfig(dee-1.0)
BuildRequires:	pkgconfig(gconf-2.0)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gsettings-desktop-schemas)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(json-glib-1.0)
BuildRequires:	pkgconfig(libcompizconfig)
BuildRequires:	pkgconfig(dbusmenu-glib-0.4)
BuildRequires:	pkgconfig(gee-1.0)
BuildRequires:	pkgconfig(indicator-0.4)
BuildRequires:	pkgconfig(indicator3-0.4)
BuildRequires:	pkgconfig(libnotify)
BuildRequires:	pkgconfig(sigc++-2.0)
BuildRequires:	pkgconfig(unity)
BuildRequires:	pkgconfig(unity-misc)
BuildRequires:	pkgconfig(unity-protocol-private) >= 5.93.1
BuildRequires:	pkgconfig(nux-3.0) >= 3.2.0
BuildRequires:	pkgconfig(pango)
BuildRequires:	pkgconfig(libstartup-notification-1.0)
BuildRequires:	pkgconfig(unique-1.0)
BuildRequires:	pkgconfig(libgeis)
BuildRequires:	pkgconfig(grail)
BuildRequires:	pkgconfig(xcb-ewmh)

Requires:	unity-common%{?_isa} = %{version}-%{release}

Requires:	compiz-gnome
Requires:	compiz-plugins
Requires:	gnome-python2-gconf
Requires:	fedora-logos
Requires:	libXfixes-ubuntu
Requires:	nux-tools
Requires:	unity-asset-pool

Requires(pre):	GConf2
Requires(post):	GConf2
Requires(preun):	GConf2

Requires:	control-center-filesystem

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
Requires:	pkgconfig(dee-1.0)
Requires:	pkgconfig(glib-2.0)
Requires:	pkgconfig(sigc++-2.0)
Requires:	pkgconfig(unity)
Requires:	pkgconfig(nux-3.0) >= 3.2.0

%description core-devel
This package contains the development files the core Unity library.


%package common
Summary:	Common files for the Unity shell
Group:		User Interface/Desktops

Requires:	%{name}%{?_isa} = %{version}-%{release}

%description common
This package contains files common to Unity and Unity 2D.


%package autopilot
Summary:	Automatic testing for Unity
Group:		Development/Tools

BuildArch:	noarch

Requires:	%{name} = %{version}-%{release}

%description autopilot
This package contains the autopilot framework, which allows for triggering
keyboard and mouse events automatically. This package also contains the bindings
needed for writing automated tests in Python.


%prep
%setup -q

%patch0 -p1 -b .gtestdir
%patch1 -p1 -b .fixdirs
%patch2 -p1 -b .gsettingsfail
%patch4 -p1 -b .dbus-glib
%patch5 -p1 -b .fedora-branding
%patch6 -p1 -b .gmodule-2.0

# Apply Ubuntu's patches
zcat '%{SOURCE99}' | patch -Np1

# Use Launchpad translations
[ -d launchpad-po ] && rm -rv launchpad-po
mkdir launchpad-po
tar zxvf '%{SOURCE90}' -C launchpad-po
pushd po
rm LINGUAS && touch LINGUAS # Recreate LINGUAS (list of languages) file
for i in ../launchpad-po/po/*.po; do
  _NEWFILE=${i##*/} # Strip path
  _NEWFILE=${_NEWFILE#*-} # Strip 'unity-'
  cp "${i}" "${_NEWFILE}" # Copy new translation
  echo "${_NEWFILE%.*}" >> LINGUAS # Add translation
done
cp ../launchpad-po/po/unity.pot unity.pot
popd


%build
mkdir build
cd build

# Remove '-gnu' from target triplet
%global _gnu %{nil}

C_COMPILER=%{_bindir}/%{_target_platform}-gcc-4.6
CXX_COMPILER=%{_bindir}/%{_target_platform}-g++-4.6

%cmake .. \
  -DCOMPIZ_BUILD_WITH_RPATH=FALSE \
  -DCOMPIZ_PACKAGING_ENABLED=TRUE \
  -DCOMPIZ_PLUGIN_INSTALL_TYPE=package \
  -DUSE_GSETTINGS=TRUE \
  -DCMAKE_C_COMPILER="${C_COMPILER}" \
  -DCMAKE_CXX_COMPILER="${CXX_COMPILER}"

#make %{?_smp_mflags}
make -j1

pushd ../tests/autopilot/
%{__python} setup.py build
popd


%install
cd build
make install DESTDIR=$RPM_BUILD_ROOT

# Install autopilot
pushd ../tests/autopilot/
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
popd

# Install dconf path migration stuff
install -dm755 $RPM_BUILD_ROOT%{_sysconfdir}/xdg/autostart/
desktop-file-install --dir $RPM_BUILD_ROOT%{_sysconfdir}/xdg/autostart/ \
  '%{SOURCE1}'
install -m755 ../tools/migration-scripts/01_unity_change_dconf_path \
  $RPM_BUILD_ROOT%{_libexecdir}/
sed -i '1 i #!/bin/bash' \
  $RPM_BUILD_ROOT%{_libexecdir}/01_unity_change_dconf_path

# Use Fedora logo
rm $RPM_BUILD_ROOT%{_datadir}/unity/6/launcher_bfb.png
ln -s %{_datadir}/pixmaps/fedora-logo-sprite.png \
  $RPM_BUILD_ROOT%{_datadir}/unity/6/launcher_bfb.png

# Install profile convert files
install -dm755 $RPM_BUILD_ROOT%{_datadir}/compiz/migration/
install -m644 ../tools/convert-files/* \
  $RPM_BUILD_ROOT%{_datadir}/compiz/migration/

# Put GConf schemas in correct directory
mv $RPM_BUILD_ROOT{%{_datadir},%{_sysconfdir}}/gconf/

# From debian/rules
rm $RPM_BUILD_ROOT%{_libdir}/compiz/libnetworkarearegion.so
rm $RPM_BUILD_ROOT%{_libdir}/compiz/libunitydialog.so
rm $RPM_BUILD_ROOT%{_datadir}/compiz/networkarearegion.xml
rm $RPM_BUILD_ROOT%{_datadir}/compiz/unitydialog.xml
rm $RPM_BUILD_ROOT%{_sysconfdir}/gconf/schemas/compiz-networkarearegion.schemas
rm $RPM_BUILD_ROOT%{_sysconfdir}/gconf/schemas/compiz-unitydialog.schemas

%find_lang unity


%pre
%gconf_schema_prepare %{_gconf_schemas}
%gconf_schema_obsolete %{_gconf_obsolete_schemas}

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


%post core -p /sbin/ldconfig

%postun core -p /sbin/ldconfig


%files -f build/unity.lang
%doc AUTHORS ChangeLog HACKING README
%{_bindir}/unity
%{_sysconfdir}/xdg/autostart/unity-migrate-dconf-path.desktop
%{_libexecdir}/01_unity_change_dconf_path
%dir %{_libdir}/compiz/
%{_libdir}/compiz/libunitymtgrabhandles.so
%{_libdir}/compiz/libunityshell.so
%{_mandir}/man1/unity.1.gz
%dir %{_datadir}/compiz/
%dir %{_datadir}/compiz/migration/
%dir %{_datadir}/compiz/unitymtgrabhandles/
%dir %{_datadir}/compiz/unitymtgrabhandles/images/
%{_datadir}/compiz/unitymtgrabhandles.xml
%{_datadir}/compiz/unityshell.xml
%{_datadir}/compiz/migration/compiz-profile-active-unity.convert
%{_datadir}/compiz/migration/compiz-profile-unity.convert
%{_datadir}/compiz/unitymtgrabhandles/images/handle-0.png
%{_datadir}/compiz/unitymtgrabhandles/images/handle-1.png
%{_datadir}/compiz/unitymtgrabhandles/images/handle-2.png
%{_datadir}/compiz/unitymtgrabhandles/images/handle-3.png
%{_datadir}/compiz/unitymtgrabhandles/images/handle-4.png
%{_datadir}/compiz/unitymtgrabhandles/images/handle-5.png
%{_datadir}/compiz/unitymtgrabhandles/images/handle-6.png
%{_datadir}/compiz/unitymtgrabhandles/images/handle-7.png
%{_datadir}/compiz/unitymtgrabhandles/images/handle-8.png
%{_datadir}/gnome-control-center/keybindings/50-unity-launchers.xml


%files core
%doc AUTHORS ChangeLog HACKING README
%{_libdir}/libunity-core-6.0.so.5
%{_libdir}/libunity-core-6.0.so.5.0.0


%files core-devel
%doc AUTHORS ChangeLog HACKING README
%dir %{_includedir}/Unity-6.0/
%dir %{_includedir}/Unity-6.0/UnityCore/
%{_includedir}/Unity-6.0/UnityCore/*.h
%{_libdir}/libunity-core-6.0.so
%{_libdir}/pkgconfig/unity-core-6.0.pc


%files common
%doc AUTHORS ChangeLog HACKING README
%{_libexecdir}/makebootchart.py*
%{_libexecdir}/unity-panel-service
%{_mandir}/man1/unity-panel-service.1.gz
%{_datadir}/ccsm/icons/hicolor/64x64/apps/plugin-unityshell.png
%{_datadir}/dbus-1/services/com.canonical.Unity.Panel.Service.service
%{_datadir}/glib-2.0/schemas/com.canonical.Unity.gschema.xml
%{_datadir}/glib-2.0/schemas/org.compiz.networkarearegion.gschema.xml
%{_datadir}/glib-2.0/schemas/org.compiz.unitydialog.gschema.xml
%{_datadir}/glib-2.0/schemas/org.compiz.unitymtgrabhandles.gschema.xml
%{_datadir}/glib-2.0/schemas/org.compiz.unityshell.gschema.xml
%{_sysconfdir}/gconf/schemas/compiz-unitymtgrabhandles.schemas
%{_sysconfdir}/gconf/schemas/compiz-unityshell.schemas
%dir %{_datadir}/unity/
%dir %{_datadir}/unity/6/
%dir %{_datadir}/unity/themes/
%{_datadir}/unity/6/dash-widgets.json
%{_datadir}/unity/6/*.png
%{_datadir}/unity/6/*.svg
%{_datadir}/unity/themes/dash-widgets.json


%files autopilot
%doc AUTHORS ChangeLog HACKING README
%dir %{python_sitelib}/unity-1.0-py2.7.egg-info/
%{python_sitelib}/unity-1.0-py2.7.egg-info/PKG-INFO
%{python_sitelib}/unity-1.0-py2.7.egg-info/SOURCES.txt
%{python_sitelib}/unity-1.0-py2.7.egg-info/dependency_links.txt
%{python_sitelib}/unity-1.0-py2.7.egg-info/top_level.txt
# Tests
%dir %{python_sitelib}/unity/
%{python_sitelib}/unity/__init__.py*
%dir %{python_sitelib}/unity/emulators/
%{python_sitelib}/unity/emulators/__init__.py*
%{python_sitelib}/unity/emulators/dash.py*
%{python_sitelib}/unity/emulators/hud.py*
%{python_sitelib}/unity/emulators/icons.py*
%{python_sitelib}/unity/emulators/launcher.py*
%{python_sitelib}/unity/emulators/panel.py*
%{python_sitelib}/unity/emulators/quicklist.py*
%{python_sitelib}/unity/emulators/shortcut_hint.py*
%{python_sitelib}/unity/emulators/switcher.py*
%{python_sitelib}/unity/emulators/tooltip.py*
%{python_sitelib}/unity/emulators/unity.py*
%{python_sitelib}/unity/emulators/window_manager.py*
%{python_sitelib}/unity/emulators/workspace.py*
%dir %{python_sitelib}/unity/tests/
%{python_sitelib}/unity/tests/__init__.py*
%dir %{python_sitelib}/unity/tests/launcher/
%{python_sitelib}/unity/tests/launcher/__init__.py*
%{python_sitelib}/unity/tests/launcher/test_capture.py*
%{python_sitelib}/unity/tests/launcher/test_icon_behavior.py*
%{python_sitelib}/unity/tests/launcher/test_keynav.py*
%{python_sitelib}/unity/tests/launcher/test_reveal.py*
%{python_sitelib}/unity/tests/launcher/test_shortcut.py*
%{python_sitelib}/unity/tests/launcher/test_switcher.py*
%{python_sitelib}/unity/tests/launcher/test_visual.py*
%{python_sitelib}/unity/tests/test_command_lens.py*
%{python_sitelib}/unity/tests/test_dash.py*
%{python_sitelib}/unity/tests/test_home_lens.py*
%{python_sitelib}/unity/tests/test_hud.py*
%{python_sitelib}/unity/tests/test_ibus.py*
%{python_sitelib}/unity/tests/test_panel.py*
%{python_sitelib}/unity/tests/test_quicklist.py*
%{python_sitelib}/unity/tests/test_shortcut_hint.py*
%{python_sitelib}/unity/tests/test_showdesktop.py*
%{python_sitelib}/unity/tests/test_switcher.py*
%{python_sitelib}/unity/tests/test_unity_logging.py*


%changelog
* Fri Sep 14 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 6.4.0-2.0ubuntu6
- Ubuntu release 0ubuntu6

* Mon Sep 03 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 6.4.0-2.0ubuntu4
- Ubuntu release 0ubuntu4

* Sat Sep 01 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 6.4.0-2.0ubuntu1
- Build with GCC 4.6 again (until Fedora has GCC 4.7.1)

* Sat Sep 01 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 6.4.0-1.0ubuntu1
- Version 6.4.0
- Ubuntu release 0ubuntu1

* Tue Aug 28 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 6.2.0-1.0ubuntu4
- Version 6.2.0
- Ubuntu release 0ubuntu4

* Mon Aug 13 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 6.2.0-1.0ubuntu1
- Version 6.2.0
- Ubuntu release 0ubuntu1

* Wed Aug 01 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 6.0.0-3.0ubuntu4
- Add Launchpad translations snapshot from 2012-08-01

* Sun Jul 29 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 6.0.0-2.0ubuntu4
- Display "Fedora Desktop" in the panel when the desktop is focused

* Sat Jul 28 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 6.0.0-1.0ubuntu4
- Version 6.0.0
- Ubuntu release 0ubuntu4
- Add new autopilot subpackage

* Thu Jul 19 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 5.14.0-1
- Add com.canonical.unity.unity.03.upgrade from Ubuntu's packaging
- Remove lines related to Ubuntu's packaging to simplify spec file
- The 'big fat button' (launcher_bfb.png) now uses the Fedora logo

* Thu Jul 19 2012 Damian Ivanov <damiantorrpm@gmail.com> - 5.14.0
- Update to 5.14.0

* Wed Jul 11 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 5.12.0-1.0ubuntu1.1
- Initial release
- Version 5.12.0
- Ubuntu release 0ubuntu1.1
