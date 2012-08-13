# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

Name:		unity-lens-applications
Version:	6.2.0
Release:	1%{?dist}
Summary:	Unity Applications Lens

Group:		User Interface/Desktops
License:	GPLv3
URL:		https://launchpad.net/unity-lens-applications
Source0:	https://launchpad.net/unity-lens-applications/6.0/%{version}/+download/unity-lens-applications-%{version}.tar.gz

Patch0:		10-no-db51.patch

BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gcc-c++
BuildRequires:	gettext

BuildRequires:	dee-devel
BuildRequires:	GConf2-devel
BuildRequires:	glib2-devel
BuildRequires:	gnome-menus301-devel
BuildRequires:	libdb-devel
BuildRequires:	libgee06-devel
BuildRequires:	libunity-devel
BuildRequires:	libuuid-devel
BuildRequires:	libzeitgeist-devel
BuildRequires:	vala-tools
BuildRequires:	xapian-core-devel

%description
This package contains the applications lens which can be used to launch
applications for the Unity shell.


%prep
%setup -q

%patch0 -p1 -b .dbversion

autoreconf -vfi


%build
%configure

# Disable rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name}


%postun
if [ $1 -eq 0 ]; then
  glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :
fi

%posttrans
glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :


%files -f %{name}.lang
%doc AUTHORS ChangeLog
%config %{_sysconfdir}/xdg/menus/unity-lens-applications.menu
%{_libexecdir}/unity-applications-daemon
%{_datadir}/dbus-1/services/unity-lens-applications.service
%{_datadir}/desktop-directories/X-Unity-All-Applications.directory
%{_datadir}/glib-2.0/schemas/com.canonical.Unity.AppsLens.gschema.xml
%dir %{_datadir}/unity/lenses/applications/
%{_datadir}/unity/lenses/applications/applications.lens
%dir %{_datadir}/unity/lenses/commands/
%{_datadir}/unity/lenses/commands/commands.lens
%{_datadir}/unity/themes/applications.png


%changelog
* Mon Aug 13 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 6.2.0-1
- Version 6.2.0

* Sun Jul 08 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 5.12.0-1
- Initial release
- Version 5.12.0
