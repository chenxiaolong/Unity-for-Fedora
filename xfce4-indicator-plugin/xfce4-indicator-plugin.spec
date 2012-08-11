# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

Name:		xfce4-indicator-plugin
Version:	0.5.0
Release:	1%{?dist}
Summary:	XFCE 4 panel plugin for display Ayatana indicators

Group:		User Interface/Desktops
License:	LGPLv2
# Website is outdated. Latest versions are at:
#   http://archive.xfce.org/src/panel-plugins/xfce4-indicator-plugin/
URL:		http://goodies.xfce.org/projects/panel-plugins/xfce4-indicator-plugin
Source0:	http://archive.xfce.org/src/panel-plugins/xfce4-indicator-plugin/0.5/xfce4-indicator-plugin-%{version}.tar.bz2

BuildRequires:	gettext
BuildRequires:	intltool
BuildRequires:	pkgconfig

BuildRequires:	pkgconfig(exo-1)
BuildRequires:	pkgconfig(indicator-0.4)
BuildRequires:	pkgconfig(libxfce4panel-1.0)
BuildRequires:	pkgconfig(libxfconf-0)

%description
This package contains a small plugin written by Mark Trompell to display
information from various applications consistently in the panel as described in
Ubuntu's MessagingMenu design specification.


%prep
%setup -q


%build
%configure
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT

%find_lang xfce4-indicator-plugin


%files -f xfce4-indicator-plugin.lang
%doc AUTHORS ChangeLog NEWS README THANKS TODO
%{_libexecdir}/xfce4/panel-plugins/xfce4-indicator-plugin
%{_datadir}/icons/hicolor/48x48/apps/xfce4-indicator-plugin.png
%{_datadir}/icons/hicolor/scalable/apps/xfce4-indicator-plugin.svg
%{_datadir}/xfce4/panel-plugins/indicator.desktop


%changelog
* Sat Aug 11 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.5.0-1
- Initial release
- Version 0.5.0
