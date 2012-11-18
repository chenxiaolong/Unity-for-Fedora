# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

%define _ubuntu_rel 0ubuntu4.1

Name:		activity-log-manager
Version:	0.9.4
Release:	1.%{_ubuntu_rel}%{?dist}
Summary:	Activity Log Manager for Zeitgeist

Group:		User Interface/Desktops
License:	LGPLv2+
URL:		https://launchpad.net/activity-log-manager
Source0:	https://launchpad.net/activity-log-manager/0.9/%{version}/+download/activity-log-manager-%{version}.tar.gz

Source99:	https://launchpad.net/ubuntu/+archive/primary/+files/activity-log-manager_%{version}-%{_ubuntu_rel}.debian.tar.gz

Patch0:		0001_disable_whoopsie.patch

BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	desktop-file-utils
BuildRequires:	gettext
BuildRequires:	intltool
BuildRequires:	vala-tools

BuildRequires:	pkgconfig(gee-1.0)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(libgnome-control-center)
BuildRequires:	pkgconfig(polkit-gobject-1)
BuildRequires:	pkgconfig(zeitgeist-1.0)

Requires:	hicolor-icon-theme
Requires:	zeitgeist

%description
Activity Log Manager is a graphical user interface which lets you easily control
what gets logged by Zeitgeist.

It supports setting up blacklists according to several criteria (such as
application or file types), temporarily stopping all logging as well as deleting
recent events.


%prep
%setup -q

# Apply Ubuntu's patches
tar zxvf '%{SOURCE99}'

# Disable patches
  # Whoopsie is upstart specific
    sed -i '/02_handle_upstart_in_whoopsie.patch/d' debian/patches/series
    sed -i '/03_correct_path_to_whoopsie_preferences.patch/d' debian/patches/series

for i in $(grep -v '#' debian/patches/series); do
  patch -Np1 -i "debian/patches/${i}"
done

# Disable whoopsie
%patch0 -p1 -b .disable-whoopsie

autoreconf -vfi


%build
%configure --with-ccpanel --disable-static
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT

install -dm755 $RPM_BUILD_ROOT%{_docdir}/
rm $RPM_BUILD_ROOT%{_prefix}/doc/alm/INSTALL
mv $RPM_BUILD_ROOT%{_prefix}/doc/alm/ \
  $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/

desktop-file-validate \
  $RPM_BUILD_ROOT%{_datadir}/applications/activity-log-manager-ccpanel.desktop
desktop-file-validate \
  $RPM_BUILD_ROOT%{_datadir}/applications/activity-log-manager.desktop

# Remove libtool files
find $RPM_BUILD_ROOT -type f -name '*.la' -delete

%find_lang activity-log-manager


%post
touch --no-create %{_datadir}/icons/hicolor/ &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
  touch --no-create %{_datadir}/icons/hicolor/ &>/dev/null
  gtk-update-icon-cache -f %{_datadir}/icons/hicolor/ &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache -f %{_datadir}/icons/hicolor/ &>/dev/null || :


%files -f activity-log-manager.lang
%doc AUTHORS ChangeLog NEWS
%{_bindir}/activity-log-manager
%dir %{_libdir}/control-center-1/
%dir %{_libdir}/control-center-1/panels/
%{_libdir}/control-center-1/panels/libactivity-log-manager.so
%{_datadir}/applications/activity-log-manager-ccpanel.desktop
%{_datadir}/applications/activity-log-manager.desktop
%{_datadir}/icons/hicolor/*/apps/activity-log-manager.svg


%changelog
* Sun Nov 18 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.9.4-1.0ubuntu4.1
- Version 0.9.4
- Ubuntu release 0ubuntu4.1

* Sun Oct 07 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.9.4-1.0ubuntu4
- Initial release
- Version 0.9.4
- Ubuntu release 0ubuntu4
