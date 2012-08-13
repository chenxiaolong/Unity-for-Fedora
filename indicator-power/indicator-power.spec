# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

Name:		indicator-power
Version:	12.10.0
Release:	1%{?dist}
Summary:	Indicator to show the battery status

Group:		User Interface/Desktops
License:	GPLv3
URL:		https://launchpad.net/indicator-power
Source0:	https://launchpad.net/indicator-power/12.10/%{version}/+download/indicator-power-%{version}.tar.gz

Patch0:		0001_Disable_-Werror.patch

BuildRequires:	autoconf
BuildRequires:	automake
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

%description
This package contains an indicator to show the battery status. It replaces the
gnome-power-manager icon in desktop environments where regular tray icons are
hidden.


%prep
%setup -q

%patch0 -p1

intltoolize --force
aclocal --verbose --force
autoconf -v -f
automake -f
#autoreconf -vfi


%build
%configure --disable-static
make %{?_smp_mflags}


%install
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
* Mon Aug 13 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 12.10.0-1
- Version 12.10.1

* Sun Jul 08 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 2.0-1
- Initial release
- Version 2.0
