# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

Name:		ido
Version:	0.3.4
Release:	1%{?dist}
Summary:	Widgets and other objects used for indicators - GTK 2

Group:		System Environment/Libraries
License:	LGPLv2 and LGPLv3
URL:		https://launchpad.net/ido
Source0:	https://launchpad.net/ido/0.3/%{version}/+download/ido-%{version}.tar.gz

BuildRequires:	gtk-doc

BuildRequires:	glib2-devel
# Ubuntu's gtk2 and gtk3 packages are required
BuildRequires:	gtk2-devel >= 1:
BuildRequires:	gtk3-devel >= 1:

%description
This package contains the GTK 2 version of the ido library.


%package devel
Summary:	Development files for ido
Group:		Development/Libraries

Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	glib2-devel
Requires:	gtk2-devel >= 1:

%description devel
This package contains the development files for the GTK 2 version of the ido
library.


%package -n %{name}3
Summary:	Widgets and other objects used for indicators - GTK 3
Group:		System Environment/Libraries

%description -n %{name}3
This package contains the GTK 3 version of the ido library.


%package -n %{name}3-devel
Summary:	Development files for ido3
Group:		Development/Libraries

Requires:	%{name}3%{?_isa} = %{version}-%{release}
Requires:	glib2-devel
Requires:	gtk3-devel >= 1:

%description -n %{name}3-devel
This package contains the development files for the GTK 3 version of the ido
library.


%prep
%setup -q


%build
%global _configure ../configure
mkdir build-gtk2 build-gtk3

pushd build-gtk2
%configure --with-gtk=2 --disable-static
make %{?_smp_mflags}
popd

pushd build-gtk3
%configure --with-gtk=3 --disable-static
make %{?_smp_mflags}
popd


%install
rm -rf $RPM_BUILD_ROOT

pushd build-gtk2
make install DESTDIR=$RPM_BUILD_ROOT
popd

pushd build-gtk3
make install DESTDIR=$RPM_BUILD_ROOT
popd

# Remove libtool files
find $RPM_BUILD_ROOT -type f -name '*.la' -delete


%post -p /usr/sbin/ldconfig

%postun -p /usr/sbin/ldconfig


%post -n %{name}3 -p /usr/sbin/ldconfig

%postun -n %{name}3 -p /usr/sbin/ldconfig


%files
%doc AUTHORS
%{_libdir}/libido-0.1.so.0
%{_libdir}/libido-0.1.so.0.0.0


%files devel
%doc AUTHORS
%dir %{_includedir}/libido-0.1/
%{_includedir}/libido-0.1/libido/idocalendarmenuitem.h
%{_includedir}/libido-0.1/libido/idoentrymenuitem.h
%{_includedir}/libido-0.1/libido/idomessagedialog.h
%{_includedir}/libido-0.1/libido/idorange.h
%{_includedir}/libido-0.1/libido/idoscalemenuitem.h
%{_includedir}/libido-0.1/libido/idotimeline.h
%{_includedir}/libido-0.1/libido/libido.h
%{_libdir}/libido-0.1.so
%{_libdir}/pkgconfig/libido-0.1.pc


%files -n %{name}3
%doc AUTHORS
%{_libdir}/libido3-0.1.so.0
%{_libdir}/libido3-0.1.so.0.0.0


%files -n %{name}3-devel
%doc AUTHORS
%dir %{_includedir}/libido3-0.1/
%{_includedir}/libido3-0.1/libido/idocalendarmenuitem.h
%{_includedir}/libido3-0.1/libido/idoentrymenuitem.h
%{_includedir}/libido3-0.1/libido/idomessagedialog.h
%{_includedir}/libido3-0.1/libido/idorange.h
%{_includedir}/libido3-0.1/libido/idoscalemenuitem.h
%{_includedir}/libido3-0.1/libido/idotimeline.h
%{_includedir}/libido3-0.1/libido/libido.h
%{_libdir}/libido3-0.1.so
%{_libdir}/pkgconfig/libido3-0.1.pc


%changelog
* Wed Jul 04 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.3.4-1
- Initial release
- Version 0.3.4
