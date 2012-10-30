# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

# Partially based off of Fedora 17's spec file

%global debug_package %{nil}

%define _ubuntu_rel 0ubuntu3

Name:		gsettings-desktop-schemas
Version:	3.6.0
Release:	1.%{_ubuntu_rel}%{?dist}
Summary:	A collection of GSettings schemas

Group:		System Environment/Libraries
License:	LGPLv2+
URL:		http://bugzilla.gnome.org/enter_bug.cgi?product=gsettings-desktop-schemas
Source0:	http://download.gnome.org/sources/gsettings-desktop-schemas/3.6/gsettings-desktop-schemas-%{version}.tar.xz

Source99:	https://launchpad.net/ubuntu/+archive/primary/+files/gsettings-desktop-schemas_%{version}-%{_ubuntu_rel}.debian.tar.gz

BuildRequires:	gettext
BuildRequires:	intltool
BuildRequires:	pkgconfig

BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gobject-introspection-1.0)

Provides:	gsettings-desktop-schemas-ubuntu = %{version}-%{release}

%description
gsettings-desktop-schemas contains a collection of GSettings schemas for
settings shared by various components of a desktop.


%package devel
Summary:	Development files for gsettings-desktop-schemas-ubuntu
Group:		Development/Libraries

Requires:	%{name}%{?_isa} = %{version}-%{release}

Provides:       gsettings-desktop-schemas-ubuntu-devel = %{version}-%{release}

%description devel
This package contains the development files for Ubuntu's patched version of
gsettings-desktop-schemas.


%prep
%setup -q

# Apply Ubuntu's patches
tar zxvf '%{SOURCE99}'

# Disable patches
  # Migration code is useless for us
    sed -i '/ubuntu_overlay-scrollbars.patch/d' debian/patches/series

for i in $(grep -v '#' debian/patches/series); do
  patch -Np1 -i "debian/patches/${i}"
done


%build
%configure \
  --disable-schemas-compile \
  --enable-introspection=yes

make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT

%find_lang gsettings-desktop-schemas


%postun
if [ ${1} -eq 0 ]; then
  glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :
fi

%posttrans
glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :


%files -f gsettings-desktop-schemas.lang
%doc AUTHORS NEWS README
%{_libdir}/girepository-1.0/GDesktopEnums-3.0.typelib
%{_datadir}/GConf/gsettings/gsettings-desktop-schemas.convert
%{_datadir}/GConf/gsettings/wm-schemas.convert
%{_datadir}/glib-2.0/schemas/*.xml


%files devel
%dir %{_includedir}/gsettings-desktop-schemas/
%{_includedir}/gsettings-desktop-schemas/gdesktop-enums.h
%{_datadir}/pkgconfig/gsettings-desktop-schemas.pc
%{_datadir}/gir-1.0/GDesktopEnums-3.0.gir


%changelog
* Mon Oct 29 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.6.0-1.0ubuntu3
- Version 3.6.0
- Ubuntu release 0ubuntu3

* Fri Sep 28 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.6.0-1.0ubuntu2
- Version 3.6.0
- Ubuntu release 0ubuntu2

* Thu Sep 20 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.5.92-1.0ubuntu2
- Initial release for Fedora 18
- Version 3.5.92
- Ubuntu release 0ubuntu2

* Fri Sep 14 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.4.2-1.0ubuntu1
- Version 3.4.2
- Ubuntu release 0ubuntu1

* Mon Jul 16 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.4.1-1.0ubuntu1
- Initial release
- Based off of F17's spec
- Version 3.4.1
- Ubuntu release 0ubuntu1
