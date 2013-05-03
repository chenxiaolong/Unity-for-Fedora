# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

Name:		libaccounts-qt
Version:	1.7
Release:	1%{?dist}
Summary:	Qt library for Single Sign On

Group:		System Environment/Libraries
License:	LGPLv2
URL:		http://code.google.com/p/accounts-sso/
Source0:	http://accounts-sso.googlecode.com/files/accounts-qt-%{version}.tar.bz2

BuildRequires:	doxygen

BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(libaccounts-glib)
BuildRequires:	pkgconfig(QtCore)

%description
This package contains the Qt library for Single Sign On.


%package devel
Summary:	Development files for libaccounts-qt
Group:		Development/Libraries

Requires:	libaccounts-qt%{_isa} = %{version}-%{release}

%description devel
This package contains the development files for the accounts-qt library.


%package docs
Summary:	Documentation for libaccounts-qt
Group:		Documentation

BuildArch:	noarch

%description docs
This package contains the documentation for the accounts-qt library.


%prep
%setup -q -n accounts-qt-%{version}

# Fix documentation directory
sed -i '/^documentation.path/ s/$/-%{version}/' doc/doc.pri

# Disable rpath
sed -i '/QMAKE_RPATHDIR/d' tests/accountstest.pro


%build
%_qt4_qmake \
  PREFIX=%{_prefix} \
  LIBDIR=%{_libdir} \
  QMAKE_CXXFLAGS="%{optflags}"

make %{?_smp_mflags}


%install
make install INSTALL_ROOT=$RPM_BUILD_ROOT

# Silence rpmlint
find -type d -name '.moc' -exec rm -rvf {} \+


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc COPYING
%{_bindir}/accountstest
%{_libdir}/libaccounts-qt.so.*
%{_datadir}/libaccounts-qt-tests/


%files devel
%dir %{_includedir}/accounts-qt/
%dir %{_includedir}/accounts-qt/Accounts/
%{_includedir}/accounts-qt/Accounts/*
%{_libdir}/libaccounts-qt.so
%{_libdir}/pkgconfig/accounts-qt.pc


%files docs
%doc %{_docdir}/accounts-qt-%{version}/


%changelog
* Fri May 03 2013 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 1.7-1
- Version 1.7

* Sun Jan 27 2013 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 1.4-1
- Version 1.4
- Drop 0001_Multilib.patch
  - Upstream tarball is multilib-compatible now

* Sun Nov 18 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 1.3-1
- Version 1.3

* Sun Oct 07 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 1.2-2
- Add 0001_Multilib.patch
  - Use appropriate multilib libdir

* Thu Sep 27 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 1.2-1
- Initial release
- Version 1.2
