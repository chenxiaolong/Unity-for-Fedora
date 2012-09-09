# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

Name:		unity-lens-photos
Version:	0.4
Release:	1%{?dist}
Summary:	Unity lens for browsing photos

Group:		User Interface/Desktops
License:	GPLv3
URL:		https://launchpad.net/unity-lens-photos
Source0:	https://launchpad.net/unity-lens-photos/trunk/%{version}/+download/unity-lens-photos-%{version}.tar.gz

Patch0:		0001_Use_libexec.patch

BuildRequires:	intltool

BuildRequires:	python-distutils-extra

Requires:	python(abi) = 2.7
Requires:	python(abi) = 3.2

BuildArch:	noarch

%description
This package contains the photos lens, which can be used for browsing pictures
in the Unity dash.


%prep
%setup -q

%patch0 -p1 -b .use-libexecdir


%build
%{__python} setup.py build


%install
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

# Install photos lens
install -dm755 $RPM_BUILD_ROOT%{_datadir}/unity/lenses/photos/
install -m644 build/share/unity/lenses/photos/photos.lens \
  $RPM_BUILD_ROOT%{_datadir}/unity/lenses/photos/


%files
%doc AUTHORS COPYING
%{python_sitelib}/unity_lens_photos-%{version}-py2.7.egg-info
%dir %{_libexecdir}/unity-lens-photos/
%{_libexecdir}/unity-lens-photos/*.py*
%{_libexecdir}/unity-lens-photos/unity-lens-photos
%dir %{_datadir}/accounts/
%dir %{_datadir}/accounts/applications/
%{_datadir}/accounts/applications/unity-lens-photos.application
%{_datadir}/dbus-1/services/unity-lens-photos.service
%dir %{_datadir}/unity-lens-photos/
%dir %{_datadir}/unity-lens-photos/media/
%{_datadir}/unity-lens-photos/media/*.svg
%dir %{_datadir}/unity/
%dir %{_datadir}/unity/lenses/
%dir %{_datadir}/unity/lenses/photos/
%{_datadir}/unity/lenses/photos/photos.lens


%changelog
* Sat Sep 08 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.4-1
- Version 0.4

* Sat Sep 01 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.3-1
- Version 0.3

* Mon Aug 27 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.2.1-1
- Initial release
- Version 0.2.1
