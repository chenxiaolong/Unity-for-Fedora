# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

Name:		libunity
Version:	6.5.2
Release:	3%{?dist}
Summary:	Library for integrating with Unity

Group:		System Environment/Libraries
License:	LGPLv3
URL:		https://launchpad.net/libunity
Source0:	https://launchpad.net/libunity/6.0/%{version}/+download/libunity-%{version}.tar.gz

Patch0:		0001_unity-protocol-private.patch

BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	pkgconfig
BuildRequires:	python2
BuildRequires:	vala-tools

BuildRequires:	pkgconfig(dbusmenu-glib-0.4)
BuildRequires:	pkgconfig(dee-1.0)
BuildRequires:	pkgconfig(gee-1.0)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(gtk+-3.0)

%description
A library for instrumenting and integrating with all aspects of the Unity
shell.


%package devel
Summary:	Development files for libunity
Group:		Development/Libraries

Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	pkgconfig(dbusmenu-glib-0.4)
Requires:	pkgconfig(dee-1.0)
Requires:	pkgconfig(gee-1.0)
Requires:	pkgconfig(glib-2.0)

%description devel
This package contains the development files for the unity library.


%package tools
Summary:	Debugging tools for libunity
Group:		Development/Tools

Requires:	%{name}%{?_isa} = %{version}-%{release}

%description tools
This package contains the debugging tools for Unity lens.


%prep
%setup -q

%patch0 -p1 -b .unity-protocol-private

autoreconf -vfi


%build
%configure --enable-headless-tests --disable-static

# Disable rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT

# Remove libtool files
find $RPM_BUILD_ROOT -type f -name '*.la' -delete


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc AUTHORS README
%{_libdir}/libunity.so.*
%{_libdir}/libunity-protocol-private.so.*
%{_libdir}/girepository-1.0/Unity-6.0.typelib
%{python_sitearch}/gi/overrides/Unity.py*


%files devel
%doc AUTHORS README
%dir %{_includedir}/unity/
%dir %{_includedir}/unity/unity/
%{_includedir}/unity/unity/*.h
%{_libdir}/libunity.so
%{_libdir}/libunity-protocol-private.so
%{_libdir}/pkgconfig/unity.pc
%{_libdir}/pkgconfig/unity-protocol-private.pc
%{_datadir}/gir-1.0/Unity-6.0.gir
%{_datadir}/vala/vapi/unity-protocol.vapi
%{_datadir}/vala/vapi/unity-trace.deps
%{_datadir}/vala/vapi/unity-trace.vapi
%{_datadir}/vala/vapi/unity.deps
%{_datadir}/vala/vapi/unity.vapi


%files tools
%doc AUTHORS README
%{_bindir}/libunity-tool


%changelog
* Sun Sep 23 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 6.5.2-3
- Move libunity-protocol-private.so* to libdir instead of libdir/libunity

* Sat Sep 22 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 6.5.2-2
- We disable rpath, so unity-protocol-private must be added to the libunity
  pkgconfig file

* Thu Sep 20 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 6.5.2-1
- Version 6.5.2

* Mon Aug 27 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 5.96.0-1.0ubuntu1
- Version 5.96.0
- Ubuntu release 0ubuntu1

* Tue Aug 14 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 5.94.0-2.0ubuntu1
- Forgot to add Ubuntu's packaging files to the source list

* Mon Aug 13 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 5.94.0-1.0ubuntu1
- Version 5.94.0
- Ubuntu release 0ubuntu1
- New subpackage: tools

* Sun Jul 08 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 5.12.0-1.0ubuntu1.1
- Initial release
- Version 5.12.0
- Ubuntu release 0ubuntu1.1
