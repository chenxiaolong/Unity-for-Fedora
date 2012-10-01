# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

%define _unity_major_ver 6

Name:		unity-lens-video
Version:	0.3.10
Release:	1%{?dist}
Summary:	Unity video lens

Group:		User Interface/Desktops
License:	GPLv3
URL:		https://launchpad.net/unity-lens-videos
Source0:	https://launchpad.net/unity-lens-videos/trunk/%{version}/+download/unity-lens-video-%{version}.tar.gz

Patch0:		0001_Use_libexec.patch

BuildRequires:	desktop-file-utils
BuildRequires:	intltool

BuildRequires:	python-distutils-extra

BuildArch:	noarch

%description
This package contains the video lens which can be used for searching videos in
the dash of the Unity shell.


%prep
%setup -q -n unity-lens-videos-%{version}

%patch0 -p1 -b .use_libexec

sed -i '/Icon/ s/^\(.*\)[0-9]\(.*\)/\1%{_unity_major_ver}\2/g' \
  video.lens.in
sed -i '/ThemedIcon/ s/^\(.*\)[0-9]\(.*\)/\1%{_unity_major_ver}\2/g' \
  src/unity-lens-video


%build
%{__python} setup.py build


%install
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

# Install video lens
install -dm755 $RPM_BUILD_ROOT%{_datadir}/unity/lenses/video/
install -m644 build/share/unity/lenses/video/video.lens \
  $RPM_BUILD_ROOT%{_datadir}/unity/lenses/video/

sed -i \
  -e '/Encoding/d' \
  -e '/Categories/ s/$/;/' \
  $RPM_BUILD_ROOT%{_datadir}/applications/unity-lens-video.desktop
#desktop-file-validate \
#  $RPM_BUILD_ROOT%{_datadir}/applications/unity-lens-video.desktop


%files
%doc COPYING
%{python_sitelib}/unity_lens_video-%{version}-py2.7.egg-info
%{_libexecdir}/unity-lens-video
%{_datadir}/dbus-1/services/unity-lens-video.service
%{_datadir}/applications/unity-lens-video.desktop
%{_datadir}/pixmaps/unity-lens-video.png
%dir %{_datadir}/unity/
%dir %{_datadir}/unity/lenses/
%dir %{_datadir}/unity/lenses/video/
%{_datadir}/unity/lenses/video/video.lens


%changelog
* Mon Oct 01 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.3.10-1
- Version 0.3.10

* Mon Aug 27 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.3.9-1
- Version 0.3.9

* Tue Aug 21 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.3.6-3
- Fix directory ownership

* Sun Jul 29 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.3.6-2
- Video lens didn't get installed
- Install daemon to libexec

* Sun Jul 08 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.3.6-1
- Initial release
- Version 0.3.6
