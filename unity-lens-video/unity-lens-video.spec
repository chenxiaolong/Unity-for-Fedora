# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

%define _unity_major_ver 6

Name:		unity-lens-video
Version:	0.3.6
Release:	2%{?dist}
Summary:	Unity video lens

Group:		User Interface/Desktops
License:	GPLv3
URL:		https://launchpad.net/unity-lens-videos
Source0:	https://launchpad.net/unity-lens-videos/trunk/%{version}/+download/unity-lens-video-%{version}.tar.gz

Patch0:		0001_Use_libexec.patch

BuildRequires:	intltool

BuildRequires:	python-distutils-extra

BuildArch:	noarch

%description
This package contains the video lens which can be used for searching videos in
the dash of the Unity shell.


%prep
%setup -q

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


%files
%doc COPYING
%{python_sitelib}/unity_lens_video-0.3.6-py2.7.egg-info
%{_libexecdir}/unity-lens-video
%{_datadir}/dbus-1/services/unity-lens-video.service
%{_datadir}/unity/lenses/video/video.lens


%changelog
* Sun Jul 29 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.3.6-2
- Video lens didn't get installed
- Install daemon to libexec

* Sun Jul 08 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.3.6-1
- Initial release
- Version 0.3.6
