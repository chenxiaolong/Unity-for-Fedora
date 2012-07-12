# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

%define _ubuntu_rel 0ubuntu5

Name:		compizconfig-backend-gconf
Version:	0.9.5.92
Release:	1.%{_ubuntu_rel}%{?dist}
Summary:	GConf backend for Compiz

Group:		User Interface/Desktops
License:	GPLv2
URL:		http://compiz.org
Source0:	https://launchpad.net/ubuntu/+archive/primary/+files/compizconfig-backend-gconf_%{version}.orig.tar.gz

Source99:	https://launchpad.net/ubuntu/+archive/primary/+files/compizconfig-backend-gconf_%{version}-%{_ubuntu_rel}.debian.tar.gz

BuildRequires:	cmake
BuildRequires:	gcc-c++
BuildRequires:	intltool
BuildRequires:	libtool

BuildRequires:	boost-devel
BuildRequires:	compiz-devel
BuildRequires:	GConf2-devel
BuildRequires:	glib2-devel
BuildRequires:	libcompizconfig-devel
BuildRequires:	libxml2-devel
BuildRequires:	libxslt-devel

# Satisfy OBS conflict on gtk3 (installed by build dependencies)
BuildRequires:	gtk3
BuildRequires:	gtk3-devel

# Satisfy OBS conflict on xorg-x11-proto-devel
BuildRequires:	xorg-x11-proto-devel

# Satisfy OBS conflict on libXfixes
BuildRequires:	libXfixes
BuildRequires:	libXfixes-devel

%description
This package contains the GConf 2 configuration backend for Compiz.


%prep
%setup -q

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
  -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  -Dlibdir=%{_libdir}

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
cd build
make install DESTDIR=$RPM_BUILD_ROOT


%files
%doc AUTHORS
%{_libdir}/compizconfig/backends/libgconf.so


%changelog
* Tue Jul 03 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.9.5.92-1.0ubuntu5
- Initial release
- Version 0.9.5.92
- Ubuntu release 0ubuntu5
