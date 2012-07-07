# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

# The following line is for the scripts in my git repository
%define _ubuntu_match_rel 0ubuntu2

Name:		indicator-datetime
Version:	0.3.94
Release:	1%{?dist}
Summary:	Indicator for displaying the date and time

Group:		User Interface/Desktops
License:	GPLv3
URL:		https://launchpad.net/indicator-datetime
Source0:	https://launchpad.net/indicator-datetime/0.4/%{version}/+download/indicator-datetime-%{version}.tar.gz

Patch0:		0001_non-locale_parsing.patch

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
rm -rf $RPM_BUILD_ROOT

pushd build-gtk2
make install DESTDIR=$RPM_BUILD_ROOT
popd

pushd build-gtk3
make install DESTDIR=$RPM_BUILD_ROOT
popd

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
%{_libdir}/indicators3/7/libdatetime.so
%{_libexecdir}/indicator-datetime-service
%{_datadir}/dbus-1/services/indicator-datetime.service
%{_datadir}/glib-2.0/schemas/com.canonical.indicator.datetime.gschema.xml


%files gtk2
%doc AUTHORS ChangeLog
%{_libdir}/indicators/7/libdatetime.so


%changelog
* Wed Jul 04 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.3.94-1
- Initial release
- Version 0.3.94
