# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

%define _ubuntu_rel 0ubuntu1.1

Name:		libunity
Version:	5.12.0
Release:	1.%{_ubuntu_rel}%{?dist}
Summary:	Library for integrating with Unity

Group:		System Environment/Libraries
License:	LGPLv3
URL:		https://launchpad.net/libunity
Source0:	https://launchpad.net/libunity/5.0/%{version}/+download/libunity-%{version}.tar.gz

BuildRequires:	dee-devel
BuildRequires:	glib2-devel
BuildRequires:	gobject-introspection-devel
BuildRequires:	libdbusmenu-glib-devel
BuildRequires:	libgee06-devel
BuildRequires:	python2
BuildRequires:	vala-tools

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
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# Remove libtool files
find $RPM_BUILD_ROOT -type f -name '*.la' -delete


%post -p /usr/sbin/ldconfig

%postun -p /usr/sbin/ldconfig


%files
%doc AUTHORS README
%{_libdir}/libunity.so.9
%{_libdir}/libunity.so.9.0.2
%{_libdir}/girepository-1.0/Unity-5.0.typelib
%{_datadir}/gir-1.0/Unity-5.0.gir
%{python_sitearch}/gi/overrides/Unity.py*


%files devel
%doc AUTHORS README
%{_bindir}/unity-tool
%dir %{_includedir}/unity/
%{_includedir}/unity/unity/unity-trace.h
%{_includedir}/unity/unity/unity.h
%{_libdir}/libunity.so
%{_libdir}/pkgconfig/unity.pc
%{_datadir}/vala/vapi/unity-trace.deps
%{_datadir}/vala/vapi/unity-trace.vapi
%{_datadir}/vala/vapi/unity.deps
%{_datadir}/vala/vapi/unity.vapi


%changelog
* Sun Jul 08 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 5.12.0-1.0ubuntu1.1
- Initial release
- Version 5.12.0
- Ubuntu release 0ubuntu1.1
