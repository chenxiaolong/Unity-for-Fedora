# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

Name:		indicator-power
Version:	2.0
Release:	1%{?dist}
Summary:	Indicator to show the battery status

Group:		User Interface/Desktops
License:	GPLv3
URL:		https://launchpad.net/indicator-power
Source0:	https://launchpad.net/indicator-power/2.0/%{version}/+download/indicator-power-%{version}.tar.gz

BuildRequires:	intltool

BuildRequires:	dbus-devel
BuildRequires:	glib2-devel
BuildRequires:	gnome-settings-daemon-devel
BuildRequires:	gtk3-devel
BuildRequires:	libindicator-gtk3-devel
BuildRequires:	upower-devel

# From Ubuntu packaging
Requires:	control-center
Requires:	gnome-settings-daemon

# Satisfy OBS conflict on what provides PackageKit-backend
BuildRequires:	PackageKit-yum

# Satisfy OBS conflict on gtk2 (required by dependencies)
BuildRequires:	gtk2
BuildRequires:	gtk2-devel

%description
This package contains an indicator to show the battery status. It replaces the
gnome-power-manager icon in desktop environments where regular tray icons are
hidden.


%prep
%setup -q


%build
%configure --disable-static
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# Remove libtool files
find $RPM_BUILD_ROOT -type f -name '*.la' -delete


%postun
if [ ${1} -eq 0 ]; then
  glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :
fi


%posttrans
glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :


%files
%doc AUTHORS ChangeLog
%{_libdir}/indicators3/7/libpower.so
%{_datadir}/glib-2.0/schemas/com.canonical.indicator.power.gschema.xml


%changelog
* Sun Jul 08 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 2.0-1
- Initial release
- Version 2.0
