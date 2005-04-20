
import ensemble
perl=ensemble.Director("./ensemble.pl")
perl.loadModule("Acme::Umlautify", "acme")
print perl.acme.umlautify("What we need more of is umlauts.")

                         


