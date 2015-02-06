%define realname cyrus
%define modname cyrus
%define dirname %{modname}
%define soname %{modname}.so
%define inifile A16_%{modname}.ini

Summary:	An extension which eases the manipulation of Cyrus IMAP servers for PHP
Name:		php-%{modname}
Version:	1.0
Release:	33
Group:		Development/PHP
License:	PHP License
URL:		http://pecl.php.net/package/cyrus
Source0:	%{modname}-%{version}.tar.bz2
Source1:	%{modname}.ini
Patch0:		cyrus-1.0-lib64.diff
Patch1:		cyrus-1.0-php54x.diff
Requires:	php-cli >= 3:5.2.0
BuildRequires:	php-devel >= 3:5.2.0
BuildRequires:	cyrus-imapd-devel
BuildRequires:	libsasl-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
An extension which eases the manipulation of Cyrus IMAP servers.

%prep

%setup -q -n %{modname}-%{version}
%patch0 -p0
%patch1 -p0

cp %{SOURCE1} %{inifile}

%build
%serverbuild

#%{_usrsrc}/php4-devel/buildext %{modname} cyrus.c "-lsasl2 -lcyrus -lcyrus_min" \
#    "-DCOMPILE_DL_CYRUS -DHAVE_CYRUS -I%{_includedir}/sasl"

phpize
export CYRUS_SHARED_LIBADD="-L%{_libdir} -lsasl2 -lcyrus -lcyrus_min"
%configure2_5x --with-libdir=%{_lib} \
    --enable-%{modname}=shared,%{_prefix}

%make
mv modules/*.so .

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

cat > README.%{modname} << EOF
The %{name} package contains a dynamic shared object (DSO) for PHP. 
EOF

install -m0644 %{inifile} %{buildroot}%{_sysconfdir}/php.d/%{inifile}
install -m0755 %{soname} %{buildroot}%{_libdir}/php/extensions/

%post
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart >/dev/null || :
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart >/dev/null || :
    fi
fi

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}
[ "../package.xml" != "/" ] && rm -f ../package.xml

%files 
%defattr(-,root,root)
%doc CREDITS README*
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}


%changelog
* Sun May 06 2012 Oden Eriksson <oeriksson@mandriva.com> 1.0-32mdv2012.0
+ Revision: 797125
- fix build
- rebuild for php-5.4.x

* Sun Jan 15 2012 Oden Eriksson <oeriksson@mandriva.com> 1.0-31
+ Revision: 761210
- rebuild

* Wed Aug 24 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0-30
+ Revision: 696403
- rebuilt for php-5.3.8

* Fri Aug 19 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0-29
+ Revision: 695376
- rebuilt for php-5.3.7

* Sat Mar 19 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0-28
+ Revision: 646621
- rebuilt for php-5.3.6

* Sat Jan 08 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0-27mdv2011.0
+ Revision: 629774
- rebuilt for php-5.3.5

* Mon Jan 03 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0-26mdv2011.0
+ Revision: 628076
- ensure it's built without automake1.7

* Wed Nov 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0-25mdv2011.0
+ Revision: 600470
- rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0-24mdv2011.0
+ Revision: 588753
- rebuild

* Fri Mar 05 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0-23mdv2010.1
+ Revision: 514527
- rebuilt for php-5.3.2

* Sat Jan 02 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0-22mdv2010.1
+ Revision: 485348
- rebuilt for php-5.3.2RC1

* Sat Nov 21 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0-21mdv2010.1
+ Revision: 468154
- rebuilt against php-5.3.1

* Wed Sep 30 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0-20mdv2010.0
+ Revision: 451260
- rebuild

* Sun Jul 19 2009 Raphaël Gertz <rapsys@mandriva.org> 1.0-19mdv2010.0
+ Revision: 397488
- Rebuild

* Mon May 18 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0-18mdv2010.0
+ Revision: 376979
- rebuilt for php-5.3.0RC2

* Sun Mar 01 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0-17mdv2009.1
+ Revision: 346408
- rebuilt for php-5.2.9

* Tue Feb 17 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0-16mdv2009.1
+ Revision: 341716
- rebuilt against php-5.2.9RC2

* Wed Dec 31 2008 Oden Eriksson <oeriksson@mandriva.com> 1.0-15mdv2009.1
+ Revision: 321717
- rebuild

* Fri Dec 05 2008 Oden Eriksson <oeriksson@mandriva.com> 1.0-14mdv2009.1
+ Revision: 310257
- rebuilt against php-5.2.7

* Fri Jul 18 2008 Oden Eriksson <oeriksson@mandriva.com> 1.0-13mdv2009.0
+ Revision: 238383
- rebuild

* Fri May 02 2008 Oden Eriksson <oeriksson@mandriva.com> 1.0-12mdv2009.0
+ Revision: 200191
- rebuilt for php-5.2.6

* Mon Feb 04 2008 Oden Eriksson <oeriksson@mandriva.com> 1.0-11mdv2008.1
+ Revision: 162141
- rebuild

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Nov 11 2007 Oden Eriksson <oeriksson@mandriva.com> 1.0-10mdv2008.1
+ Revision: 107610
- restart apache if needed

* Sat Sep 01 2007 Oden Eriksson <oeriksson@mandriva.com> 1.0-9mdv2008.0
+ Revision: 77533
- rebuilt against php-5.2.4
- use distro conditional -fstack-protector

* Fri Jun 01 2007 Oden Eriksson <oeriksson@mandriva.com> 1.0-7mdv2008.0
+ Revision: 33802
- rebuilt against new upstream version (5.2.3)

* Thu May 03 2007 Oden Eriksson <oeriksson@mandriva.com> 1.0-6mdv2008.0
+ Revision: 21322
- rebuilt against new upstream version (5.2.2)


* Thu Feb 08 2007 Oden Eriksson <oeriksson@mandriva.com> 1.0-5mdv2007.0
+ Revision: 117560
- rebuilt against new upstream version (5.2.1)

* Thu Nov 09 2006 Oden Eriksson <oeriksson@mandriva.com> 1.0-4mdv2007.0
+ Revision: 79281
- rebuild
- fix deps
- fix deps
- rebuilt for php-5.2.0
- Import php-cyrus

* Mon Aug 28 2006 Oden Eriksson <oeriksson@mandriva.com> 1.0-1
- rebuilt for php-5.1.6

* Mon Aug 28 2006 Oden Eriksson <oeriksson@mandriva.com> 1:1.0-5
- rebuilt for php-4.4.4

* Sun Aug 06 2006 Oden Eriksson <oeriksson@mandriva.com> 1:1.0-4mdv2007.0
- rebuilt for php-4.4.3

* Wed Jul 26 2006 Oden Eriksson <oeriksson@mandriva.com> 1:1.0-3mdk
- rebuild

* Mon Jan 16 2006 Oden Eriksson <oeriksson@mandriva.com> 1:1.0-2mdk
- rebuilt against php-4.4.2

* Wed Nov 02 2005 Oden Eriksson <oeriksson@mandriva.com> 1:1.0-1mdk
- rebuilt for php-4.4.1
- fix versioning

* Tue Jul 12 2005 Oden Eriksson <oeriksson@mandriva.com> 4.4.0-1mdk
- rebuilt for php-4.4.0 final

* Wed Jul 06 2005 Oden Eriksson <oeriksson@mandriva.com> 4.4.0-0.RC2.1mdk
- rebuilt for php-4.4.0RC2

* Wed Jun 15 2005 Oden Eriksson <oeriksson@mandriva.com> 4.4.0_1.0-0.RC1.1mdk
- rebuilt for php-4.4.0RC1

* Fri Jun 03 2005 Oden Eriksson <oeriksson@mandriva.com> 4.3.11_1.0-1mdk
- renamed to php4-*

* Sun Apr 17 2005 Oden Eriksson <oeriksson@mandriva.com> 4.3.11_1.0-1mdk
- 4.3.11

* Mon Mar 21 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.10_1.0-6mdk
- use the %%mkrel macro

* Sat Feb 12 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.10_1.0-5mdk
- rebuilt against a non hardened-php aware php lib

* Tue Feb 01 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.10_1.0-4mdk
- link against libcyrus_min to resolve missing symbols
- fix deps

* Sat Jan 15 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.10_1.0-3mdk
- rebuild due to hardened-php-0.2.6
- cleanups

* Tue Jan 04 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.10_1.0-2mdk
- lib64 fixes (P0)

* Thu Dec 16 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.10_1.0-1mdk
- rebuild for php 4.3.10

* Sat Oct 02 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.9_1.0-1mdk
- rebuild for php 4.3.9

* Mon Aug 02 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.8_1.0-2mdk
- make it find missing symbols

* Thu Jul 15 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.8_1.0-1mdk
- rebuilt for php-4.3.8

* Tue Jul 13 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.7_1.0-2mdk
- remove redundant provides

* Tue Jun 15 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.7_1.0-1mdk
- rebuilt for php-4.3.7

* Mon May 24 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.6_1.0-2mdk
- use the %%configure2_5x macro
- move scandir to /etc/php4.d

* Thu May 06 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.6_1.0-1mdk
- fix url
- built for php 4.3.6

