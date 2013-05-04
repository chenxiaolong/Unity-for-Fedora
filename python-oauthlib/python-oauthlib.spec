# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

%define _ubuntu_rel 0ubuntu1

Name:		python-oauthlib
Version:	0.3.7
Release:	1.%{_ubuntu_rel}%{?dist}
Summary:	A Python implementation of the OAuth request-signing logic

Group:		System Environment/Libraries
License:	BSD
URL:		http://pypi.python.org/pypi/oauthlib
Source0:	http://pypi.python.org/packages/source/o/oauthlib/oauthlib-%{version}.tar.gz

Source99:	https://launchpad.net/ubuntu/+archive/primary/+files/python-oauthlib_%{version}-%{_ubuntu_rel}.debian.tar.gz

BuildRequires:	python3-crypto
BuildRequires:	python3-nose
BuildRequires:	python3-setuptools
BuildRequires:	python-crypto
BuildRequires:	python-nose
BuildRequires:	python-setuptools
BuildRequires:	python-unittest2

BuildRequires:	pkgconfig(python2)
BuildRequires:	pkgconfig(python3)

BuildArch:	noarch

%description
OAuthLib is a generic utility which implements the logic of OAuth without
assuming a specific HTTP request object. Use it to graft OAuth support onto your
favorite HTTP library. If you're a maintainer of such a library, write a thin
veneer on top of OAuthLib and get OAuth support for very little effort.


%package -n python3-oauthlib
Summary:	A Python implementation of the OAuth request-signing logic
Group:		System Environment/Libraries

BuildArch:	noarch

%description -n python3-oauthlib
OAuthLib is a generic utility which implements the logic of OAuth without
assuming a specific HTTP request object. Use it to graft OAuth support onto your
favorite HTTP library. If you're a maintainer of such a library, write a thin
veneer on top of OAuthLib and get OAuth support for very little effort.


%prep
%setup -q -n oauthlib-%{version}

# Apply Ubuntu's patches
tar zxvf '%{SOURCE99}'

for i in $(grep -v '#' debian/patches/series); do
  patch -Np1 -i "debian/patches/${i}"
done


%build
%{__python} setup.py build
%{__python3} setup.py build


%install
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
%{__python3} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT


%files -n python-oauthlib
%doc LICENSE README.rst
%{python_sitelib}/oauthlib/
%{python_sitelib}/oauthlib-%{version}-py*.egg-info/


%files -n python3-oauthlib
%doc LICENSE README.rst
%{python3_sitelib}/oauthlib/
%{python3_sitelib}/oauthlib-%{version}-py*.egg-info/


%changelog
* Sat May 04 2013 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.3.7-1.0ubuntu1
- Version 0.3.7
- Ubuntu release 0ubuntu1

* Thu Jan 31 2013 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.3.5-1.0ubuntu1
- Version 0.3.5
- Ubuntu release 0ubuntu1

* Sun Nov 18 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.3.3-1.0ubuntu2
- Version 0.3.3
- Ubuntu release 0ubuntu2

* Fri Sep 28 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.3.0-1.0ubuntu1
- Initial release
- Version 0.3.0
