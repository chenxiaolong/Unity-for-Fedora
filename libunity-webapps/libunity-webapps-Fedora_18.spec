# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

%define _translations 20130418

Name:		libunity-webapps
Version:	2.5.0~daily13.03.18
Release:	1%{?dist}
Summary:	WebApps: Library for the integration with the Unity desktop

Group:		System Environment/Libraries
License:	LGPLv3
URL:		https://launchpad.net/libunity-webapps
Source0:	https://launchpad.net/ubuntu/+archive/primary/+files/libunity-webapps_%{version}.orig.tar.gz

Source98:	https://dl.dropboxusercontent.com/u/486665/Translations/translations-%{_translations}-libunity-webapps.tar.gz

BuildRequires:	chrpath
BuildRequires:	gettext
BuildRequires:	gnome-common
BuildRequires:	intltool
BuildRequires:	pkgconfig

BuildRequires:	pkgconfig(dbusmenu-gtk3-0.4)
BuildRequires:	pkgconfig(geoclue)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(indicate-0.7)
BuildRequires:	pkgconfig(indicate-gtk3-0.7)
BuildRequires:	pkgconfig(json-glib-1.0)
BuildRequires:	pkgconfig(libnotify)
BuildRequires:	pkgconfig(libsoup-2.4)
BuildRequires:	pkgconfig(libwnck-3.0)
BuildRequires:	pkgconfig(messaging-menu)
BuildRequires:	pkgconfig(packagekit-glib2)
BuildRequires:	pkgconfig(polkit-gobject-1)
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	pkgconfig(telepathy-glib)
BuildRequires:	pkgconfig(unity)

# CheckRequires
BuildRequires:	dbus-test-runner
BuildRequires:	xorg-x11-server-Xvfb

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


%prep
%setup -q

mkdir po_new
tar zxvf '%{SOURCE98}' -C po_new
rm -f po/LINGUAS po/*.pot
mv po_new/po/*.pot po/
for i in po_new/po/*.po; do
  FILE=$(sed -n "s|.*/unity_webapps-||p" <<< ${i})
  mv ${i} po/${FILE}
  echo ${FILE%.*} >> po/LINGUAS
done

autoreconf -vfi
intltoolize -f


%build
%configure --disable-static

make %{?_smp_mflags}


%check
make check


%install
make install DESTDIR=$RPM_BUILD_ROOT

# Remove libtool files
find $RPM_BUILD_ROOT -type f -name '*.la' -delete

chrpath -d $RPM_BUILD_ROOT%{_libdir}/*.so

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
%{_bindir}/unity-webapps-desktop-file
%{_bindir}/unity-webapps-runner
%{_libexecdir}/unity-webapps-context-daemon
%{_libexecdir}/unity-webapps-service
%{_datadir}/dbus-1/services/com.canonical.Unity.Webapps.Service.service
%{_datadir}/glib-2.0/schemas/com.canonical.unity.webapps.gschema.xml


%changelog
* Fri May 03 2013 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 2.5.0~daily13.03.18-1
- Version 2.5.0~daily13.03.18

* Sun Jan 27 2013 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 2.4.3daily13.01.10-1
- Version 2.4.3daily13.01.10
- Drop docs subpackage (non-existant documentation)

* Mon Nov 26 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 2.4.1-1.0ubuntu3.2
- Version 2.4.1
- Ubuntu release 0ubuntu3.2

* Sun Nov 18 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 2.4.1-1.0ubuntu3.1
- Version 2.4.1
- Ubuntu release 0ubuntu3.1

* Wed Oct 03 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 2.4.1-1
- Version 2.4.1

* Fri Sep 21 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 2.3.8-1
- Version 2.3.8

* Sat Sep 01 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 2.1-2
- Fix pkgconfig files ('-lunity_webapps' -> '-lunity-webapps')

* Sat Sep 01 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 2.1-1
- Initial release
- Version 2.1
