#
# Conditional build:
%bcond_with	tests		# build without tests
%bcond_with	doc			# don't build ri/rdoc

%define pkgname multipart-post
Summary:	Creates a multipart form post accessory for Net::HTTP
Name:		ruby-%{pkgname}
Version:	2.0.0
Release:	1
License:	MIT
Group:		Development/Languages
Source0:	http://rubygems.org/gems/%{pkgname}-%{version}.gem
# Source0-md5:	1be431f2e8b50cc5b63cc7b7e23fef44
URL:		http://github.com/nicksieger/multipart-post
BuildRequires:	rpm-rubyprov
BuildRequires:	rpmbuild(macros) >= 1.665
%if %{with tests}
BuildRequires:	rubygem(minitest)
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Use with Net::HTTP to do multipart form posts. IO values that have
content_type, original_filename, and local_path will be posted as a
binary file.

%package doc
Summary:	Documentation for %{name}
Group:		Documentation
Requires:	%{name} = %{version}-%{release}

%description doc
Documentation for %{name}

%prep
%setup -q -n %{pkgname}-%{version}

%build
# write .gemspec
%__gem_helper spec

%if %{with tests}
# To run the tests using minitest 5
ruby -rminitest/autorun -Ilib - << 'EOF'
	module Kernel
		alias orig_require require
		remove_method :require

		def require path
			orig_require path unless path == 'test/unit'
		end

	end

	Test = Minitest

	Dir.glob "./test/**/test_*.rb", &method(:require)
EOF
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{ruby_vendorlibdir},%{ruby_specdir}}
cp -a lib/* $RPM_BUILD_ROOT%{ruby_vendorlibdir}
cp -p %{pkgname}-%{version}.gemspec $RPM_BUILD_ROOT%{ruby_specdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md
%{ruby_vendorlibdir}/composite_io.rb
%{ruby_vendorlibdir}/multipart_post.rb
%{ruby_vendorlibdir}/multipartable.rb
%dir %{ruby_vendorlibdir}/net/http/post
%{ruby_vendorlibdir}/net/http/post/multipart.rb
%{ruby_vendorlibdir}/parts.rb
%{ruby_specdir}/%{pkgname}-%{version}.gemspec

%if %{with doc}
%files doc
%defattr(644,root,root,755)
%doc Manifest.txt History.txt
%endif
