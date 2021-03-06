# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

Name:		signon
Version:	8.51
Release:	1%{?dist}
Summary:	Single Sign On Framework

Group:		System Environment/Libraries
License:	LGPLv2
URL:		https://code.google.com/p/accounts-sso/
Source0:	https://accounts-sso.googlecode.com/files/signon-%{version}.tar.bz2

Patch0:		0001_Multilib.patch

BuildRequires:	doxygen
BuildRequires:	graphviz
BuildRequires:	pkgconfig

BuildRequires:	pkgconfig(libproxy-1.0)
BuildRequires:	pkgconfig(libssl)
BuildRequires:	pkgconfig(QtCore)

%description
(no files installed)


%package -n libsignon-qt
Summary:	Single Sign On Framework for Qt
Group:		System Environment/Libraries

%description -n libsignon-qt
Framework that provides credential storage and authentication service.


%package -n libsignon-qt-devel
Summary:	Development files for libsignon-qt
Group:		Development/Libraries

Requires:	libsignon-qt%{?_isa} = %{version}-%{release}
Requires:	pkgconfig(QtCore)

%description -n libsignon-qt-devel
This package contains the development files for the signon-qt library.


%package -n libsignon-qt-docs
Summary:	Documentation for libsignon-qt
Group:		Documentation

BuildArch:	noarch

%description -n libsignon-qt-docs
This package contains the documentation for the signon-qt library.


%package -n signond
Summary:	Single Sign On Framework
Group:		System Environment/Libraries

%description -n signond
Framework that provides credential storage and authentication service.


%package -n signond-libs
Summary:	Single Sign On Framework
Group:		System Environment/Libraries

%description -n signond-libs
Framework that provides credential storage and authentication service.


%package -n signond-libs-devel
Summary:	Development files for signond-libs
Group:		Development/Libraries

Requires:	signond%{?_isa} = %{version}-%{release}
Requires:	signond-libs%{?_isa} = %{version}-%{release}
Requires:	pkgconfig(QtCore)

%description -n signond-libs-devel
This package contains the development files for signond-libs.


%package -n signond-docs
Summary:	Single Sign On Framework - Documentation
Group:		Documentation

BuildArch:	noarch

%description -n signond-docs
This package contains the documentation for signond.


%package -n signon-plugins
Summary:	Plugins for the Single Sign On Framework
Group:		System Environment/Libraries

Requires:	signond%{?_isa} = %{version}-%{release}

%description -n signon-plugins
This package contains the following plugins for the Single Sign On Framework:
- Password plugin
- Test plugin


%package -n signon-plugins-devel
Summary:	Development files for the Single Sign On Framework's plugins
Group:		Development/Libraries

Requires:	libsignon-qt-devel%{?_isa} = %{version}-%{release}

%description -n signon-plugins-devel
This package contains the development files necessary for creating plugins for
the Single Sign On Framework.


%package -n signon-plugins-docs
Summary:	Documentation for the Single Sign On Framework's plugins
Group:		Documentation

BuildArch:	noarch

%description -n signon-plugins-docs
This package contains the documentation for the Single Sign On Framework's
plugins.


%prep
%setup -q

# Use correct libdir
%patch0 -p1 -b .multilib
sed -i 's|@LIB@|%{_lib}|g' \
  lib/plugins/signon-plugins.pc.in \
  lib/plugins/signon-plugins-common/signon-plugins-common.pc.in \
  src/signond/signondaemon.h \
  src/remotepluginprocess/remotepluginprocess.h \
  src/plugins/example/exampleplugin.pro

# Fix documentation directory
sed -i '/^documentation.path/ s/$/-%{version}/' \
  doc/doc.pri \
  lib/plugins/doc/doc.pri \
  lib/SignOn/doc/doc.pri

sed -i '/^example.path/ s/\(signon-plugins-dev\)/\1-%{version}/' \
  src/plugins/example/example.pro


%build
%_qt4_qmake \
  PREFIX=%{_prefix} \
  LIBDIR=%{_libdir} \
  QMAKE_CXXFLAGS="%{optflags}"

make %{?_smp_mflags}


%install
make install INSTALL_ROOT=$RPM_BUILD_ROOT

# Remove tests
find $RPM_BUILD_ROOT -type f -name '*tests*' -delete


%post -n libsignon-qt -p /sbin/ldconfig

%postun -n libsignon-qt -p /sbin/ldconfig


%post -n signond-libs -p /sbin/ldconfig

%postun -n signond-libs -p /sbin/ldconfig


%files -n libsignon-qt
%{_libdir}/libsignon-qt.so.*


%files -n libsignon-qt-devel
%dir %{_includedir}/signon-qt/
%dir %{_includedir}/signon-qt/SignOn/
%{_includedir}/signon-qt/SignOn/*
%{_libdir}/libsignon-qt.so
%{_libdir}/libsignon-qt.a
%{_libdir}/pkgconfig/libsignon-qt.pc


%files -n libsignon-qt-docs
%doc %{_docdir}/libsignon-qt-%{version}/


%files -n signond
%doc COPYING
%{_bindir}/signond
%{_bindir}/signonpluginprocess
%config(noreplace) %{_sysconfdir}/signond.conf
%{_datadir}/dbus-1/services/com.google.code.AccountsSSO.SingleSignOn.service
%{_datadir}/dbus-1/services/com.nokia.SingleSignOn.Backup.service


%files -n signond-libs
%{_libdir}/libsignon-extension.so.*
%{_libdir}/libsignon-plugins-common.so.*


%files -n signond-libs-devel
%dir %{_includedir}/signond/
%{_includedir}/signond/*.h
%dir %{_includedir}/signon-extension/
%dir %{_includedir}/signon-extension/SignOn/
%{_includedir}/signon-extension/SignOn/*
%{_libdir}/libsignon-extension.so
%{_libdir}/libsignon-plugins-common.so
%{_libdir}/pkgconfig/signond.pc
%{_libdir}/pkgconfig/SignOnExtension.pc
%{_datadir}/dbus-1/interfaces/com.google.code.AccountsSSO.SingleSignOn.AuthService.xml
%{_datadir}/dbus-1/interfaces/com.google.code.AccountsSSO.SingleSignOn.AuthSession.xml
%{_datadir}/dbus-1/interfaces/com.google.code.AccountsSSO.SingleSignOn.Identity.xml


%files -n signond-docs
%doc %{_docdir}/signon-%{version}/


%files -n signon-plugins
%dir %{_libdir}/signon/
%{_libdir}/signon/libexampleplugin.so
%{_libdir}/signon/libpasswordplugin.so
%{_libdir}/signon/libssotest2plugin.so
%{_libdir}/signon/libssotestplugin.so


%files -n signon-plugins-devel
%doc %{_docdir}/signon-plugins-dev-%{version}/
%dir %{_includedir}/signon-plugins/
%dir %{_includedir}/signon-plugins/SignOn/
%{_includedir}/signon-plugins/SignOn/*.h
%{_includedir}/signon-plugins/*
%{_libdir}/libsignon-plugins.a
%{_libdir}/pkgconfig/signon-plugins-common.pc
%{_libdir}/pkgconfig/signon-plugins.pc


%files -n signon-plugins-docs
%doc %{_docdir}/signon-plugins-%{version}/


%changelog
* Fri May 03 2013 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 8.51-1
- Version 8.51

* Sun Jan 27 2013 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 8.46-1
- Version 8.46

* Sun Nov 18 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 8.44-1.0ubuntu1
- Version 8.44
- Ubuntu release 0ubuntu1

* Sun Oct 07 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 8.43-2.0ubuntu1
- Add 0001_Multilib.patch
  - Use appropriate multilib libdir

* Thu Sep 20 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 8.43-1.0ubuntu1
- Version 8.43
- Ubuntu release 0ubuntu1

* Fri Sep 14 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 8.42-2.0ubuntu2
- Ship static libraries

* Fri Sep 14 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 8.42-1.0ubuntu2
- Version 8.42
- Ubuntu release 0ubuntu2

* Mon Sep 03 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 8.41-1.0ubuntu3
- Initial release
- Version 8.41
- Ubuntu release 0ubuntu3
