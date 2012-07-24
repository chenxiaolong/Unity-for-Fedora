# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

# The following line is for the scripts in my git repository
%define _ubuntu_match_rel 0ubuntu2

Name:		indicator-datetime
Version:	0.3.94
Release:	2%{?dist}
Summary:	Indicator for displaying the date and time

Group:		User Interface/Desktops
License:	GPLv3
URL:		https://launchpad.net/indicator-datetime
Source0:	https://launchpad.net/indicator-datetime/0.4/%{version}/+download/indicator-datetime-%{version}.tar.gz

Patch0:		0001_non-locale_parsing.patch
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
BuildRequires:	gtk2-devel
BuildRequires:	gtk3-devel
BuildRequires:	ido-devel
BuildRequires:	ido3-devel
BuildRequires:	json-glib-devel
BuildRequires:	libdbusmenu-glib-devel
BuildRequires:	libdbusmenu-gtk2-devel
BuildRequires:	libdbusmenu-gtk3-devel
BuildRequires:	libical-devel
BuildRequires:	libindicator-devel
BuildRequires:	libindicator-gtk3-devel
BuildRequires:	libtimezonemap-devel
BuildRequires:	polkit-devel

# OBS build fix
BuildRequires:	PackageKit-yum

# OBS dependency solver fix: dependencies use gtk3-ubuntu, so don't install gtk3
#!BuildIgnore:  gtk3
#!BuildIgnore:  gtk3-devel

# Satisfy OBS conflict on xorg-x11-proto-devel
BuildRequires:	xorg-x11-proto-devel

# Satisfy OBS conflict on libXfixes
BuildRequires:	libXfixes
BuildRequires:	libXfixes-devel

# Satisfy OBS conflict on gsettings-desktop-schemas
BuildRequires:	gsettings-desktop-schemas

# Satisfy OBS conflict on control-center
BuildRequires:	control-center-ubuntu
BuildRequires:	control-center-ubuntu-devel

# Satisfy OBS conflict on gnome-bluetooth-libs
BuildRequires:	gnome-bluetooth-libs

Requires:	control-center-ubuntu

%description
This package contains an indicator for displaying the date and time in the
panel.


%package gtk2
Summary:	Indicator for displaying the date and time - GTK 2
Group:		User Interface/Desktops

Requires:	%{name}%{?_isa} = %{version}-%{release}

%description gtk2
This package contains the development files for the datetime indicator.


%prep
%setup -q

%patch0 -p1
%patch1 -p1

autoreconf -vfi


%build
%global _configure ../configure
mkdir build-gtk2 build-gtk3

pushd build-gtk2
%configure --with-gtk=2 --disable-static
make %{?_smp_mflags}
popd

pushd build-gtk3
%configure --with-gtk=3 --disable-static
make %{?_smp_mflags}
popd


%install
pushd build-gtk2
make install DESTDIR=$RPM_BUILD_ROOT
popd

pushd build-gtk3
make install DESTDIR=$RPM_BUILD_ROOT
popd

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


%files gtk2
%doc AUTHORS ChangeLog
%{_libdir}/indicators/7/libdatetime.so


%changelog
* Mon Jul 16 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.3.94-2
- Read timezone from /etc/sysconfig/clock

* Wed Jul 04 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.3.94-1
- Initial release
- Version 0.3.94
