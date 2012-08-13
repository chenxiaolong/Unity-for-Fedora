# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

%define _ubuntu_rel 0ubuntu1

Name:		libunity
Version:	5.94.0
Release:	1.%{_ubuntu_rel}%{?dist}
Summary:	Library for integrating with Unity

Group:		System Environment/Libraries
License:	LGPLv3
URL:		https://launchpad.net/libunity
Source0:	https://launchpad.net/libunity/6.0/%{version}/+download/libunity-%{version}.tar.gz

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
A library for instrumenting- and integrating with all aspects of the Unity
shell.


%package devel
Summary:	Development files for libunity
Group:		Development/Libraries

Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	dee-devel
Requires:	glib2-devel
Requires:	libdbusmenu-glib-devel
Requires:	libgee06-devel


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

# Apply Ubuntu's patches
zcat '%{SOURCE99}' | patch -Np1
for i in $(grep -v '#' debian/patches/series); do
  patch -Np1 -i "debian/patches/${i}"
done


%build
%configure --enable-headless-tests --disable-static
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT

# Remove libtool files
find $RPM_BUILD_ROOT -type f -name '*.la' -delete


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc AUTHORS README
%{_libdir}/libunity.so.9
%{_libdir}/libunity.so.9.0.2
%dir %{_libdir}/libunity/
%{_libdir}/libunity/libunity-protocol-private.so.0
%{_libdir}/libunity/libunity-protocol-private.so.0.0.0
%{_libdir}/girepository-1.0/Unity-5.0.typelib
%{_datadir}/gir-1.0/Unity-5.0.gir
%{python_sitearch}/gi/overrides/Unity.py*


%files devel
%doc AUTHORS README
%dir %{_includedir}/unity/
%{_includedir}/unity/unity/unity-protocol.h
%{_includedir}/unity/unity/unity-trace.h
%{_includedir}/unity/unity/unity.h
%{_libdir}/libunity.so
%dir %{_libdir}/libunity/
%{_libdir}/libunity/libunity-protocol-private.so
%{_libdir}/pkgconfig/unity.pc
%{_libdir}/pkgconfig/unity-protocol-private.pc
%{_datadir}/vala/vapi/unity-protocol.vapi
%{_datadir}/vala/vapi/unity-trace.deps
%{_datadir}/vala/vapi/unity-trace.vapi
%{_datadir}/vala/vapi/unity.deps
%{_datadir}/vala/vapi/unity.vapi


%files tools
%doc AUTHORS README
%{_bindir}/libunity-tool


%changelog
* Mon Aug 13 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 5.94.0-1.0ubuntu1
- Version 5.94.0
- Ubuntu release 0ubuntu1
- New subpackage: tools

* Sun Jul 08 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 5.12.0-1.0ubuntu1.1
- Initial release
- Version 5.12.0
- Ubuntu release 0ubuntu1.1
