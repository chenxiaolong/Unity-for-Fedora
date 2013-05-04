# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

%define _translations 20130419

Name:		indicator-session
Version:	12.10.5daily13.03.08
Release:	1%{?dist}
Summary:	Indicator for session management and status information

Group:		User Interface/Desktops
License:	GPLv3
URL:		https://launchpad.net/indicator-session
Source0:	https://launchpad.net/ubuntu/+archive/primary/+files/indicator-session_%{version}.orig.tar.gz

Source98:	https://dl.dropboxusercontent.com/u/486665/Translations/translations-%{_translations}-indicator-session.tar.gz

Patch1:		0001_Lock_Screen_Live_CD_Detection.patch
Patch2:		0002_There_is_no_help.patch
Patch3:		0003_Link_Against_pthread.patch
Patch4:		0004_Lock_Screen_Guest_Session_Detection.patch
Patch5:		revert_r382.patch

BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	desktop-file-utils
BuildRequires:	gettext
BuildRequires:	gnome-doc-utils
BuildRequires:	intltool

BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(dbusmenu-glib-0.4)
BuildRequires:	pkgconfig(dbusmenu-gtk3-0.4)
BuildRequires:	pkgconfig(gconf-2.0)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(gudev-1.0)
BuildRequires:	pkgconfig(indicator3-0.4)
BuildRequires:	pkgconfig(packagekit-glib2)
BuildRequires:	pkgconfig(polkit-gobject-1)

Requires:	gnome-packagekit

# From Ubuntu's packaging
Requires:	gnome-settings-daemon
Requires:	upower

%description
Quick! Change your status. Switch users. Close your session. All provided by the
The Session Menu these tasks are conveniently placed in the upper-right corner
of the desktop to make them available and easy to use.


%prep
%setup -q

%patch1 -p0
%patch2 -p1
%patch3 -p1
# Arch Linux specific for now
#patch4 -p1
%patch5 -p0

mkdir po_new
tar zxvf '%{SOURCE98}' -C po_new
rm -f po/LINGUAS po/*.pot
mv po_new/po/*.pot po/
for i in po_new/po/*.po; do
  FILE=$(sed -n "s|.*/%{name}-||p" <<< ${i})
  mv ${i} po/${FILE}
  echo ${FILE%.*} >> po/LINGUAS
done

autoreconf -vfi
intltoolize -f


%build
%configure --disable-static
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT

desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/indicators/session/applications/classic-desktop.desktop

# Remove libtool files
find $RPM_BUILD_ROOT -type f -name '*.la' -delete

%find_lang %{name}


%postun
if [ ${1} -eq 0 ]; then
  glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :
fi


%posttrans
glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :


%files -f %{name}.lang
%doc AUTHORS ChangeLog
%dir %{_libdir}/indicators3/
%dir %{_libdir}/indicators3/7/
%{_libdir}/indicators3/7/libsession.so
%{_libexecdir}/gtk-logout-helper
%{_libexecdir}/indicator-session-service
%{_datadir}/GConf/gsettings/indicator-session.convert
%{_datadir}/dbus-1/services/indicator-session.service
%{_datadir}/glib-2.0/schemas/com.canonical.indicator.session.gschema.xml
%dir %{_datadir}/indicators/
%dir %{_datadir}/indicators/session/
%dir %{_datadir}/indicators/session/applications/
%{_datadir}/indicators/session/applications/classic-desktop.desktop
%attr(755,root,root) %{_datadir}/indicators/session/applications/classic-desktop.sh
%dir %{_datadir}/libindicator/
%{_datadir}/libindicator/icons/


%changelog
* Fri May 03 2013 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 12.10.5daily13.03.08-1
- Version 12.10.5daily13.03.08

* Tue Jan 29 2013 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 12.10.5daily13.01.25-1
- Version 12.10.5daily13.01.25

* Sat Oct 06 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 12.10.4-1
- Version 12.10.4

* Thu Sep 20 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 12.10.3-1
- Version 12.10.3
- Drop 0003_Workaround_disappearing_icon.patch - merged upstream

* Sat Sep 08 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 12.10.2-1
- Version 12.10.2

* Thu Aug 30 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 12.10.1-2
- Workaround disappearing icon

* Mon Aug 27 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 12.10.1-1
- Version 12.10.1

* Mon Aug 20 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 12.10.0-3
- Fix directory ownership
- Use pkgconfig for dependencies
- Run desktop-file-validate on desktop file

* Tue Aug 14 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 12.10.0-2
- Disable "Ubuntu Help" item in menu: there are no help files for Unity

* Mon Aug 13 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 12.10.0-1
- Version 12.10.0
- Drop GTK 2 subpackage: deprecated

* Thu Jul 12 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.3.96-2
- Use gpk-update-viewer to show updates

* Sat Jul 08 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.3.96-1
- Initial release
- Version 0.3.96
