# written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

# This package uses the same structure as the official (outdated) Fedora
# package. Feel free to merge it :)

%define _ubuntu_rel 0ubuntu1

Name:		dee
Version:	1.0.14
Release:	1.%{_ubuntu_rel}%{?dist}
Summary:	Library for creating Model-View-Controller programs across DBus

Group:		System Environment/Libraries
License:	LGPLv3
URL:		https://launchpad.net/dee
Source0:	https://launchpad.net/dee/1.0/%{version}/+download/dee-%{version}.tar.gz

Source99:	https://launchpad.net/ubuntu/+archive/primary/+files/dee_%{version}-%{_ubuntu_rel}.diff.gz

BuildRequires:	gtk-doc
BuildRequires:	pkgconfig
BuildRequires:	vala-tools

BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(icu-i18n)
BuildRequires:	pkgconfig(python2)
BuildRequires:	pkgconfig(python3)

%description
Libdee is a library that uses DBus to provide objects allowing you to create
Model-View-Controller type programs across DBus. It also consists of utility
objects which extend DBus allowing for peer-to-peer discoverability of known
objects without needing a central registrar.


%package devel
Summary:	Development files for dee
Group:		Development/Libraries

Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	dbus-glib-devel
Requires:	glib2-devel

%description devel
This package contains the development files for the dee library.


%package tools
Summary:	Library for creating Model-View-Controller programs across DBus - Tools
Group:		Development/Tools

Requires:	%{name}%{?_isa} = %{version}-%{release}

%description tools
This package contains some tools from the dee library.


%package docs
Summary:	Documentation for dee
Group:		Documentation

BuildArch:	noarch

%description docs
This package contains the documentation for the dee library.


%prep
%setup -q

# Apply Ubuntu's patches
zcat '%{SOURCE99}' | patch -Np1


%build
%global _configure ../configure
mkdir build-python2 build-python3

pushd build-python2/
%configure --disable-static --enable-gtk-doc
make %{?_smp_mflags}
popd

pushd build-python3/
export PYTHON=python3
%configure --disable-static
popd


%install
pushd build-python2/
make install DESTDIR=$RPM_BUILD_ROOT
popd

pushd build-python3/bindings/python/
make install DESTDIR=$RPM_BUILD_ROOT
popd

# Remove libtool files
find $RPM_BUILD_ROOT -type f -name '*.la' -delete


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc AUTHORS
%{_libdir}/libdee-1.0.so.*
%{_libdir}/girepository-1.0/Dee-1.0.typelib
%{python_sitearch}/gi/overrides/Dee.py*
%{python3_sitearch}/gi/overrides/Dee.py*


%files devel
%doc AUTHORS
%dir %{_includedir}/dee-1.0/
%{_includedir}/dee-1.0/*.h
%{_libdir}/libdee-1.0.so
%{_libdir}/pkgconfig/dee-1.0.pc
%{_libdir}/pkgconfig/dee-icu-1.0.pc
%{_datadir}/gir-1.0/Dee-1.0.gir
%{_datadir}/vala/vapi/dee-1.0.deps
%{_datadir}/vala/vapi/dee-1.0.vapi


%files tools
%doc AUTHORS
%{_bindir}/dee-tool


%files docs
%{_datadir}/gtk-doc/html/dee-1.0/*.html
%{_datadir}/gtk-doc/html/dee-1.0/*.png
%{_datadir}/gtk-doc/html/dee-1.0/dee-1.0.devhelp2
%{_datadir}/gtk-doc/html/dee-1.0/index.sgml
%{_datadir}/gtk-doc/html/dee-1.0/style.css


%changelog
* Mon Aug 27 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 1.0.14-1.0ubuntu1
- Version 1.0.14
- Ubuntu release 0ubuntu1

* Sat Aug 18 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 1.0.12-2.0ubuntu1
- Remove unneeded dependencies
- Use pkgconfig for dependencies

* Mon Aug 13 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 1.0.12-1.0ubuntu1
- Version 1.0.12
- Ubuntu release 0ubuntu1

* Tue Jul 02 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 1.0.10-1.0ubuntu1
- Initial release
- Version 1.0.10
- Ubuntu release 0ubuntu1
