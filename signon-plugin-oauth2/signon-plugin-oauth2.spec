# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

Name:		signon-plugin-oauth2
Version:	0.14
Release:	1%{?dist}
Summary:	Oauth2 plugin for the Single Sign On Framework

Group:		User Interface/Desktops
License:	LGPLv2
URL:		http://code.google.com/p/accounts-sso/
Source0:	http://accounts-sso.googlecode.com/files/signon-oauth2-%{version}.tar.bz2

Patch0:		0001_Multilib.patch

BuildRequires:	signon-plugins-devel

BuildRequires:	pkgconfig(libsignon-qt)
BuildRequires:	pkgconfig(QJson)

Requires:	signon-ui

%description
This package contains the Oauth2 plugin for the Single Sign On Framework.


%package devel
Summary:	Development files for signon-plugin-oauth2
Group:		Development/Libraries

Requires:	%{name}%{_isa} = %{version}-%{release}

%description devel
This package contains the development files for the Oauth2 plugin for the Single
Sign On Framework.


%prep
%setup -q -n signon-oauth2-%{version}

%patch0 -p1 -b .multilib
sed -i 's|@LIB@|%{_lib}|g' src/signon-oauth2plugin.pc src/src.pro


%build
%_qt4_qmake \
  PREFIX=%{_prefix} \
  LIBDIR=%{_libdir} \
  QMAKE_CXXFLAGS="%{optflags}"

make %{?_smp_mflags}


%install
make install INSTALL_ROOT=$RPM_BUILD_ROOT

rm -v $RPM_BUILD_ROOT%{_sysconfdir}/signon-ui/webkit-options.d/*


%files
%doc COPYING
%{_bindir}/oauthclient
%{_bindir}/signon-oauth2plugin-tests
%dir %{_libdir}/signon/
%{_libdir}/signon/liboauth2plugin.so
%dir %{_datadir}/signon-oauth2plugin-tests/
%{_datadir}/signon-oauth2plugin-tests/tests.xml


%files devel
%dir %{_includedir}/signon-plugins/
%{_includedir}/signon-plugins/*.h
%{_libdir}/pkgconfig/signon-oauth2plugin.pc


%changelog
* Mon Jan 28 2013 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.14-1
- Version 0.14

* Sun Nov 18 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.12-1
- Version 0.12

* Sun Oct 07 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.11-2
- Add 0001_Multilib.patch
  - Use correct multilib libdir

* Thu Sep 27 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.11-1
- Initial release
- Version 0.11
