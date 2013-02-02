# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

%define _ubuntu_rel 0ubuntu2

Name:		libaccounts-glib
Version:	1.5
Release:	1.%{_ubuntu_rel}%{?dist}
Summary:	Account management library for GLib Applications

Group:		System Environment/Libraries
License:	LGPLv2
URL:		https://code.google.com/p/accounts-sso/
Source0:	https://accounts-sso.googlecode.com/files/libaccounts-glib-%{version}.tar.gz

Source99:	https://launchpad.net/ubuntu/+archive/primary/+files/libaccounts-glib_%{version}-%{_ubuntu_rel}.debian.tar.gz

BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gtk-doc
BuildRequires:	pkgconfig

BuildRequires:	pkgconfig(check)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(pygobject-3.0)
BuildRequires:	pkgconfig(python2)
BuildRequires:	pkgconfig(python3)
BuildRequires:	pkgconfig(sqlite3)

BuildRequires:	python3-gobject

%description
This package contains the shared libraries for use by applications.


%package devel
Summary:	Development files for libaccounts-glib
Group:		Development/Libraries

Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	pkgconfig(glib-2.0)
Requires:	pkgconfig(libxml-2.0)
Requires:	pkgconfig(sqlite3)

%description devel
This package contains the development files for the accounts-glib library.


%package docs
Summary:	Documentation for libaccounts-glib
Group:		Documentation

BuildArch:	noarch

%description docs
This package contains the documentation for the accounts-glib library.


%package tools
Summary:	Tools for libaccounts-glib
Group:		Development/Tools

Requires:	%{name} = %{version}-%{release}

%description tools
This package contains the tools for the accounts-glib library.


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

pushd build-python3/pygobject/
make install DESTDIR=$RPM_BUILD_ROOT
popd

# Remove Meego specific file
rm -v $RPM_BUILD_ROOT%{_datadir}/backup-framework/applications/accounts.conf

# Remove libtool files
find $RPM_BUILD_ROOT -type f -name '*.la' -delete


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc AUTHORS
%{_libdir}/libaccounts-glib.so.*
%{_libdir}/girepository-1.0/Accounts-1.0.typelib
%{python_sitearch}/gi/overrides/Accounts.py*
%{python3_sitearch}/gi/overrides/Accounts.py*
%{python3_sitearch}/gi/overrides/__pycache__/Accounts.cpython-*.py*


%files devel
%dir %{_includedir}/libaccounts-glib/
%{_includedir}/libaccounts-glib/*.h
%{_libdir}/libaccounts-glib.so
%{_libdir}/pkgconfig/libaccounts-glib.pc
%{_datadir}/gir-1.0/Accounts-1.0.gir
%{_datadir}/vala/vapi/accounts.deps
%{_datadir}/vala/vapi/accounts.vapi


%files docs
%doc %{_datadir}/gtk-doc/html/libaccounts-glib/


%files tools
%{_bindir}/ag-backup
%{_bindir}/ag-tool
%{_mandir}/man1/ag-backup.1.gz
%{_mandir}/man1/ag-tool.1.gz
# Do these belong here?
%dir %{_datadir}/xml/
%dir %{_datadir}/xml/accounts/
%dir %{_datadir}/xml/accounts/schema/
%dir %{_datadir}/xml/accounts/schema/dtd/
%{_datadir}/xml/accounts/schema/dtd/accounts-*.dtd


%changelog
* Sun Jan 27 2013 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 1.5-1.0ubuntu2
- Version 1.5
- Ubuntu release 0ubuntu2
- Drop dependencies on dbus-glib

* Mon Sep 03 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 1.3-1.0ubuntu2
- Initial release
- Version 1.3
- Ubuntu release 0ubuntu2
