# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

Name:		bamf3
Version:	0.4.0daily13.04.03
Release:	1%{?dist}
Summary:	Application Matching Framework

Group:		System Environment/Libraries
License:	LGPLv3
URL:		https://launchpad.net/bamf
Source0:	https://launchpad.net/ubuntu/+archive/primary/+files/bamf_%{version}.orig.tar.gz

Patch0:		0001_Fix_documentation.patch

BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gtk-doc
BuildRequires:	vala-tools

BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(libgtop-2.0)
BuildRequires:	pkgconfig(libunity_webapps-0.2)
BuildRequires:	pkgconfig(libwnck-3.0)

# CheckRequires
BuildRequires:	xorg-x11-server-Xvfb

# No %{_isa} because the libraries are multilib, but bamf-daemon isn't
Requires:	bamf-daemon = %{version}-%{release}

%description
BAMF removes the headache of applications matching into a simple DBus daemon
and c wrapper library. Currently features application matching at amazing
levels of accuracy (covering nearly every corner case).


%package -n bamf-daemon
Summary:	Application Matching Framework - Daemon
Group:		System Environment/Libraries

%description -n bamf-daemon
BAMF removes the headache of applications matching into a simple DBus daemon
and c wrapper library. Currently features application matching at amazing
levels of accuracy (covering nearly every corner case).

This package contains the daemon for the bamf library.


%package devel
Summary:	Development files for bamf3
Group:		Development/Libraries

Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	pkgconfig(glib-2.0)
Requires:	pkgconfig(libwnck-3.0)

%description devel
This package contains the development files for the bamf library.


%package docs
Summary:	Documentation for bamf3
Group:		Documentation

BuildArch:	noarch

%description docs
This package contains the documentation for the bamf library.


%prep
%setup -q -n bamf-%{version}

%patch0 -p1 -b .fix-docs

gtkdocize
autoreconf -vfi


%build
%configure --enable-gtk-doc --disable-static --enable-headless-tests
make %{?_smp_mflags}


%check
make check


%install
make install DESTDIR=$RPM_BUILD_ROOT

# Remove libtool files
find $RPM_BUILD_ROOT -type f -name '*.la' -delete

install -dm755 $RPM_BUILD_ROOT%{_datadir}/applications/
touch $RPM_BUILD_ROOT%{_datadir}/applications/bamf.index


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc TODO
%{_libdir}/libbamf3.so.*
%{_libdir}/girepository-1.0/Bamf-3.typelib


%files -n bamf-daemon
%doc TODO
%dir %{_libexecdir}/bamf/
%{_libexecdir}/bamf/bamfdaemon
%{_datadir}/dbus-1/services/org.ayatana.bamf.service
%attr(644,root,root) %ghost %{_datadir}/applications/bamf.index


%files devel
%doc TODO
%dir %{_includedir}/libbamf3/
%dir %{_includedir}/libbamf3/libbamf/
%{_includedir}/libbamf3/libbamf/*.h
%{_libdir}/libbamf3.so
%{_libdir}/pkgconfig/libbamf3.pc
%{_datadir}/gir-1.0/Bamf-3.gir
%{_datadir}/vala/vapi/libbamf3.vapi


%files docs
%doc %{_datadir}/gtk-doc/html/libbamf/


%changelog
* Fri May 03 2013 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.4.0daily13.04.03-1
- Version 0.4.0daily13.04.03

* Sun Jan 27 2013 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.4.0daily13.01.11-1
- Version 0.4.0daily13.01.11
- Drop deprecated GTK 2 subpackages

* Sat Oct 29 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.3.4-1
- Version 0.3.4

* Sat Oct 06 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.3.2-1
- Version 0.3.2

* Sat Sep 01 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.3.0-1
- Version 0.3.0

* Sat Aug 18 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.2.122-2
- Clean up spec file
- Use pkgconfig for dependencies

* Mon Aug 13 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.2.122-1
- Version 0.2.122

* Tue Jul 03 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.2.118-1
- Initial release
- Version 0.2.118
