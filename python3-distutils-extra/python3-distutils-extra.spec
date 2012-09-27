# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

# Partially based off of Fedora's python-distutils-extra spec file

Name:		python3-distutils-extra
Version:	2.37
Release:	1%{?dist}
Summary:	Integrate more support into Python 3's distutils

Group:		Development/Libraries
License:	GPLv2+
URL:		https://launchpad.net/python-distutils-extra
Source0:	https://launchpad.net/python-distutils-extra/trunk/%{version}/+download/python-distutils-extra-%{version}.tar.gz

BuildArch:	noarch

BuildRequires:	python3-setuptools

BuildRequires:	pkgconfig(python3)

%description
Enables you to easily integrate gettext support, themed icons and scrollkeeper
based documentation into Python's distutils.


%prep
%setup -q -n python-distutils-extra-%{version}


%build
%{__python3} setup.py build


%install
%{__python3} setup.py install --root=$RPM_BUILD_ROOT


%files
%doc LICENSE doc/*
%{python3_sitelib}/DistUtilsExtra/
%{python3_sitelib}/python_distutils_extra-%{version}-py*.egg-info/


%changelog
* Thu Sep 27 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 2.37-1
- Initial release
- Based on Fedora's python-distutils-extra spec file
- Version 2.37
