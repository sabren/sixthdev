##################################################

package PerlChildTest;

sub hello {
    return "hello, world!";
}

sub add {
    my ($a, $b) = @_;
    return $a + $b;
}


sub fail {
    die();
}

##################################################

1;
__END__
