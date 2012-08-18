# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

# This spec is partially based off of the official Fedora 17 spec. If a Fedora
# developer is reading this, feel free to merge this spec file :)

Name:		libindicator
Version:	12.10.0
Release:	2%{?dist}
Summary:	Shared functions for Ayatana indicators

Group:		System Environment/Libraries
License:	GPLv3
URL:		https://launchpad.net/libindicator
Source0:	https://launchpad.net/libindicator/12.10/%{version}/+download/libindicator-%{version}.tar.gz

BuildRequires:	gtk-doc
BuildRequires:	libtool

BuildRequires:	dbus-glib-devel
BuildRequires:	gtk2-devel
BuildRequires:	gtk3-devel

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

# Ubuntu doesn't package the dummy indicator
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
%dir %{_includedir}/libindicator-0.4/
%dir %{_includedir}/libindicator-0.4/libindicator/
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
%dir %{_datadir}/libindicator/
%{_datadir}/libindicator/80indicator-debugging


%files gtk3
%doc AUTHORS ChangeLog
%{_libdir}/libindicator3.so.7
%{_libdir}/libindicator3.so.7.0.0


%files gtk3-devel
%doc AUTHORS ChangeLog
%dir %{_includedir}/libindicator3-0.4/
%dir %{_includedir}/libindicator3-0.4/libindicator/
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
* Fri Aug 17 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 12.10.0-2
- Fix directory ownership

* Mon Aug 13 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 12.10.0-1
- Version 12.10.0

* Tue Jul 03 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.5.0-1
- Initial release
- Version 0.5.0
