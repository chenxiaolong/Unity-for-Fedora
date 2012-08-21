# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

Name:		unity-scope-video-remote
Version:	0.3.6
Release:	2%{?dist}
Summary:	Scope that adds remote video search engine support to the Unity video lens

Group:		User Interface/Desktops
License:	GPLv3
URL:		https://launchpad.net/unity-lens-videos
Source0:	https://launchpad.net/unity-lens-videos/remote-videos-scope-trunk/remote-videos-%{version}/+download/unity-scope-video-remote-%{version}.tar.gz

Patch0:		0001_Use_libexec.patch

BuildRequires:	intltool

BuildRequires:	python-distutils-extra

BuildArch:	noarch

%description
This package contains a "scope" for the Unity video lens that adds remote video
search engine support.


%prep
%setup -q

%patch0 -p1 -b .use_libexec


%build
%{__python} setup.py build


%install
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT


%files
%doc COPYING
%{python_sitelib}/unity_scope_video_remote-0.3.6-py2.7.egg-info
%{_libexecdir}/unity-scope-video-remote
%{_datadir}/dbus-1/services/unity-scope-video-remote.service
%dir %{_datadir}/unity/
%dir %{_datadir}/unity/lenses/
%dir %{_datadir}/unity/lenses/video/
%{_datadir}/unity/lenses/video/video-remote.scope


%changelog
* Tue Aug 21 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.3.6-2
- Fix directory ownership
- Move daemon to libexecdir

* Sun Jul 08 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.3.6-1
- Initial release
- Version 0.3.6
