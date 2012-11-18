# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

Name:		account-plugins
Version:	0.9
Release:	1%{?dist}
Summary:	GNOME Control Center account plugins for Single Sign On

Group:		User Interface/Desktops
License:	GPLv2+
URL:		https://launchpad.net/online-accounts-account-plugins
Source0:	https://launchpad.net/account-plugins/12.10/%{version}/+download/account-plugins-%{version}.tar.gz

BuildRequires:	vala

BuildRequires:	pkgconfig(account-plugin)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(libaccounts-glib)
BuildRequires:	pkgconfig(libsignon-glib)
BuildRequires:	pkgconfig(python3)

%description
(no files installed)


%package -n account-plugin-google
Summary:	GNOME Control Center account plugin for Single Sign On - Google

Requires:	signon-keyring-extension
Requires:	signon-plugin-oauth2

%description -n account-plugin-google
This package contains the GNOME Control Center account plugin for signing on to
Google's services.


%package -n account-plugin-facebook
Summary:	GNOME Control Center account plugin for Single Sign On - Facebook

Requires:	signon-keyring-extension
Requires:	signon-plugin-oauth2

%description -n account-plugin-facebook
This package contains the GNOME Control Center account plugin for signing on to
Facebook.


%package -n account-plugin-twitter
Summary:	GNOME Control Center account plugin for Single Sign On - Twitter

Requires:	signon-keyring-extension
Requires:	signon-plugin-oauth2

%description -n account-plugin-twitter
This package contains the GNOME Control Center account plugin for signing on to
Twitter.


%package -n account-plugin-flickr
Summary:	GNOME Control Center account plugin for Single Sign On - Flickr

Requires:	signon-keyring-extension
Requires:	signon-plugin-oauth2

%description -n account-plugin-flickr
This package contains the GNOME Control Center account plugin for signing on to
Flickr.


%package -n account-plugin-identica
Summary:	GNOME Control Center account plugin for Single Sign On - identi.ca

Requires:	signon-keyring-extension
Requires:	signon-plugin-oauth2

%description -n account-plugin-identica
This package contains the GNOME Control Center account plugin for signing on to
identi.ca.


%package -n account-plugin-foursquare
Summary:	GNOME Control Center account plugin for Single Sign On - foursquare

Requires:	signon-keyring-extension
Requires:	signon-plugin-oauth2

%description -n account-plugin-foursquare
This package contains the GNOME Control Center account plugin for signing on to
foursquare.


%package -n account-plugin-windows-live
Summary:	GNOME Control Center account plugin for Single Sign On - Windows Live

Requires:	signon-keyring-extension
Requires:	signon-plugin-oauth2

%description -n account-plugin-windows-live
This package contains the GNOME Control Center account plugin for signing on to
Windows Live.


%package -n account-plugin-sohu
Summary:	GNOME Control Center account plugin for Single Sign On - Sohu

Requires:	signon-keyring-extension
Requires:	signon-plugin-oauth2

%description -n account-plugin-sohu
This package contains the GNOME Control Center account plugin for signing on to
搜狐网.


%package -n account-plugin-sina
Summary:	GNOME Control Center account plugin for Single Sign On - Sina

Requires:	signon-keyring-extension
Requires:	signon-plugin-oauth2

%description -n account-plugin-sina
This package contains the GNOME Control Center account plugin for signing on to
Sina.


%package -n account-plugin-tools
Summary:	GNOME Control Center account plugin for Single Sign On - Tools

Requires:	signon-keyring-extension
Requires:	signon-plugin-oauth2

%description -n account-plugin-tools
This package contains some tools for the GNOME Control Center account plugins.


%package -n account-plugin-icons
Summary:	GNOME Control Center account plugin for Single Sign On - Icons

BuildArch:	noarch

Requires:	hicolor-icon-theme

%description -n account-plugin-icons
This package contains the icons for the GNOME Control Center account plugins.


%prep
%setup -q


%build
%configure \
  --with-twitter-consumer-key="IOW164CqEJdlrkXlrQ17GA" \
  --with-twitter-consumer-secret="mJ38xSp6kqUzB2XMOq9USrmTgWAXOqXpS0g6WUEk"

make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT

# Remove libtool files
find $RPM_BUILD_ROOT -type f -name '*.la' -delete


### Begin: Icon Cache post ###
%post -n account-plugin-google
touch --no-create %{_datadir}/icons/hicolor/ &>/dev/null || :

%post -n account-plugin-facebook
touch --no-create %{_datadir}/icons/hicolor/ &>/dev/null || :

%post -n account-plugin-twitter
touch --no-create %{_datadir}/icons/hicolor/ &>/dev/null || :

%post -n account-plugin-flickr
touch --no-create %{_datadir}/icons/hicolor/ &>/dev/null || :

%post -n account-plugin-identica
touch --no-create %{_datadir}/icons/hicolor/ &>/dev/null || :

%post -n account-plugin-foursquare
touch --no-create %{_datadir}/icons/hicolor/ &>/dev/null || :

%post -n account-plugin-windows-live
touch --no-create %{_datadir}/icons/hicolor/ &>/dev/null || :

%post -n account-plugin-icons
touch --no-create %{_datadir}/icons/hicolor/ &>/dev/null || :
###  End: Icon Cache post  ###

### Begin: Icon Cache postun ###
%postun -n account-plugin-google
if [ ${1} -eq 0 ]; then
  touch --no-create %{_datadir}/icons/hicolor/ &>/dev/null
  gtk-update-icon-cache -f %{_datadir}/icons/hicolor/ &>/dev/null || :
fi

%postun -n account-plugin-facebook
if [ ${1} -eq 0 ]; then
  touch --no-create %{_datadir}/icons/hicolor/ &>/dev/null
  gtk-update-icon-cache -f %{_datadir}/icons/hicolor/ &>/dev/null || :
fi

%postun -n account-plugin-twitter
if [ ${1} -eq 0 ]; then
  touch --no-create %{_datadir}/icons/hicolor/ &>/dev/null
  gtk-update-icon-cache -f %{_datadir}/icons/hicolor/ &>/dev/null || :
fi

%postun -n account-plugin-flickr
if [ ${1} -eq 0 ]; then
  touch --no-create %{_datadir}/icons/hicolor/ &>/dev/null
  gtk-update-icon-cache -f %{_datadir}/icons/hicolor/ &>/dev/null || :
fi

%postun -n account-plugin-identica
if [ ${1} -eq 0 ]; then
  touch --no-create %{_datadir}/icons/hicolor/ &>/dev/null
  gtk-update-icon-cache -f %{_datadir}/icons/hicolor/ &>/dev/null || :
fi

%postun -n account-plugin-foursquare
if [ ${1} -eq 0 ]; then
  touch --no-create %{_datadir}/icons/hicolor/ &>/dev/null
  gtk-update-icon-cache -f %{_datadir}/icons/hicolor/ &>/dev/null || :
fi

%postun -n account-plugin-windows-live
if [ ${1} -eq 0 ]; then
  touch --no-create %{_datadir}/icons/hicolor/ &>/dev/null
  gtk-update-icon-cache -f %{_datadir}/icons/hicolor/ &>/dev/null || :
fi

%postun -n account-plugin-icons
if [ ${1} -eq 0 ]; then
  touch --no-create %{_datadir}/icons/hicolor/ &>/dev/null
  gtk-update-icon-cache -f %{_datadir}/icons/hicolor/ &>/dev/null || :
fi
###  End: Icon Cache postun  ###

### Begin: Icon Cache posttrans ###
%posttrans -n account-plugin-google
gtk-update-icon-cache -f %{_datadir}/icons/hicolor/ &>/dev/null || :

%posttrans -n account-plugin-facebook
gtk-update-icon-cache -f %{_datadir}/icons/hicolor/ &>/dev/null || :

%posttrans -n account-plugin-twitter
gtk-update-icon-cache -f %{_datadir}/icons/hicolor/ &>/dev/null || :

%posttrans -n account-plugin-flickr
gtk-update-icon-cache -f %{_datadir}/icons/hicolor/ &>/dev/null || :

%posttrans -n account-plugin-identica
gtk-update-icon-cache -f %{_datadir}/icons/hicolor/ &>/dev/null || :

%posttrans -n account-plugin-foursquare
gtk-update-icon-cache -f %{_datadir}/icons/hicolor/ &>/dev/null || :

%posttrans -n account-plugin-windows-live
gtk-update-icon-cache -f %{_datadir}/icons/hicolor/ &>/dev/null || :

%posttrans -n account-plugin-icons
gtk-update-icon-cache -f %{_datadir}/icons/hicolor/ &>/dev/null || :
###  End: Icon Cache posttrans


%files -n account-plugin-google
%dir %{_sysconfdir}/signon-ui/
%dir %{_sysconfdir}/signon-ui/webkit-options.d/
%dir %{_libdir}/libaccount-plugin-1.0/
%dir %{_libdir}/libaccount-plugin-1.0/providers/
%dir %{_datadir}/accounts/
%dir %{_datadir}/accounts/services/
%dir %{_datadir}/accounts/providers/
%{_sysconfdir}/signon-ui/webkit-options.d/accounts.google.com.conf
%{_libdir}/libaccount-plugin-1.0/providers/libgoogle.so
%{_datadir}/accounts/services/google-docs.service
%{_datadir}/accounts/services/google-im.service
%{_datadir}/accounts/services/picasa.service
%{_datadir}/accounts/providers/google.provider
%{_datadir}/icons/hicolor/32x32/apps/google.png


%files -n account-plugin-facebook
%dir %{_sysconfdir}/signon-ui/
%dir %{_sysconfdir}/signon-ui/webkit-options.d/
%dir %{_libdir}/libaccount-plugin-1.0/
%dir %{_libdir}/libaccount-plugin-1.0/providers/
%dir %{_datadir}/accounts/
%dir %{_datadir}/accounts/services/
%dir %{_datadir}/accounts/providers/
%{_sysconfdir}/signon-ui/webkit-options.d/www.facebook.com.conf
%{_libdir}/libaccount-plugin-1.0/providers/libfacebook.so
%{_datadir}/accounts/services/facebook-im.service
%{_datadir}/accounts/services/facebook-microblog.service
%{_datadir}/accounts/services/facebook-sharing.service
%{_datadir}/accounts/providers/facebook.provider
%{_datadir}/icons/hicolor/32x32/apps/facebook.png


%files -n account-plugin-twitter
%dir %{_sysconfdir}/signon-ui/
%dir %{_sysconfdir}/signon-ui/webkit-options.d/
%dir %{_libdir}/libaccount-plugin-1.0/
%dir %{_libdir}/libaccount-plugin-1.0/providers/
%dir %{_datadir}/accounts/
%dir %{_datadir}/accounts/services/
%dir %{_datadir}/accounts/providers/
%{_sysconfdir}/signon-ui/webkit-options.d/api.twitter.com.conf
%{_libdir}/libaccount-plugin-1.0/providers/libtwitter.so
%{_datadir}/accounts/services/twitter-microblog.service
%{_datadir}/accounts/providers/twitter.provider
%{_datadir}/icons/hicolor/32x32/apps/twitter.png


%files -n account-plugin-flickr
%dir %{_sysconfdir}/signon-ui/
%dir %{_sysconfdir}/signon-ui/webkit-options.d/
%dir %{_libdir}/libaccount-plugin-1.0/
%dir %{_libdir}/libaccount-plugin-1.0/providers/
%dir %{_datadir}/accounts/
%dir %{_datadir}/accounts/services/
%dir %{_datadir}/accounts/providers/
%{_sysconfdir}/signon-ui/webkit-options.d/login.yahoo.com.conf
%{_libdir}/libaccount-plugin-1.0/providers/libflickr.so
%{_datadir}/accounts/services/flickr-microblog.service
%{_datadir}/accounts/services/flickr-sharing.service
%{_datadir}/accounts/providers/flickr.provider
%{_datadir}/icons/hicolor/32x32/apps/flickr.png


%files -n account-plugin-identica
%dir %{_sysconfdir}/signon-ui/
%dir %{_sysconfdir}/signon-ui/webkit-options.d/
%dir %{_libdir}/libaccount-plugin-1.0/
%dir %{_libdir}/libaccount-plugin-1.0/providers/
%dir %{_datadir}/accounts/
%dir %{_datadir}/accounts/services/
%dir %{_datadir}/accounts/providers/
%{_sysconfdir}/signon-ui/webkit-options.d/identi.ca.conf
%{_libdir}/libaccount-plugin-1.0/providers/libidentica.so
%{_datadir}/accounts/services/identica-microblog.service
%{_datadir}/accounts/providers/identica.provider
%{_datadir}/icons/hicolor/32x32/apps/identica.png


%files -n account-plugin-foursquare
%dir %{_sysconfdir}/signon-ui/
%dir %{_sysconfdir}/signon-ui/webkit-options.d/
%dir %{_libdir}/libaccount-plugin-1.0/
%dir %{_libdir}/libaccount-plugin-1.0/providers/
%dir %{_datadir}/accounts/
%dir %{_datadir}/accounts/services/
%dir %{_datadir}/accounts/providers/
%{_sysconfdir}/signon-ui/webkit-options.d/foursquare.com.conf
%{_libdir}/libaccount-plugin-1.0/providers/libfoursquare.so
%{_datadir}/accounts/services/foursquare-microblog.service
%{_datadir}/accounts/providers/foursquare.provider
%{_datadir}/icons/hicolor/32x32/apps/foursquare.png


%files -n account-plugin-windows-live
%dir %{_sysconfdir}/signon-ui/
%dir %{_sysconfdir}/signon-ui/webkit-options.d/
%dir %{_libdir}/libaccount-plugin-1.0/
%dir %{_libdir}/libaccount-plugin-1.0/providers/
%dir %{_datadir}/accounts/
%dir %{_datadir}/accounts/services/
%dir %{_datadir}/accounts/providers/
%{_sysconfdir}/signon-ui/webkit-options.d/login.live.com.conf
%{_libdir}/libaccount-plugin-1.0/providers/libwindows-live.so
%{_datadir}/accounts/services/wlm.service
%{_datadir}/accounts/providers/windows-live.provider
%{_datadir}/icons/hicolor/32x32/apps/live.png


%files -n account-plugin-sohu
%dir %{_sysconfdir}/signon-ui/
%dir %{_sysconfdir}/signon-ui/webkit-options.d/
%dir %{_libdir}/libaccount-plugin-1.0/
%dir %{_libdir}/libaccount-plugin-1.0/providers/
%dir %{_datadir}/accounts/
%dir %{_datadir}/accounts/services/
%dir %{_datadir}/accounts/providers/
%{_sysconfdir}/signon-ui/webkit-options.d/api.t.sohu.com.conf
%{_libdir}/libaccount-plugin-1.0/providers/libsohu.so
%{_datadir}/accounts/services/sohu-microblog.service
%{_datadir}/accounts/providers/sohu.provider


%files -n account-plugin-sina
%dir %{_sysconfdir}/signon-ui/
%dir %{_sysconfdir}/signon-ui/webkit-options.d/
%dir %{_libdir}/libaccount-plugin-1.0/
%dir %{_libdir}/libaccount-plugin-1.0/providers/
%dir %{_datadir}/accounts/
%dir %{_datadir}/accounts/services/
%dir %{_datadir}/accounts/providers/
%{_sysconfdir}/signon-ui/webkit-options.d/api.t.sina.com.cn.conf
%{_libdir}/libaccount-plugin-1.0/providers/libsina.so
%{_datadir}/accounts/services/sina-microblog.service
%{_datadir}/accounts/providers/sina.provider


%files -n account-plugin-tools
%{_bindir}/account-console


%files -n account-plugin-icons
%{_datadir}/icons/hicolor/32x32/apps/aim.png
%{_datadir}/icons/hicolor/32x32/apps/gadugadu.png
%{_datadir}/icons/hicolor/32x32/apps/groupwise.png
%{_datadir}/icons/hicolor/32x32/apps/icq.png
%{_datadir}/icons/hicolor/32x32/apps/irc.png
%{_datadir}/icons/hicolor/32x32/apps/jabber.png
%{_datadir}/icons/hicolor/32x32/apps/msn.png
%{_datadir}/icons/hicolor/32x32/apps/mxit.png
%{_datadir}/icons/hicolor/32x32/apps/myspace.png
%{_datadir}/icons/hicolor/32x32/apps/people-nearby.png
%{_datadir}/icons/hicolor/32x32/apps/sametime.png
%{_datadir}/icons/hicolor/32x32/apps/sip.png
%{_datadir}/icons/hicolor/32x32/apps/yahoo.png
%{_datadir}/icons/hicolor/32x32/apps/zephyr.png


%changelog
* Sun Nov 18 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.9-1
- Version 0.9

* Thu Sep 27 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.8-1
- Initial release
- Version 0.8
