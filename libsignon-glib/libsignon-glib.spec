# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

%define _ubuntu_rel 0ubuntu1

Name:		libsignon-glib
Version:	1.6
Release:	1.%{_ubuntu_rel}%{?dist}
Summary:	Authentication management library for GLib applications

Group:		System Environment/Libraries
License:	LGPLv2
URL:		https://code.google.com/p/accounts-sso/
Source0:	https://accounts-sso.googlecode.com/files/libsignon-glib-%{version}.tar.gz

Source99:	https://launchpad.net/ubuntu/+archive/primary/+files/libsignon-glib_%{version}-%{_ubuntu_rel}.debian.tar.gz

BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gtk-doc
BuildRequires:	pkgconfig

BuildRequires:	pkgconfig(check)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(pygobject-3.0)
BuildRequires:	pkgconfig(python2)
BuildRequires:	pkgconfig(python3)
BuildRequires:	pkgconfig(signond)

BuildRequires:	python3-gobject

Requires:	signond

%description
This package contains the shared libraries for use by applications.


%package devel
Summary:	Development files libsignon-glib
Group:		Development/Libraries

Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	pkgconfig(dbus-glib-1)
Requires:	pkgconfig(glib-2.0)
Requires:	pkgconfig(signond)

%description devel
This package contains the development files for the signon-glib library.


%package docs
Summary:	Documentation for libsignon-glib
Group:		Documentation

BuildArch:	noarch

%description docs
This package contains the documentation for the signon-glib library.


%prep
%setup -q

# Apply Ubuntu's patches
tar zxvf '%{SOURCE99}'

for i in $(grep -v '#' debian/patches/series); do
  patch -Np1 -i "debian/patches/${i}"
done

autoreconf -vfi


%build
%global _configure ../configure
mkdir build-python2 build-python3

pushd build-python2/
%configure --disable-static --enable-gtk-doc
make -j1
popd

pushd build-python3/
export PYTHON=python3
%configure --disable-static
popd


%install
pushd build-python2/
make install DESTDIR=$RPM_BUILD_ROOT
popd

pushd build-python3/pygobject/
make install DESTDIR=$RPM_BUILD_ROOT
popd

# Remove useless empty files put in the wrong directory
rm -rv $RPM_BUILD_ROOT%{_prefix}/doc/

# Remove libtool files
find $RPM_BUILD_ROOT -type f -name '*.la' -delete


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc AUTHORS
%{_libdir}/libsignon-glib.so.*
%{_libdir}/girepository-1.0/Signon-1.0.typelib
%{python_sitearch}/gi/overrides/Signon.py*
%{python3_sitearch}/gi/overrides/Signon.py*
%{python3_sitearch}/gi/overrides/__pycache__/Signon.cpython-*.py*


%files devel
%dir %{_includedir}/libsignon-glib/
%{_includedir}/libsignon-glib/*.h
%{_libdir}/libsignon-glib.so
%{_libdir}/pkgconfig/libsignon-glib.pc
%{_datadir}/gir-1.0/Signon-1.0.gir
%{_datadir}/vala/vapi/signon.vapi


%files docs
%doc %{_datadir}/gtk-doc/html/libsignon-glib/


%changelog
* Mon Sep 03 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 1.6-1.0ubuntu1
- Initial release
- Version 1.6
- Ubuntu release 0ubuntu1
