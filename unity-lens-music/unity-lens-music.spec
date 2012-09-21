# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

Name:		unity-lens-music
Version:	6.8.0
Release:	1%{?dist}
Summary:	Unity music lens

Group:		User Interface/Desktops
License:	GPLv3
URL:		https://launchpad.net/unity-lens-music
Source0:	https://launchpad.net/unity-lens-music/6.0/%{version}/+download/unity-lens-music-%{version}.tar.gz

Patch0:		0001_unity-lens-music.patch

BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	pkgconfig
BuildRequires:	vala-tools

BuildRequires:	pkgconfig(dee-1.0)
BuildRequires:	pkgconfig(gee-1.0)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gstreamer-0.10)
BuildRequires:	pkgconfig(gstreamer-pbutils-0.10)
BuildRequires:	pkgconfig(json-glib-1.0)
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	pkgconfig(tdb)
BuildRequires:	pkgconfig(unity)

%description
This package contains the music lens which can be used to browse media files.


%prep
%setup -q

%patch0 -p1 -b .unity-protocol-private

autoreconf -vfi


%build
%configure
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT


%files
%doc AUTHORS ChangeLog
%{_libexecdir}/music-preview-player
%{_libexecdir}/unity-music-daemon
%{_libexecdir}/unity-musicstore-daemon
%{_datadir}/dbus-1/services/music-preview-player.service
%{_datadir}/dbus-1/services/musicstore-scope.service
%{_datadir}/dbus-1/services/unity-lens-music.service
%dir %{_datadir}/unity/
%dir %{_datadir}/unity/lenses/
%dir %{_datadir}/unity/lenses/music/
%{_datadir}/unity/lenses/music/music.lens
%{_datadir}/unity/lenses/music/musicstore.scope


%changelog
* Thu Sep 20 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 6.8.0-1
- Version 6.8.0

* Mon Aug 27 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 6.6.0-1
- Version 6.6.0

* Tue Aug 21 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 6.2.0-2
- Fix directory ownership
- Use pkgconfig for dependencies

* Mon Aug 13 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 6.2.0-1
- Version 6.2.0

* Sun Jul 29 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 6.0.0-1
- Version 6.0.0

* Sun Jul 08 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 5.12.0-1
- Initial release
- Version 5.12.0
