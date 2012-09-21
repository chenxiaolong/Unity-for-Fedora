# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

Name:		ido
Version:	12.10.2
Release:	1%{?dist}
Summary:	Widgets and other objects used for indicators

Group:		System Environment/Libraries
License:	LGPLv2 and LGPLv3
URL:		https://launchpad.net/ido
Source0:	https://launchpad.net/ido/12.10/%{version}/+download/ido-%{version}.tar.gz

BuildRequires:	gtk-doc
BuildRequires:	pkgconfig

# Ubuntu's gtk3 package is required
BuildRequires:	gtk3-ubuntu-devel

BuildRequires:	pkgconfig(glib-2.0)

%description
(no files installed)


%package -n %{name}3
Summary:	Widgets and other objects used for indicators
Group:		System Environment/Libraries

Requires:	gtk3-ubuntu

%description -n %{name}3
This package contains the ido library.


%package -n %{name}3-devel
Summary:	Development files for ido3
Group:		Development/Libraries

Requires:	%{name}3%{?_isa} = %{version}-%{release}
Requires:	glib2-devel
# Ubuntu's gtk3 required
Requires:	gtk3-ubuntu-devel

%description -n %{name}3-devel
This package contains the development files for the ido library.


%prep
%setup -q


%build
%configure --disable-static
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT

# Remove libtool files
find $RPM_BUILD_ROOT -type f -name '*.la' -delete


%post -n %{name}3 -p /sbin/ldconfig

%postun -n %{name}3 -p /sbin/ldconfig


%files -n %{name}3
%doc AUTHORS
%{_libdir}/libido3-0.1.so.*


%files -n %{name}3-devel
%doc AUTHORS
%dir %{_includedir}/libido3-0.1/
%dir %{_includedir}/libido3-0.1/libido/
%{_includedir}/libido3-0.1/libido/*.h
%{_libdir}/libido3-0.1.so
%{_libdir}/pkgconfig/libido3-0.1.pc


%changelog
* Thu Sep 20 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 12.10.2-1
- Initial release for Fedora 18
- Version 12.10.2
- Drop gtk 2 package

* Wed Jul 04 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.3.4-1
- Initial release
- Version 0.3.4
