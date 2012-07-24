# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

# This spec is partially based off of the official Fedora 17 spec. If a Fedora
# developer is reading this, feel free to merge this spec file :)

# The following line is for the scripts in my git repo
%define _ubuntu_match_rel 0ubuntu1

Name:		libindicator
Version:	0.5.0
Release:	1%{?dist}
Summary:	Shared functions for Ayatana indicators

Group:		System Environment/Libraries
License:	GPLv3
URL:		https://launchpad.net/libindicator
Source0:	https://launchpad.net/libindicator/0.5/%{version}/+download/libindicator-%{version}.tar.gz

BuildRequires:	gtk-doc
BuildRequires:	libtool

BuildRequires:	dbus-glib-devel
BuildRequires:	gtk2-devel
BuildRequires:	gtk3-devel

%if 0%{?opensuse_bs}
# Satisfy OBS conflict on xorg-x11-proto-devel
BuildRequires:	xorg-x11-proto-devel

# Satisfy OBS conflict on libXfixes-devel
BuildRequires:	libXfixes-devel
%endif

%description
A set of symbols and convenience functions that all Ayatana indicators are
likely to use.

This package contains the GTK2 version of this library.


%package devel
Summary:	Development files for libindicator
Group:		Development/Libraries

Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	gtk2-devel

%description devel
This package contains the development files for the indicator library.


%package tools
Summary:	Shared functions for Ayatana indicators - Tools
Group:		Development/Tools

Requires:	%{name}%{?_isa} = %{version}-%{release}

%description tools
This package contains the developer tools for the indicator library.


%package gtk3
Summary:	Shared functions for Ayatana indicators - GTK3
Group:		System Environment/Libraries

%description gtk3
A set of symbols and convenience functions that all Ayatana indicators are
likely to use.

This package contains the GTK 3 version of this library.


%package gtk3-devel
Summary:	Development files for libindicator-gtk3
Group:		Development/Libraries

Requires:	%{name}-gtk3%{?_isa} = %{version}-%{release}
Requires:	gtk3-devel
# Ubuntu's packaging says that this package should also depend on the GTK2
# versions of this library.
Requires:	%{name}-devel%{?_isa} = %{version}-%{release}

%description gtk3-devel
This package contains the development files for the indicator-gtk3 library.


%package gtk3-tools
Summary:	Shared functions for Ayatana indicators - GTK3 Tools
Group:		Development/Tools

Requires:	%{name}-gtk3%{?_isa} = %{version}-%{release}

%description gtk3-tools
This package contains the developer tools for the indicator-gtk3 library.


%prep
%setup -q


%build
%global _configure ../configure
mkdir build-gtk2 build-gtk3

pushd build-gtk2
%configure --with-gtk=2 --disable-static

# Disable rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}
popd

pushd build-gtk3
%configure --with-gtk=3 --disable-static

# Disable rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}
popd


%install
pushd build-gtk2
make install DESTDIR=$RPM_BUILD_ROOT
popd

pushd build-gtk3
make install DESTDIR=$RPM_BUILD_ROOT
popd

# Remove libtool files
find $RPM_BUILD_ROOT -type f -name '*.la' -delete

# Ubuntu doesn't package dummy indicator
rm $RPM_BUILD_ROOT%{_libdir}/libdummy-indicator-*.so


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%post gtk3 -p /sbin/ldconfig

%postun gtk3 -p /sbin/ldconfig


%files
%doc AUTHORS ChangeLog
%{_libdir}/libindicator.so.7
%{_libdir}/libindicator.so.7.0.0


%files devel
%doc AUTHORS ChangeLog
%{_includedir}/libindicator-0.4/libindicator/indicator-desktop-shortcuts.h
%{_includedir}/libindicator-0.4/libindicator/indicator-image-helper.h
%{_includedir}/libindicator-0.4/libindicator/indicator-object.h
%{_includedir}/libindicator-0.4/libindicator/indicator-service-manager.h
%{_includedir}/libindicator-0.4/libindicator/indicator-service.h
%{_includedir}/libindicator-0.4/libindicator/indicator.h
%{_libdir}/libindicator.so
%{_libdir}/pkgconfig/indicator-0.4.pc


%files tools
%doc AUTHORS ChangeLog
%{_libexecdir}/indicator-loader
%{_datadir}/libindicator/80indicator-debugging


%files gtk3
%doc AUTHORS ChangeLog
%{_libdir}/libindicator3.so.7
%{_libdir}/libindicator3.so.7.0.0


%files gtk3-devel
%doc AUTHORS ChangeLog
%{_includedir}/libindicator3-0.4/libindicator/indicator-desktop-shortcuts.h
%{_includedir}/libindicator3-0.4/libindicator/indicator-image-helper.h
%{_includedir}/libindicator3-0.4/libindicator/indicator-object.h
%{_includedir}/libindicator3-0.4/libindicator/indicator-service-manager.h
%{_includedir}/libindicator3-0.4/libindicator/indicator-service.h
%{_includedir}/libindicator3-0.4/libindicator/indicator.h
%{_libdir}/libindicator3.so
%{_libdir}/pkgconfig/indicator3-0.4.pc


%files gtk3-tools
%doc AUTHORS ChangeLog
%{_libexecdir}/indicator-loader3


%changelog
* Tue Jul 03 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.5.0-1
- Initial release
- Version 0.5.0
