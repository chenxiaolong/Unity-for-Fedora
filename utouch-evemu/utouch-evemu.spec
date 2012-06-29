# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

Name:		utouch-evemu
Version:	1.0.9
Release:	1%{?dist}
Summary:	Event Emulation for the uTouch Stack

Group:		System Environment/Libraries
License:	GPLv3 and LGPLv3
URL:		https://launchpad.net/utouch-evemu
Source0:	https://launchpad.net/utouch-evemu/trunk/utouch-evemu-%{version}/+download/utouch-evemu-%{version}.tar.xz

BuildRequires:	asciidoc
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	python2-devel
BuildRequires:	xmlto

%description
uTouch-evemu provides a programmatic API to access the kernel input event
devices. The original and intended purpose is for supporting multi-touch input,
especially with regard to the uTouch touch and gesture stack.


%package devel
Summary:	Development files for the utouch-evemu library
Group:		Development/Libraries

Requires:	%{name} = %{version}-%{release}

%description devel
This package contains the development files for the utouch-evemu library.


%package tools
Summary:	Event Emulation for the uTouch Stack - Tools
Group:		Development/Tools

Requires:	%{name} = %{version}-%{release}

%description tools
This package testing tools for the utouch-evemu library.


%package -n python-utouch-evemu
Summary:	Python 2 bindings for the utouch-evemu library
Group:		Development/Libraries

BuildArch:	noarch

Requires:	%{name} = %{version}-%{release}

%description -n python-utouch-evemu
This package includes the Python 2 bindings for the utouch-evemu library.


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


%post -p /usr/sbin/ldconfig

%postun -p /usr/sbin/ldconfig


%files
%doc ChangeLog README
%{_libdir}/libutouch-evemu.so.1
%{_libdir}/libutouch-evemu.so.1.0.0


%files devel
%doc ChangeLog README
%{_includedir}/evemu.h
%{_libdir}/libutouch-evemu.so
%{_libdir}/pkgconfig/utouch-evemu.pc


%files tools
%{_bindir}/evemu-describe
%{_bindir}/evemu-device
%{_bindir}/evemu-play
%{_bindir}/evemu-record
%{_mandir}/man1/evemu-describe.1.gz
%{_mandir}/man1/evemu-device.1.gz
%{_mandir}/man1/evemu-play.1.gz
%{_mandir}/man1/evemu-record.1.gz


%files -n python-utouch-evemu
%doc ChangeLog README
%dir %{python_sitelib}/evemu/
%{python_sitelib}/evemu/__init__.py*
%{python_sitelib}/evemu/base.py*
%{python_sitelib}/evemu/const.py*
%{python_sitelib}/evemu/exception.py*


%changelog
* Fri Jun 29 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 1.0.9-1
- Initial release
- Version 1.0.9
