Summary: The GNOME Display Manager
Name: gdm
Version: 2.19.4
Release: %mkrel 1
License: LGPL/GPL
Group: Graphical desktop/GNOME
URL: http://www.gnome.org/projects/gdm/
Source0: ftp://ftp.gnome.org/pub/GNOME/sources/gdm/%{name}-%{version}.tar.bz2
Source2: gdm_48.png
Source3: gdm_32.png
Source4: gdm_16.png

# (fc) 2.2.2.1-1mdk change default configuration
Patch0: gdm-2.19.4-defaultconf.patch
# (fc) 2.4.0.11-3mdk use xvt instead of xterm
Patch1: gdm-2.19.1-xvt.patch
# (fc) 2.6.0.6-3mdk use pam_timestamp for gdmsetup (Fedora)
# and  don't use deprecated pam_stack (blino)
Patch4: gdm-2.19.0-pam.patch
# (fc) 2.6.0.6-3mdk clean up xses if session was sucessfully completed (Fedora)
Patch5: gdm-2.19.0-cleanup-xses.patch
# (fc) 2.18.0-2mdv force TMPDIR to /tmp, fix a11y startup inside gdm (Mdv bug #23215)
Patch6: gdm-2.19.1-tmpdir.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-root

Provides: dm

Requires(pre):     rpm-helper
Requires(postun):  rpm-helper
Requires(post):	   scrollkeeper >= 0.3
Requires(postun):  scrollkeeper >= 0.3
Requires(post): desktop-common-data
Requires: pam >= 0.72-11mdk
Requires: setup >= 2.1.9-33mdk
Requires: sessreg
Requires: usermode
Requires: cdialog
Requires: zenity
Requires: drakxtools-newt
Requires: xinitrc >= 2.4.14
%if %mdkversion >= 200610
BuildRequires: X11-static-devel
BuildRequires: x11-server-xorg
%else
BuildRequires: XFree86-static-devel
%endif
BuildRequires: gettext
BuildRequires: libglade2.0-devel
BuildRequires: libgnomeui2-devel
BuildRequires: librsvg-devel
BuildRequires: pam-devel
BuildRequires: usermode
BuildRequires: scrollkeeper
BuildRequires: gnome-doc-utils
BuildRequires: automake1.9 intltool
#gw for running intltool scripts
BuildRequires: perl-XML-Parser


%description
Gdm (the GNOME Display Manager) is a highly configurable
reimplementation of xdm, the X Display Manager. Gdm allows you to log
into your system with the X Window System running and supports running
several different X sessions on your local machine at the same time.

%package Xnest
Summary: Xnest (ie embedded X) server for GDM
Group: %{group}
Requires: %{name} = %{version}
Requires: x11-server-xnest

%description Xnest
Gdm (the GNOME Display Manager) is a highly configurable
reimplementation of xdm, the X Display Manager. Gdm allows you to log
into your system with the X Window System running and supports running
several different X sessions on your local machine at the same time.

This package add support for Xnest server in gdm

%prep
%setup -q
cp config/Init.in config/Default.in

%patch0 -p1 -b .defaultconf
%patch1 -p1 -b .xvt
%patch4 -p1 -b .pam
%patch5 -p1 -b .cleanup_xses
%patch6 -p1 -b .tmpdir

cp config/locale.alias config/locales.alias.noutf8
sed -i -e 's/..\(_..\)*\.UTF-8\(@[^,]\+\)*,//g' config/locale.alias


%build

%configure2_5x --enable-console-helper --sysconfdir=%{_sysconfdir}/X11 \
  --disable-scrollkeeper 
%make

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall_std PAM_PREFIX=%{_sysconfdir} 

# don't provide PreSession/PostSession, pam handle this
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/X11/PreSession/Default
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/X11/PostSession/Default

ln -s consolehelper $RPM_BUILD_ROOT%{_bindir}/gdmsetup
perl -pi -e "s^%{_sbindir}/^^" %buildroot%_datadir/applications/gdmsetup.desktop

mkdir -p $RPM_BUILD_ROOT%{_datadir}/hosts

mkdir -p  $RPM_BUILD_ROOT%{_liconsdir} $RPM_BUILD_ROOT%{_miconsdir}
cp %{SOURCE2} $RPM_BUILD_ROOT%{_liconsdir}/gdm.png
cp %{SOURCE3} $RPM_BUILD_ROOT%{_iconsdir}/gdm.png
cp %{SOURCE4} $RPM_BUILD_ROOT%{_miconsdir}/gdm.png

%{find_lang} %{name}-2.4 --with-gnome --all-name
for omf in %buildroot%_datadir/omf/%name/%name-??*.omf;do 
echo "%lang($(basename $omf|sed -e s/%name-// -e s/.omf//)) $(echo $omf|sed -e s!%buildroot!!)" >> %name-2.4.lang
done

mkdir -p $RPM_BUILD_ROOT%{_var}/log/gdm $RPM_BUILD_ROOT%{_sysconfdir}/X11/dm/Sessions

#remove unpackaged files
rm -rf $RPM_BUILD_ROOT%{_sysconfdir}/X11/dm/Sessions/*.desktop \
  $RPM_BUILD_ROOT%{_libdir}/gtk-2.0/modules/*.{la,a} \
  $RPM_BUILD_ROOT%{_sysconfdir}/X11/gdm/PostLogin/Default.sample \
  $RPM_BUILD_ROOT%{_datadir}/xsessions

%clean
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT

%pre
%_pre_useradd gdm %{_localstatedir}/gdm /bin/false
%_pre_groupadd xgrp gdm

%triggerpostun -- gdm < 2.8.0.0-2mdk
if [ -d %{_datadir}/gdm/themes/mdk.to_remove ]; then 
  rm -fr %{_datadir}/gdm/themes/mdk.to_remove
  ln -s -f ../../mdk/dm %{_datadir}/gdm/themes/mdk
fi
#replace changed paths in gdm.conf
sed -i -e "s^%_bindir/\(gdm[^ \t]\+\)^%_libexecdir/\1^g"  %{_sysconfdir}/X11/gdm/gdm.conf

%post
#needed to update old gdm without removing new theme
#is removed by triggerpostun
if [ "$1" = "2" -a ! -L %{_datadir}/gdm/themes/mdk ]; then 
 mv %{_datadir}/gdm/themes/mdk  %{_datadir}/gdm/themes/mdk.to_remove
else 
 if [ ! -L %{_datadir}/gdm/themes/mdk ]; then
  ln -s -f ../../mdk/dm %{_datadir}/gdm/themes/mdk
 fi
fi

if [ -f /%{_sysconfdir}/X11/xdm/Xsession -a ! -x /%{_sysconfdir}/X11/xdm/Xsession ]; then
	chmod +x /%{_sysconfdir}/X11/xdm/Xsession
fi
%{make_session}
%{update_menus}
/sbin/ldconfig
%update_scrollkeeper
# Attempt to restart GDM softly by use of the fifo.  Wont work on older
# then 2.2.3.1 versions but should work nicely on later upgrades.
# FIXME: this is just way too complex
FIFOFILE=`grep '^ServAuthDir=' %{_sysconfdir}/X11/gdm/custom.conf | sed -e 's/^ServAuthDir=//'`
if test x$FIFOFILE = x ; then
        FIFOFILE=%{_localstatedir}/gdm/.gdmfifo
else
        FIFOFILE="$FIFOFILE"/.gdmfifo
fi
PIDFILE=`grep '^PidFile=' %{_sysconfdir}/X11/gdm/custom.conf | sed -e 's/^PidFile=//'`
if test x$PIDFILE = x ; then
        PIDFILE=/var/run/gdm.pid
fi
if test -w $FIFOFILE ; then
        if test -f $PIDFILE ; then
                if kill -0 `cat $PIDFILE` ; then
                        (echo;echo SOFT_RESTART) >> $FIFOFILE
                fi
        fi
fi
# ignore error in the above
exit 0

%preun
if [ "$1" = "0" ]; then
 rm -f %{_datadir}/gdm/themes/mdk > /dev/null
fi

%postun
%{make_session}
%_postun_userdel gdm
%_postun_groupdel xgrp gdm
%{clean_menus}
/sbin/ldconfig
%clean_scrollkeeper

%files -f %{name}-2.4.lang
%defattr(-, root, root)

%doc AUTHORS COPYING NEWS README gui/greeter/greeter.dtd
%_bindir/gdm-dmx-reconnect-proxy
%_bindir/gdmdynamic
%_bindir/gdmsetup
%{_bindir}/gdmphotosetup
%{_bindir}/gdmflexiserver
%{_libexecdir}/gdmchooser
%{_libexecdir}/gdmgreeter
%{_libexecdir}/gdmlogin
%{_libexecdir}/gdmaskpass
%{_libexecdir}/gdmopen
%{_libexecdir}/gdmtranslate
%{_sbindir}/*
%dir %{_sysconfdir}/X11/gdm
%{_sysconfdir}/X11/gdm/XKeepsCrashing
%config(noreplace) %{_sysconfdir}/pam.d/gdm
%config(noreplace) %{_sysconfdir}/pam.d/gdmsetup
%config(noreplace) %{_sysconfdir}/pam.d/gdm-autologin
%config(noreplace) %{_sysconfdir}/security/console.apps/gdmsetup
%config(noreplace) %{_sysconfdir}/X11/gdm/custom.conf
%config(noreplace) %{_sysconfdir}/X11/gdm/locale.alias
%config(noreplace) %{_sysconfdir}/X11/gdm/Xsession
%dir %{_sysconfdir}/X11/dm
%dir %{_sysconfdir}/X11/dm/Sessions
%config(noreplace) %{_sysconfdir}/X11/gdm/PreSession
%config(noreplace) %{_sysconfdir}/X11/gdm/PostSession
%config(noreplace) %{_sysconfdir}/X11/gdm/PostLogin
%config(noreplace) %{_sysconfdir}/X11/gdm/Init
%config(noreplace) %{_sysconfdir}/X11/gdm/modules
%{_libdir}/gtk-2.0/modules/*.so
%{_datadir}/pixmaps/*
%{_datadir}/gdm
%dir %{_datadir}/hosts
%attr(1770, gdm, gdm) %dir %{_localstatedir}/gdm
%dir %{_var}/log/gdm
%_datadir/icons/hicolor/*/apps/gdm*.png
%{_liconsdir}/*.png
%{_iconsdir}/*.png
%{_miconsdir}/*.png
%dir %{_datadir}/omf/%name
%{_datadir}/omf/%name/%name-C.omf
%{_mandir}/man1/*

%files Xnest
%defattr(-, root, root)
%{_bindir}/gdmthemetester
%{_bindir}/gdmXnestchooser
%{_bindir}/gdmXnest
