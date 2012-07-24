# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

# This following line is for the scripts in my git repo
%define _ubuntu_match_rel 0ubuntu0.2

Name:		bamf
Version:	0.2.118
Release:	1%{?dist}
Summary:	Application Matching Framework - GTK 2

Group:		System Environment/Libraries
License:	LGPLv3
URL:		https://launchpad.net/bamf
Source0:	https://launchpad.net/bamf/0.2/%{version}/+download/bamf-%{version}.tar.gz

# Patches that Ubuntu backported (taken from Ubuntu packaging version 0.2.118
# -0ubuntu0.2).
Patch0:		0001_Ubuntu_backports_0.2.118-0ubuntu0.2.patch

BuildRequires:	dbus-glib-devel
BuildRequires:	glib2-devel
BuildRequires:	gobject-introspection-devel
BuildRequires:	gtk-doc
BuildRequires:	gtk2-devel
BuildRequires:	gtk3-devel
BuildRequires:	libgtop2-devel
BuildRequires:	libwnck-devel
BuildRequires:	libwnck3-devel

# No %{_isa} because the libraries are multilib, but bamf-daemon isn't
Requires:	bamf-daemon = %{version}-%{release}

# Satisfy OBS conflict on xorg-x11-proto-devel
BuildRequires:	xorg-x11-proto-devel

# Satisfy OBS conflict on libXfixes-devel
BuildRequires:	libXfixes-devel

%description
BAMF removes the headache of applications matching into a simple DBus daemon
and c wrapper library. Currently features application matching at amazing
levels of accuracy (covering nearly every corner case).

This package contains the GTK 2 version of this library.


%package daemon
Summary:	Application Matching Framework - Daemon
Group:		System Environment/Libraries

%description daemon
BAMF removes the headache of applications matching into a simple DBus daemon
and c wrapper library. Currently features application matching at amazing
levels of accuracy (covering nearly every corner case).

This package contains the daemon for the bamf library.


%package devel
Summary:	Development files for libbamf
Group:		Development/Libraries

Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	glib2-devel
Requires:	libwnck-devel

%description devel
This package contains the development files for the GTK 2 version of the bamf
library.


%package -n %{name}3
Summary:	Application Matching Library - GTK 3
Group:		System Environment/Libraries

Requires:	bamf-daemon = %{version}-%{release}

%description -n %{name}3
BAMF removes the headache of applications matching into a simple DBus daemon
and c wrapper library. Currently features application matching at amazing
levels of accuracy (covering nearly every corner case).

This package contains the GTK 3 version of this library.


%package -n %{name}3-devel
Summary:	Development files for libbamf3
Group:		Development/Libraries

Requires:	%{name}3%{?_isa} = %{version}-%{release}
Requires:	glib2-devel
Requires:	libwnck3-devel

%description -n %{name}3-devel
This package contains the development files for the GTK 3 version of the bamf
library.


%package docs
Summary:	Documentation for libbamf and libbamf3
Group:		Documentation

BuildArch:	noarch

%description docs
This package contains the documentation for the bamf library.


%prep
%setup -q

%patch0 -p1 -b .backports


%build
%global _configure ../configure
mkdir build-gtk2 build-gtk3

pushd build-gtk2
%configure --with-gtk=2 --enable-gtk-doc --disable-static
make %{?_smp_mflags}
popd

pushd build-gtk3
%configure --with-gtk=3 --enable-gtk-doc --disable-static
make %{?_smp_mflags}
popd


%install
rm -rf $RPM_BUILD_ROOT

pushd build-gtk2
make install DESTDIR=$RPM_BUILD_ROOT
popd

pushd build-gtk3
make install DESTDIR=$RPM_BUILD_ROOT
popd

# Remove libtool files
find $RPM_BUILD_ROOT -type f -name '*.la' -delete


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%post -n %{name}3 -p /sbin/ldconfig

%postun -n %{name}3 -p /sbin/ldconfig


%files
%doc TODO
%{_libdir}/libbamf.so.0
%{_libdir}/libbamf.so.0.0.0


%files daemon
%doc TODO
%{_libexecdir}/bamfdaemon
%{_datadir}/dbus-1/services/org.ayatana.bamf.service
%attr(644,root,root) %ghost %{_datadir}/applications/bamf.index


%files devel
%doc TODO
%dir %{_includedir}/libbamf/
%{_includedir}/libbamf/libbamf/bamf-application.h
%{_includedir}/libbamf/libbamf/bamf-control.h
%{_includedir}/libbamf/libbamf/bamf-indicator.h
%{_includedir}/libbamf/libbamf/bamf-matcher.h
%{_includedir}/libbamf/libbamf/bamf-tab-source.h
%{_includedir}/libbamf/libbamf/bamf-tab.h
%{_includedir}/libbamf/libbamf/bamf-view.h
%{_includedir}/libbamf/libbamf/bamf-window.h
%{_includedir}/libbamf/libbamf/libbamf.h
%{_libdir}/libbamf.so
%{_libdir}/pkgconfig/libbamf.pc


%files -n %{name}3
%doc TODO
%{_libdir}/libbamf3.so.0
%{_libdir}/libbamf3.so.0.0.0


%files -n %{name}3-devel
%doc TODO
%dir %{_includedir}/libbamf3/
%{_includedir}/libbamf3/libbamf/bamf-application.h
%{_includedir}/libbamf3/libbamf/bamf-control.h
%{_includedir}/libbamf3/libbamf/bamf-indicator.h
%{_includedir}/libbamf3/libbamf/bamf-matcher.h
%{_includedir}/libbamf3/libbamf/bamf-tab-source.h
%{_includedir}/libbamf3/libbamf/bamf-tab.h
%{_includedir}/libbamf3/libbamf/bamf-view.h
%{_includedir}/libbamf3/libbamf/bamf-window.h
%{_includedir}/libbamf3/libbamf/libbamf.h
%{_libdir}/libbamf3.so
%{_libdir}/pkgconfig/libbamf3.pc


%files docs
%dir %{_datadir}/gtk-doc/html/libbamf/
%{_datadir}/gtk-doc/html/libbamf/BamfApplication.html
%{_datadir}/gtk-doc/html/libbamf/BamfControl.html
%{_datadir}/gtk-doc/html/libbamf/BamfFactory.html
%{_datadir}/gtk-doc/html/libbamf/BamfMatcher.html
%{_datadir}/gtk-doc/html/libbamf/BamfTabSource.html
%{_datadir}/gtk-doc/html/libbamf/BamfView.html
%{_datadir}/gtk-doc/html/libbamf/BamfWindow.html
%{_datadir}/gtk-doc/html/libbamf/api-index-full.html
%{_datadir}/gtk-doc/html/libbamf/ch01.html
%{_datadir}/gtk-doc/html/libbamf/home.png
%{_datadir}/gtk-doc/html/libbamf/index.html
%{_datadir}/gtk-doc/html/libbamf/index.sgml
%{_datadir}/gtk-doc/html/libbamf/left.png
%{_datadir}/gtk-doc/html/libbamf/libbamf.devhelp2
%{_datadir}/gtk-doc/html/libbamf/object-tree.html
%{_datadir}/gtk-doc/html/libbamf/right.png
%{_datadir}/gtk-doc/html/libbamf/style.css
%{_datadir}/gtk-doc/html/libbamf/up.png


%changelog
* Tue Jul 03 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.2.118-1
- Initial release
- Version 0.2.118
