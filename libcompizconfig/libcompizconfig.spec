# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

%define _bzr_rev 428
%define _ubuntu_rel 0ubuntu6

Name:		libcompizconfig
Version:	0.9.7.0
Release:	1.bzr%{_bzr_rev}.%{_ubuntu_rel}%{?dist}
Summary:	Settings library for Compiz plugins

Group:		System Environment/Libraries
License:	GPLv2
URL:		https://launchpad.net/libcompizconfig
Source0:	https://launchpad.net/ubuntu/+archive/primary/+files/libcompizconfig_%{version}~bzr%{_bzr_rev}.orig.tar.bz2

Source99:	https://launchpad.net/ubuntu/+archive/primary/+files/libcompizconfig_%{version}~bzr%{_bzr_rev}-%{_ubuntu_rel}.debian.tar.gz

# Do not hardcode library directory to %{_prefix}/lib/
Patch0:		0001_Fix_compizconfig_backend_install_dir.patch

BuildRequires:	cmake
BuildRequires:	gcc-c++
BuildRequires:	intltool

BuildRequires:	boost-devel
BuildRequires:	compiz-devel
BuildRequires:	libxml2-devel
BuildRequires:	libxslt-devel
BuildRequires:	protobuf-compiler
BuildRequires:	protobuf-devel

Requires:	compiz

BuildRequires:	GConf2
Requires(pre):	GConf2
Requires(post):	GConf2
Requires(preun): GConf2

# Satisfy OBS conflict on gtk3 (installed by build dependencies)
BuildRequires:	gtk3
BuildRequires:	gtk3-devel

%description
This package provides the library to configure settings for Compiz plugins.


%package devel
Summary:	Development files for libcompizconfig
Group:		Development/Libraries

Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains the development files creating Compiz plugins with
settings support.


%prep
%setup -q -n %{name}-0.9.5.94

%patch0 -p1 -b .libdir

# Apply Ubuntu's patches
tar zxvf '%{SOURCE99}'
for i in $(grep -v '#' debian/patches/series); do
  patch -Np1 -i "debian/patches/${i}"
done


%build
mkdir build
cd build
%cmake .. \
  -DCOMPIZ_BUILD_WITH_RPATH=FALSE \
  -DCOMPIZ_PACKAGING_ENABLED=TRUE \
  -DCOMPIZ_PLUGIN_INSTALL_TYPE=package \
  -DUSE_GSETTINGS=OFF \
  -DCOMPIZ_DISABLE_GS_SCHEMAS_INSTALL=ON \
  -DCOMPIZ_DESTDIR=$RPM_BUILD_ROOT # Compiz's build system is messed up

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
cd build
make install #DESTDIR=$RPM_BUILD_ROOT
make findcompizconfig_install

# Install Compiz profiles
install -dm755 $RPM_BUILD_ROOT%{_datadir}/compizconfig/
install -m644 ../debian/{normal,extra}.profile \
              $RPM_BUILD_ROOT%{_datadir}/compizconfig/

# Install configuration file
install -dm755 $RPM_BUILD_ROOT%{_sysconfdir}/compizconfig/
install -m644 ../config/config \
              $RPM_BUILD_ROOT%{_sysconfdir}/compizconfig/

# Put GConf schemas in correct directory
install -dm755 $RPM_BUILD_ROOT%{_sysconfdir}/
mv $RPM_BUILD_ROOT{%{_datadir},%{_sysconfdir}}/gconf/


%pre
%gconf_schema_prepare compiz-ccp


%post
/usr/sbin/ldconfig
%gconf_schema_upgrade compiz-ccp


%preun
%gconf_schema_remove compiz-ccp


%postun -p /usr/sbin/ldconfig


%files
%doc AUTHORS TODO
%config(noreplace) %{_sysconfdir}/compizconfig/config
%{_libdir}/compizconfig/backends/libini.so
%{_libdir}/compiz/libccp.so
%{_libdir}/libcompizconfig.so.0
%{_libdir}/libcompizconfig.so.0.0.0
%{_datadir}/compiz/ccp.xml
%{_datadir}/compizconfig/extra.profile
%{_datadir}/compizconfig/normal.profile
%config(noreplace) %{_sysconfdir}/gconf/schemas/compiz-ccp.schemas


%files devel
%doc AUTHORS TODO
%{_includedir}/compizconfig/ccs-backend.h
%{_includedir}/compizconfig/ccs.h
%{_libdir}/libcompizconfig.so
%{_libdir}/pkgconfig/libcompizconfig.pc
%{_datadir}/cmake/Modules/FindCompizConfig.cmake
%{_datadir}/compiz/cmake/LibCompizConfigCommon.cmake


%changelog
* Mon Jul 02 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.9.7.0-1.bzr428.0ubuntu6
- Initial release
- Version 0.9.7.0~bzr428
- Ubuntu release 0ubuntu6
