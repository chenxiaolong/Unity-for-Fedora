# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

Name:		frame
Version:	2.2.4
Release:	1%{?dist}
Summary:	Open Input Framework Frame Library

Group:		System Environment/Libraries
License:	GPLv3 and LGPLv3
URL:		https://launchpad.net/frame
Source0:	https://launchpad.net/frame/trunk/utouch-frame-%{version}/+download/frame-%{version}.tar.xz

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

Provides:	utouch-frame%{?_isa} = %{version}-%{release}
Provides:	utouch-frame         = %{version}-%{release}
Obsoletes:	utouch-frame%{?_isa} < %{version}-%{release}
Obsoletes:	utouch-frame         < %{version}-%{release}

%description
# Description from Ubuntu's package
This library handles the buildup and synchronization of a set of simultaneous
touches. The library is input agnostic, with bindings for frame and XI2.1.


%package devel
Summary:	Development files for the frame library
Group:		Development/Libraries

Requires:	%{name}%{?_isa} = %{version}-%{release}

Provides:	utouch-frame-devel%{?_isa} = %{version}-%{release}
Provides:	utouch-frame-devel         = %{version}-%{release}
Obsoletes:	utouch-frame-devel%{?_isa} < %{version}-%{release}
Obsoletes:	utouch-frame-devel         < %{version}-%{release}

%description devel
This package contains the development files for the frame library.


%package tools
Summary:	Touch Frame Library - Tools
Group:		Development/Tools

Requires:	%{name}%{?_isa} = %{version}-%{release}

Provides:	utouch-frame-tools%{?_isa} = %{version}-%{release}
Provides:	utouch-frame-tools         = %{version}-%{release}
Obsoletes:	utouch-frame-tools%{?_isa} < %{version}-%{release}
Obsoletes:	utouch-frame-tools         < %{version}-%{release}

%description tools
This package contains testing tools for the frame library.


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
%{_libdir}/libframe.so.6
%{_libdir}/libframe.so.6.0.0


%files devel
%doc README
%{_includedir}/oif/frame.h
%{_includedir}/oif/frame_internal.h
%{_includedir}/oif/frame_x11.h
%{_libdir}/libframe.so
%{_libdir}/pkgconfig/frame.pc


%files tools
%{_bindir}/frame-test-x11
%{_mandir}/man1/frame-test-x11.1.gz


%changelog
* Tue Jul 24 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 2.2.4-1
- Version 2.2.4
- Upstream renamed from utouch-frame to frame

* Fri Jun 29 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 2.2.3-1
- Initial release
- Version 2.2.3
