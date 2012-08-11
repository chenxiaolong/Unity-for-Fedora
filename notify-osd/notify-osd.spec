# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

Name:		notify-osd
Version:	0.9.34
Release:	1%{?dist}
Summary:	Notification daemon which displays semi-transparent click-through bubbles

Group:		User Interface/X
License:	GPLv3
URL:		https://launchpad.net/notify-osd
Source0:	https://launchpad.net/notify-osd/precise/%{version}/+download/notify-osd-%{version}.tar.gz

BuildRequires:	gnome-common
BuildRequires:	intltool

BuildRequires:	dbus-devel
BuildRequires:	dbus-glib-devel
BuildRequires:	glib2-devel
BuildRequires:	gtk3-devel
BuildRequires:	libnotify-devel
BuildRequires:	libwnck3-devel

Provides:	desktop-notification-daemon

%description
The freedesktop.org Desktop Notifications Specification provides a standard way
for applications to display pop-up notifications. These are designed to make you
aware of something, without interrupting your work with a window you must close.

Notify OSD presents these notifications as ephemeral overlays, which can be
clicked through so they don't block your work. It queues notifications, to
prevent them from flooding your screen. And as well as handling standard
notification updates, Notify OSD introduces the idea of appending — allowing
notifications to grow over time, for example in the case of instant messages
from a particular person.


%prep
%setup -q


%build
%configure
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT


%postun
if [ ${1} -eq 0 ] ; then
  glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :
fi

%posttrans
glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :


%files
%doc AUTHORS NEWS README TODO
%{_libexecdir}/notify-osd
%{_datadir}/GConf/gsettings/notify-osd.convert
%{_datadir}/dbus-1/services/org.freedesktop.Notifications.service
%{_datadir}/glib-2.0/schemas/com.canonical.NotifyOSD.gschema.xml
%dir %{_datadir}/notify-osd/
%{_datadir}/notify-osd/icons/


%changelog
* Sat Aug 11 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.9.34-1
- Initial release
- Version 0.9.34
