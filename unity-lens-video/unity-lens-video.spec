# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

Name:		unity-lens-video
Version:	0.3.6
Release:	1%{?dist}
Summary:	Unity video lens

Group:		User Interface/Desktops
License:	GPLv3
URL:		https://launchpad.net/unity-lens-videos
Source0:	https://launchpad.net/unity-lens-videos/trunk/%{version}/+download/unity-lens-video-%{version}.tar.gz

BuildRequires:	intltool

BuildRequires:	python-distutils-extra

BuildArch:	noarch

%description
This package contains the video lens which can be used for searching videos in
the dash of the Unity shell.


%prep
%setup -q


%build
%{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT


%files
%doc COPYING
%{python_sitelib}/unity_lens_video-0.3.6-py2.7.egg-info
%dir %{_prefix}/lib/unity-lens-video/
%{_prefix}/lib/unity-lens-video/unity-lens-video
%{_datadir}/dbus-1/services/unity-lens-video.service


%changelog
* Sun Jul 08 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.3.6-1
- Initial release
- Version 0.3.6
