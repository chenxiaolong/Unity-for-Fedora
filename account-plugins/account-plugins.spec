# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

Name:		account-plugins
Version:	0.10bzr13.03.26
Release:	1%{?dist}
Summary:	GNOME Control Center account plugins for Single Sign On

Group:		User Interface/Desktops
License:	GPLv2+
URL:		https://launchpad.net/online-accounts-account-plugins
Source0:	https://launchpad.net/ubuntu/+archive/primary/+files/account-plugins_%{version}.orig.tar.gz

BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	intltool
BuildRequires:	libxml2
BuildRequires:	vala

BuildRequires:	pkgconfig(account-plugin)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(libaccounts-glib)
BuildRequires:	pkgconfig(libsignon-glib)
BuildRequires:	pkgconfig(python3)

%description
(no files installed)


%package -n account-plugin-generic-oauth
Summary:	GNOME Control Center account plugin for Single Sign On - Generic OAuth

Requires:	signon-keyring-extension
Requires:	signon-plugin-oauth2

%description -n account-plugin-generic-oauth
This package contains the GNOME Control Center account plugin for signing on to
OAuth-based services.


%package -n account-plugin-google
Summary:	GNOME Control Center account plugin for Single Sign On - Google

Requires:	signon-keyring-extension
Requires:	signon-plugin-oauth2
Requires:	unity-asset-pool

%description -n account-plugin-google
This package contains the GNOME Control Center account plugin for signing on to
Google's services.


%package -n account-plugin-facebook
Summary:	GNOME Control Center account plugin for Single Sign On - Facebook

Requires:	account-plugin-generic-oauth
Requires:	unity-asset-pool

%description -n account-plugin-facebook
This package contains the GNOME Control Center account plugin for signing on to
Facebook.


%package -n account-plugin-twitter
Summary:	GNOME Control Center account plugin for Single Sign On - Twitter

Requires:	account-plugin-generic-oauth
Requires:	unity-asset-pool

%description -n account-plugin-twitter
This package contains the GNOME Control Center account plugin for signing on to
Twitter.


%package -n account-plugin-flickr
Summary:	GNOME Control Center account plugin for Single Sign On - Flickr

Requires:	account-plugin-generic-oauth
Requires:	unity-asset-pool

%description -n account-plugin-flickr
This package contains the GNOME Control Center account plugin for signing on to
Flickr.


%package -n account-plugin-identica
Summary:	GNOME Control Center account plugin for Single Sign On - identi.ca

Requires:	account-plugin-generic-oauth
Requires:	unity-asset-pool

%description -n account-plugin-identica
This package contains the GNOME Control Center account plugin for signing on to
identi.ca.


%package -n account-plugin-foursquare
Summary:	GNOME Control Center account plugin for Single Sign On - foursquare

Requires:	account-plugin-generic-oauth
Requires:	unity-asset-pool

%description -n account-plugin-foursquare
This package contains the GNOME Control Center account plugin for signing on to
foursquare.


%package -n account-plugin-windows-live
Summary:	GNOME Control Center account plugin for Single Sign On - Windows Live

Requires:	account-plugin-generic-oauth
Requires:	unity-asset-pool

%description -n account-plugin-windows-live
This package contains the GNOME Control Center account plugin for signing on to
Windows Live.


%package -n account-plugin-sohu
Summary:	GNOME Control Center account plugin for Single Sign On - Sohu

Requires:	account-plugin-generic-oauth
Requires:	unity-asset-pool

%description -n account-plugin-sohu
This package contains the GNOME Control Center account plugin for signing on to
搜狐网.


%package -n account-plugin-sina
Summary:	GNOME Control Center account plugin for Single Sign On - Sina

Requires:	account-plugin-generic-oauth
Requires:	unity-asset-pool

%description -n account-plugin-sina
This package contains the GNOME Control Center account plugin for signing on to
Sina.


%package -n account-plugin-tools
Summary:	GNOME Control Center account plugin for Single Sign On - Tools

# Explicitly require for GObject Introspection bindings
Requires:	libaccounts-glib
Requires:	libsignon-glib
Requires:	signon-keyring-extension
Requires:	signon-plugin-oauth2
Requires:	python3-gobject
Requires:	unity-asset-pool

%description -n account-plugin-tools
This package contains some tools for the GNOME Control Center account plugins.


%prep
%setup -q

autoreconf -vfi
intltoolize -f


%build
%configure \
  --with-twitter-consumer-key="IOW164CqEJdlrkXlrQ17GA" \
  --with-twitter-consumer-secret="mJ38xSp6kqUzB2XMOq9USrmTgWAXOqXpS0g6WUEk"

make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT

# Remove libtool files
find $RPM_BUILD_ROOT -type f -name '*.la' -delete


%files -n account-plugin-generic-oauth
%dir %{_libdir}/libaccount-plugin-1.0/
%dir %{_libdir}/libaccount-plugin-1.0/providers/
%{_libdir}/libaccount-plugin-1.0/providers/libgeneric-oauth.so


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


%files -n account-plugin-facebook
%dir %{_sysconfdir}/signon-ui/
%dir %{_sysconfdir}/signon-ui/webkit-options.d/
%dir %{_libdir}/libaccount-plugin-1.0/
%dir %{_libdir}/libaccount-plugin-1.0/providers/
%dir %{_datadir}/accounts/
%dir %{_datadir}/accounts/services/
%dir %{_datadir}/accounts/providers/
%{_sysconfdir}/signon-ui/webkit-options.d/www.facebook.com.conf
%{_datadir}/accounts/services/facebook-im.service
%{_datadir}/accounts/services/facebook-microblog.service
%{_datadir}/accounts/services/facebook-sharing.service
%{_datadir}/accounts/providers/facebook.provider


%files -n account-plugin-twitter
%dir %{_sysconfdir}/signon-ui/
%dir %{_sysconfdir}/signon-ui/webkit-options.d/
%dir %{_libdir}/libaccount-plugin-1.0/
%dir %{_libdir}/libaccount-plugin-1.0/providers/
%dir %{_datadir}/accounts/
%dir %{_datadir}/accounts/services/
%dir %{_datadir}/accounts/providers/
%{_sysconfdir}/signon-ui/webkit-options.d/api.twitter.com.conf
%{_datadir}/accounts/services/twitter-microblog.service
%{_datadir}/accounts/providers/twitter.provider


%files -n account-plugin-flickr
%dir %{_sysconfdir}/signon-ui/
%dir %{_sysconfdir}/signon-ui/webkit-options.d/
%dir %{_libdir}/libaccount-plugin-1.0/
%dir %{_libdir}/libaccount-plugin-1.0/providers/
%dir %{_datadir}/accounts/
%dir %{_datadir}/accounts/services/
%dir %{_datadir}/accounts/providers/
%{_sysconfdir}/signon-ui/webkit-options.d/login.yahoo.com.conf
%{_sysconfdir}/signon-ui/webkit-options.d/secure.flickr.com.conf
%{_datadir}/accounts/services/flickr-microblog.service
%{_datadir}/accounts/services/flickr-sharing.service
%{_datadir}/accounts/providers/flickr.provider


%files -n account-plugin-identica
%dir %{_sysconfdir}/signon-ui/
%dir %{_sysconfdir}/signon-ui/webkit-options.d/
%dir %{_libdir}/libaccount-plugin-1.0/
%dir %{_libdir}/libaccount-plugin-1.0/providers/
%dir %{_datadir}/accounts/
%dir %{_datadir}/accounts/services/
%dir %{_datadir}/accounts/providers/
%{_sysconfdir}/signon-ui/webkit-options.d/identi.ca.conf
%{_datadir}/accounts/services/identica-microblog.service
%{_datadir}/accounts/providers/identica.provider


%files -n account-plugin-foursquare
%dir %{_sysconfdir}/signon-ui/
%dir %{_sysconfdir}/signon-ui/webkit-options.d/
%dir %{_libdir}/libaccount-plugin-1.0/
%dir %{_libdir}/libaccount-plugin-1.0/providers/
%dir %{_datadir}/accounts/
%dir %{_datadir}/accounts/services/
%dir %{_datadir}/accounts/providers/
%{_sysconfdir}/signon-ui/webkit-options.d/foursquare.com.conf
%{_datadir}/accounts/services/foursquare-microblog.service
%{_datadir}/accounts/providers/foursquare.provider


%files -n account-plugin-windows-live
%dir %{_sysconfdir}/signon-ui/
%dir %{_sysconfdir}/signon-ui/webkit-options.d/
%dir %{_libdir}/libaccount-plugin-1.0/
%dir %{_libdir}/libaccount-plugin-1.0/providers/
%dir %{_datadir}/accounts/
%dir %{_datadir}/accounts/services/
%dir %{_datadir}/accounts/providers/
%{_sysconfdir}/signon-ui/webkit-options.d/login.live.com.conf
%{_datadir}/accounts/services/wlm.service
%{_datadir}/accounts/providers/windows-live.provider


%files -n account-plugin-sohu
%dir %{_sysconfdir}/signon-ui/
%dir %{_sysconfdir}/signon-ui/webkit-options.d/
%dir %{_libdir}/libaccount-plugin-1.0/
%dir %{_libdir}/libaccount-plugin-1.0/providers/
%dir %{_datadir}/accounts/
%dir %{_datadir}/accounts/services/
%dir %{_datadir}/accounts/providers/
%{_sysconfdir}/signon-ui/webkit-options.d/api.t.sohu.com.conf
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
%{_datadir}/accounts/services/sina-microblog.service
%{_datadir}/accounts/providers/sina.provider


%files -n account-plugin-tools
%{_bindir}/account-console


%changelog
* Fri May 03 2013 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.10bzr13.03.26-1
- Version 0.10bzr13.03.26

* Mon Jan 28 2013 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.10bzr12.12.10-1
- Version 0.10bzr12.12.10
- Add python3-gobject to account-plugins-tools's dependencies
  - Also libacounts-glib and libsignon-glib for their GObject Introspection
    bindings

* Sun Nov 18 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.9-1
- Version 0.9

* Thu Sep 27 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.8-1
- Initial release
- Version 0.8
