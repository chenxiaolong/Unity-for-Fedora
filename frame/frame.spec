# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

Name:		frame
Version:	2.4.3
Release:	1%{?dist}
Summary:	Open Input Framework Frame Library

Group:		System Environment/Libraries
License:	GPLv3 and LGPLv3
URL:		https://launchpad.net/frame
Source0:	https://launchpad.net/frame/trunk/v%{version}/+download/frame-%{version}.tar.xz

BuildRequires:	asciidoc
BuildRequires:	xmlto
BuildRequires:	pkgconfig

BuildRequires:	pkgconfig(evemu)
BuildRequires:	pkgconfig(mtdev)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xi)
BuildRequires:	pkgconfig(xorg-server)

%description
# Description from Ubuntu's package
This library handles the buildup and synchronization of a set of simultaneous
touches. The library is input agnostic, with bindings for frame and XI2.1.


%package devel
Summary:	Development files for the frame library
Group:		Development/Libraries

Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains the development files for the frame library.


%package tools
Summary:	Touch Frame Library - Tools
Group:		Development/Tools

Requires:	%{name}%{?_isa} = %{version}-%{release}

%description tools
This package contains testing tools for the frame library.


%prep
%setup -q


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
%{_libdir}/libframe.so.*


%files devel
%doc README
%dir %{_includedir}/oif
%{_includedir}/oif/frame.h
%{_includedir}/oif/frame_backend.h
%{_includedir}/oif/frame_internal.h
%{_includedir}/oif/frame_x11.h
%{_libdir}/libframe.so
%{_libdir}/pkgconfig/frame.pc


%files tools
%{_bindir}/frame-test-x11
%{_mandir}/man1/frame-test-x11.1.gz


%changelog
* Sun Nov 18 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 2.4.3-1
- Version 2.4.3

* Tue Jul 24 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 2.2.4-1
- Version 2.2.4
- Upstream renamed from utouch-frame to frame

* Fri Jun 29 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 2.2.3-1
- Initial release
- Version 2.2.3
