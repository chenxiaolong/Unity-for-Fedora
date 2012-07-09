# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

# Do not provide the Python 2 binding library
%filter_provides_in %{python_sitearch}/compizconfig\.so$
%filter_setup

%define _ubuntu_rel 0ubuntu4

Name:		python-compizconfig
Version:	0.9.5.94
Release:	1.%{_ubuntu_rel}%{?dist}
Summary:	Python 2 bindings for libcompizconfig

Group:		System Environment/Libraries
License:	GPLv2
URL:		https://launchpad.net/compizconfig-python
Source0:	https://launchpad.net/ubuntu/+archive/primary/+files/compizconfig-python_%{version}.orig.tar.gz

Source99:	https://launchpad.net/ubuntu/+archive/primary/+files/compizconfig-python_%{version}-%{_ubuntu_rel}.diff.gz

BuildRequires:	libtool

BuildRequires:	compiz-devel
BuildRequires:	Cython
BuildRequires:	glib2-devel
BuildRequires:	libcompizconfig-devel
BuildRequires:	libxml2-devel
BuildRequires:	libXtst-devel
BuildRequires:	Pyrex
BuildRequires:	python2-devel

# Satisfy obs conflict on gtk3 too (installed by build dependencies)
BuildRequires:  gtk3
BuildRequires:  gtk3-devel

%description
This package contains the Python 2 bindings for the compizconfig libraries.


%prep
%setup -q -n compizconfig-python-%{version}

# Apply Ubuntu's patches
zcat '%{SOURCE99}' | patch -Np1
for i in $(grep -v '#' debian/patches/series); do
  patch -Np1 -i "debian/patches/${i}"
done


%build
%{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT


%files
%doc AUTHORS ChangeLog
%{python_sitearch}/compizconfig.so
%{python_sitearch}/compizconfig_python-0.9.5.94-py2.7.egg-info


%changelog
* Sun Jul 08 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.9.5.94-1.0ubuntu4
- Initial release
- Version 0.9.5.94
- Ubuntu release 0ubuntu4
