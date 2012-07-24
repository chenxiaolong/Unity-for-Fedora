# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

Name:		utouch-frame
Version:	2.2.3
Release:	1%{?dist}
Summary:	Touch Frame Library

Group:		System Environment/Libraries
License:	GPLv3 and LGPLv3
URL:		https://launchpad.net/utouch-frame
Source0:	https://launchpad.net/utouch-frame/trunk/utouch-frame-%{version}/+download/utouch-frame-%{version}.tar.xz

BuildRequires:	asciidoc
BuildRequires:	automake
BuildRequires:	gcc-c++
BuildRequires:	libtool
BuildRequires:	libX11-devel
BuildRequires:	libXi-devel
BuildRequires:	mtdev-devel
BuildRequires:	evemu-devel
BuildRequires:	xorg-x11-server-devel
BuildRequires:	xmlto

# Satisfy OBS conflict on xorg-x11-proto-devel
BuildRequires:	xorg-x11-proto-devel

%description
# Description from Ubuntu's package
This library handles the buildup and synchronization of a set of simultaneous
touches. The library is input agnostic, with bindings for mtdev, frame and
XI2.1.


%package devel
Summary:	Development files for the utouch-frame library
Group:		Development/Libraries

Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains the development files for the utouch-frame library.


%package tools
Summary:	Touch Frame Library - Tools
Group:		Development/Tools

Requires:	%{name}%{?_isa} = %{version}-%{release}

%description tools
This package testing tools for the utouch-frame library.


%prep
%setup -q

autoreconf -vfi


%build
%configure --disable-static
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# Remove libtool files
find $RPM_BUILD_ROOT -type f -name '*.la' -delete


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc ChangeLog README
%{_libdir}/libutouch-frame.so.1
%{_libdir}/libutouch-frame.so.1.4.0


%files devel
%doc ChangeLog README
%{_includedir}/utouch/frame-mtdev.h
%{_includedir}/utouch/frame.h
%{_includedir}/utouch/frame_internal.h
%{_includedir}/utouch/frame_x11.h
%{_libdir}/libutouch-frame.so
%{_libdir}/pkgconfig/utouch-frame.pc


%files tools
%{_bindir}/utouch-frame-test-mtdev
%{_bindir}/utouch-frame-test-x11
%{_mandir}/man1/utouch-frame-test-mtdev.1.gz
%{_mandir}/man1/utouch-frame-test-x11.1.gz


%changelog
* Fri Jun 29 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 2.2.3-1
- Initial release
- Version 2.2.3
