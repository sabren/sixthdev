
class Model: pass
model = Model()

def show():

    print "<h1>Credit Card</h1>"

    if model.creditcards:

        print '<form action="checkout.py" method="POST">'
        print '<h3>Select a credit card from the list below...</h3>'
        print '<select name="cardID">'
        for item in model.creditcards:
            cc = ("x" * (len(item["number"])-4)) + item["number"][-4:]
            print '<option value="%s">%s' \
                  % (item["ID"], cc)
        print '</select>'
        print '<input type="hidden" name="action" value="update">'
        print '<input type="submit" value="submit">'
        print '</form>'
        
        print '<h3>... or enter a new card below:</h3>'
    else:
        print '<h3>enter your credit card info below:</h3>'

    print '<form action="checkout.py" method="post">'
    print '<b>name on card:</b> '
    print '<input type="text" name="name" value=""><br>'
    print 'card number: <input type="text" name="number"><br>'
    print 'expiration month: <select name="expMonth">'
    for i in range(12):
        print '<option>%02i</option>' % (i+1) # months start at base 1
    print '</select>'
    print 'year: <select name="expYear">'
    for i in range(2000,2011):
        print '<option>%04i</option>' % i
    print '</select>'
    print '<br>'
    print '<input type="hidden" name="context" value="checkout">'
    print '<input type="hidden" name="action" value="addcard">'
    print '<input type="submit" value="submit">'
    print '</form>'
    
