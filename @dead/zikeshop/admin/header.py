# just a header

import weblib

print weblib.trim(
    """
    <table align="center" border="0" cellspacing="5"><tr>
    <td>[<a href="l_category.py">categories</a>]</td>
    <td>[<a href="l_product.py">products</a>]</td>
    <td>[<a href="l_location.py">locations</a>]</td>
    <td>[<a href="sales.py">sales</a>]</td>
    <td>[<a href="l_category.py?auth_logout_flag=1">logout</a>]</td>
    </tr></table><br>
    """)


#     <td>[<a href="inventory.py">inventory</a>]</td>
