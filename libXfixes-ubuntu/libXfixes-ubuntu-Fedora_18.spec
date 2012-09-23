# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

%define _ubuntu_rel 4ubuntu4
%define _obsolete_ver 5.0-100

Name:		libXfixes
Version:	5.0
Release:	100.%{_ubuntu_rel}%{?dist}
Summary:	X.Org fixes extension library

Group:		System Environment/Libraries
License:	MIT
URL:		http://www.x.org
Source0:	http://xorg.freedesktop.org/releases/individual/lib/libXfixes-%{version}.tar.bz2

Source99:	https://launchpad.net/ubuntu/+archive/primary/+files/libxfixes_%{version}-%{_ubuntu_rel}.diff.gz

BuildRequires:	pkgconfig

# Ubuntu's patched fixesproto required
BuildRequires:	xorg-x11-proto-ubuntu-devel
BuildRequires:	pkgconfig(xext)

Provides:	libXfixes-ubuntu = %{version}-%{release}

%description
This package contains the X.Org fixes extension library.


%package devel
Summary:	Development files for libXfixes-ubuntu
Group:		Development/Libraries

Requires:	%{name}%{?_isa} = %{version}-%{release}

Provides:	libXfixes-ubuntu-devel = %{version}-%{release}

%description devel
This package contains the development files for Ubuntu's patched Xfixes library.


%prep
%setup -q

# Apply Ubuntu's patches
zcat '%{SOURCE99}' | patch -Np1
for i in $(grep -v '#' debian/patches/series); do
  patch -Np1 -i "debian/patches/${i}"
done


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
%doc AUTHORS ChangeLog README
%{_libdir}/libXfixes.so.3
%{_libdir}/libXfixes.so.3.1.0


%files devel
%doc AUTHORS ChangeLog README
%dir %{_includedir}/X11/
%dir %{_includedir}/X11/extensions/
%{_includedir}/X11/extensions/Xfixes.h
%{_libdir}/libXfixes.so
%{_libdir}/pkgconfig/xfixes.pc
%{_mandir}/man3/Xfixes.3.gz


%changelog
* Sun Sep 23 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 5.0-100.4ubuntu4
- Initial release for Fedora 18

* Wed Jul 11 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 5.0-1.4ubuntu4
- Initial release
- Version 5.0
- Ubuntu release 4ubuntu4
