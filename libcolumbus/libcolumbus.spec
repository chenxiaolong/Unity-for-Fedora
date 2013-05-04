# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

Name:		libcolumbus
Version:	0.4.0daily13.04.16~13.04
Release:	1%{?dist}
Summary:	Error tolerant matching engine

Group:		System Environment/Libraries
License:	LGPLv3
URL:		https://launchpad.net/libcolumbus
Source0:	https://launchpad.net/ubuntu/+archive/primary/+files/libcolumbus_%{version}.orig.tar.gz

Patch0:		0001_Fix_boost-python_Detection.patch

BuildRequires:	boost-python-devel
BuildRequires:	cmake

BuildRequires:	pkgconfig(icu-i18n)
BuildRequires:	pkgconfig(libsparsehash)
BuildRequires:	pkgconfig(python3)

Requires:	%{name}-common = %{version}-%{release}

%description
A search engine designed to work with unclean data.


%package common
Summary:	Error tolerant matching engine - Common files
Group:		System Environment/Libraries

BuildArch:	noarch

%description common
This package contains the architecture-independent files for the columbus
library.


%package devel
Summary:	Development files for libcolumbus
Group:		Development/Libraries

Requires:	%{name} = %{version}-%{release}

%description devel
This package contains the development files for the columbus library.


%package -n python3-columbus
Summary:	Python bindings for libcolumbus
Group:		System Environment/Libraries

Requires:	%{name} = %{version}-%{release}

%description -n python3-columbus
This package contains the Python 3 bindings for the columbus library.


%prep
%setup -q

%patch0 -p1


%build
mkdir build/
cd build/
%cmake .. -DLIBDIR=%{_libdir} -DPYTHONDIR=%{python3_sitearch}
make %{?_smp_mflags}


%install
cd build/
make install DESTDIR=$RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc hacking.txt readme.txt
%{_libdir}/libcolumbus0.so.*


%files common
%{_datadir}/columbus0/


%files devel
%{_includedir}/columbus0/
%{_libdir}/libcolumbus0.so
%{_libdir}/pkgconfig/libcolumbus0.pc


%files -n python3-columbus
%{python3_sitearch}/columbus.py*
%{python3_sitearch}/_columbus.cpython-*.so
%{python3_sitearch}/__pycache__/columbus.cpython-*.py*


%changelog
* Sat May 04 2013 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.4.0daily13.04.16~13.04-1
- Initial release
- Version 0.4.0daily13.04.06~13.04
