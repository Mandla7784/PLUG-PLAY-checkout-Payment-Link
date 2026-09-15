# This is where i work on generaoing the payment link for the user to pay for the order. I will be using the payment gateway API to generate the payment link and return it to the user.
# calaculating expriation 

#creates the payment link
#saves it to SQLite
#returns the created record

import secrets
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from ..models import PaymentLink
from ..schemas import PaymentLinkCreate



#function to create payment link

