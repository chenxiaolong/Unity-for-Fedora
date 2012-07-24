# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

# Partially based off of Fedora 17's spec file

%global debug_package %{nil}

%define _ubuntu_rel 0ubuntu1

%define _obsolete_ver 3.5.0-100

Name:		gsettings-desktop-schemas-ubuntu
Version:	3.4.1
Release:	1.%{_ubuntu_rel}%{?dist}
Summary:	A collection of GSettings schemas

Group:		System Environment/Libraries
License:	LGPLv2+
URL:		http://bugzilla.gnome.org/enter_bug.cgi?product=gsettings-desktop-schemas
Source0:	http://download.gnome.org/sources/gsettings-desktop-schemas/3.4/gsettings-desktop-schemas-%{version}.tar.xz

Source99:	https://launchpad.net/ubuntu/+archive/primary/+files/gsettings-desktop-schemas_%{version}-%{_ubuntu_rel}.debian.tar.gz

BuildRequires:	gettext
BuildRequires:	intltool

BuildRequires:	glib2-devel
BuildRequires:	gobject-introspection-devel

Provides:	gsettings-desktop-schemas%{?_isa} = %{version}-%{release}
Provides:	gsettings-desktop-schemas         = %{version}-%{release}
Obsoletes:	gsettings-desktop-schemas%{?_isa} < %{_obsolete_ver}
Obsoletes:	gsettings-desktop-schemas         < %{_obsolete_ver}

%description
gsettings-desktop-schemas contains a collection of GSettings schemas for
settings shared by various components of a desktop.


%package devel
Summary:	Development files for gsettings-desktop-schemas-ubuntu
Group:		Development/Libraries

Requires:	%{name}%{?_isa} = %{version}-%{release}

Provides:       gsettings-desktop-schemas-devel%{?_isa} = %{version}-%{release}
Provides:       gsettings-desktop-schemas-devel         = %{version}-%{release}
Obsoletes:      gsettings-desktop-schemas-devel%{?_isa} < %{_obsolete_ver}
Obsoletes:      gsettings-desktop-schemas-devel         < %{_obsolete_ver}

%description devel
This package contains the development files for Ubuntu's patched version of
gsettings-desktop-schemas.


%prep
%setup -q -n gsettings-desktop-schemas-%{version}

# Apply Ubuntu's patches
tar zxvf '%{SOURCE99}'
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

install -dm755 $RPM_BUILD_ROOT%{_datadir}/glib-2.0/schemas/
install -m644 debian/gsettings-desktop-schemas.gsettings-override \
  $RPM_BUILD_ROOT%{_datadir}/glib-2.0/schemas/10_%{name}.gschema.override

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
%{_datadir}/glib-2.0/schemas/10_gsettings-desktop-schemas-ubuntu.gschema.override
%{_datadir}/glib-2.0/schemas/*.xml


%files devel
%dir %{_includedir}/gsettings-desktop-schemas/
%{_includedir}/gsettings-desktop-schemas/gdesktop-enums.h
%{_datadir}/pkgconfig/gsettings-desktop-schemas.pc
%{_datadir}/gir-1.0/GDesktopEnums-3.0.gir


%changelog
* Mon Jul 16 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.4.1-1.0ubuntu1
- Initial release
- Based off of F17's spec
- Version 3.4.1
- Ubuntu release 0ubuntu1
