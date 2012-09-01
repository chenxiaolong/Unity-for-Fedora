# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

Name:		libunity-webapps
Version:	2.1
Release:	1%{?dist}
Summary:	WebApps: Library for the integration with the Unity desktop

Group:		System Environment/Libraries
License:	LGPLv3
URL:		https://launchpad.net/libunity-webapps
Source0:	https://launchpad.net/libunity-webapps/trunk/%{version}/+download/unity_webapps-%{version}.tar.gz

Patch0:		0001_Fix_g_malloc.patch

BuildRequires:	gettext
BuildRequires:	gnome-common
BuildRequires:	gtk-doc
BuildRequires:	pkgconfig

BuildRequires:	pkgconfig(dbusmenu-gtk3-0.4)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(indicate-0.7)
BuildRequires:	pkgconfig(indicate-gtk-0.7)
BuildRequires:	pkgconfig(json-glib-1.0)
BuildRequires:	pkgconfig(libnotify)
BuildRequires:	pkgconfig(libsoup-2.4)
BuildRequires:	pkgconfig(libwnck-3.0)
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	pkgconfig(telepathy-glib)
BuildRequires:	pkgconfig(unity)

Requires:	unity-webapps-service

%description
This package contains a library for integrating Web Apps with the Unity desktop.


%package devel
Summary:	Development files for libunity-webapps
Group:		Development/Libraries

Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains the development files for the unity-webapps library.


%package -n unity-webapps-service
Summary:	Service for the unity-webapps library
Group:		User Interface/Desktops

%description -n unity-webapps-service
This package contains the DBus service, the GSettings schemas, the daemon, etc.
for the unity-webapps library.


%package docs
Summary:	Documentation for the unity-webapps library
Group:		Documentation

BuildArch:	noarch

%description docs
This package contains the documentation for the unity-webapps library.


%prep
%setup -q -n unity_webapps-%{version}

%patch0 -p1 -b .fix_g_malloc


%build
%configure --disable-static

# Disable rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT

# Remove libtool files
find $RPM_BUILD_ROOT -type f -name '*.la' -delete

%find_lang unity_webapps


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%postun -n unity-webapps-service
if [ ${1} -eq 0 ]; then
  glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans -n unity-webapps-service
glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :


%files
%doc COPYING
%{_libdir}/libunity-webapps-repository.so.*
%{_libdir}/libunity-webapps.so.*
%{_libdir}/girepository-1.0/UnityWebapps-0.2.typelib
%{_libdir}/girepository-1.0/UnityWebappsRepository-0.2.typelib


%files devel
%dir %{_includedir}/libunity-webapps-repository/
%{_includedir}/libunity-webapps-repository/*.h
%dir %{_includedir}/libunity_webapps-0.2/
%{_includedir}/libunity_webapps-0.2/*.h
%{_libdir}/libunity-webapps-repository.so
%{_libdir}/libunity-webapps.so
%{_libdir}/pkgconfig/libunity-webapps-repository.pc
%{_libdir}/pkgconfig/libunity_webapps-0.2.pc
%{_datadir}/gir-1.0/UnityWebapps-0.2.gir
%{_datadir}/gir-1.0/UnityWebappsRepository-0.2.gir


%files -n unity-webapps-service -f unity_webapps.lang
%{_bindir}/ubuntu-webapps-update-index
%{_bindir}/unity-webapps-runner
%{_libexecdir}/unity-webapps-context-daemon
%{_libexecdir}/unity-webapps-service
%{_datadir}/dbus-1/services/com.canonical.Unity.Webapps.Service.service
%{_datadir}/glib-2.0/schemas/com.canonical.unity.webapps.gschema.xml


%files docs
%doc %{_datadir}/gtk-doc/html/libunity-webapps/


%changelog
* Sat Sep 01 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 2.1-1
- Initial release
- Version 2.1
