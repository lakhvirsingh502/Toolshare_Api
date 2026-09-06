from app.celery_app import celery_app
from app.services.notifications import send_notification
from app.database import sessionlocal
from app.models.reservations import Reservation
from app.models.user import User
from app.database import sessionlocal
from datetime import datetime, timedelta
@celery_app.task
def test_task():
    print("Bro it is working")

@celery_app.task(bind=True)
def send_reservation_email(self,reservation_id):
    try:
        db=sessionlocal()
        reservation = db.query(Reservation).filter(Reservation.id==reservation_id).first()
        if reservation is None:
            
            return
        user = db.query(User).filter(User.id == reservation.borrower_id).first()
        if user is None:
            
            return
        if reservation.status == "accepted":
            subject = "Reservation approved"
            message = "Reservation has been approved"
        elif reservation.status == "rejected":
            subject = "Reservation rejected"
            message = "Reservation has been rejected."
        else:
               return
        try:
            send_notification(user.email,subject,message)
        except Exception as exc:
            raise self.retry(exc=exc,countdown=10,max_retries=3)
    finally:
        db.close()

@celery_app.task
def beat_test():
    print("Beat is working")


@celery_app.task(bind = True,max_retries=3)
def send_reservation_reminders(self):
    try:
        db = sessionlocal()
        tommorrow = datetime.now() + timedelta(days=1)
        tommorrow_start = tommorrow.replace(
            hour = 0,
            minute = 0,
            second = 0,
            microsecond = 0
        )
        tommorrow_end = tommorrow_start + timedelta(days=1)
        reservations = db.query(Reservation).filter(Reservation.status == "accepted",
                                                    Reservation.reminder_sent==False,
                                                    Reservation.start_date>=tommorrow_start,
                                                    Reservation.start_date<tommorrow_end).all()
        
            
                                                    
        
        for reservation in reservations:
            user = db.query(User).filter(User.id == reservations.borrower_id).first()
            subject = "Reservation reminder"
            message = f"""Your reservation is scheduled for {reservation.start_date}.
                        This is a reminder that your reservation is coming up tomorrow."""
            try:                        
                send_notification(user.email,subject,message)
                reservation.reminder_sent = True
                db.commit()
            except Exception as exc:
                raise self.retry(exc = exc,countdown=10)
    finally:
        db.close()

@celery_app.task(bind=True,max_retries=3,countdown=10)
def expired_reservations(self):
    try:
        db = sessionlocal()
        reservations = db.query(Reservation.status == "pending",
                                Reservation.start_date< datetime.now()).all()
        for reservation in reservations:
            reservation.status = "expired"
        db.commit()
    except Exception as exc:
        raise self.retry(exc = exc)
    finally:
        db.close()


                            
                    
                
    


