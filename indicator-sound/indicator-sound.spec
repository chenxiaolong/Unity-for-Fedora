# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

# Based off of Damian's spec file

%define _ubuntu_rel 0ubuntu3

Name:		indicator-sound
Version:	0.8.5.0
Release:	1.%{_ubuntu_rel}%{?dist}
Summary:	Indicator for displaying a unified sound menu

Group:		User Interface/Desktops
License:	GPLv3
URL:		https://launchpad.net/indicator-sound
Source0:	https://launchpad.net/ubuntu/+archive/primary/+files/indicator-sound_%{version}.orig.tar.gz

Source99:	https://launchpad.net/ubuntu/+archive/primary/+files/indicator-sound_%{version}-%{_ubuntu_rel}.debian.tar.gz

BuildRequires:	glib2-devel
BuildRequires:	gtk2-devel
BuildRequires:	gtk3-devel
BuildRequires:	ido-devel
BuildRequires:	ido3-devel
BuildRequires:	libdbusmenu-glib-devel
BuildRequires:	libdbusmenu-gtk2-devel
BuildRequires:	libdbusmenu-gtk3-devel
BuildRequires:	libindicator-devel
BuildRequires:	libindicator-gtk3-devel
BuildRequires:	libgee06-devel
BuildRequires:	libnotify-devel
BuildRequires:	libxml2-devel
BuildRequires:	pulseaudio-libs-devel
BuildRequires:	vala-tools

# Ubuntu's gnome-control-center is required
Requires:	control-center-ubuntu

%description
A system sound indicator which provides easy control of the PulseAudio sound
daemon. The sound menu also provides integration with several multimedia
players (ex: Banshee).


%package gtk2
Summary:	Indicator for displaying a unified sound menu - GTK 2
Group:		User Interface/Desktops

Requires:	%{name}%{?_isa} = %{version}-%{release}

%description gtk2
This package contains the GTK 2 version of the sound indicator.


%prep
%setup -q

# Apply Ubuntu's patches
tar zxvf '%{SOURCE99}'
for i in $(grep -v '#' debian/patches/series); do
  patch -Np1 -i "debian/patches/${i}"
done


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

# Remove libtool files
find $RPM_BUILD_ROOT -type f -name '*.la' -delete


%postun
if [ ${1} -eq 0 ]; then
  glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :
fi


%posttrans
glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :


%files
%doc AUTHORS
%{_libdir}/indicators3/7/libsoundmenu.so
%{_libexecdir}/indicator-sound-service
%{_datadir}/dbus-1/services/indicator-sound.service
%{_datadir}/glib-2.0/schemas/com.canonical.indicator.sound.gschema.xml
%{_datadir}/libindicator/icons/hicolor/16x16/status/sound-icon.png
%{_datadir}/libindicator/icons/hicolor/scalable/status/sound-icon.svg


%files gtk2
%doc AUTHORS
%{_libdir}/indicators/7/libsoundmenu.so


%changelog
* Sun Jul 08 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.8.5.0-1.0ubuntu3
- Initial release
- Version 0.8.5.0
- Ubuntu release 0ubuntu3
