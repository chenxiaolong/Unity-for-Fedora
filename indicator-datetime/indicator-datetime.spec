# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

Name:		indicator-datetime
Version:	12.10.0
Release:	1%{?dist}
Summary:	Indicator for displaying the date and time

Group:		User Interface/Desktops
License:	GPLv3
URL:		https://launchpad.net/indicator-datetime
Source0:	https://launchpad.net/indicator-datetime/12.10/%{version}/+download/indicator-datetime-%{version}.tar.gz

Patch0:		0001_Revert_port_to_EDS_3.6_API.patch
Patch1:		0002_Read_etc_sysconfig_clock.patch

BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	desktop-file-utils
BuildRequires:	gettext
BuildRequires:	intltool

BuildRequires:	cairo-devel
BuildRequires:	control-center-devel
BuildRequires:	evolution-data-server-devel
BuildRequires:	GConf2-devel
BuildRequires:	geoclue-devel
BuildRequires:	glib2-devel
BuildRequires:	gtk3-devel
BuildRequires:	ido-devel
BuildRequires:	ido3-devel
BuildRequires:	json-glib-devel
BuildRequires:	libdbusmenu-glib-devel
BuildRequires:	libdbusmenu-gtk3-devel
BuildRequires:	libical-devel
BuildRequires:	libindicator-devel
BuildRequires:	libindicator-gtk3-devel
BuildRequires:	libtimezonemap-devel
BuildRequires:	polkit-devel

Requires:	control-center-ubuntu

%description
This package contains an indicator for displaying the date and time in the
panel.


%prep
%setup -q

%patch0 -p1
%patch1 -p1

autoreconf -vfi


%build
%configure --disable-static
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT

desktop-file-validate \
 $RPM_BUILD_ROOT%{_datadir}/applications/indicator-datetime-preferences.desktop

# Remove libtool files
find $RPM_BUILD_ROOT -type f -name '*.la' -delete

%find_lang %{name}


%postun
if [ ${1} -eq 0 ]; then
  glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans
glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :


%files -f %{name}.lang
%doc AUTHORS ChangeLog
%{_libdir}/control-center-1/panels/libindicator-datetime.so
%{_libdir}/indicators3/7/libdatetime.so
%{_libexecdir}/indicator-datetime-service
%{_datadir}/applications/indicator-datetime-preferences.desktop
%{_datadir}/dbus-1/services/indicator-datetime.service
%{_datadir}/glib-2.0/schemas/com.canonical.indicator.datetime.gschema.xml
%dir %{_datadir}/indicator-datetime/
%{_datadir}/indicator-datetime/datetime-dialog.ui


%changelog
* Mon Aug 13 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 12.10.0-1
- Version 12.10.0
- Drop GTK 2 subpackage: deprecated
- Add patch: Revert evolution-data-server 3.6 API

* Mon Jul 16 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.3.94-2
- Read timezone from /etc/sysconfig/clock

* Wed Jul 04 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.3.94-1
- Initial release
- Version 0.3.94
