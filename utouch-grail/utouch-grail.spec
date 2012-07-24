# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

Name:		utouch-grail
Version:	3.0.5
Release:	1%{?dist}
Summary:	Gesture Recognition And Instantiation Library

Group:		System Environment/Libraries
License:	GPLv3
URL:		https://launchpad.net/utouch-grail
Source0:	https://launchpad.net/utouch-grail/trunk/utouch-grail-3.0.5/+download/utouch-grail-3.0.5.tar.gz

BuildRequires:	asciidoc
BuildRequires:	automake
BuildRequires:	gcc-c++
BuildRequires:	libtool
BuildRequires:	libX11-devel
BuildRequires:	libXext-devel
BuildRequires:	libXi-devel
BuildRequires:	mtdev-devel
BuildRequires:	evemu-devel
BuildRequires:	utouch-frame-devel
BuildRequires:	xorg-x11-proto-devel
BuildRequires:	xmlto

%description
When a multitouch gesture is performed on a device, the recognizer emits one or
several possible gestures. Once the context of the gesture is known, i.e., in
what window the touches land and what gestures the clients of that window
listen to, the instantiator delivers the matching set of gestures.

The library handles tentative getures, i.e., buffering of events for several
alternative gestures until a match is confirmed.


%package devel
Summary:	Development files for the utouch-grail library
Group:		Development/Libraries

Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	utouch-frame-devel

%description devel
This package contains the development files for the utouch-grail library.


%package tools
Summary:	Gesture Recognition And Instantiation Library - Tools
Group:		Development/Tools

Requires:	%{name}%{?_isa} = %{version}-%{release}

%description tools
This package testing tools for the utouch-grail library.


%prep
%setup -q

autoreconf -vfi


%build
%configure --disable-static
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT

# Remove libtool files
find $RPM_BUILD_ROOT -type f -name '*.la' -delete


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc ChangeLog README
%{_libdir}/libutouch-grail.so.1
%{_libdir}/libutouch-grail.so.1.3.0


%files devel
%doc ChangeLog README
%{_includedir}/grail-bits.h
%{_includedir}/grail-types.h
%{_includedir}/grail.h
%{_includedir}/utouch/grail.h
%{_libdir}/libutouch-grail.so
%{_libdir}/pkgconfig/utouch-grail.pc


%files tools
%{_bindir}/grail-gesture
%{_bindir}/grail-test-3-1
%{_bindir}/grail-test-atomic
%{_bindir}/grail-test-edge
%{_bindir}/grail-test-mtdev
%{_bindir}/grail-test-propagation
%{_mandir}/man1/grail-gesture.1.gz
%{_mandir}/man1/grail-test-3-1.1.gz
%{_mandir}/man1/grail-test-atomic.1.gz
%{_mandir}/man1/grail-test-edge.1.gz
%{_mandir}/man1/grail-test-mtdev.1.gz
%{_mandir}/man1/grail-test-propagation.1.gz


%changelog
* Fri Jun 29 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.0.5-1
- Initial release
- Version 3.0.5
