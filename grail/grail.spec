# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

Name:		grail
Version:	3.1.0daily13.02.26
Release:	1%{?dist}
Summary:	Gesture Recognition And Instantiation Library

Group:		System Environment/Libraries
License:	GPLv3
URL:		https://launchpad.net/grail
Source0:	https://launchpad.net/ubuntu/+archive/primary/+files/grail_%{version}.orig.tar.gz

BuildRequires:	asciidoc
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	xmlto

BuildRequires:	pkgconfig(evemu)
BuildRequires:	pkgconfig(frame)
BuildRequires:	pkgconfig(mtdev)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xfixes)
BuildRequires:	pkgconfig(xi)

BuildRequires:	xorg-x11-proto-devel

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
Requires:	pkgconfig(frame)

%description devel
This package contains the development files for the grail library.


%package tools
Summary:	Gesture Recognition And Instantiation Library - Tools
Group:		Development/Tools

Requires:	%{name}%{?_isa} = %{version}-%{release}

%description tools
This package contains testing tools for the grail library.


%prep
%setup -q

autoreconf -vfi


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


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc README
%{_libdir}/libgrail.so.*


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
* Sat May 04 2013 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.1.0daily13.02.26-1
- Version 3.1.0daily13.02.26

* Tue Jan 29 2013 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.0.9daily12.12.07.1-1
- Version 3.0.9daily12.12.07.1

* Sun Nov 18 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.0.8-1
- Version 3.0.8

* Fri Jul 27 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.0.6-1
- Version 3.0.6
- Upstream renamed from utouch-grail to grail

* Fri Jun 29 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.0.5-1
- Initial release
- Version 3.0.5
