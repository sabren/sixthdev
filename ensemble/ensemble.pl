#!/usr/bin/perl -w
##################################################
#
# ensemble is a method for controlling
# script engines running in child 
# processes. For example, you can use it
# to communicate with perl from python.
#
# this is the driver to communicate with
# perl. it only implements the "child" 
# side of the system.
#
# http://ensemble.tangentcode.com/
#
##################################################

use XMLRPC::Lite;

##################################################

package main;

my $modules = {
    "@@" => "main"
};

sub loadModule {
    my $name = shift;
    my $as = shift;
    $as ||= $name;
    eval "use $name";
    $modules->{$as} = $name;
}

##################################################

package main::ensemble; # just to hide this junk

sub decode {
    my $xml = shift;
    my $parser = new XMLRPC::Deserializer();
    my $data = $parser->deserialize($xml);
    return $data->valueof("methodName"), $data->valueof("params");
}

sub encode {
    return XMLRPC::Serializer->envelope(response => 'toMethod', shift);
}

sub invoke {
    my ($meth, $params) = @_;
    my $mod = "@@";
    
    my ($head, $tail) = split( /\./, $meth, 2);
    if ($tail) {
	$mod = $head;
	$meth = $tail;
    }
    $mod = $modules->{$mod};
    return &{"$mod" . "::$meth"}(@$params);
}

sub xml_invoke {
    my $xml = shift;
    return encode(invoke(decode($xml)));
}


## main loop #####################################

print  "## ensemble v1.0 ##\n";

$| = 1; # perlish for nonbuffered stdout
my $req = "";
while (<>) {
    $req .= $_;
    if ( m|</methodCall>| ) {
	print xml_invoke($req);
	print "\n";
	$req = "";	
    }
}

__END__
