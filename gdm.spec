%define _disable_ld_no_undefined 1

%define major		1
%define	gmajor		1.0
%define libname		%mklibname gdm %{major}
%define libnamesimple	%mklibname gdmsimplegreeter %{major}
%define develname	%mklibname -d %{name}
%define girname		%mklibname gdm-gir %{gmajor}

%define url_ver	%(echo %{version}|cut -d. -f1,2)

Summary:	The GNOME Display Manager
Name:		gdm
Version:	3.6.2
Release:	2
License:	GPLv2+
Group:		Graphical desktop/GNOME
URL:		http://www.gnome.org/projects/gdm/
Source0:	ftp://ftp.gnome.org/pub/GNOME/sources/%{name}/%{url_ver}/%{name}-%{version}.tar.xz
# (cg) Managing patches via git
# git format-patch --start-number 100 3.1.2..mga-3.1.2-cherry-picks

# git format-patch --start-number 200 mga-3.1.2-cherry-picks..mga-3.1.2-plymouth
#Patch0200:	0200-Save-root-window-to-pixmap-at-_XROOTPMAP_ID.patch
#Patch0201:	0201-Enable-smooth-transition-between-plymouth-and-X.patch
#Patch0202:	0202-Fedora-force-active-vt-patch-separated-from-plymouth.patch
#Patch0203:	0203-Mageia-force-active-vt-patch-fix.patch
# git format-patch --start-number 300 mga-3.1.2-plymouth..mga-3.1.2-patches
Patch0300:	0300-Novell-Make-keyboard-selector-not-neglect-to-apply-t.patch
Patch0301:	0301-Novell-Look-at-the-current-runlevel-before-managing-.patch
Patch0302:	0302-Fix-gdm-pam.d-configs.patch
Patch0303:	0303-Read-.xsetup-scripts.patch
Patch0400:	gdm-3.6.2-automake-1.13.patch

Provides:	dm

Requires(pre):		rpm-helper
Requires(postun):	rpm-helper
Requires(post):		dconf
Requires:	pam
Requires:	sessreg
Requires:	usermode
Requires:	cdialog
Requires:	zenity
Requires:	gnome-session-bin
Requires:	gnome-settings-daemon
Requires:	metacity
Suggests:	gnome-power-manager
# for XFdrake on failsafe fallback:
Requires:	drakx-kbd-mouse-x11
Requires:	xinitrc >= 2.4.14
Requires:	dbus-x11
Requires:	polkit-gnome
Requires:	accountsservice
Requires:	gnome-icon-theme-symbolic
Provides:	gdm-Xnest
Obsoletes:	gdm-Xnest

Obsoletes:	gdm-themes
Conflicts:	gdm-220
BuildRequires: 	pkgconfig(accountsservice) >= 0.6.12
BuildRequires:	pkgconfig(check) >= 0.9.4
BuildRequires:	pkgconfig(dbus-glib-1) >= 0.74
BuildRequires:	pkgconfig(fontconfig) >= 2.5.0
BuildRequires:	pkgconfig(gconf-2.0) >= 2.31.3
BuildRequires:	pkgconfig(gio-2.0) >= 2.29.3
BuildRequires:	pkgconfig(gobject-2.0) >= 2.29.3
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(gthread-2.0)
BuildRequires:	pkgconfig(gtk+-3.0) >= 2.91.1
BuildRequires:	pkgconfig(libcanberra-gtk3) >= 0.4
BuildRequires:	pkgconfig(libxklavier) >= 4.0
BuildRequires:	pkgconfig(nss) >= 3.11.1
BuildRequires:	pkgconfig(libsystemd-login)
BuildRequires:	pkgconfig(libsystemd-daemon)
BuildRequires:	pkgconfig(ply-boot-client)
BuildRequires:	pkgconfig(upower-glib) >= 0.9.0
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xau)
BuildRequires:	pkgconfig(xdmcp)
BuildRequires:	pkgconfig(xrandr)
BuildRequires:	pam-devel
BuildRequires:	libwrap-devel
BuildRequires:	audit-devel
BuildRequires:	intltool >= 0.40.0
BuildRequires:	gettext-devel
BuildRequires:	yelp-tools
BuildRequires:	itstool
BuildRequires:	gnome-common

Obsoletes:	gdm-user-switch-applet < 3.0.0

%description
Gdm (the GNOME Display Manager) is a highly configurable
reimplementation of xdm, the X Display Manager. Gdm allows you to log
into your system with the X Window System running and supports running
several different X sessions on your local machine at the same time.

%pre
%_pre_useradd gdm %{_var}/lib/gdm /bin/false
%_pre_groupadd xgrp gdm

%post

# (cg) Setup dconf settings for gdm
# http://git.gnome.org/browse/gdm/commit/?id=eebeb62e2daccc932f3033fbd857b619ba9936d0
dconf update

if [ -f /%{_sysconfdir}/X11/xdm/Xsession -a ! -x /%{_sysconfdir}/X11/xdm/Xsession ]; then
        chmod +x /%{_sysconfdir}/X11/xdm/Xsession
fi
if [ -x /usr/sbin/chksession ]; then /usr/sbin/chksession -g || true; fi

%update_scrollkeeper
%{_sbindir}/gdm-safe-restart >/dev/null 2>&1 || :

%postun
%_postun_userdel gdm
%_postun_groupdel xgrp gdm

%files -f %{name}.lang
%doc AUTHORS COPYING NEWS README
%_sysconfdir/dbus-1/system.d/gdm.conf
%{_bindir}/gdm-screenshot
%{_bindir}/gdmflexiserver
%{_sbindir}/gdm
%{_sbindir}/gdm-binary
%dir %{_sysconfdir}/X11/gdm
%config(noreplace) %{_sysconfdir}/pam.d/gdm
%config(noreplace) %{_sysconfdir}/pam.d/gdm-autologin
%config(noreplace) %{_sysconfdir}/pam.d/gdm-fingerprint
%config(noreplace) %{_sysconfdir}/pam.d/gdm-password
%config(noreplace) %{_sysconfdir}/pam.d/gdm-smartcard
%config(noreplace) %{_sysconfdir}/pam.d/gdm-launch-environment
%config(noreplace) %{_sysconfdir}/X11/gdm/custom.conf
%config(noreplace) %{_sysconfdir}/X11/gdm/Xsession
%dir %{_sysconfdir}/X11/dm
%dir %{_sysconfdir}/X11/dm/Sessions
%config(noreplace) %{_sysconfdir}/X11/gdm/PreSession
%config(noreplace) %{_sysconfdir}/X11/gdm/PostSession
%config(noreplace) %{_sysconfdir}/X11/gdm/PostLogin
%config(noreplace) %{_sysconfdir}/X11/gdm/Init
%{_libexecdir}/gdm-crash-logger
%{_libexecdir}/gdm-host-chooser
%{_libexecdir}/gdm-session-worker
%{_libexecdir}/gdm-simple-chooser
%{_libexecdir}/gdm-simple-greeter
%{_libexecdir}/gdm-simple-slave
%{_libexecdir}/gdm-smartcard-worker
%{_libexecdir}/gdm-xdmcp-chooser-slave
%dir %{_libdir}/gdm
%dir %{_libdir}/gdm/simple-greeter
%dir %{_libdir}/gdm/simple-greeter/extensions
%{_libdir}/gdm/simple-greeter/extensions/libfingerprint.so
%{_libdir}/gdm/simple-greeter/extensions/libpassword.so
%{_libdir}/gdm/simple-greeter/extensions/libsmartcard.so
%{_datadir}/pixmaps/*
%{_datadir}/gdm
%{_datadir}/glib-2.0/schemas/org.gnome.login-screen.gschema.xml
%dir %{_datadir}/hosts
%attr(1770, gdm, gdm) %dir %{_localstatedir}/lib/gdm
%attr(1750, gdm, gdm) %dir %{_localstatedir}/lib/gdm/.config
%attr(1750, gdm, gdm) %dir %{_localstatedir}/lib/gdm/.config/dconf
#attr(1750, gdm, gdm) %dir %{_localstatedir}/lib/gdm/.local/share/applications
%attr(1755, gdm, gdm) %dir %{_localstatedir}/run/gdm/greeter
%attr(1777, root, gdm) %dir %{_localstatedir}/run/gdm
%attr(1755, root, gdm) %dir %{_localstatedir}/cache/gdm
%attr(640,gdm,gdm) %{_localstatedir}/lib/gdm/.local
%{_sysconfdir}/dconf/profile/gdm
%ghost %{_sysconfdir}/dconf/db/%{name}
%dir %{_sysconfdir}/dconf/db/gdm.d
%{_sysconfdir}/dconf/db/gdm.d/00-upstream-settings
%dir %{_sysconfdir}/dconf/db/gdm.d/locks
%{_sysconfdir}/dconf/db/gdm.d/locks/00-upstream-settings-locks
%{_datadir}/gnome-session/sessions/gdm-shell.session
%{_datadir}/gnome-session/sessions/gdm-fallback.session
%dir %{_var}/log/gdm
%{_datadir}/icons/hicolor/*/apps/gdm*
# (cg) Note: Ship this, but lets not enable it or do anything fancy
# until we fully redo any prefdm stuff and have units for all DMs
# we support.
%{_unitdir}/gdm.service

#--------------------------------------------------------------------
%package -n %{libnamesimple}
Summary:	Library for the %name simple greeter
Group:		System/Libraries

%description -n %{libnamesimple}
Gdm (the GNOME Display Manager) is a highly configurable
reimplementation of xdm, the X Display Manager. Gdm allows you to log
into your system with the X Window System running and supports running
several different X sessions on your local machine at the same time.

%files -n %{libnamesimple}
%{_libdir}/libgdmsimplegreeter.so.%{major}*

#--------------------------------------------------------------------
%package -n %{libname}
Summary:	Library for the %name greeter
Group:		System/Libraries
Obsoletes:	%{_lib}gdmreeter1 < 3.2.1-3

%description -n %{libname}
Gdm (the GNOME Display Manager) is a highly configurable
reimplementation of xdm, the X Display Manager. Gdm allows you to log
into your system with the X Window System running and supports running
several different X sessions on your local machine at the same time.

%files -n %{libname}
%{_libdir}/libgdm.so.%{major}*

#--------------------------------------------------------------------

%package -n %{girname}
Summary:        GObject Introspection interface description for %{name}
Group:          System/Libraries
Requires:       %{libname} = %{version}-%{release}

%description -n %{girname}
GObject Introspection interface description for %{name}.

%files -n %{girname}
%{_libdir}/girepository-1.0/Gdm-%{gmajor}.typelib

#--------------------------------------------------------------------

%package -n %{develname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{develname}
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%files -n %{develname}
%{_includedir}/gdm
%{_libdir}/libgdmsimplegreeter.so
%{_libdir}/libgdm.so
%{_libdir}/pkgconfig/gdmsimplegreeter.pc
%{_libdir}/pkgconfig/gdm.pc
%{_datadir}/gir-1.0/Gdm-%{gmajor}.gir

#--------------------------------------------------------------------

%prep
%setup -q
cp data/Init.in data/Default.in
%apply_patches

%build
NOCONFIGURE=yes gnome-autogen.sh
%configure2_5x \
	--with-sysconfsubdir=X11/gdm \
	--with-dmconfdir=%{_sysconfdir}/X11/dm \
	--disable-static \
	--with-console-kit=no \
	--with-systemd \
	--with-plymouth

%make

%install
%makeinstall_std PAM_PREFIX=%{_sysconfdir}

# don't provide PreSession/PostSession, pam handle this
rm -f %{buildroot}%{_sysconfdir}/X11/PreSession/Default
rm -f %{buildroot}%{_sysconfdir}/X11/PostSession/Default

mkdir -p %{buildroot}%{_datadir}/hosts

%find_lang %{name} --with-gnome --all-name

mkdir -p %{buildroot}%{_var}/log/gdm %{buildroot}%{_sysconfdir}/X11/dm/Sessions

#remove unpackaged files
rm -rf %{buildroot}%{_sysconfdir}/X11/gdm/PostLogin/Default.sample \
  %{buildroot}%{_datadir}/xsessions/gnome.desktop

find %{buildroot} -name '*.la' -delete

# (cg) The existing gdm file is what we really want for gdm-password
rm -f %{buildroot}%{_sysconfdir}/pam.d/gdm-password
ln -s gdm %{buildroot}%{_sysconfdir}/pam.d/gdm-password

# (cg) For ghost ownership
touch %{buildroot}%{_sysconfdir}/dconf/db/%{name}
