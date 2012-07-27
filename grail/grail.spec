# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

Name:		grail
Version:	3.0.6
Release:	1%{?dist}
Summary:	Gesture Recognition And Instantiation Library

Group:		System Environment/Libraries
License:	GPLv3
URL:		https://launchpad.net/grail
Source0:	https://launchpad.net/grail/trunk/%{version}/+download/grail-%{version}.tar.gz

BuildRequires:	asciidoc
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gcc-c++
BuildRequires:	libtool
BuildRequires:	libX11-devel
BuildRequires:	libXext-devel
BuildRequires:	libXi-devel
BuildRequires:	mtdev-devel
BuildRequires:	evemu-devel
BuildRequires:	frame-devel
BuildRequires:	xorg-x11-proto-devel
BuildRequires:	xmlto

Provides:	utouch-grail%{?_isa} = %{version}-%{release}
Provides:	utouch-grail         = %{version}-%{release}
Obsoletes:	utouch-grail%{?_isa} < %{version}-%{release}
Obsoletes:	utouch-grail         < %{version}-%{release}

%description
When a multitouch gesture is performed on a device, the recognizer emits one or
several possible gestures. Once the context of the gesture is known, i.e., in
what window the touches land and what gestures the clients of that window
listen to, the instantiator delivers the matching set of gestures.

The library handles tentative getures, i.e., buffering of events for several
alternative gestures until a match is confirmed.


%package devel
Summary:	Development files for the grail library
Group:		Development/Libraries

Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	frame-devel

Provides:	utouch-grail-devel%{?_isa} = %{version}-%{release}
Provides:	utouch-grail-devel         = %{version}-%{release}
Obsoletes:	utouch-grail-devel%{?_isa} < %{version}-%{release}
Obsoletes:	utouch-grail-devel         < %{version}-%{release}

%description devel
This package contains the development files for the grail library.


%package tools
Summary:	Gesture Recognition And Instantiation Library - Tools
Group:		Development/Tools

Requires:	%{name}%{?_isa} = %{version}-%{release}

Provides:	utouch-grail-tools%{?_isa} = %{version}-%{release}
Provides:	utouch-grail-tools         = %{version}-%{release}
Obsoletes:	utouch-grail-tools%{?_isa} < %{version}-%{release}
Obsoletes:	utouch-grail-tools         < %{version}-%{release}

%description tools
This package contains testing tools for the grail library.


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
%doc README
%{_libdir}/libgrail.so.5
%{_libdir}/libgrail.so.5.0.0


%files devel
%doc README
%{_includedir}/oif/grail.h
%{_libdir}/libgrail.so
%{_libdir}/pkgconfig/grail.pc


%files tools
%{_bindir}/grail-test-3-1
%{_bindir}/grail-test-atomic
%{_bindir}/grail-test-edge
%{_bindir}/grail-test-propagation
%{_mandir}/man1/grail-test-3-1.1.gz
%{_mandir}/man1/grail-test-atomic.1.gz
%{_mandir}/man1/grail-test-edge.1.gz
%{_mandir}/man1/grail-test-propagation.1.gz


%changelog
* Fri Jul 27 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.0.6-1
- Version 3.0.6
- Upstream renamed from utouch-grail to grail

* Fri Jun 29 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.0.5-1
- Initial release
- Version 3.0.5
