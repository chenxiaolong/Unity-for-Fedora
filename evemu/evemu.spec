# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

Name:		evemu
Version:	1.0.11daily13.02.20
Release:	1%{?dist}
Summary:	Linux Evdev Event Emulation Library

Group:		System Environment/Libraries
License:	GPLv3 and LGPLv3
URL:		https://launchpad.net/evemu
Source0:	https://launchpad.net/ubuntu/+archive/primary/+files/evemu_%{version}.orig.tar.gz

BuildRequires:	asciidoc
BuildRequires:	python2-devel
BuildRequires:	xmlto

%description
Evemu provides a programmatic API to access the kernel input event devices. The
original and intended purpose is for supporting multi-touch input, especially
with regard to the uTouch touch and gesture stack.


%package devel
Summary:	Development files for the evemu library
Group:		Development/Libraries

Requires:	%{name} = %{version}-%{release}

%description devel
This package contains the development files for the evemu library.


%package tools
Summary:	Linux Evdev Event Emulation Library - Tools
Group:		Development/Tools

Requires:	%{name} = %{version}-%{release}

%description tools
This package testing tools for the evemu library.


%package -n python-evemu
Summary:	Python 2 bindings for the evemu library
Group:		Development/Libraries

BuildArch:	noarch

Requires:	%{name} = %{version}-%{release}

%description -n python-evemu
This package includes the Python 2 bindings for the evemu library.


%prep
%setup -q

autoreconf -vfi


%build
%configure --disable-static
make -j1


%install
make install DESTDIR=$RPM_BUILD_ROOT

# Remove libtool files
find $RPM_BUILD_ROOT -type f -name '*.la' -delete


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc README
%{_libdir}/libevemu.so.*


%files devel
%doc README
%{_includedir}/evemu.h
%{_libdir}/libevemu.so
%{_libdir}/pkgconfig/evemu.pc


%files tools
%{_bindir}/evemu-describe
%{_bindir}/evemu-device
%{_bindir}/evemu-event
%{_bindir}/evemu-play
%{_bindir}/evemu-record
%{_mandir}/man1/evemu-describe.1.gz
%{_mandir}/man1/evemu-device.1.gz
%{_mandir}/man1/evemu-event.1.gz
%{_mandir}/man1/evemu-play.1.gz
%{_mandir}/man1/evemu-record.1.gz


%files -n python-evemu
%doc README
%dir %{python_sitelib}/evemu/
%{python_sitelib}/evemu/__init__.py*
%{python_sitelib}/evemu/base.py*
%{python_sitelib}/evemu/const.py*
%{python_sitelib}/evemu/exception.py*


%changelog
* Fri May 03 2013 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 1.0.11daily13.02.20-1
- Version 1.0.11daily13.02.20

* Tue Jan 29 2013 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 1.0.11daily12.11.29.1-1
- Version 1.0.11daily12.11.29.1

* Tue Jul 24 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 1.0.10-1
- Version 1.0.10
- Upstream renamed from utouch-evemu to evemu

* Fri Jun 29 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 1.0.9-1
- Initial release
- Version 1.0.9
