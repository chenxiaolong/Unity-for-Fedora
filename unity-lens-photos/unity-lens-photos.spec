# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

Name:		unity-lens-photos
Version:	0.8
Release:	1%{?dist}
Summary:	Unity lens for browsing photos

Group:		User Interface/Desktops
License:	GPLv3
URL:		https://launchpad.net/unity-lens-photos
Source0:	https://launchpad.net/unity-lens-photos/trunk/%{version}/+download/unity-lens-photos-%{version}.tar.gz

Patch0:		0001_Use_libexec.patch

BuildRequires:	intltool
BuildRequires:	desktop-file-utils

BuildRequires:	python-distutils-extra

Requires:	python3-gobject
Requires:	python3-oauthlib
# Typelibs for the following packages are needed
Requires:	dee
Requires:	libaccounts-glib
Requires:	libdbusmenu-gtk3
Requires:	libsignon-glib
Requires:	libunity

Requires:	python(abi) = 2.7
%if 0%{fedora} >= 18
Requires:	python(abi) = 3.3
%else
Requires:	python(abi) = 3.2
%endif

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

sed -i \
  -e '/Categories/ s/$/;/' \
  -e '/Encoding/d' \
  $RPM_BUILD_ROOT%{_datadir}/applications/%{name}.desktop
desktop-file-validate \
  $RPM_BUILD_ROOT%{_datadir}/applications/%{name}.desktop || :


%files
%doc AUTHORS COPYING
%{python_sitelib}/unity_lens_photos-%{version}-py2.7.egg-info
%dir %{_libexecdir}/unity-lens-photos/
%{_libexecdir}/unity-lens-photos/*.py*
%{_libexecdir}/unity-lens-photos/unity-lens-photos
%{_datadir}/applications/unity-lens-photos.desktop
%{_datadir}/dbus-1/services/unity-lens-photos.service
%{_datadir}/pixmaps/unity-lens-photos.png
%dir %{_datadir}/unity/
%dir %{_datadir}/unity/lenses/
%dir %{_datadir}/unity/lenses/photos/
%{_datadir}/unity/lenses/photos/photos.lens


%changelog
* Sat Oct 06 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.8-1
- Version 0.8

* Wed Oct 03 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.7-1
- Version 0.7

* Thu Sep 20 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.6-1
- Version 0.6

* Fri Sep 14 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.5-1
- Version 0.5

* Sat Sep 08 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.4-1
- Version 0.4

* Sat Sep 01 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.3-1
- Version 0.3

* Mon Aug 27 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.2.1-1
- Initial release
- Version 0.2.1
