# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

Name:		unity-lens-music
Version:	5.12.0
Release:	1%{?dist}
Summary:	Unity music lens

Group:		User Interface/Desktops
License:	GPLv3
URL:		https://launchpad.net/unity-lens-music
Source0:	https://launchpad.net/unity-lens-music/5.0/%{version}/+download/unity-lens-music-%{version}.tar.gz

BuildRequires:	dee-devel
BuildRequires:	glib2-devel
BuildRequires:	json-glib-devel
BuildRequires:	libgee06-devel
BuildRequires:	libtdb-devel
BuildRequires:	libunity-devel
BuildRequires:	sqlite-devel
BuildRequires:	vala-tools

# Satisfy OBS conflict on xorg-x11-proto-devel
BuildRequires:	xorg-x11-proto-devel

%description
This package contains the music lens which can be used to browse media files.


%prep
%setup -q


%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT


%files
%doc AUTHORS ChangeLog
%{_libexecdir}/unity-music-daemon
%{_libexecdir}/unity-musicstore-daemon
%{_datadir}/dbus-1/services/musicstore-scope.service
%{_datadir}/dbus-1/services/unity-lens-music.service
%dir %{_datadir}/unity/lenses/music/
%{_datadir}/unity/lenses/music/music.lens
%{_datadir}/unity/lenses/music/musicstore.scope


%changelog
* Sun Jul 08 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 5.12.0-1
- Initial release
- Version 5.12.0
