# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

Name:		dbus-test-runner
Version:	12.10.2daily13.02.26
Release:	1%{?dist}
Summary:	Run tests under a new DBus session

Group:		Development/Tools
License:	GPLv3
URL:		https://launchpad.net/dbus-test-runner
Source0:	https://launchpad.net/ubuntu/+archive/primary/+files/dbus-test-runner_%{version}.orig.tar.gz

BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gnome-common
BuildRequires:	gvfs
BuildRequires:	xorg-x11-server-Xvfb

BuildRequires:	pkgconfig(dbus-glib-1)

#Requires:	bustle
Requires:	gvfs
Requires:	libdbustest%{?_isa} = %{version}-%{release}

%description
A simple little executable for running a couple of programs under a new DBus
session.


%package -n libdbustest
Summary:	Shared library for running programs under a new DBus session
Group:		System Environment/Libraries

%description -n libdbustest
This package contains a shared library for running programs under a new DBus
session.


%package -n libdbustest-devel
Summary:	Development files for libdbustest
Group:		Development/Libraries

Requires:	libdbustest%{?_isa} = %{version}-%{release}
Requires:	pkgconfig(glib-2.0)

%description -n libdbustest-devel
This package contains the development files for the dbustest library.


%prep
%setup -q

autoreconf -vfi


%build
%configure --disable-static
make %{?_smp_mflags}


%check
make check


%install
make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name '*.la' -delete


%post -n libdbustest -p /sbin/ldconfig

%postun -n libdbustest -p /sbin/ldconfig


%files
%{_bindir}/dbus-test-runner
%dir %{_libexecdir}/dbus-test-runner/
%{_libexecdir}/dbus-test-runner/dbus-test-watchdog
%dir %{_datadir}/dbus-test-runner/
%{_datadir}/dbus-test-runner/dbus-test-bustle-handler
%{_datadir}/dbus-test-runner/session.conf


%files -n libdbustest
%{_libdir}/libdbustest.so.*


%files -n libdbustest-devel
%{_includedir}/libdbustest-1/
%{_libdir}/libdbustest.so
%{_libdir}/pkgconfig/dbustest-1.pc


%changelog
* Fri May 03 2013 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 12.10.2daily13.02.26-1
- Initial release
- Version 12.10.2daily13.02.26
